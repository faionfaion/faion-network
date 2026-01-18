# M-API-010: API Monitoring

## Metadata
- **ID:** M-API-010
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, monitoring, observability, metrics, logging]
- **Agent:** faion-api-agent

---

## Problem

Without API monitoring:
- Issues discovered by users, not you
- No insight into performance bottlenecks
- Unable to capacity plan
- Security incidents go unnoticed
- SLA violations undetected

---

## Framework

### Step 1: Define Key Metrics

**Golden Signals (Google SRE):**

| Signal | Description | Example Metrics |
|--------|-------------|-----------------|
| Latency | Time to respond | p50, p95, p99 response time |
| Traffic | Request volume | Requests per second |
| Errors | Failure rate | Error rate %, 5xx count |
| Saturation | Resource usage | CPU, memory, connections |

**API-Specific Metrics:**

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Request rate | Requests/second | Baseline +50% |
| Error rate | 4xx/5xx percentage | >1% |
| Response time p95 | 95th percentile latency | >500ms |
| Availability | Uptime percentage | <99.9% |

### Step 2: Implement Health Checks

**Simple health endpoint:**

```python
# Django
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    checks = {
        'status': 'healthy',
        'checks': {}
    }

    # Database check
    try:
        connection.ensure_connection()
        checks['checks']['database'] = 'ok'
    except Exception as e:
        checks['checks']['database'] = f'error: {str(e)}'
        checks['status'] = 'unhealthy'

    # Redis check
    try:
        redis_client.ping()
        checks['checks']['redis'] = 'ok'
    except Exception as e:
        checks['checks']['redis'] = f'error: {str(e)}'
        checks['status'] = 'unhealthy'

    status_code = 200 if checks['status'] == 'healthy' else 503
    return JsonResponse(checks, status=status_code)
```

```javascript
// Express.js
app.get('/health', async (req, res) => {
  const checks = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    checks: {}
  };

  // Database check
  try {
    await mongoose.connection.db.admin().ping();
    checks.checks.database = 'ok';
  } catch (error) {
    checks.checks.database = `error: ${error.message}`;
    checks.status = 'unhealthy';
  }

  // Redis check
  try {
    await redis.ping();
    checks.checks.redis = 'ok';
  } catch (error) {
    checks.checks.redis = `error: ${error.message}`;
    checks.status = 'unhealthy';
  }

  // Memory check
  const memUsage = process.memoryUsage();
  checks.checks.memory = {
    heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024) + 'MB',
    heapTotal: Math.round(memUsage.heapTotal / 1024 / 1024) + 'MB'
  };

  const statusCode = checks.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(checks);
});

// Detailed readiness check
app.get('/health/ready', async (req, res) => {
  // Check if app is ready to serve traffic
  const isReady = await checkAllDependencies();
  res.status(isReady ? 200 : 503).json({ ready: isReady });
});

// Liveness check (simple)
app.get('/health/live', (req, res) => {
  res.json({ alive: true });
});
```

### Step 3: Add Request Logging

**Structured logging:**

```python
# Django middleware
import logging
import time
import uuid
import json

logger = logging.getLogger('api')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        start_time = time.time()

        response = self.get_response(request)

        duration_ms = (time.time() - start_time) * 1000

        log_data = {
            'request_id': request.request_id,
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'duration_ms': round(duration_ms, 2),
            'user_id': getattr(request.user, 'id', None),
            'ip': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }

        if response.status_code >= 400:
            logger.warning(json.dumps(log_data))
        else:
            logger.info(json.dumps(log_data))

        response['X-Request-ID'] = request.request_id
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
```

```javascript
// Express.js with morgan + custom format
const morgan = require('morgan');
const { v4: uuidv4 } = require('uuid');

// Add request ID
app.use((req, res, next) => {
  req.id = uuidv4();
  res.set('X-Request-ID', req.id);
  next();
});

// Custom logging format
morgan.token('request-id', (req) => req.id);
morgan.token('user-id', (req) => req.user?.id || 'anonymous');
morgan.token('body', (req) => JSON.stringify(req.body));

const logFormat = JSON.stringify({
  request_id: ':request-id',
  method: ':method',
  path: ':url',
  status: ':status',
  duration_ms: ':response-time',
  user_id: ':user-id',
  ip: ':remote-addr',
  user_agent: ':user-agent'
});

app.use(morgan(logFormat));
```

### Step 4: Implement Metrics Collection

**Prometheus metrics (Python):**

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

# Middleware
class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ACTIVE_REQUESTS.inc()
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        endpoint = self.get_endpoint(request)

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)

        ACTIVE_REQUESTS.dec()
        return response

    def get_endpoint(self, request):
        # Normalize endpoint (e.g., /users/123 -> /users/{id})
        return request.resolver_match.route if request.resolver_match else request.path

# Metrics endpoint
def metrics_view(request):
    return HttpResponse(
        generate_latest(),
        content_type='text/plain'
    )
```

**Prometheus metrics (JavaScript):**

```javascript
// metrics.js
const promClient = require('prom-client');

// Enable default metrics
promClient.collectDefaultMetrics();

// Custom metrics
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'path', 'status']
});

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request latency',
  labelNames: ['method', 'path'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
});

const activeRequests = new promClient.Gauge({
  name: 'http_requests_active',
  help: 'Active HTTP requests'
});

// Middleware
const metricsMiddleware = (req, res, next) => {
  activeRequests.inc();
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const path = req.route?.path || req.path;

    httpRequestsTotal.labels(req.method, path, res.statusCode).inc();
    httpRequestDuration.labels(req.method, path).observe(duration);
    activeRequests.dec();
  });

  next();
};

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.send(await promClient.register.metrics());
});

module.exports = { metricsMiddleware };
```

### Step 5: Set Up Alerts

**Prometheus alerting rules:**

```yaml
# alerts.yml
groups:
  - name: api-alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # Slow responses
      - alert: SlowResponses
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow API responses"
          description: "95th percentile latency is {{ $value }}s"

      # High traffic
      - alert: HighTraffic
        expr: |
          sum(rate(http_requests_total[5m])) > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High traffic detected"
          description: "Request rate is {{ $value }} req/s"

      # Service down
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} is not responding"
```

### Step 6: Implement Distributed Tracing

**OpenTelemetry setup:**

```python
# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

def setup_tracing():
    provider = TracerProvider()

    exporter = OTLPSpanExporter(
        endpoint="http://jaeger:4317",
        insecure=True
    )

    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Auto-instrument
    DjangoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()

# Custom spans
tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        with tracer.start_as_current_span("validate_order"):
            validate(order_id)

        with tracer.start_as_current_span("charge_payment"):
            charge(order_id)

        with tracer.start_as_current_span("send_notification"):
            notify(order_id)
```

```javascript
// tracing.js
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-otlp-grpc');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');
const { MongoDBInstrumentation } = require('@opentelemetry/instrumentation-mongodb');

const provider = new NodeTracerProvider();

const exporter = new OTLPTraceExporter({
  url: 'http://jaeger:4317'
});

provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
    new MongoDBInstrumentation()
  ]
});

// Custom spans
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

async function processOrder(orderId) {
  return tracer.startActiveSpan('process_order', async (span) => {
    span.setAttribute('order.id', orderId);

    await tracer.startActiveSpan('validate_order', async (validateSpan) => {
      await validate(orderId);
      validateSpan.end();
    });

    await tracer.startActiveSpan('charge_payment', async (chargeSpan) => {
      await charge(orderId);
      chargeSpan.end();
    });

    span.end();
  });
}
```

### Step 7: Create Dashboards

**Grafana dashboard JSON:**

```json
{
  "title": "API Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(http_requests_total[5m]))"
      }]
    },
    {
      "title": "Error Rate",
      "type": "gauge",
      "targets": [{
        "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
      }],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              { "value": 0, "color": "green" },
              { "value": 1, "color": "yellow" },
              { "value": 5, "color": "red" }
            ]
          },
          "unit": "percent"
        }
      }
    },
    {
      "title": "Response Time (p95)",
      "type": "timeseries",
      "targets": [{
        "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))"
      }]
    },
    {
      "title": "Requests by Status",
      "type": "piechart",
      "targets": [{
        "expr": "sum by (status) (increase(http_requests_total[1h]))"
      }]
    },
    {
      "title": "Top Endpoints by Traffic",
      "type": "table",
      "targets": [{
        "expr": "topk(10, sum by (path) (rate(http_requests_total[5m])))"
      }]
    }
  ]
}
```

---

## Templates

### Monitoring Checklist

```markdown
## API Monitoring Setup

### Health Checks
- [ ] /health endpoint (dependencies status)
- [ ] /health/live (liveness probe)
- [ ] /health/ready (readiness probe)

### Logging
- [ ] Structured JSON logging
- [ ] Request ID tracking
- [ ] User ID in logs
- [ ] Error stack traces
- [ ] Log aggregation (ELK/Loki)

### Metrics
- [ ] Request count by endpoint/status
- [ ] Response time histograms
- [ ] Active connections
- [ ] Business metrics

### Alerting
- [ ] Error rate > threshold
- [ ] Latency > threshold
- [ ] Service down
- [ ] Database connection issues

### Tracing
- [ ] Distributed tracing enabled
- [ ] Cross-service correlation
- [ ] Database query tracing

### Dashboards
- [ ] Overview dashboard
- [ ] Endpoint-specific dashboards
- [ ] Error analysis dashboard
```

---

## Common Mistakes

1. **No health checks**
   - Load balancers can't route properly
   - Kubernetes can't manage pods

2. **Missing request IDs**
   - Can't correlate logs across services
   - Debugging becomes impossible

3. **Alerting on symptoms, not causes**
   - Alert fatigue
   - Focus on actionable alerts

4. **No historical data**
   - Can't compare to baseline
   - Retain at least 30 days

5. **Missing business metrics**
   - Technical metrics only
   - Track orders, signups, etc.

---

## Next Steps

1. **Add health checks** - Basic availability
2. **Implement structured logging** - Request tracking
3. **Add Prometheus metrics** - Performance visibility
4. **Set up alerts** - Proactive monitoring
5. **Create dashboards** - Visual overview

---

## Related Methodologies

- [M-API-006: Rate Limiting](./M-API-006_rate_limiting.md)
- [M-API-007: Error Handling](./M-API-007_error_handling.md)
- [M-API-011: API Gateway Patterns](./M-API-011_api_gateway_patterns.md)

---

*Methodology: API Monitoring*
*Version: 1.0*
*Agent: faion-api-agent*
