# Prometheus Monitoring Examples

## Prometheus Stack Installation (Helm)

```yaml
# prometheus-values.yaml
prometheus:
  prometheusSpec:
    replicas: 2
    retention: 30d
    retentionSize: 50GB

    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi

    resources:
      requests:
        cpu: 500m
        memory: 2Gi
      limits:
        cpu: 2000m
        memory: 8Gi

    # External labels for federation
    externalLabels:
      cluster: production
      region: eu-central-1

    # Remote write for long-term storage
    remoteWrite:
      - url: https://thanos-receive.example.com/api/v1/receive
        writeRelabelConfigs:
          - sourceLabels: [__name__]
            regex: 'go_.*'
            action: drop

    # Additional scrape configs
    additionalScrapeConfigs:
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
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__

    # Rule selector
    ruleSelector:
      matchLabels:
        prometheus: main

alertmanager:
  alertmanagerSpec:
    replicas: 3
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 10Gi

  config:
    global:
      resolve_timeout: 5m
      slack_api_url: 'https://hooks.slack.com/services/xxx'

    route:
      group_by: ['alertname', 'namespace']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'slack-notifications'
      routes:
        - match:
            severity: critical
          receiver: 'pagerduty-critical'
          continue: true
        - match:
            severity: warning
          receiver: 'slack-warnings'
        - match_re:
            namespace: 'team-.*'
          receiver: 'team-notifications'
          group_by: ['alertname', 'namespace', 'team']

    receivers:
      - name: 'slack-notifications'
        slack_configs:
          - channel: '#alerts'
            send_resolved: true
            title: '{{ template "slack.title" . }}'
            text: '{{ template "slack.text" . }}'

      - name: 'slack-warnings'
        slack_configs:
          - channel: '#alerts-warning'
            send_resolved: true

      - name: 'pagerduty-critical'
        pagerduty_configs:
          - service_key: '<pagerduty-key>'
            send_resolved: true

      - name: 'team-notifications'
        slack_configs:
          - channel: '#team-{{ .GroupLabels.team }}-alerts'
            send_resolved: true

    templates:
      - '/etc/alertmanager/config/*.tmpl'

grafana:
  enabled: true
  adminPassword: ${GRAFANA_ADMIN_PASSWORD}

  persistence:
    enabled: true
    size: 10Gi

  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://prometheus-prometheus:9090
          isDefault: true
        - name: Loki
          type: loki
          url: http://loki:3100

  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'default'
          folder: ''
          type: file
          options:
            path: /var/lib/grafana/dashboards/default

kubeStateMetrics:
  enabled: true

nodeExporter:
  enabled: true

prometheusOperator:
  enabled: true
```

## ServiceMonitor

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
  namespace: production
  labels:
    prometheus: main
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
      scrapeTimeout: 10s
      honorLabels: true
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: namespace
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'go_gc_.*'
          action: drop
  namespaceSelector:
    matchNames:
      - production
      - staging
```

## PodMonitor

```yaml
# podmonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: myapp-sidecar
  namespace: production
  labels:
    prometheus: main
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  podMetricsEndpoints:
    - port: sidecar-metrics
      path: /metrics
      interval: 15s
  namespaceSelector:
    matchNames:
      - production
```

## PrometheusRule (Recording Rules + Alerts)

```yaml
# prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
  namespace: production
  labels:
    prometheus: main
spec:
  groups:
    - name: myapp.rules
      interval: 30s
      rules:
        # Recording rules
        - record: myapp:request_rate:5m
          expr: sum(rate(http_requests_total{app="myapp"}[5m])) by (method, status)

        - record: myapp:error_rate:5m
          expr: |
            sum(rate(http_requests_total{app="myapp",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{app="myapp"}[5m]))

        - record: myapp:latency_p99:5m
          expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{app="myapp"}[5m])) by (le))

    - name: myapp.alerts
      rules:
        # High error rate
        - alert: MyAppHighErrorRate
          expr: myapp:error_rate:5m > 0.05
          for: 5m
          labels:
            severity: critical
            team: backend
          annotations:
            summary: "High error rate for MyApp"
            description: "Error rate is {{ $value | humanizePercentage }} (>5%)"
            runbook_url: https://runbooks.example.com/myapp-high-error-rate

        # High latency
        - alert: MyAppHighLatency
          expr: myapp:latency_p99:5m > 1
          for: 10m
          labels:
            severity: warning
            team: backend
          annotations:
            summary: "High P99 latency for MyApp"
            description: "P99 latency is {{ $value | humanizeDuration }}"

        # Pod restarts
        - alert: MyAppPodRestarts
          expr: increase(kube_pod_container_status_restarts_total{namespace="production",container="myapp"}[1h]) > 3
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "MyApp pod restarting frequently"
            description: "Pod {{ $labels.pod }} has restarted {{ $value }} times in the last hour"

        # Memory usage
        - alert: MyAppHighMemory
          expr: |
            container_memory_working_set_bytes{namespace="production",container="myapp"}
            / container_spec_memory_limit_bytes{namespace="production",container="myapp"}
            > 0.85
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "MyApp memory usage high"
            description: "Memory usage is {{ $value | humanizePercentage }} of limit"

        # CPU throttling
        - alert: MyAppCPUThrottling
          expr: |
            sum(increase(container_cpu_cfs_throttled_periods_total{namespace="production",container="myapp"}[5m]))
            /
            sum(increase(container_cpu_cfs_periods_total{namespace="production",container="myapp"}[5m]))
            > 0.25
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "MyApp CPU throttling detected"
            description: "CPU throttling at {{ $value | humanizePercentage }}"
```

## Application Instrumentation (Python/FastAPI)

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from functools import wraps
import time

# Metrics definitions
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


def track_request(method, endpoint):
    """Decorator to track request metrics"""
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()
            start_time = time.time()

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
                    status=status
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
    # ... implementation
    pass
```

## Application Instrumentation (Node.js/Express)

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

## Application Instrumentation (Go)

```go
// metrics.go
package main

import (
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "path", "status"},
    )

    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
        },
        []string{"method", "path"},
    )

    httpRequestsInProgress = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "http_requests_in_progress",
            Help: "HTTP requests in progress",
        },
        []string{"method", "path"},
    )

    buildInfo = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "app_build_info",
            Help: "Application build information",
        },
        []string{"version", "commit", "build_date"},
    )
)

func init() {
    buildInfo.WithLabelValues("1.0.0", "abc123", "2025-01-01").Set(1)
}

func metricsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        path := r.URL.Path
        method := r.Method

        httpRequestsInProgress.WithLabelValues(method, path).Inc()
        timer := prometheus.NewTimer(httpRequestDuration.WithLabelValues(method, path))

        wrapped := &responseWriter{ResponseWriter: w, statusCode: 200}
        next.ServeHTTP(wrapped, r)

        timer.ObserveDuration()
        httpRequestsTotal.WithLabelValues(method, path, fmt.Sprintf("%d", wrapped.statusCode)).Inc()
        httpRequestsInProgress.WithLabelValues(method, path).Dec()
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

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.Handle("/", metricsMiddleware(http.HandlerFunc(handler)))
    http.ListenAndServe(":8080", nil)
}
```

## Common PromQL Queries

```promql
# Request rate
sum(rate(http_requests_total[5m])) by (method, status)

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m]))
* 100

# P50, P90, P99 latency
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# CPU usage percentage
sum(rate(container_cpu_usage_seconds_total{namespace="production"}[5m])) by (pod)
/ sum(container_spec_cpu_quota{namespace="production"}/container_spec_cpu_period{namespace="production"}) by (pod)
* 100

# Memory usage percentage
container_memory_working_set_bytes{namespace="production"}
/ container_spec_memory_limit_bytes{namespace="production"}
* 100

# Pod restarts in last hour
increase(kube_pod_container_status_restarts_total[1h])

# Available replicas
kube_deployment_status_replicas_available{namespace="production"}

# Node CPU available
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) * 100

# Disk usage percentage
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100

# Network traffic
sum(rate(container_network_receive_bytes_total[5m])) by (pod)
sum(rate(container_network_transmit_bytes_total[5m])) by (pod)
```

## CI/CD Specific PromQL Queries

```promql
# Jenkins build duration (p95)
histogram_quantile(0.95,
  sum(rate(jenkins_builds_duration_milliseconds_bucket[1h])) by (le, job_name)
)

# Jenkins build success rate
sum(rate(jenkins_builds_success_total[24h])) by (job_name)
/ sum(rate(jenkins_builds_total[24h])) by (job_name)
* 100

# GitLab CI pipeline duration (average)
avg(gitlab_ci_pipeline_duration_seconds) by (project, ref)

# GitLab CI pipeline success rate
sum(gitlab_ci_pipeline_status{status="success"}) by (project)
/ sum(gitlab_ci_pipeline_status) by (project)
* 100

# ArgoCD application sync status
sum(argocd_app_info{sync_status="Synced"}) by (name)

# ArgoCD application health
sum(argocd_app_info{health_status="Healthy"}) by (name)

# Deployment frequency (DORA)
count(increase(argocd_app_sync_total[7d])) by (name)

# Failed deployments
sum(argocd_app_sync_total{phase="Failed"}) by (name)
```

## Pushgateway for CI/CD Jobs

```bash
#!/bin/bash
# push-metrics.sh - Push metrics from CI/CD job

PUSHGATEWAY_URL="http://pushgateway:9091"
JOB_NAME="ci_pipeline"
INSTANCE="github-actions"

# Push build duration
cat <<EOF | curl --data-binary @- ${PUSHGATEWAY_URL}/metrics/job/${JOB_NAME}/instance/${INSTANCE}
# TYPE ci_build_duration_seconds gauge
ci_build_duration_seconds{pipeline="$GITHUB_WORKFLOW",status="$BUILD_STATUS"} $BUILD_DURATION
# TYPE ci_build_timestamp gauge
ci_build_timestamp{pipeline="$GITHUB_WORKFLOW"} $(date +%s)
# TYPE ci_build_info gauge
ci_build_info{pipeline="$GITHUB_WORKFLOW",commit="$GITHUB_SHA",branch="$GITHUB_REF_NAME"} 1
EOF
```

## GitHub Actions Workflow with Metrics

```yaml
# .github/workflows/ci.yml
name: CI with Metrics

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build
        id: build
        run: |
          START_TIME=$(date +%s)
          # Your build commands here
          npm ci && npm run build
          END_TIME=$(date +%s)
          echo "duration=$((END_TIME - START_TIME))" >> $GITHUB_OUTPUT

      - name: Push Metrics
        if: always()
        env:
          PUSHGATEWAY_URL: ${{ secrets.PUSHGATEWAY_URL }}
          BUILD_DURATION: ${{ steps.build.outputs.duration }}
          BUILD_STATUS: ${{ job.status }}
        run: |
          cat <<EOF | curl --data-binary @- ${PUSHGATEWAY_URL}/metrics/job/github_actions/instance/${{ github.repository }}
          # TYPE ci_build_duration_seconds gauge
          ci_build_duration_seconds{workflow="${{ github.workflow }}",status="${BUILD_STATUS}"} ${BUILD_DURATION}
          # TYPE ci_build_total counter
          ci_build_total{workflow="${{ github.workflow }}",status="${BUILD_STATUS}"} 1
          EOF
```

## Grafana Dashboard JSON (CI/CD Overview)

```json
{
  "title": "CI/CD Pipeline Overview",
  "uid": "cicd-overview",
  "panels": [
    {
      "title": "Build Success Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(ci_build_total{status=\"success\"}[24h])) / sum(rate(ci_build_total[24h])) * 100",
          "legendFormat": "Success Rate"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "thresholds": {
            "steps": [
              {"value": 0, "color": "red"},
              {"value": 80, "color": "yellow"},
              {"value": 95, "color": "green"}
            ]
          }
        }
      }
    },
    {
      "title": "Build Duration (P95)",
      "type": "timeseries",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(ci_build_duration_seconds_bucket[1h])) by (le, workflow))",
          "legendFormat": "{{ workflow }}"
        }
      ]
    },
    {
      "title": "Deployment Frequency",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(increase(argocd_app_sync_total{phase=\"Succeeded\"}[7d]))",
          "legendFormat": "Deployments (7d)"
        }
      ]
    }
  ]
}
```
