---
slug: data-pipeline-design
tier: pro
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Poor pipeline design causes data quality failures that propagate silently into dashboards and ML models.
content_id: "ee50bb1e03fb5b85"
tags: [data, pipeline, etl, orchestration, dbt, airflow, streaming, data-quality]
---
# Data Pipeline Design

## Summary

**One-sentence:** Poor pipeline design causes data quality failures that propagate silently into dashboards and ML models.

**One-paragraph:** Poor pipeline design causes data quality failures that propagate silently into dashboards and ML models. The medallion architecture enforces explicit data quality tiers: raw bronze preserves source fidelity, silver enforces schema and deduplication, gold delivers business-ready assets. Idempotent tasks and DLQs ensure reruns after failures produce identical results without duplicates.

## Applies If (ALL must hold)

- Designing a new analytical or operational data pipeline from scratch
- Choosing between batch vs streaming processing for a latency requirement
- Migrating from custom ETL scripts to a managed orchestrator (Airflow, Dagster)
- Adding data quality validation gates to an existing pipeline
- Reviewing pipeline reliability: retries, dead letter queues, schema evolution

## Skip If (ANY kills it)

- Direct OLTP query optimisation — this is about data movement, not query tuning
- Real-time API response paths — use caching/CDN patterns instead
- Small one-off data exports — a SQL script or dbt run is sufficient

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

- parent skill: `pro/dev/software-architect/`
