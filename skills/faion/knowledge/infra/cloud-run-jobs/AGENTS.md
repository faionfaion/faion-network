# Cloud Run Jobs

## Summary

**One-sentence:** Cloud Run Jobs for batch processing: parallel task execution, CLOUD_RUN_TASK_INDEX work distribution, idempotency, checkpointing, Cloud Scheduler integration, and Terraform configuration.

**One-paragraph:** Cloud Run Jobs run containers to completion rather than serving HTTP requests. Jobs support up to 10,000 parallel tasks, 168-hour timeouts, and automatic retries. Use CLOUD_RUN_TASK_INDEX and CLOUD_RUN_TASK_COUNT environment variables to distribute work across parallel tasks. Tasks MUST be idempotent because retries re-execute the same task.

**Ефективно для:**

- Batch ETL над великим датасетом, що партиціонується по індексу таски.
- Нічні звіти / дамп-експорти, де треба до 168 годин на виконання.
- ML data-prep або evaluation-пайплайни з паралелізмом до 10000 тасок.
- Адміністративні one-off міграції БД, бекфіли, cleanup.

## Applies If (ALL must hold)

- Batch processing large datasets that can be partitioned across parallel tasks.
- ETL pipelines, data exports, report generation, and scheduled data transformations.
- One-off administrative tasks (database migrations, cleanup jobs, backfills).
- ML training data preparation or model evaluation pipelines.
- Recurring scheduled tasks (replace Cloud Functions cron triggers for complex jobs).

## Skip If (ANY kills it)

- HTTP-triggered request processing — use Cloud Run Services (`gcp-cloud-run-serverless`).
- Streaming or continuous processing — use Dataflow or Pub/Sub push subscriptions.
- Workflows with complex DAG dependencies — use Cloud Workflows or Composer.
- Jobs needing more than 8 vCPU or 32 GB memory per task — use GKE Batch or Dataproc.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Container image | OCI image in Artifact Registry | container build step |
| Idempotency design | doc / code review | team |
| Cloud Scheduler cron (if scheduled) | cron expression + timezone | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cloud-run-deployment]] | Sibling methodology that supplies context required here. |
| [[gcp-cloud-run-serverless]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-config` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-cloud-run-jobs.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cloud-run-jobs.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloud-run-jobs.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[cloud-run-deployment]]
- [[gcp-cloud-run-serverless]]
- [[cloud-run-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. cloud-run-jobs vs an adjacent sibling).
