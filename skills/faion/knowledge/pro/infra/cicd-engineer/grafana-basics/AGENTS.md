---
slug: grafana-basics
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Grafana is an open-source observability platform for visualizing metrics, logs, and traces.
content_id: "fc00d5ebd4a4ef5b"
tags: [grafana, observability, dashboards, prometheus, monitoring]
---
# Grafana Basics

## Summary

**One-sentence:** Grafana is an open-source observability platform for visualizing metrics, logs, and traces.

**One-paragraph:** Grafana is an open-source observability platform for visualizing metrics, logs, and traces. It supports multiple data sources (Prometheus, Loki, Elasticsearch, InfluxDB), provides rich visualization options, and enables alerting based on dashboard panels. Treat dashboards as code from day one: generate JSON, review via API or Grafonnet, never hand-click in the UI.

## Applies If (ALL must hold)

- Visualizing Prometheus metrics
- Creating operational dashboards
- Building SLO/SLI dashboards
- Log analysis with Loki
- Unified observability across multiple data sources
- Real-time monitoring and incident response
- Surfacing Prometheus / Loki / Tempo data the team already collects but never looks at — turning silent metrics into a dashboard the on-call actually opens
- Building per-service RED/USE/Golden-Signals dashboards as part of a service onboarding template, so every new service ships with the same five panels
- SLO/error-budget visualization once recording rules exist (job:slo_burn:ratio_rate1h)
- Incident-response timelines: combining annotations (deploys, releases) with metrics on a single graph
- Loki log exploration with LogQL next to the metric panel that triggered an alert (split-pane view)

## Skip If (ANY kills it)

- As the metrics store itself — Grafana is a rendering layer; a missing datasource or a slow Prometheus is the real failure
- For long-term query performance audits — use pprof/Mimir directly, not the dashboard
- When you need transactional accuracy (counts must match invoicing) — time-series + downsampling produces approximations
- As a CMDB or service catalog — use Backstage / Cortex / Port; Grafana drops "soft" labels
- Single-pane-of-glass for security events (SIEM) — use Grafana for ops; route auth/audit logs to a SIEM

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
