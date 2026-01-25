# Observability Architecture

Understanding system behavior through metrics, logs, and traces.

## Three Pillars

```
┌─────────────────────────────────────────────────────┐
│                  Observability                       │
│                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐        │
│  │ Metrics │    │  Logs   │    │ Traces  │        │
│  │         │    │         │    │         │        │
│  │ What    │    │ Why     │    │ Where   │        │
│  │happened │    │happened │    │happened │        │
│  └─────────┘    └─────────┘    └─────────┘        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| Pillar | Purpose | Example |
|--------|---------|---------|
| Metrics | Aggregate numbers | CPU: 75%, RPS: 1000 |
| Logs | Event details | "User 123 logged in" |
| Traces | Request flow | Service A → B → C |

## Metrics

### Types

| Type | Use | Example |
|------|-----|---------|
| Counter | Cumulative total | Total requests |
| Gauge | Current value | Active connections |
| Histogram | Distribution | Latency buckets |
| Summary | Quantiles | p95 latency |

### RED Method (Services)

```
Rate    - Requests per second
Errors  - Failed requests
Duration - Latency distribution
```

### USE Method (Resources)

```
Utilization - % resource busy
Saturation  - Queue depth
Errors      - Error count
```

### Golden Signals

```
Latency   - Response time
Traffic   - Request rate
Errors    - Error rate
Saturation - Resource usage
```

### Prometheus Example

```python
from prometheus_client import Counter, Histogram

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency',
    ['method', 'endpoint']
)

# Use in code
@app.middleware
def metrics_middleware(request, call_next):
    start = time.time()
    response = call_next(request)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path
    ).observe(time.time() - start)

    return response
```

## Logs

### Structured Logging

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "order-service",
  "trace_id": "abc123",
  "user_id": "user-456",
  "action": "order_created",
  "order_id": "order-789",
  "amount": 99.99,
  "message": "Order created successfully"
}
```

### Log Levels

| Level | Use |
|-------|-----|
| ERROR | Failures requiring attention |
| WARN | Potential issues |
| INFO | Normal operations |
| DEBUG | Detailed debugging |

### Best Practices

```python
# DO: Structured with context
logger.info("Order created", extra={
    "order_id": order.id,
    "user_id": user.id,
    "amount": order.total
})

# DON'T: Unstructured string
logger.info(f"Order {order.id} created for user {user.id}")
```

### Log Aggregation Stack

```
Applications ──▶ Collector ──▶ Storage ──▶ UI
     │              │            │          │
  Fluentd/      Vector/      Elasticsearch  Kibana
  Filebeat      Logstash     Loki          Grafana
```

## Distributed Tracing

### Trace Structure

```
Trace (full request journey)
│
├── Span A (API Gateway)
│   └── Span B (User Service)
│       └── Span C (Database)
│
└── Span D (Order Service)
    ├── Span E (Inventory)
    └── Span F (Payment)
```

### Context Propagation

```
Service A ──▶ Service B ──▶ Service C
    │             │             │
    └─ Headers ───┴─ Headers ───┘
       trace_id: abc123
       span_id: span-001
       parent_id: span-000
```

### OpenTelemetry Example

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        # Child span
        with tracer.start_as_current_span("validate_order"):
            validate(order_id)

        with tracer.start_as_current_span("charge_payment"):
            charge(order_id)
```

## Alerting

### Alert Design

```yaml
# Good alert
alert: HighErrorRate
expr: error_rate > 0.01
for: 5m  # Avoid flapping
labels:
  severity: critical
annotations:
  summary: "Error rate above 1% for 5 minutes"
  runbook: "https://wiki/runbooks/high-error-rate"

# Bad alert: Too sensitive
alert: AnyError
expr: errors > 0  # Will fire constantly
```

### Severity Levels

| Severity | Response | Example |
|----------|----------|---------|
| Critical | Page immediately | Service down |
| Warning | Review soon | High latency |
| Info | Check when available | Unusual pattern |

### Alert Routing

```yaml
routes:
  - match:
      severity: critical
    receiver: pagerduty

  - match:
      severity: warning
    receiver: slack

  - receiver: email  # Default
```

## Dashboards

### Service Dashboard

```
┌─────────────────────────────────────────────────────┐
│                 Order Service                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Request Rate        Error Rate       Latency p99   │
│  ┌─────────┐        ┌─────────┐      ┌─────────┐   │
│  │   ╱╲    │        │    ─    │      │   ╱     │   │
│  │  ╱  ╲   │        │         │      │  ╱      │   │
│  │ ╱    ╲  │        │         │      │ ╱       │   │
│  └─────────┘        └─────────┘      └─────────┘   │
│   1,234 RPS          0.1%             150ms        │
│                                                     │
├─────────────────────────────────────────────────────┤
│  Top Endpoints by Latency                           │
│  POST /orders         250ms  ████████████          │
│  GET /orders/{id}     50ms   ████                  │
│  GET /orders          80ms   ██████                │
└─────────────────────────────────────────────────────┘
```

### Dashboard Best Practices

1. **Start with SLOs** - Show what matters
2. **Use consistent layouts** - Same panels across services
3. **Include context** - Deployments, incidents markers
4. **Layer details** - Overview → Details → Debugging

## Observability Tools

| Category | Tools |
|----------|-------|
| Metrics | Prometheus, Datadog, CloudWatch |
| Logs | ELK, Loki, Splunk |
| Traces | Jaeger, Zipkin, Tempo |
| All-in-one | Datadog, New Relic, Dynatrace |
| Open source | Grafana stack (LGTM) |

## Observability Pipeline

```
┌─────────────────────────────────────────────────────┐
│               Observability Pipeline                 │
│                                                     │
│  Sources        Collection      Storage      UI     │
│  ┌──────┐      ┌──────────┐   ┌────────┐  ┌─────┐ │
│  │ Apps │─────▶│  OTel    │──▶│Metrics │──▶      │ │
│  │      │      │Collector │   │(Mimir) │  │     │ │
│  │      │      │          │   ├────────┤  │Graf-│ │
│  │Infra │─────▶│          │──▶│ Logs   │──▶ana  │ │
│  │      │      │          │   │(Loki)  │  │     │ │
│  │      │      │          │   ├────────┤  │     │ │
│  │ K8s  │─────▶│          │──▶│Traces  │──▶     │ │
│  └──────┘      └──────────┘   │(Tempo) │  └─────┘ │
│                               └────────┘          │
└─────────────────────────────────────────────────────┘
```

## Observability Checklist

### Metrics
- [ ] RED/USE metrics defined
- [ ] Custom business metrics
- [ ] Dashboards created
- [ ] Alerts configured

### Logs
- [ ] Structured logging
- [ ] Correlation IDs
- [ ] Appropriate log levels
- [ ] Retention policy

### Traces
- [ ] Instrumentation added
- [ ] Context propagation
- [ ] Sampling configured
- [ ] Critical paths traced

### Alerts
- [ ] SLO-based alerts
- [ ] Runbooks linked
- [ ] On-call rotation
- [ ] Alert fatigue avoided

## Related

- [reliability-architecture.md](reliability-architecture.md) - SLOs
- [performance-architecture.md](performance-architecture.md) - Performance
- [microservices-architecture.md](microservices-architecture.md) - Services
