# Cohort Analysis Implementation

## Summary

Cohort implementation moves cohort analysis from ad-hoc analytics-tool reports to warehouse-native dbt models that refresh daily, survive schema changes, and feed BI dashboards. The canonical model uses long-format output (`cohort_week, user_id, day_offset`) and an incremental materialization strategy. Three query types cover the core use cases: acquisition cohorts, behavioral cohorts, and feature-adoption cohorts.

## Why

Analytics-tool built-ins (Mixpanel, Amplitude) are fast to set up but break when schema changes, cannot join to billing data, and are opaque to data-quality tests. Warehouse-native cohort models give the team a single source of truth, support dbt tests (not-null, retention-pct bounds), and integrate with any BI tool. The incremental + partitioned approach scales to hundreds of millions of rows without full rebuilds.

## When To Use

- Completed framing in `cohort-basics` and ready to ship production tables, dashboards, and refresh jobs.
- Migrating from analytics-tool reports to warehouse-native models (BigQuery / Snowflake / Redshift).
- Building executive dashboards that refresh daily and survive schema changes.
- Embedding cohort tables in a product analytics surface (Metabase, Looker, Hex).

## When NOT To Use

- Pre-instrumentation: events inconsistent or `signup_date` unreliable — fix data first.
- Scale below a few thousand users — analytics-tool built-in or a notebook is sufficient.
- One-off investigation that will not be re-run — stop at a SQL notebook, do not productionize.

## Content

| File | What's inside |
|------|---------------|
| `content/01-queries.xml` | Three SQL query patterns (acquisition, behavioral, feature-adoption cohorts), Python/pandas variant, BigQuery schema |
| `content/02-checklist.xml` | Infrastructure setup, tracking, dashboard, data-quality, automation, and team adoption steps |

## Templates

| File | Purpose |
|------|---------|
| `templates/cohort-retention-weekly.sql` | dbt incremental model for weekly cohort retention (BigQuery/Snowflake compatible) |
| `templates/schema.yml` | dbt schema tests for cohort model (not_null, accepted_values, retention-pct bounds) |
