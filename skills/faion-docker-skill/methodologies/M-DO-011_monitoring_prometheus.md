# M-DO-011: Monitoring with Prometheus

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #monitoring, #prometheus, #observability, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Without metrics, you're blind to system health. Problems are discovered by users, not monitoring. Capacity planning is guesswork.

## Promise

After this methodology, you will collect and visualize metrics with Prometheus and Grafana. You'll detect issues before users do.

## Overview

Prometheus is a time-series database for metrics. It scrapes targets, stores data, and enables alerting. Grafana provides visualization.

---

## Framework

### Step 1: Prometheus Setup

```yaml
# docker-compose.yml
version: "3.9"

services:
  prometheus:
    image: prom/prometheus:v2.48.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=15d'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana:10.2.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  alertmanager:
    image: prom/alertmanager:v0.26.0
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml

volumes:
  prometheus_data:
  grafana_data:
```

### Step 2: Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: production
    env: prod

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'application'
    static_configs:
      - targets: ['app:3000']
    metrics_path: /metrics

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

### Step 3: Application Metrics

```javascript
// Node.js with prom-client
const promClient = require('prom-client');

// Enable default metrics
promClient.collectDefaultMetrics({ prefix: 'app_' });

// Custom metrics
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5],
});

const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
});

const activeConnections = new promClient.Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
});

// Middleware
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();

  res.on('finish', () => {
    const labels = {
      method: req.method,
      route: req.route?.path || req.path,
      status_code: res.statusCode,
    };

    end(labels);
    httpRequestsTotal.inc(labels);
  });

  next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});
```

```python
# Python with prometheus_client
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Flask, Response
import time

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
)

ACTIVE_REQUESTS = Gauge('active_requests', 'Active requests')

# Decorator
def track_metrics(func):
    def wrapper(*args, **kwargs):
        ACTIVE_REQUESTS.inc()
        start = time.time()

        try:
            result = func(*args, **kwargs)
            status = 200
        except Exception:
            status = 500
            raise
        finally:
            duration = time.time() - start
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.endpoint,
                status=status
            ).inc()
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.endpoint
            ).observe(duration)
            ACTIVE_REQUESTS.dec()

        return result
    return wrapper

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

### Step 4: Alert Rules

```yaml
# rules/alerts.yml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
          > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value }}s"

      - alert: InstanceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Instance {{ $labels.instance }} is down"

  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: |
          100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
          > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}%"

      - alert: HighMemoryUsage
        expr: |
          (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
          > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: |
          (1 - node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes) * 100
          > 85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Disk space low on {{ $labels.instance }}"
```

### Step 5: Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/xxx'

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
  receiver: 'slack-notifications'

  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true

    - match:
        severity: warning
      receiver: 'slack-notifications'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#alerts'
        send_resolved: true
        title: '{{ .Status | toUpper }}: {{ .CommonLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'xxx'
        severity: critical

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

### Step 6: PromQL Queries

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
* 100

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Average response time
rate(http_request_duration_seconds_sum[5m])
/
rate(http_request_duration_seconds_count[5m])

# Top 5 endpoints by request count
topk(5, sum by(route) (rate(http_requests_total[1h])))

# CPU usage percentage
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# Disk usage
(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100
```

---

## Templates

### Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "Application Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m]))",
            "legendFormat": "requests/s"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 5}
              ]
            },
            "unit": "percent"
          }
        }
      },
      {
        "title": "Response Time",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "P99"
          }
        ]
      }
    ]
  }
}
```

---

## Common Mistakes

1. **High cardinality labels** - Don't use user_id as label
2. **Missing rate()** - Counters must use rate()
3. **No retention policy** - Disk fills up
4. **Alert fatigue** - Too many non-actionable alerts
5. **No runbooks** - Alerts without response procedures

---

## Checklist

- [ ] Prometheus and Grafana deployed
- [ ] Application metrics exported
- [ ] Node exporter for infrastructure
- [ ] Alert rules defined
- [ ] Alertmanager configured
- [ ] Dashboards created
- [ ] Retention policy set
- [ ] Runbooks documented

---

## Next Steps

- M-DO-012: Logging with ELK
- M-DO-013: Tracing with Jaeger
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-011 v1.0*
