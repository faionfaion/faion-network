# Observability Architecture Templates

Copy-paste configurations for Prometheus, Grafana, OpenTelemetry, Loki, and Tempo.

## Table of Contents

1. [OpenTelemetry Collector](#opentelemetry-collector)
2. [Prometheus](#prometheus)
3. [Alertmanager](#alertmanager)
4. [Grafana Loki](#grafana-loki)
5. [Grafana Tempo](#grafana-tempo)
6. [Grafana Dashboards](#grafana-dashboards)
7. [Application Instrumentation](#application-instrumentation)
8. [Kubernetes Manifests](#kubernetes-manifests)

---

## OpenTelemetry Collector

### Basic Configuration

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 10000

  memory_limiter:
    check_interval: 1s
    limit_mib: 1500
    spike_limit_mib: 300

exporters:
  otlphttp/prometheus:
    endpoint: http://prometheus:9090/api/v1/otlp

  otlphttp/loki:
    endpoint: http://loki:3100/otlp

  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlphttp/prometheus]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlphttp/loki]
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/tempo]
```

### Production Configuration with Tail Sampling

```yaml
# otel-collector-production.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        max_recv_msg_size_mib: 4
      http:
        endpoint: 0.0.0.0:4318

  prometheus:
    config:
      scrape_configs:
        - job_name: 'otel-collector'
          scrape_interval: 15s
          static_configs:
            - targets: ['localhost:8888']

processors:
  batch:
    timeout: 10s
    send_batch_size: 10000
    send_batch_max_size: 11000

  memory_limiter:
    check_interval: 1s
    limit_mib: 4000
    spike_limit_mib: 800

  resource:
    attributes:
      - key: service.namespace
        value: production
        action: upsert
      - key: deployment.environment
        value: ${ENVIRONMENT}
        action: upsert

  attributes:
    actions:
      - key: http.request.header.authorization
        action: delete
      - key: db.statement
        action: hash

  filter/healthcheck:
    error_mode: ignore
    traces:
      span:
        - 'attributes["http.route"] == "/health"'
        - 'attributes["http.route"] == "/ready"'

  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    expected_new_traces_per_sec: 10000
    policies:
      - name: errors
        type: status_code
        status_code:
          status_codes: [ERROR]
      - name: slow-traces
        type: latency
        latency:
          threshold_ms: 1000
      - name: probabilistic
        type: probabilistic
        probabilistic:
          sampling_percentage: 5

exporters:
  otlphttp/mimir:
    endpoint: https://mimir.example.com/api/v1/push
    headers:
      X-Scope-OrgID: ${TENANT_ID}
    retry_on_failure:
      enabled: true
      initial_interval: 5s
      max_interval: 30s
      max_elapsed_time: 300s

  otlphttp/loki:
    endpoint: https://loki.example.com/otlp
    headers:
      X-Scope-OrgID: ${TENANT_ID}

  otlp/tempo:
    endpoint: tempo.example.com:4317
    headers:
      X-Scope-OrgID: ${TENANT_ID}
    compression: gzip

  debug:
    verbosity: detailed

extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  zpages:
    endpoint: 0.0.0.0:55679

service:
  extensions: [health_check, zpages]
  telemetry:
    logs:
      level: info
    metrics:
      address: 0.0.0.0:8888
  pipelines:
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, resource, batch]
      exporters: [otlphttp/mimir]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, resource, attributes, batch]
      exporters: [otlphttp/loki]
    traces:
      receivers: [otlp]
      processors: [memory_limiter, filter/healthcheck, tail_sampling, resource, batch]
      exporters: [otlp/tempo]
```

---

## Prometheus

### Basic Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: production
    region: us-east-1

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
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: pod
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: replace
        target_label: app
```

### Alerting Rules

```yaml
# prometheus-rules.yml
groups:
  - name: slo-alerts
    rules:
      # Multi-burn-rate SLO alert
      - alert: SLOBurnRateCritical
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > (14.4 * 0.001)
          and
          (
            sum(rate(http_requests_total{status=~"5.."}[1h]))
            /
            sum(rate(http_requests_total[1h]))
          ) > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error budget burn rate (critical)"
          description: "Error budget is burning 14.4x faster than sustainable"
          runbook_url: https://wiki.example.com/runbooks/slo-burn-rate

      - alert: SLOBurnRateWarning
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[30m]))
            /
            sum(rate(http_requests_total[30m]))
          ) > (6 * 0.001)
          and
          (
            sum(rate(http_requests_total{status=~"5.."}[6h]))
            /
            sum(rate(http_requests_total[6h]))
          ) > (6 * 0.001)
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Elevated error budget burn rate"
          description: "Error budget is burning 6x faster than sustainable"

  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: |
          (
            100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
          ) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value | printf \"%.1f\" }}%"

      - alert: HighMemoryUsage
        expr: |
          (
            (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
            /
            node_memory_MemTotal_bytes
          ) * 100 > 85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | printf \"%.1f\" }}%"

      - alert: DiskSpaceLow
        expr: |
          (
            (node_filesystem_size_bytes - node_filesystem_avail_bytes)
            /
            node_filesystem_size_bytes
          ) * 100 > 85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"

  - name: kubernetes
    rules:
      - alert: PodCrashLooping
        expr: |
          increase(kube_pod_container_status_restarts_total[1h]) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
          runbook_url: https://wiki.example.com/runbooks/pod-crash-loop

      - alert: PodNotReady
        expr: |
          kube_pod_status_ready{condition="true"} == 0
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} not ready"

      - alert: DeploymentReplicasMismatch
        expr: |
          kube_deployment_spec_replicas != kube_deployment_status_replicas_available
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} replica mismatch"

  - name: application
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          ) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate for {{ $labels.service }}"
          description: "Error rate is {{ $value | printf \"%.2f\" }}%"
          runbook_url: https://wiki.example.com/runbooks/high-error-rate

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency for {{ $labels.service }}"
          description: "p99 latency is {{ $value | printf \"%.2f\" }}s"
```

### Recording Rules

```yaml
# prometheus-recording-rules.yml
groups:
  - name: slo-recording-rules
    interval: 30s
    rules:
      # Error rate
      - record: service:http_requests_error_rate:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)

      # Success rate (SLI)
      - record: service:http_requests_success_rate:rate5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)

      # Latency percentiles
      - record: service:http_request_duration_seconds:p50
        expr: |
          histogram_quantile(0.50,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          )

      - record: service:http_request_duration_seconds:p95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          )

      - record: service:http_request_duration_seconds:p99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          )

      # Request rate
      - record: service:http_requests:rate5m
        expr: |
          sum(rate(http_requests_total[5m])) by (service)
```

---

## Alertmanager

### Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: ${SLACK_WEBHOOK_URL}
  pagerduty_url: https://events.pagerduty.com/v2/enqueue

route:
  receiver: 'default'
  group_by: ['alertname', 'service', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true

    - match:
        severity: critical
      receiver: 'slack-critical'

    - match:
        severity: warning
      receiver: 'slack-warning'

    - match:
        alertname: Watchdog
      receiver: 'null'

inhibit_rules:
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: ['alertname', 'service']

receivers:
  - name: 'null'

  - name: 'default'
    slack_configs:
      - channel: '#alerts-default'
        send_resolved: true
        title: '{{ .Status | toUpper }} | {{ .CommonLabels.alertname }}'
        text: >-
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          *Severity:* {{ .Labels.severity }}
          {{ if .Annotations.runbook_url }}*Runbook:* {{ .Annotations.runbook_url }}{{ end }}
          {{ end }}

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: ${PAGERDUTY_SERVICE_KEY}
        severity: critical
        description: '{{ .CommonAnnotations.summary }}'
        details:
          firing: '{{ .Alerts.Firing | len }}'
          resolved: '{{ .Alerts.Resolved | len }}'

  - name: 'slack-critical'
    slack_configs:
      - channel: '#alerts-critical'
        send_resolved: true
        color: '{{ if eq .Status "firing" }}danger{{ else }}good{{ end }}'
        title: '{{ .Status | toUpper }} | {{ .CommonLabels.alertname }}'
        title_link: '{{ .CommonAnnotations.runbook_url }}'
        text: >-
          {{ range .Alerts }}
          *Service:* {{ .Labels.service }}
          *Summary:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          {{ end }}

  - name: 'slack-warning'
    slack_configs:
      - channel: '#alerts-warning'
        send_resolved: true
        color: '{{ if eq .Status "firing" }}warning{{ else }}good{{ end }}'
        title: '{{ .Status | toUpper }} | {{ .CommonLabels.alertname }}'
        text: >-
          {{ range .Alerts }}
          *Service:* {{ .Labels.service }}
          *Summary:* {{ .Annotations.summary }}
          {{ end }}
```

---

## Grafana Loki

### Loki Configuration

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  instance_addr: 127.0.0.1
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

query_range:
  results_cache:
    cache:
      embedded_cache:
        enabled: true
        max_size_mb: 100

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://alertmanager:9093

limits_config:
  retention_period: 720h  # 30 days
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  max_query_series: 500
```

### Loki Production Configuration (S3)

```yaml
# loki-production.yaml
auth_enabled: true

server:
  http_listen_port: 3100
  grpc_listen_port: 9096
  log_level: info

common:
  path_prefix: /loki
  replication_factor: 3
  ring:
    kvstore:
      store: consul
      consul:
        host: consul:8500

storage_config:
  aws:
    s3: s3://us-east-1/loki-logs
    s3forcepathstyle: false
  tsdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/index_cache
    shared_store: s3

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: s3
      schema: v13
      index:
        prefix: loki_index_
        period: 24h

compactor:
  working_directory: /loki/compactor
  shared_store: s3
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150

limits_config:
  retention_period: 2160h  # 90 days
  ingestion_rate_mb: 50
  ingestion_burst_size_mb: 100
  per_stream_rate_limit: 5MB
  per_stream_rate_limit_burst: 15MB
  max_query_parallelism: 32
  max_query_series: 1000
```

---

## Grafana Tempo

### Tempo Configuration

```yaml
# tempo-config.yaml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        http:
        grpc:
    jaeger:
      protocols:
        thrift_http:
        grpc:

ingester:
  max_block_duration: 5m

compactor:
  compaction:
    block_retention: 336h  # 14 days

metrics_generator:
  registry:
    external_labels:
      source: tempo
      cluster: production
  storage:
    path: /tmp/tempo/generator/wal
    remote_write:
      - url: http://prometheus:9090/api/v1/write
        send_exemplars: true

storage:
  trace:
    backend: local
    wal:
      path: /tmp/tempo/wal
    local:
      path: /tmp/tempo/blocks

overrides:
  defaults:
    metrics_generator:
      processors: [service-graphs, span-metrics]
```

### Tempo Production Configuration (S3)

```yaml
# tempo-production.yaml
server:
  http_listen_port: 3200
  grpc_listen_port: 9095

distributor:
  receivers:
    otlp:
      protocols:
        http:
        grpc:
  ring:
    kvstore:
      store: consul
      consul:
        host: consul:8500

ingester:
  max_block_duration: 5m
  lifecycler:
    ring:
      kvstore:
        store: consul
        consul:
          host: consul:8500
      replication_factor: 3

compactor:
  compaction:
    block_retention: 336h
  ring:
    kvstore:
      store: consul
      consul:
        host: consul:8500

querier:
  frontend_worker:
    frontend_address: tempo-query-frontend:9095

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: s3.amazonaws.com
      region: us-east-1
    wal:
      path: /tmp/tempo/wal
    block:
      bloom_filter_false_positive: 0.05
      v2_index_downsample_bytes: 1000
      v2_encoding: zstd

metrics_generator:
  registry:
    external_labels:
      source: tempo
  storage:
    path: /tmp/tempo/generator/wal
    remote_write:
      - url: http://mimir:9090/api/v1/write
```

---

## Grafana Dashboards

### Service Overview Dashboard (JSON)

```json
{
  "title": "Service Overview",
  "uid": "service-overview",
  "templating": {
    "list": [
      {
        "name": "service",
        "type": "query",
        "query": "label_values(http_requests_total, service)",
        "current": { "text": "All", "value": "$__all" },
        "multi": true
      }
    ]
  },
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "gridPos": { "x": 0, "y": 0, "w": 8, "h": 8 },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{service=~\"$service\"}[5m])) by (service)",
          "legendFormat": "{{ service }}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "reqps"
        }
      }
    },
    {
      "title": "Error Rate",
      "type": "timeseries",
      "gridPos": { "x": 8, "y": 0, "w": 8, "h": 8 },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{service=~\"$service\",status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total{service=~\"$service\"}[5m])) by (service)",
          "legendFormat": "{{ service }}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percentunit",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 0.01 },
              { "color": "red", "value": 0.05 }
            ]
          }
        }
      }
    },
    {
      "title": "Latency (p99)",
      "type": "timeseries",
      "gridPos": { "x": 16, "y": 0, "w": 8, "h": 8 },
      "targets": [
        {
          "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service=~\"$service\"}[5m])) by (le, service))",
          "legendFormat": "{{ service }}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "s"
        }
      }
    },
    {
      "title": "SLO Status",
      "type": "stat",
      "gridPos": { "x": 0, "y": 8, "w": 6, "h": 4 },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{service=~\"$service\",status!~\"5..\"}[30d])) / sum(rate(http_requests_total{service=~\"$service\"}[30d]))",
          "legendFormat": "Availability (30d)"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percentunit",
          "decimals": 4,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "red", "value": null },
              { "color": "yellow", "value": 0.99 },
              { "color": "green", "value": 0.999 }
            ]
          }
        }
      }
    }
  ]
}
```

### SLO Dashboard (JSON)

```json
{
  "title": "SLO Dashboard",
  "uid": "slo-dashboard",
  "panels": [
    {
      "title": "Error Budget Remaining",
      "type": "gauge",
      "gridPos": { "x": 0, "y": 0, "w": 8, "h": 8 },
      "targets": [
        {
          "expr": "1 - ((1 - (sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d])))) / 0.001)",
          "legendFormat": "Budget Remaining"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percentunit",
          "min": 0,
          "max": 1,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "red", "value": null },
              { "color": "yellow", "value": 0.25 },
              { "color": "green", "value": 0.5 }
            ]
          }
        }
      }
    },
    {
      "title": "Burn Rate (1h)",
      "type": "stat",
      "gridPos": { "x": 8, "y": 0, "w": 4, "h": 4 },
      "targets": [
        {
          "expr": "(sum(rate(http_requests_total{status=~\"5..\"}[1h])) / sum(rate(http_requests_total[1h]))) / 0.001",
          "legendFormat": "Burn Rate"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "x",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 1 },
              { "color": "orange", "value": 6 },
              { "color": "red", "value": 14.4 }
            ]
          }
        }
      }
    }
  ]
}
```

---

## Application Instrumentation

### Python (FastAPI + OpenTelemetry)

```python
# instrumentation.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
import logging
import structlog

def setup_observability(app, service_name: str, service_version: str):
    """Configure OpenTelemetry for a FastAPI application."""

    # Create resource
    resource = Resource(attributes={
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "deployment.environment": os.getenv("ENVIRONMENT", "development"),
    })

    # Configure tracing
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317"))
        )
    )
    trace.set_tracer_provider(trace_provider)

    # Configure metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")),
        export_interval_millis=15000
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Instrument libraries
    FastAPIInstrumentor.instrument_app(app)
    HTTPXClientInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()

    # Configure structured logging
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            add_trace_context,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

def add_trace_context(logger, method_name, event_dict):
    """Add trace context to log entries."""
    span = trace.get_current_span()
    if span:
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict

# Custom metrics
meter = metrics.get_meter(__name__)

request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total HTTP requests",
    unit="1"
)

request_duration = meter.create_histogram(
    name="http_request_duration_seconds",
    description="HTTP request duration",
    unit="s"
)

# Usage in FastAPI
from fastapi import FastAPI, Request
import time

app = FastAPI()
setup_observability(app, "my-service", "1.0.0")

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    request_counter.add(
        1,
        attributes={
            "method": request.method,
            "endpoint": request.url.path,
            "status": response.status_code
        }
    )

    request_duration.record(
        duration,
        attributes={
            "method": request.method,
            "endpoint": request.url.path
        }
    )

    return response
```

### Go (with OpenTelemetry)

```go
// instrumentation.go
package observability

import (
    "context"
    "log"
    "os"
    "time"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
    "go.opentelemetry.io/otel/metric"
    "go.opentelemetry.io/otel/propagation"
    sdkmetric "go.opentelemetry.io/otel/sdk/metric"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func InitObservability(ctx context.Context, serviceName, serviceVersion string) (func(), error) {
    res, err := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName(serviceName),
            semconv.ServiceVersion(serviceVersion),
            attribute.String("deployment.environment", os.Getenv("ENVIRONMENT")),
        ),
    )
    if err != nil {
        return nil, err
    }

    // Trace exporter
    traceExporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint(os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(traceExporter),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.TraceIDRatioBased(0.1)),
    )
    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    ))

    // Metric exporter
    metricExporter, err := otlpmetricgrpc.New(ctx,
        otlpmetricgrpc.WithEndpoint(os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")),
        otlpmetricgrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    mp := sdkmetric.NewMeterProvider(
        sdkmetric.WithReader(sdkmetric.NewPeriodicReader(metricExporter, sdkmetric.WithInterval(15*time.Second))),
        sdkmetric.WithResource(res),
    )
    otel.SetMeterProvider(mp)

    return func() {
        ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
        defer cancel()
        tp.Shutdown(ctx)
        mp.Shutdown(ctx)
    }, nil
}

// Custom metrics
var (
    meter           = otel.Meter("my-service")
    requestCounter  metric.Int64Counter
    requestDuration metric.Float64Histogram
)

func init() {
    var err error
    requestCounter, err = meter.Int64Counter(
        "http_requests_total",
        metric.WithDescription("Total HTTP requests"),
    )
    if err != nil {
        log.Fatal(err)
    }

    requestDuration, err = meter.Float64Histogram(
        "http_request_duration_seconds",
        metric.WithDescription("HTTP request duration"),
        metric.WithUnit("s"),
    )
    if err != nil {
        log.Fatal(err)
    }
}

func RecordRequest(ctx context.Context, method, endpoint string, status int, duration float64) {
    attrs := []attribute.KeyValue{
        attribute.String("method", method),
        attribute.String("endpoint", endpoint),
        attribute.Int("status", status),
    }
    requestCounter.Add(ctx, 1, metric.WithAttributes(attrs...))
    requestDuration.Record(ctx, duration, metric.WithAttributes(attrs[:2]...))
}
```

---

## Kubernetes Manifests

### OTEL Collector DaemonSet

```yaml
# otel-collector-daemonset.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: observability
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
    processors:
      batch:
        timeout: 10s
      memory_limiter:
        check_interval: 1s
        limit_mib: 1500
    exporters:
      otlphttp:
        endpoint: http://tempo.observability:4318
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [otlphttp]
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: otel-collector
  namespace: observability
spec:
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      serviceAccountName: otel-collector
      containers:
      - name: collector
        image: otel/opentelemetry-collector-contrib:0.92.0
        args:
          - --config=/etc/otel/config.yaml
        ports:
        - containerPort: 4317
          name: otlp-grpc
        - containerPort: 4318
          name: otlp-http
        - containerPort: 8888
          name: metrics
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        volumeMounts:
        - name: config
          mountPath: /etc/otel
        livenessProbe:
          httpGet:
            path: /
            port: 13133
        readinessProbe:
          httpGet:
            path: /
            port: 13133
      volumes:
      - name: config
        configMap:
          name: otel-collector-config
---
apiVersion: v1
kind: Service
metadata:
  name: otel-collector
  namespace: observability
spec:
  selector:
    app: otel-collector
  ports:
  - name: otlp-grpc
    port: 4317
    targetPort: 4317
  - name: otlp-http
    port: 4318
    targetPort: 4318
```

### Prometheus Operator ServiceMonitor

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-service
  namespace: observability
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: my-service
  namespaceSelector:
    matchNames:
      - default
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
```

### PrometheusRule

```yaml
# prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: my-service-alerts
  namespace: observability
  labels:
    release: prometheus
spec:
  groups:
  - name: my-service
    rules:
    - alert: MyServiceHighErrorRate
      expr: |
        sum(rate(http_requests_total{service="my-service",status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total{service="my-service"}[5m])) > 0.01
      for: 5m
      labels:
        severity: critical
        service: my-service
      annotations:
        summary: "High error rate for my-service"
        runbook_url: https://wiki.example.com/runbooks/my-service-errors
```

---

## Quick Reference

### OTEL Environment Variables

```bash
# Common OTEL environment variables
OTEL_SERVICE_NAME=my-service
OTEL_SERVICE_VERSION=1.0.0
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production,service.namespace=default
```

### PromQL Cheat Sheet

```promql
# Request rate
sum(rate(http_requests_total[5m])) by (service)

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Latency percentiles
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Availability (success rate)
sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Error budget burn rate
(error_rate / error_budget_per_second)
```

### LogQL Cheat Sheet

```logql
# Filter by service and level
{service="my-service"} |= "error"

# JSON parsing
{service="my-service"} | json | level="error"

# Rate of errors
sum(rate({service="my-service"} |= "error" [5m]))

# Correlation with trace
{service="my-service"} | json | trace_id="abc123"
```
