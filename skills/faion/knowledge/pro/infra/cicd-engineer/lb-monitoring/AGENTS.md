---
slug: lb-monitoring
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LB monitoring requires Prometheus exporters (haproxy-exporter:9101, nginx-exporter:9113), four core alert rules (BackendDown, HighErrorRate >5%, HighLatency p99 >2s, ConnectionPoolExhausted >90%), Grafana dashboards with per-backend breakdown, and centralized log aggregation (ELK/Loki) of LB access logs for audit trail and debugging.
content_id: "8de24fa3f1a4c474"
tags: [monitoring, prometheus, grafana, load-balancing, observability]
---
# Load Balancer Monitoring and Observability

## Summary

**One-sentence:** LB monitoring requires Prometheus exporters (haproxy-exporter:9101, nginx-exporter:9113), four core alert rules (BackendDown, HighErrorRate >5%, HighLatency p99 >2s, ConnectionPoolExhausted >90%), Grafana dashboards with per-backend breakdown, and centralized log aggregation (ELK/Loki) of LB access logs for audit trail and debugging.

**One-paragraph:** LB monitoring requires Prometheus exporters (haproxy-exporter:9101, nginx-exporter:9113), four core alert rules (BackendDown, HighErrorRate >5%, HighLatency p99 >2s, ConnectionPoolExhausted >90%), Grafana dashboards with per-backend breakdown, and centralized log aggregation (ELK/Loki) of LB access logs for audit trail and debugging.

## Applies If (ALL must hold)

- Setting up observability for a new HAProxy or Nginx production deployment.
- Adding Prometheus scraping and alerting to an existing LB that lacks monitoring.
- Defining SLIs (error rate, latency p99) and SLOs for a load-balanced service.
- Diagnosing intermittent backend health flapping via log correlation.

## Skip If (ANY kills it)

- Cloud managed LBs (AWS ALB/NLB) — use CloudWatch metrics and AWS-native alerting instead; Prometheus exporters are not applicable.
- Kubernetes Ingress controller metrics — use the controller's built-in /metrics endpoint with a ServiceMonitor; no separate exporter needed.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
