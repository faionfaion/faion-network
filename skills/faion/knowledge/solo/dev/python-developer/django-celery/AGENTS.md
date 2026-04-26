# Django Celery Tasks

## Summary

Celery 5.4+ with Django 5.x enables asynchronous task execution outside the HTTP
request/response cycle. Tasks accept primitive arguments (IDs, not model instances), are
idempotent by design, declare explicit retry policies (`autoretry_for`, `retry_backoff`), and set
both `soft_time_limit` and `time_limit`. Inside `@transaction.atomic` blocks, always call
`task.delay_on_commit()` — never `task.delay()` — to prevent the task from running before the DB
commit completes.

## Why

Blocking operations (email, PDF, image processing, external API calls) inside a request degrade
response latency, cannot be retried on failure, and exhaust WSGI workers. Celery decouples task
execution from the request cycle, provides durable retry with backoff, and supports
`chain`/`group`/`chord` primitives for multi-step workflows. The `delay_on_commit` fix alone
eliminates an entire class of race conditions common in transactional views.

## When To Use

- Any Django operation taking >100ms that is not critical to the HTTP response.
- Scheduled batch work (nightly aggregations, reminder emails) via Celery Beat.
- Retry-with-backoff for flaky third-party APIs (Stripe, Twilio, SendGrid).
- Long-running background flows orchestrated as `chain`/`chord`/`group`.
- CPU-intensive work (image processing, ML inference) that needs dedicated worker resources.

## When NOT To Use

- Sub-100/day jobs — `python manage.py` + system cron is simpler.
- Hard real-time (<100ms) — use ASGI + WebSocket.
- Simple async I/O inside a request — Django 4.1+ async views work.
- Tasks that must succeed inline with the user response (payment authorization).
- Tiny apps where running Redis + worker + beat is pure operational overhead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Core rules: pass IDs not instances, idempotency, delay_on_commit, time limits, queue separation. |
| `content/02-patterns.xml` | Task templates: basic retry, idempotent, progress tracking, chain/chord workflow. |
| `content/03-examples.xml` | Real-world patterns: email, report generation, parallel groups, fan-out notifications. |

## Templates

| File | Purpose |
|------|---------|
| `templates/celery-app.py` | Celery app bootstrap (`config/celery.py` + `__init__.py`). |
| `templates/task.py` | Canonical task skeleton: bind=True, autoretry, backoff, soft_time_limit, idempotency guard. |
| `templates/settings.py` | Full Django `CELERY_*` settings block for reliability in production. |
| `templates/docker-compose.yml` | Worker + beat + flower + Redis services for local/prod. |
| `templates/conftest.py` | pytest fixtures: `celery_config`, `celery_eager`, `celery_worker_parameters`. |
| `templates/prompt-task.txt` | LLM prompt template for generating a complete idempotent task with tests. |
