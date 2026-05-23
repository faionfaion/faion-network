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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-monitoring.py` | Validate the monitoring artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-haproxy-production]]
- [[lb-nginx-production]]
- [[lb-kubernetes-ingress]]
- [[prometheus-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (LB tech, alert sensitivity, log destination) to a concrete monitoring stack, each leaf referencing a rule from `01-core-rules.xml`.
