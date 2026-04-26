# Data Pipeline Design

## Summary

Designing data ingestion, transformation, and storage pipelines for batch and streaming workloads. Covers ETL vs ELT decision, medallion architecture (Bronze/Silver/Gold), orchestration tool selection (Airflow/Dagster/Prefect), Kafka + Spark streaming patterns, dbt transformation conventions, data quality strategy, and error handling (DLQ, idempotency, retries).

## Why

Poor pipeline design causes data quality failures that propagate silently into dashboards and ML models. The medallion architecture enforces explicit data quality tiers: raw bronze preserves source fidelity, silver enforces schema and deduplication, gold delivers business-ready assets. Idempotent tasks and DLQs ensure reruns after failures produce identical results without duplicates.

## When To Use

- Designing a new analytical or operational data pipeline from scratch
- Choosing between batch vs streaming processing for a latency requirement
- Migrating from custom ETL scripts to a managed orchestrator (Airflow, Dagster)
- Adding data quality validation gates to an existing pipeline
- Reviewing pipeline reliability: retries, dead letter queues, schema evolution

## When NOT To Use

- Direct OLTP query optimisation — this is about data movement, not query tuning
- Real-time API response paths — use caching/CDN patterns instead
- Small one-off data exports — a SQL script or dbt run is sufficient

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-types-and-stack.xml` | Batch vs streaming vs Lambda/Kappa trade-offs, ETL vs ELT decision, medallion architecture layers, modern data stack component map |
| `content/02-orchestration-and-ingestion.xml` | Airflow vs Dagster vs Prefect selection guide, DAG design rules, incremental vs full vs CDC ingestion patterns, schema registry |
| `content/03-transformation-and-quality.xml` | dbt model naming conventions, materialisation choice, Great Expectations vs Soda vs dbt tests, data contracts, error handling patterns (DLQ, idempotency, retry strategies) |

## Templates

| File | Purpose |
|------|---------|
| `templates/dbt-model-staging.sql` | Canonical staging model with source reference, type casting, and deduplication |
| `templates/airflow-dag.py` | DAG skeleton with exponential backoff retry, SLA miss callback, and idempotent task pattern |
