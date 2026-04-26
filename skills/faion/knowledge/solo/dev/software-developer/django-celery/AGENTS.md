# Django Celery Tasks

## Summary

A methodology for integrating Celery into Django applications: every async task must declare explicit `name`, idempotency guard, retry policy (`max_retries`, `retry_backoff`, `retry_jitter`), and time limits (`soft_time_limit`, `time_limit`). Tasks receive primitive IDs only — never model instances. Queues map to workload classes; workers are deployed as systemd services per queue.

## Why

HTTP requests must respond in milliseconds; Celery moves slow work (emails, reports, API calls) into background workers over a message broker. Idempotency prevents duplicate side effects on retry. Time limits protect worker slots from long-running jobs. Passing IDs instead of objects prevents stale-data bugs from ORM serialization. Without explicit queue routing, fast and slow tasks share workers and starve each other.

## When To Use

- Offloading work that exceeds ~500ms inside an HTTP request (emails, PDF gen, image processing)
- Scheduled jobs (Celery beat) replacing cron for deploy-portable scheduling
- Fan-out workloads (nightly digests, batch notifications) with concurrency limits
- Webhook receivers that must return 200 immediately and process async
- Retry-with-backoff for flaky upstreams without poisoning the request thread

## When NOT To Use

- Sub-second jobs already inside the request — Celery overhead dominates
- Strict-ordering pipelines with stateful dependencies — use Prefect/Temporal/Dagster
- Streaming or exactly-once semantics — Celery is at-least-once; design idempotency or use Kafka
- Tasks needing mid-flight cancellation across many workers — Celery revoke is best-effort
- Apps already on django-q2, huey, dramatiq, or arq where switching costs don't pay back

## Content

| File | What's inside |
|------|---------------|
| `content/01-task-rules.xml` | Mandatory task attributes, idempotency pattern, time limits, calling conventions |
| `content/02-antipatterns.xml` | Common failures: stale objects, missing bind=True, no time limits, beat duplication |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-idempotent.py` | Canonical idempotent task with full retry + time-limit config |
| `templates/celery-worker.service` | Systemd unit for a single-queue Celery worker |
