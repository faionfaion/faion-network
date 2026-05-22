---
slug: django-celery
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for integrating Celery into Django applications: every async task must declare explicit name, idempotency guard, retry policy (max_retries, retry_backoff, retry_jitter), and time limits (soft_time_limit, time_limit).
content_id: "f08c7e65f5c4fc81"
tags: [django, celery, async, task-queue, redis]
---
# Django Celery Tasks

## Summary

**One-sentence:** A methodology for integrating Celery into Django applications: every async task must declare explicit name, idempotency guard, retry policy (max_retries, retry_backoff, retry_jitter), and time limits (soft_time_limit, time_limit).

**One-paragraph:** A methodology for integrating Celery into Django applications: every async task must declare explicit name, idempotency guard, retry policy (max_retries, retry_backoff, retry_jitter), and time limits (soft_time_limit, time_limit). Tasks receive primitive IDs only — never model instances. Queues map to workload classes; workers are deployed as systemd services per queue.

## Applies If (ALL must hold)

- Offloading work that exceeds ~500ms inside an HTTP request (emails, PDF gen, image processing).
- Scheduled jobs (Celery beat) replacing cron for deploy-portable scheduling.
- Fan-out workloads (nightly digests, batch notifications) with concurrency limits.
- Webhook receivers that must return 200 immediately and process async.
- Retry-with-backoff for flaky upstreams without poisoning the request thread.

## Skip If (ANY kills it)

- Sub-second jobs already inside the request — Celery overhead dominates.
- Strict-ordering pipelines with stateful dependencies — use Prefect/Temporal/Dagster.
- Streaming or exactly-once semantics — Celery is at-least-once; design idempotency or use Kafka.
- Tasks needing mid-flight cancellation across many workers — Celery revoke is best-effort.
- Apps already on django-q2, huey, dramatiq, or arq where switching costs don't pay back.

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

- parent skill: `solo/dev/software-developer/`
