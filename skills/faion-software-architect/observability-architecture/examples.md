# Observability Architecture Examples

Real-world observability stack implementations for different scales and use cases.

## Example 1: Startup / Small Team (< 10 services)

### Context
- 5-10 microservices
- Kubernetes on single cloud
- Team of 3-5 engineers
- Budget-conscious

### Stack

| Component | Tool | Reason |
|-----------|------|--------|
| Metrics | Prometheus | Free, Kubernetes native |
| Logs | Loki | Cost-effective, Grafana integration |
| Traces | Tempo | Free, easy setup |
| Visualization | Grafana | Unified dashboards |
| Alerting | Alertmanager | Prometheus native |
| Collection | Grafana Alloy | Single binary, OTEL compatible |

### Architecture

```
                    Kubernetes Cluster
+----------------------------------------------------------+
|                                                          |
|  +------------+  +------------+  +------------+          |
|  | Service A  |  | Service B  |  | Service C  |          |
|  | (OTEL SDK) |  | (OTEL SDK) |  | (OTEL SDK) |          |
|  +-----+------+  +-----+------+  +-----+------+          |
|        |               |               |                 |
|        +-------+-------+-------+-------+                 |
|                |                                         |
|         +------v------+                                  |
|         | Grafana     |                                  |
|         | Alloy       |  (DaemonSet)                     |
|         | (Collector) |                                  |
|         +------+------+                                  |
|                |                                         |
+----------------+------------------------------------------+
                 |
    +------------+------------+------------+
    |            |            |            |
+---v---+   +----v----+   +---v---+   +----v----+
| Mimir |   | Loki    |   | Tempo |   | Grafana |
|(metrics)  | (logs)  |   |(traces)   | (viz)   |
+-------+   +---------+   +-------+   +---------+
    |            |            |
    +------------+------------+
                 |
         +-------v-------+
         | Object Storage|
         | (S3/MinIO)    |
         +---------------+
```

### Configuration

**Grafana Alloy (collector):**
```hcl
// Receive OTLP data from applications
otelcol.receiver.otlp "default" {
  grpc {
    endpoint = "0.0.0.0:4317"
  }
  http {
    endpoint = "0.0.0.0:4318"
  }
  output {
    metrics = [otelcol.processor.batch.default.input]
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.batch.default.input]
  }
}

// Batch processing
otelcol.processor.batch "default" {
  output {
    metrics = [otelcol.exporter.prometheus.default.input]
    logs    = [otelcol.exporter.loki.default.input]
    traces  = [otelcol.exporter.otlp.tempo.input]
  }
}

// Export to backends
otelcol.exporter.prometheus "default" {
  forward_to = [prometheus.remote_write.mimir.receiver]
}

otelcol.exporter.loki "default" {
  forward_to = [loki.write.default.receiver]
}

otelcol.exporter.otlp "tempo" {
  client {
    endpoint = "tempo:4317"
    tls {
      insecure = true
    }
  }
}
```

### SLO Example

**API Service SLO:**
```yaml
# 99.9% of requests complete successfully in < 200ms
service: api-gateway
slos:
  - name: availability
    sli: sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
    target: 0.999
    window: 30d

  - name: latency
    sli: sum(rate(http_request_duration_seconds_bucket{le="0.2"}[5m])) / sum(rate(http_request_duration_seconds_count[5m]))
    target: 0.99
    window: 30d
```

### Cost Estimate

| Component | Monthly Cost |
|-----------|--------------|
| Compute (3 nodes) | $150-300 |
| Storage (500GB) | $25-50 |
| Total | ~$200-400/month |

---

## Example 2: Mid-Size Company (50-100 services)

### Context
- 50-100 microservices
- Multi-cluster Kubernetes
- Team of 15-25 engineers
- Moderate budget

### Stack

| Component | Tool | Reason |
|-----------|------|--------|
| Metrics | Prometheus + Thanos | Scalable, long-term storage |
| Logs | Loki (distributed) | Cost-effective at scale |
| Traces | Tempo (distributed) | Scalable tracing |
| Visualization | Grafana Enterprise | Advanced features |
| Alerting | Alertmanager (HA) | Reliable alerting |
| Collection | OTEL Collector | Vendor-neutral |
| On-call | PagerDuty | Professional incident management |

### Architecture

```
                         Production Clusters
+---------------------------+  +---------------------------+
|     Cluster: US-East      |  |     Cluster: EU-West      |
|                           |  |                           |
| +-------+ +-------+       |  | +-------+ +-------+       |
| |Service| |Service| ...   |  | |Service| |Service| ...   |
| +---+---+ +---+---+       |  | +---+---+ +---+---+       |
|     |         |           |  |     |         |           |
| +---v---------v---+       |  | +---v---------v---+       |
| | OTEL Collector  |       |  | | OTEL Collector  |       |
| | (Gateway)       |       |  | | (Gateway)       |       |
| +-------+---------+       |  | +-------+---------+       |
|         |                 |  |         |                 |
| +-------v-------+         |  | +-------v-------+         |
| | Prometheus    |         |  | | Prometheus    |         |
| | (local)       |         |  | | (local)       |         |
| +-------+-------+         |  | +-------+-------+         |
+---------+-----------------+  +---------+-----------------+
          |                              |
          +-------------+----------------+
                        |
              +---------v---------+
              |     Thanos        |
              | (Query + Store)   |
              +---------+---------+
                        |
    +-------------------+-------------------+
    |                   |                   |
+---v---+         +-----v-----+       +-----v-----+
| Loki  |         |   Tempo   |       |  Grafana  |
| (HA)  |         |   (HA)    |       |Enterprise |
+---+---+         +-----+-----+       +-----------+
    |                   |
    +-------------------+
            |
    +-------v-------+
    | Object Storage|
    | (S3/GCS)      |
    +---------------+
```

### Thanos Configuration

**Thanos Sidecar (per Prometheus):**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: prometheus
spec:
  template:
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:v2.48.0
        args:
          - --config.file=/etc/prometheus/prometheus.yml
          - --storage.tsdb.path=/prometheus
          - --storage.tsdb.min-block-duration=2h
          - --storage.tsdb.max-block-duration=2h

      - name: thanos-sidecar
        image: quay.io/thanos/thanos:v0.32.0
        args:
          - sidecar
          - --tsdb.path=/prometheus
          - --prometheus.url=http://localhost:9090
          - --objstore.config-file=/etc/thanos/objstore.yml
```

**Thanos Query:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thanos-query
spec:
  template:
    spec:
      containers:
      - name: thanos-query
        image: quay.io/thanos/thanos:v0.32.0
        args:
          - query
          - --store=dnssrv+_grpc._tcp.thanos-sidecar.monitoring.svc
          - --store=dnssrv+_grpc._tcp.thanos-store.monitoring.svc
          - --query.auto-downsampling
```

### Multi-Cluster Loki

```yaml
# Loki distributed mode
loki:
  schemaConfig:
    configs:
      - from: 2024-01-01
        store: tsdb
        object_store: s3
        schema: v13
        index:
          prefix: loki_index_
          period: 24h

  storage:
    type: s3
    s3:
      endpoint: s3.amazonaws.com
      bucketnames: company-loki-logs
      region: us-east-1

  limits_config:
    retention_period: 30d
    ingestion_rate_mb: 50
    ingestion_burst_size_mb: 100
```

### SLO Dashboard

**Grafana SLO Panel:**
```json
{
  "title": "SLO: API Availability (30d)",
  "type": "stat",
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{job=\"api\",status!~\"5..\"}[30d])) / sum(rate(http_requests_total{job=\"api\"}[30d]))",
      "legendFormat": "Availability"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "color": "red", "value": 0 },
          { "color": "yellow", "value": 0.99 },
          { "color": "green", "value": 0.999 }
        ]
      },
      "unit": "percentunit",
      "decimals": 4
    }
  }
}
```

### Cost Estimate

| Component | Monthly Cost |
|-----------|--------------|
| Compute (10 nodes) | $1,500-3,000 |
| Storage (5TB) | $250-500 |
| Grafana Enterprise | $500-1,000 |
| PagerDuty | $300-600 |
| Total | ~$2,500-5,000/month |

---

## Example 3: Enterprise (500+ services)

### Context
- 500+ microservices
- Multi-cloud, multi-region
- Team of 100+ engineers
- Multiple teams with different needs

### Stack

| Component | Tool | Reason |
|-----------|------|--------|
| Metrics | Grafana Mimir | Infinitely scalable |
| Logs | Grafana Loki | Unified with metrics |
| Traces | Grafana Tempo | Native Grafana integration |
| Visualization | Grafana Cloud | Managed, enterprise features |
| Alerting | Grafana Alerting + Opsgenie | Unified alerting |
| Collection | OTEL Collector (fleet) | Centrally managed |
| APM | Grafana Application Observability | Full APM |

### Architecture

```
+------------------------------------------------------------------+
|                    Global Observability Platform                  |
+------------------------------------------------------------------+

     Region: US                Region: EU                Region: APAC
+------------------+     +------------------+     +------------------+
|  +-----------+   |     |  +-----------+   |     |  +-----------+   |
|  | Cluster 1 |   |     |  | Cluster 1 |   |     |  | Cluster 1 |   |
|  +-----------+   |     |  +-----------+   |     |  +-----------+   |
|  +-----------+   |     |  +-----------+   |     |  +-----------+   |
|  | Cluster 2 |   |     |  | Cluster 2 |   |     |  | Cluster 2 |   |
|  +-----------+   |     |  +-----------+   |     |  +-----------+   |
|        |         |     |        |         |     |        |         |
|  +-----v-----+   |     |  +-----v-----+   |     |  +-----v-----+   |
|  | Regional  |   |     |  | Regional  |   |     |  | Regional  |   |
|  | OTEL GW   |   |     |  | OTEL GW   |   |     |  | OTEL GW   |   |
|  +-----+-----+   |     |  +-----+-----+   |     |  +-----+-----+   |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                    +-------------v-------------+
                    |    Global Load Balancer   |
                    +-------------+-------------+
                                  |
         +------------------------+------------------------+
         |                        |                        |
   +-----v-----+            +-----v-----+            +-----v-----+
   |   Mimir   |            |   Loki    |            |   Tempo   |
   |  (metrics)|            |  (logs)   |            | (traces)  |
   +-----------+            +-----------+            +-----------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                    +-------------v-------------+
                    |    Object Storage (S3)    |
                    |    (Multi-Region Replica) |
                    +---------------------------+

                    +---------------------------+
                    |      Grafana Cloud        |
                    |  - Unified Dashboards     |
                    |  - Alerting               |
                    |  - SLO Management         |
                    |  - Team Workspaces        |
                    +---------------------------+
```

### OTEL Collector Fleet Management

**Central Configuration (GitOps):**
```yaml
# collector-config.yaml (stored in Git, deployed via ArgoCD)
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-collector
  namespace: observability
spec:
  mode: daemonset
  targetAllocator:
    enabled: true
    serviceAccount: target-allocator-sa
    prometheusCR:
      enabled: true
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      prometheus:
        config:
          scrape_configs:
            - job_name: 'kubernetes-pods'
              kubernetes_sd_configs:
                - role: pod
              relabel_configs:
                - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
                  action: keep
                  regex: true

    processors:
      batch:
        timeout: 10s
        send_batch_size: 10000
      memory_limiter:
        check_interval: 1s
        limit_mib: 2000
        spike_limit_mib: 400
      resource:
        attributes:
          - key: cluster
            value: ${CLUSTER_NAME}
            action: insert
          - key: region
            value: ${REGION}
            action: insert
      tail_sampling:
        decision_wait: 10s
        policies:
          - name: error-sampling
            type: status_code
            status_code:
              status_codes: [ERROR]
          - name: latency-sampling
            type: latency
            latency:
              threshold_ms: 1000
          - name: probabilistic
            type: probabilistic
            probabilistic:
              sampling_percentage: 5

    exporters:
      otlphttp/mimir:
        endpoint: https://mimir.observability.company.com/api/v1/push
        headers:
          X-Scope-OrgID: ${TENANT_ID}
      otlphttp/loki:
        endpoint: https://loki.observability.company.com/loki/api/v1/push
        headers:
          X-Scope-OrgID: ${TENANT_ID}
      otlp/tempo:
        endpoint: tempo.observability.company.com:4317
        headers:
          X-Scope-OrgID: ${TENANT_ID}

    service:
      pipelines:
        metrics:
          receivers: [otlp, prometheus]
          processors: [memory_limiter, batch, resource]
          exporters: [otlphttp/mimir]
        logs:
          receivers: [otlp]
          processors: [memory_limiter, batch, resource]
          exporters: [otlphttp/loki]
        traces:
          receivers: [otlp]
          processors: [memory_limiter, tail_sampling, batch, resource]
          exporters: [otlp/tempo]
```

### Multi-Tenant Configuration

**Mimir Multi-Tenancy:**
```yaml
# mimir-config.yaml
multitenancy_enabled: true

limits:
  # Per-tenant limits
  ingestion_rate: 100000
  ingestion_burst_size: 200000
  max_global_series_per_user: 5000000
  max_label_names_per_series: 30

overrides:
  # Team-specific overrides
  team-payments:
    ingestion_rate: 200000
    max_global_series_per_user: 10000000
  team-search:
    ingestion_rate: 150000
    max_global_series_per_user: 8000000
```

### Enterprise SLO Management

**SLO Definition (Grafana SLO):**
```yaml
apiVersion: slo.grafana.net/v1
kind: ServiceLevelObjective
metadata:
  name: checkout-availability
  labels:
    team: payments
    tier: critical
spec:
  description: "Checkout service availability"
  service: checkout-service
  query:
    freeform:
      query: |
        sum(rate(http_requests_total{job="checkout",status!~"5.."}[{{.window}}]))
        /
        sum(rate(http_requests_total{job="checkout"}[{{.window}}]))
  objectives:
    - target: 0.9995  # 99.95%
      window: 30d
  alerting:
    fastBurn:
      labels:
        severity: critical
      annotations:
        runbook_url: https://wiki.company.com/runbooks/checkout-availability
    slowBurn:
      labels:
        severity: warning
```

### Cost Estimate

| Component | Monthly Cost |
|-----------|--------------|
| Grafana Cloud (Enterprise) | $15,000-50,000 |
| Compute (50+ nodes) | $20,000-50,000 |
| Storage (50TB+) | $2,500-5,000 |
| Opsgenie | $1,000-3,000 |
| Total | ~$40,000-100,000/month |

---

## Example 4: E-Commerce Platform

### Context
- High traffic (10K+ RPS)
- Black Friday spikes (10x normal)
- Payment processing (PCI DSS)
- Real-time inventory

### Critical Metrics

**Business SLOs:**
```yaml
slos:
  - name: checkout_success_rate
    target: 99.9%
    window: 30d
    query: |
      sum(rate(checkout_completed_total[5m]))
      /
      sum(rate(checkout_started_total[5m]))

  - name: payment_latency
    target: 99%  # < 2 seconds
    window: 30d
    query: |
      histogram_quantile(0.99,
        sum(rate(payment_duration_seconds_bucket[5m])) by (le)
      ) < 2

  - name: inventory_sync_lag
    target: 99.9%  # < 30 seconds
    window: 30d
    query: |
      (time() - inventory_last_sync_timestamp) < 30
```

**Critical Alerts:**
```yaml
groups:
  - name: ecommerce-critical
    rules:
      - alert: CheckoutErrorRateHigh
        expr: |
          (
            sum(rate(checkout_errors_total[5m]))
            /
            sum(rate(checkout_attempts_total[5m]))
          ) > 0.01
        for: 2m
        labels:
          severity: critical
          team: payments
        annotations:
          summary: "Checkout error rate > 1%"
          runbook_url: https://wiki/runbooks/checkout-errors

      - alert: PaymentProviderDown
        expr: |
          sum(rate(payment_provider_errors_total{type="connection"}[1m])) > 0
        for: 30s
        labels:
          severity: critical
          team: payments
        annotations:
          summary: "Payment provider connection failures"
          runbook_url: https://wiki/runbooks/payment-provider
```

**Black Friday Scaling:**
```yaml
# Auto-scaling based on observability data
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: checkout-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout
  minReplicas: 10
  maxReplicas: 100
  metrics:
    - type: External
      external:
        metric:
          name: checkout_queue_depth
          selector:
            matchLabels:
              service: checkout
        target:
          type: AverageValue
          averageValue: 100
```

---

## Example 5: SaaS Platform (Multi-Tenant)

### Context
- B2B SaaS application
- Per-tenant isolation
- Different SLAs per tier
- Compliance requirements

### Per-Tenant Observability

**Tenant-Aware Metrics:**
```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['tenant_id', 'method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency',
    ['tenant_id', 'method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Usage
@app.middleware
def metrics_middleware(request, call_next):
    tenant_id = get_tenant_id(request)
    start = time.time()

    response = call_next(request)

    REQUEST_COUNT.labels(
        tenant_id=tenant_id,
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        tenant_id=tenant_id,
        method=request.method,
        endpoint=request.path
    ).observe(time.time() - start)

    return response
```

**Tiered SLOs:**
```yaml
# slos-by-tier.yaml
tiers:
  enterprise:
    availability_target: 99.99%
    latency_p99_target: 100ms
    support_response: 15min

  business:
    availability_target: 99.9%
    latency_p99_target: 200ms
    support_response: 4h

  starter:
    availability_target: 99.5%
    latency_p99_target: 500ms
    support_response: 24h
```

**Per-Tenant Dashboards (Grafana):**
```json
{
  "templating": {
    "list": [
      {
        "name": "tenant_id",
        "type": "query",
        "query": "label_values(http_requests_total, tenant_id)",
        "multi": false
      }
    ]
  },
  "panels": [
    {
      "title": "Request Rate - $tenant_id",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{tenant_id=\"$tenant_id\"}[5m]))"
        }
      ]
    }
  ]
}
```

---

## Comparison Summary

| Aspect | Startup | Mid-Size | Enterprise | E-Commerce | SaaS |
|--------|---------|----------|------------|------------|------|
| Services | 5-10 | 50-100 | 500+ | 50-200 | 100-500 |
| Data Volume | 10GB/day | 500GB/day | 10TB/day | 1TB/day | 2TB/day |
| Retention | 15 days | 30 days | 1 year | 90 days | 90 days |
| HA Required | No | Yes | Yes | Yes | Yes |
| Multi-Region | No | Optional | Yes | Yes | Yes |
| Cost/Month | $200-400 | $2.5-5K | $40-100K | $10-30K | $5-20K |
| Team Size | 3-5 | 15-25 | 100+ | 20-50 | 10-30 |

## Key Takeaways

1. **Start Simple**: Begin with Prometheus + Grafana + Loki, scale later
2. **Use OpenTelemetry**: Avoid vendor lock-in from day one
3. **Define SLOs First**: Build observability around what matters
4. **Automate Everything**: GitOps for collector configs, alerts, dashboards
5. **Plan for Scale**: Choose tools that can grow with you
6. **Control Costs**: Implement sampling and retention early
