# Prometheus Monitoring Examples

## Application Instrumentation

### Python (FastAPI)

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from functools import wraps
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
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

IN_PROGRESS = Gauge(
    'http_requests_in_progress',
    'HTTP requests in progress',
    ['method', 'endpoint']
)

DB_CONNECTIONS = Gauge(
    'db_connections_active',
    'Active database connections'
)

APP_INFO = Info(
    'app',
    'Application information'
)

# Initialize app info
APP_INFO.info({
    'version': '1.0.0',
    'environment': 'production'
})


def track_request(method: str, endpoint: str):
    """Decorator to track request metrics"""
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()
            start_time = time.time()
            status = 200

            try:
                result = await f(*args, **kwargs)
                status = getattr(result, 'status_code', 200)
                return result
            except Exception as e:
                status = 500
                raise
            finally:
                duration = time.time() - start_time
                REQUEST_COUNT.labels(
                    method=method,
                    endpoint=endpoint,
                    status=str(status)
                ).inc()
                REQUEST_LATENCY.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(duration)
                IN_PROGRESS.labels(method=method, endpoint=endpoint).dec()

        return wrapper
    return decorator


# FastAPI integration
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/api/users")
@track_request("GET", "/api/users")
async def get_users():
    # Implementation
    return {"users": []}
```

### Node.js (Express)

```javascript
// metrics.js
const promClient = require('prom-client');

// Enable default metrics
promClient.collectDefaultMetrics({
  prefix: 'nodejs_',
  gcDurationBuckets: [0.001, 0.01, 0.1, 1, 2, 5],
});

// Custom metrics
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
});

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
});

const httpRequestsInProgress = new promClient.Gauge({
  name: 'http_requests_in_progress',
  help: 'HTTP requests in progress',
  labelNames: ['method', 'route'],
});

const dbConnectionsActive = new promClient.Gauge({
  name: 'db_connections_active',
  help: 'Active database connections',
});

// Express middleware
const metricsMiddleware = (req, res, next) => {
  const start = Date.now();
  const route = req.route?.path || req.path;

  httpRequestsInProgress.labels(req.method, route).inc();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;

    httpRequestsTotal.labels(req.method, route, res.statusCode).inc();
    httpRequestDuration.labels(req.method, route).observe(duration);
    httpRequestsInProgress.labels(req.method, route).dec();
  });

  next();
};

// Express setup
const express = require('express');
const app = express();

app.use(metricsMiddleware);

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

module.exports = {
  httpRequestsTotal,
  httpRequestDuration,
  dbConnectionsActive,
  register: promClient.register,
};
```

### Go

```go
// metrics.go
package metrics

import (
    "net/http"
    "time"

    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "path", "status"},
    )

    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
        },
        []string{"method", "path"},
    )

    httpRequestsInProgress = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "http_requests_in_progress",
            Help: "HTTP requests in progress",
        },
        []string{"method", "path"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestsTotal)
    prometheus.MustRegister(httpRequestDuration)
    prometheus.MustRegister(httpRequestsInProgress)
}

// Middleware wraps HTTP handlers with metrics
func Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        path := r.URL.Path
        method := r.Method

        httpRequestsInProgress.WithLabelValues(method, path).Inc()
        defer httpRequestsInProgress.WithLabelValues(method, path).Dec()

        // Wrap response writer to capture status
        rw := &responseWriter{ResponseWriter: w, statusCode: 200}
        next.ServeHTTP(rw, r)

        duration := time.Since(start).Seconds()
        status := fmt.Sprintf("%d", rw.statusCode)

        httpRequestsTotal.WithLabelValues(method, path, status).Inc()
        httpRequestDuration.WithLabelValues(method, path).Observe(duration)
    })
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

// Handler returns the metrics HTTP handler
func Handler() http.Handler {
    return promhttp.Handler()
}
```

---

## PromQL Queries

### Request Metrics

```promql
# Request rate per second (5m average)
sum(rate(http_requests_total[5m])) by (method, status)

# Request rate by service
sum(rate(http_requests_total[5m])) by (service)

# Total requests in last hour
sum(increase(http_requests_total[1h]))

# Top 10 endpoints by request count
topk(10, sum(rate(http_requests_total[5m])) by (endpoint))
```

### Error Rates

```promql
# Error rate percentage (5xx responses)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m]))
* 100

# Error rate by endpoint
sum(rate(http_requests_total{status=~"5.."}[5m])) by (endpoint)
/ sum(rate(http_requests_total[5m])) by (endpoint)
* 100

# 4xx error rate
sum(rate(http_requests_total{status=~"4.."}[5m]))
/ sum(rate(http_requests_total[5m]))
* 100

# Non-2xx responses
sum(rate(http_requests_total{status!~"2.."}[5m])) by (status)
```

### Latency

```promql
# P50 latency
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# P90 latency
histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# P99 latency
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# P99 latency by endpoint
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
)

# Average latency
sum(rate(http_request_duration_seconds_sum[5m]))
/ sum(rate(http_request_duration_seconds_count[5m]))

# Apdex score (satisfied < 0.5s, tolerating < 2s)
(
  sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
  + sum(rate(http_request_duration_seconds_bucket{le="2"}[5m]))
) / 2
/ sum(rate(http_request_duration_seconds_count[5m]))
```

### Kubernetes Resources

```promql
# CPU usage percentage per pod
sum(rate(container_cpu_usage_seconds_total{namespace="production"}[5m])) by (pod)
/ sum(container_spec_cpu_quota{namespace="production"}/container_spec_cpu_period{namespace="production"}) by (pod)
* 100

# Memory usage percentage per pod
container_memory_working_set_bytes{namespace="production"}
/ container_spec_memory_limit_bytes{namespace="production"}
* 100

# Memory usage in GB
container_memory_working_set_bytes{namespace="production"} / 1024 / 1024 / 1024

# Pod restarts in last hour
increase(kube_pod_container_status_restarts_total[1h])

# Pods not ready
kube_pod_status_ready{condition="false"}

# Available vs desired replicas
kube_deployment_status_replicas_available / kube_deployment_spec_replicas

# CPU throttling percentage
sum(increase(container_cpu_cfs_throttled_periods_total[5m])) by (pod)
/ sum(increase(container_cpu_cfs_periods_total[5m])) by (pod)
* 100
```

### Node Metrics

```promql
# Node CPU usage percentage
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) * 100

# Node memory usage percentage
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# Disk usage percentage
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100

# Network receive rate (MB/s)
sum(rate(node_network_receive_bytes_total[5m])) by (instance) / 1024 / 1024

# Network transmit rate (MB/s)
sum(rate(node_network_transmit_bytes_total[5m])) by (instance) / 1024 / 1024

# Disk I/O utilization
rate(node_disk_io_time_seconds_total[5m]) * 100
```

### SLI/SLO Queries

```promql
# Availability SLI (successful requests / total requests)
sum(rate(http_requests_total{status!~"5.."}[5m]))
/ sum(rate(http_requests_total[5m]))

# Error budget remaining (for 99.9% SLO)
1 - (
  (1 - sum(rate(http_requests_total{status!~"5.."}[30d])) / sum(rate(http_requests_total[30d])))
  / (1 - 0.999)
)

# Latency SLI (requests under threshold / total)
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
/ sum(rate(http_request_duration_seconds_count[5m]))

# Error budget burn rate
(1 - sum(rate(http_requests_total{status!~"5.."}[1h])) / sum(rate(http_requests_total[1h])))
/ (1 - 0.999)
```

---

## Recording Rules

```yaml
# recording-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: recording-rules
  labels:
    prometheus: main
spec:
  groups:
    - name: http.rules
      interval: 30s
      rules:
        # Request rate
        - record: job:http_requests:rate5m
          expr: sum(rate(http_requests_total[5m])) by (job)

        - record: job:http_requests:rate5m:by_method_status
          expr: sum(rate(http_requests_total[5m])) by (job, method, status)

        # Error rate
        - record: job:http_requests:error_rate5m
          expr: |
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
            / sum(rate(http_requests_total[5m])) by (job)

        # Latency percentiles
        - record: job:http_request_duration_seconds:p50
          expr: |
            histogram_quantile(0.50,
              sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)
            )

        - record: job:http_request_duration_seconds:p90
          expr: |
            histogram_quantile(0.90,
              sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)
            )

        - record: job:http_request_duration_seconds:p99
          expr: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)
            )

        # Average latency
        - record: job:http_request_duration_seconds:avg
          expr: |
            sum(rate(http_request_duration_seconds_sum[5m])) by (job)
            / sum(rate(http_request_duration_seconds_count[5m])) by (job)

    - name: kubernetes.rules
      interval: 30s
      rules:
        # Pod CPU usage
        - record: namespace_pod:container_cpu_usage:rate5m
          expr: |
            sum(rate(container_cpu_usage_seconds_total[5m])) by (namespace, pod)

        # Pod memory usage
        - record: namespace_pod:container_memory_working_set:bytes
          expr: |
            sum(container_memory_working_set_bytes) by (namespace, pod)

        # Pod restarts
        - record: namespace_pod:kube_pod_container_status_restarts:increase1h
          expr: |
            sum(increase(kube_pod_container_status_restarts_total[1h])) by (namespace, pod)

    - name: sli.rules
      interval: 30s
      rules:
        # Availability SLI
        - record: job:sli_availability:rate5m
          expr: |
            sum(rate(http_requests_total{status!~"5.."}[5m])) by (job)
            / sum(rate(http_requests_total[5m])) by (job)

        # Latency SLI (under 500ms threshold)
        - record: job:sli_latency:rate5m
          expr: |
            sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m])) by (job)
            / sum(rate(http_request_duration_seconds_count[5m])) by (job)
```

---

## Alerting Rules

```yaml
# alerting-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: alerting-rules
  labels:
    prometheus: main
spec:
  groups:
    - name: availability.alerts
      rules:
        - alert: HighErrorRate
          expr: job:http_requests:error_rate5m > 0.05
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate for {{ $labels.job }}"
            description: "Error rate is {{ $value | humanizePercentage }} (>5%)"
            runbook_url: "https://runbooks.example.com/high-error-rate"

        - alert: ServiceDown
          expr: up == 0
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: "Service {{ $labels.job }} is down"
            description: "Target {{ $labels.instance }} has been down for 2 minutes"
            runbook_url: "https://runbooks.example.com/service-down"

    - name: latency.alerts
      rules:
        - alert: HighLatencyP99
          expr: job:http_request_duration_seconds:p99 > 1
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "High P99 latency for {{ $labels.job }}"
            description: "P99 latency is {{ $value | humanizeDuration }}"
            runbook_url: "https://runbooks.example.com/high-latency"

        - alert: HighLatencyP50
          expr: job:http_request_duration_seconds:p50 > 0.5
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "High median latency for {{ $labels.job }}"
            description: "P50 latency is {{ $value | humanizeDuration }}"

    - name: kubernetes.alerts
      rules:
        - alert: PodCrashLooping
          expr: |
            increase(kube_pod_container_status_restarts_total[1h]) > 5
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
            description: "Pod has restarted {{ $value }} times in the last hour"
            runbook_url: "https://runbooks.example.com/pod-crash-loop"

        - alert: PodHighMemory
          expr: |
            container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.85
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} memory usage high"
            description: "Memory usage is {{ $value | humanizePercentage }} of limit"

        - alert: PodCPUThrottling
          expr: |
            sum(increase(container_cpu_cfs_throttled_periods_total[5m])) by (namespace, pod)
            / sum(increase(container_cpu_cfs_periods_total[5m])) by (namespace, pod)
            > 0.25
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} CPU throttling"
            description: "CPU throttling at {{ $value | humanizePercentage }}"

        - alert: DeploymentReplicasMismatch
          expr: |
            kube_deployment_status_replicas_available
            != kube_deployment_spec_replicas
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} replica mismatch"
            description: "Available: {{ $value }}, Desired: {{ $labels.kube_deployment_spec_replicas }}"

    - name: infrastructure.alerts
      rules:
        - alert: NodeHighCPU
          expr: |
            (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) > 0.85
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "High CPU usage on {{ $labels.instance }}"
            description: "CPU usage is {{ $value | humanizePercentage }}"

        - alert: NodeHighMemory
          expr: |
            (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.90
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "High memory usage on {{ $labels.instance }}"
            description: "Memory usage is {{ $value | humanizePercentage }}"

        - alert: DiskSpaceLow
          expr: |
            (1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) > 0.85
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "Low disk space on {{ $labels.instance }}"
            description: "Disk usage is {{ $value | humanizePercentage }}"

    - name: slo.alerts
      rules:
        - alert: ErrorBudgetBurn
          expr: |
            (1 - job:sli_availability:rate5m) / (1 - 0.999) > 14.4
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Error budget burning fast for {{ $labels.job }}"
            description: "Burn rate is {{ $value }}x (>14.4x triggers page)"
            runbook_url: "https://runbooks.example.com/error-budget-burn"
```
