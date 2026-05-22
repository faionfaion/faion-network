---
slug: cohort-implementation
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cohort implementation moves cohort analysis from ad-hoc analytics-tool reports to warehouse-native dbt models that refresh daily, survive schema changes, and feed BI dashboards.
content_id: "07b5ef646f43bf35"
tags: [cohort-analysis, retention, dbt, warehouse, analytics]
---
# Cohort Analysis Implementation

## Summary

**One-sentence:** Cohort implementation moves cohort analysis from ad-hoc analytics-tool reports to warehouse-native dbt models that refresh daily, survive schema changes, and feed BI dashboards.

**One-paragraph:** Cohort implementation moves cohort analysis from ad-hoc analytics-tool reports to warehouse-native dbt models that refresh daily, survive schema changes, and feed BI dashboards. The canonical model uses long-format output (cohort_week, user_id, day_offset) and an incremental materialization strategy. Three query types cover the core use cases: acquisition cohorts, behavioral cohorts, and feature-adoption cohorts.

## Applies If (ALL must hold)

- Completed framing in cohort-basics and ready to ship production tables, dashboards, and refresh jobs.
- Migrating from analytics-tool reports to warehouse-native models (BigQuery / Snowflake / Redshift).
- Building executive dashboards that refresh daily and survive schema changes.
- Embedding cohort tables in a product analytics surface (Metabase, Looker, Hex).

## Skip If (ANY kills it)

- Pre-instrumentation: events inconsistent or signup_date unreliable — fix data first.
- Scale below a few thousand users — analytics-tool built-in or a notebook is sufficient.
- One-off investigation that will not be re-run — stop at a SQL notebook, do not productionize.

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

- parent skill: `pro/marketing/growth-marketer/`
