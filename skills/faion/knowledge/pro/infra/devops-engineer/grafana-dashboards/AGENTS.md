---
slug: grafana-dashboards
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Grafana is the leading open-source observability platform for visualizing metrics, logs, and traces.
content_id: "b612033fa605e75c"
tags: [grafana, monitoring, observability, dashboards, prometheus]
---
# Grafana Dashboards

## Summary

**One-sentence:** Grafana is the leading open-source observability platform for visualizing metrics, logs, and traces.

**One-paragraph:** Grafana is the leading open-source observability platform for visualizing metrics, logs, and traces. Use the RED method (Rate, Errors, Duration) for service dashboards and the USE method (Utilization, Saturation, Errors) for infrastructure. Provision dashboards as code via ConfigMaps or GitOps — never rely on UI-only dashboards that vanish on pod restart.

## Applies If (ALL must hold)

- Visualizing Prometheus, Loki, or Elasticsearch data for ops teams.
- Building SLO dashboards showing error budgets alongside availability.
- Creating on-call runbook dashboards with annotated deployment markers.
- Standardizing observability across microservices with shared dashboard templates.
- Grafana 12+: using Tabs to segment large dashboards without splitting metrics.

## Skip If (ANY kills it)

- Business intelligence / analytics — use dedicated BI tools (Looker, Metabase).
- Alerting without Alertmanager/Grafana Alerting configured — dashboards alone do not page.
- Replacing application logging — Grafana shows metrics, not log content (use Explore for that).
- Public customer-facing status pages — use Statuspage or similar.

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
