---
slug: cloud-run-jobs
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Run Jobs run containers to completion rather than serving HTTP requests.
content_id: "54ecd5dacaa451dd"
tags: [gcp, cloud-run, jobs, batch, scheduler]
---
# Cloud Run Jobs

## Summary

**One-sentence:** Cloud Run Jobs run containers to completion rather than serving HTTP requests.

**One-paragraph:** Cloud Run Jobs run containers to completion rather than serving HTTP requests. Jobs support up to 10,000 parallel tasks, 168-hour timeouts, and automatic retries. Use CLOUD_RUN_TASK_INDEX and CLOUD_RUN_TASK_COUNT environment variables to distribute work across parallel tasks. Tasks MUST be idempotent because retries re-execute the same task.

## Applies If (ALL must hold)

- Batch processing large datasets that can be partitioned across parallel tasks.
- ETL pipelines, data exports, report generation, and scheduled data transformations.
- One-off administrative tasks (database migrations, cleanup jobs, backfills).
- ML training data preparation or model evaluation pipelines.
- Recurring scheduled tasks (replace Cloud Functions cron triggers for complex jobs).

## Skip If (ANY kills it)

- HTTP-triggered request processing — use Cloud Run Services.
- Streaming or continuous processing — use Dataflow or Pub/Sub push subscriptions.
- Workflows with complex DAG dependencies — use Cloud Workflows or Composer.
- Jobs needing more than 8 vCPU or 32 GB memory per task — use GKE Batch or Dataproc.

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

- parent skill: `pro/infra/infrastructure-engineer/`
