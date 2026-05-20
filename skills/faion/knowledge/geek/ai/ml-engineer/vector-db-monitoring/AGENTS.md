---
slug: vector-db-monitoring
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Instrument a production vector database with Prometheus metrics, configure Grafana dashboards, define warning and critical alert thresholds for latency, error rate, memory, and disk, and establish capacity planning baselines to prevent surprise outages before they reach users.
content_id: "44f1919c3c15e88d"
tags: [vector-database, monitoring, prometheus, alerting, observability]
---
# Vector Database Monitoring and Alerting

## Summary

**One-sentence:** Instrument a production vector database with Prometheus metrics, configure Grafana dashboards, define warning and critical alert thresholds for latency, error rate, memory, and disk, and establish capacity planning baselines to prevent surprise outages before they reach users.

**One-paragraph:** Instrument a production vector database with Prometheus metrics, configure Grafana dashboards, define warning and critical alert thresholds for latency, error rate, memory, and disk, and establish capacity planning baselines to prevent surprise outages before they reach users.

## Applies If (ALL must hold)

- Any vector database serving production traffic.
- Adding a new vector database to an existing observability stack.
- After scaling a collection past 1M vectors where resource consumption patterns change.
- Before enabling quantization or changing index parameters — establish a baseline first.

## Skip If (ANY kills it)

- Fully managed services (Pinecone Serverless, Weaviate Cloud) — use the provider's built-in dashboards and alert webhooks instead.
- Development environments — log-based debugging is sufficient; Prometheus overhead is not justified.

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

- parent skill: `geek/ai/ml-engineer/`
