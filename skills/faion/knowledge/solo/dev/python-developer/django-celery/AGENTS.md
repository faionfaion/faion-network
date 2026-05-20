---
slug: django-celery
tier: solo
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Celery 5.
content_id: "f08c7e65f5c4fc81"
tags: [celery, django, async, background-tasks, python]
---
# Django Celery Tasks

## Summary

**One-sentence:** Celery 5.

**One-paragraph:** Celery 5.4+ with Django 5.x enables asynchronous task execution outside the HTTP request/response cycle. Tasks accept primitive arguments (IDs, not model instances), are idempotent by design, declare explicit retry policies (autoretry_for, retry_backoff), and set both soft_time_limit and time_limit. Inside @transaction.atomic blocks, always call task.delay_on_commit() — never task.delay() — to prevent the task from running before the DB commit completes.

## Applies If (ALL must hold)

- Any Django operation taking >100ms that is not critical to the HTTP response.
- Scheduled batch work (nightly aggregations, reminder emails) via Celery Beat.
- Retry-with-backoff for flaky third-party APIs (Stripe, Twilio, SendGrid).
- Long-running background flows orchestrated as chain/chord/group.
- CPU-intensive work (image processing, ML inference) that needs dedicated worker resources.

## Skip If (ANY kills it)

- Sub-100/day jobs — python manage.py + system cron is simpler.
- Hard real-time (<100ms) — use ASGI + WebSocket.
- Simple async I/O inside a request — Django 4.1+ async views work.
- Tasks that must succeed inline with the user response (payment authorization).
- Tiny apps where running Redis + worker + beat is pure operational overhead.

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

- parent skill: `solo/dev/python-developer/`
