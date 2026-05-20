---
slug: prometheus-monitoring
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Prometheus is the de facto standard for Kubernetes monitoring: pull-based metrics, PromQL queries, Alertmanager routing.
content_id: "c6637d6806d5e305"
tags: [prometheus, monitoring, metrics, alerting, kubernetes]
---
# Prometheus Monitoring

## Summary

**One-sentence:** Prometheus is the de facto standard for Kubernetes monitoring: pull-based metrics, PromQL queries, Alertmanager routing.

**One-paragraph:** Prometheus is the de facto standard for Kubernetes monitoring: pull-based metrics, PromQL queries, Alertmanager routing. Never use unbounded labels — each unique value creates a time series. Alert on symptoms, not causes.

## Applies If (ALL must hold)

- Kubernetes cluster and workload monitoring (kube-state-metrics, node-exporter, cAdvisor)
- Application SLI/SLO measurement via custom metrics
- Alert routing with Alertmanager (Slack, PagerDuty, email)
- Pre-computing expensive dashboard queries with recording rules
- Long-term storage via remote write to Thanos, Mimir, or Cortex

## Skip If (ANY kills it)

- Log aggregation — use Loki or ELK; Prometheus is metrics only
- Distributed tracing — use Jaeger or Tempo
- High-cardinality event data (per-request attributes) — use a log/trace system
- When you need sub-second resolution — Prometheus scrape interval minimum is ~10s

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

- parent skill: `pro/infra/devops-engineer/`
