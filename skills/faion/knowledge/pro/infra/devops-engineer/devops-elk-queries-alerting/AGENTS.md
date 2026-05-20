---
slug: devops-elk-queries-alerting
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kibana Query Language (KQL) enables fast structured filtering in Kibana dashboards.
content_id: "872afdaebb8feb3c"
tags: [kibana, elasticsearch, alerting, logging, observability]
---
# Kibana Queries, Dashboards, and Alerting

## Summary

**One-sentence:** Kibana Query Language (KQL) enables fast structured filtering in Kibana dashboards.

**One-paragraph:** Kibana Query Language (KQL) enables fast structured filtering in Kibana dashboards. Elasticsearch DSL supports complex aggregations (terms, percentiles, date-histograms) for analytics queries via the REST API or Dev Tools. Kibana alerting rules and Elasticsearch Watcher send notifications when error rates exceed thresholds or when expected logs are absent.

## Applies If (ALL must hold)

- Building operational dashboards showing error rates, response time percentiles, and request volumes by service.
- Debugging production incidents by filtering logs to a specific service, time window, and error type.
- Setting up automated alerts for error rate spikes, missing heartbeat logs, or slow request rates.
- Ad-hoc aggregation analysis to identify top error types or slowest API endpoints.

## Skip If (ANY kills it)

- Real-time metrics with sub-second resolution — Prometheus+Grafana is more efficient for time-series metrics; Elasticsearch is optimized for search, not for high-cardinality metrics.
- Long-running reports against frozen/cold indices where query latency is minutes — pre-aggregate into a rollup index instead.

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
