# Load Balancer Monitoring and Observability

## Summary

**One-sentence:** Generates a Prometheus scrape + 4-alert rule set + Grafana dashboard + log shipping config for HAProxy / Nginx LBs with per-backend dimensions.

**One-paragraph:** LB monitoring requires Prometheus exporters (`haproxy-exporter:9101`, `nginx-prometheus-exporter:9113`), four core alert rules (BackendDown for 1 m, HighErrorRate &gt; 5% for 5 m, HighLatency p99 &gt; 2 s for 5 m, ConnectionPoolExhausted &gt; 90% for 2 m), Grafana dashboards with per-backend breakdown, and centralized log aggregation (ELK / Loki) of LB access logs for audit trail and debugging.

**Ефективно для:**

- New HAProxy / Nginx deploy: одночасно з config — Prometheus exporter + 4 alerts.
- Existing LB без monitoring — додати scrape + alerts, не змінюючи самого LB.
- Define SLI / SLO для load-balanced service (5xx rate, p99 latency).
- Flapping backend → log correlation через Loki / ELK + Grafana annotations.
- К8s Ingress: ServiceMonitor + Grafana panel замість окремого exporter.

## Applies If (ALL must hold)

- Setting up observability for a new HAProxy or Nginx production deployment.
- Adding Prometheus scraping and alerting to an existing LB that lacks monitoring.
- Defining SLIs (error rate, latency p99) and SLOs for a load-balanced service.
- Diagnosing intermittent backend health flapping via log correlation.

## Skip If (ANY kills it)

- Cloud-managed LBs (AWS ALB / NLB) — use CloudWatch metrics + alerting.
- Kubernetes Ingress controllers — use the controller's `/metrics` via ServiceMonitor; no separate exporter.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| LB technology | haproxy / nginx | infra |
| Prometheus instance | URL | platform team |
| Grafana instance | URL | platform team |
| Log sink | ELK / Loki / S3 | logging |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[lb-haproxy-production]] | HAProxy stats socket / endpoint required by exporter. |
| [[lb-nginx-production]] | Nginx `stub_status` required by exporter. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: exporter-required, 4-core-alerts, per-backend-dimension, log-shipping, dashboard-templated | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wire-exporter` | sonnet | Per-LB exporter selection. |
| `write-alerts` | sonnet | Promql tuning for thresholds. |
| `import-dashboard` | haiku | Mechanical import of dashboard JSON. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prometheus-rules.yaml` | Four-alert PromQL ruleset |
| `templates/grafana-dashboard.json` | LB dashboard with per-backend panels |
| `templates/promtail-haproxy.yaml` | Promtail config shipping HAProxy logs to Loki |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-monitoring.py` | Validate the monitoring artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[lb-haproxy-production]]
- [[lb-nginx-production]]
- [[lb-kubernetes-ingress]]
- [[prometheus-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (LB tech, alert sensitivity, log destination) to a concrete monitoring stack, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prometheus-rules.yaml`

```yaml
groups:
  - name: load_balancer_alerts
    rules:
      - alert: BackendDown
        expr: haproxy_backend_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Backend {{ $labels.backend }} on {{ $labels.instance }} is down"

      - alert: HighErrorRate
        expr: |
          sum by (backend, instance) (
            rate(haproxy_backend_http_responses_total{code="5xx"}[5m])
          )
          /
          sum by (backend, instance) (
            rate(haproxy_backend_http_responses_total[5m])
          ) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "5xx rate > 5% on {{ $labels.backend }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum by (backend, instance, le) (
              rate(haproxy_backend_http_response_time_seconds_bucket[5m])
            )
          ) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency > 2 s on {{ $labels.backend }}"

      - alert: ConnectionPoolExhausted
        expr: |
          haproxy_backend_current_sessions
          / haproxy_backend_limit_sessions > 0.9
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Connection pool > 90% on {{ $labels.backend }}"
```

### `templates/grafana-dashboard.json`

```json
{
  "title": "Load Balancer",
  "schemaVersion": 38,
  "templating": {
    "list": [
      {
        "name": "instance",
        "type": "query",
        "query": "label_values(haproxy_backend_up, instance)",
        "refresh": 1
      },
      {
        "name": "backend",
        "type": "query",
        "query": "label_values(haproxy_backend_up{instance=~\"$instance\"}, backend)",
        "refresh": 1
      }
    ]
  },
  "panels": [
    {
      "title": "Backend up",
      "type": "stat",
      "targets": [
        {
          "expr": "haproxy_backend_up{instance=~\"$instance\",backend=~\"$backend\"}"
        }
      ]
    },
    {
      "title": "Request rate",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sum by (backend) (rate(haproxy_backend_http_responses_total{instance=~\"$instance\",backend=~\"$backend\"}[1m]))"
        }
      ]
    },
    {
      "title": "5xx rate",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sum by (backend) (rate(haproxy_backend_http_responses_total{code=\"5xx\",instance=~\"$instance\",backend=~\"$backend\"}[5m]))"
        }
      ]
    },
    {
      "title": "p99 latency",
      "type": "timeseries",
      "targets": [
        {
          "expr": "histogram_quantile(0.99, sum by (backend, le) (rate(haproxy_backend_http_response_time_seconds_bucket{instance=~\"$instance\",backend=~\"$backend\"}[5m])))"
        }
      ]
    },
    {
      "title": "Connection pool",
      "type": "timeseries",
      "targets": [
        {
          "expr": "haproxy_backend_current_sessions{instance=~\"$instance\",backend=~\"$backend\"} / haproxy_backend_limit_sessions"
        }
      ]
    }
  ]
}
```

### `templates/promtail-haproxy.yaml`

```yaml
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

positions:
  filename: /var/lib/promtail/positions.yaml

scrape_configs:
  - job_name: haproxy
    static_configs:
      - targets: [localhost]
        labels:
          job: haproxy
          host: ${HOSTNAME}
          __path__: /var/log/haproxy.log
    pipeline_stages:
      - regex:
          expression: '(?P<remote_addr>\S+) (?P<frontend>\S+) (?P<backend>\S+)/(?P<server>\S+) (?P<tq>\d+)/(?P<tw>\d+)/(?P<tc>\d+)/(?P<tr>\d+)/(?P<tt>\d+) (?P<status>\d+) (?P<bytes>\d+).+ \"(?P<request>[^\"]+)\"'
      - labels:
          backend:
          status:
      - timestamp:
          source: time
          format: RFC3339
```
