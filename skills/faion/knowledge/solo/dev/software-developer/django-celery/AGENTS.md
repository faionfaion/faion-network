---
slug: django-celery
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Integrate Celery into Django with explicit task names, idempotency, retry policy, time limits, and DLQ for every async task.
content_id: "f08c7e65f5c4fc81"
complexity: medium
produces: code
est_tokens: 4200
tags: [django, celery, async, task-queue, redis]
---
# Django Celery Tasks

## Summary

**One-sentence:** Integrate Celery into Django with explicit task names, idempotency, retry policy, time limits, and DLQ for every async task.

**One-paragraph:** Every Celery task declares an explicit name, an idempotency guard, retry policy (max_retries, retry_backoff, retry_jitter), and time limits (soft_time_limit, time_limit). Tasks land on a named queue with a known worker pool. Failures route to a dead-letter queue with alert + retry policy. Output is task module code + queue config + monitoring spec.

**Ефективно для:**

- Building reliable async pipelines (emails, webhooks, ETL, report generation).
- Replacing synchronous request handlers with background processing.
- Designing predictable retry + failure semantics across many task types.
- Onboarding engineers to a Celery codebase with consistent conventions.

## Applies If (ALL must hold)

- Django project with Celery 5+ as the async runner.
- Broker is Redis or RabbitMQ; result backend chosen.
- Tasks have user-visible failure modes (retry, alert, DLQ).
- Operations team needs visibility into task health (Flower, Prometheus exporters).

## Skip If (ANY kills it)

- Sync request handling is fast enough — Celery adds complexity without payoff.
- Use case is a single cron job (django-extensions runscript or crontab is simpler).
- Project uses a different runner (RQ, Dramatiq, Huey) — methodology specifics differ.
- Long-running pipelines belong in Airflow / Prefect, not Celery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task inventory: name, trigger, payload shape, frequency | table | tech-lead |
| Broker + result backend chosen + version pinned | config | platform |
| Queue topology decision: per-priority or per-domain queues | ADR | tech-lead |
| Alerting integration (PagerDuty, Slack) for DLQ events | endpoint | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[django-services]] | Tasks call into service-layer functions. |
| [[logging-patterns]] | Structured logs around task lifecycle. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (explicit name, idempotency, retry policy, time limits, named queues, DLQ) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for Celery task module spec + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory → name + idempotency → policies → queues → monitoring | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `task_authoring` | sonnet | Mechanical task module emission with policies. |
| `queue_topology_design` | opus | Cross-cutting decision about isolation + priority. |
| `dlq_alerting_wire_up` | sonnet | Plumbing exporters + alert routes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-idempotent.py` | Celery task template with idempotency, retry, time limits |
| `templates/celery-worker.service` | systemd unit for worker |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-celery.py` | Validate the task module spec metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[django-services]]
- [[message-queues]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps async need, runner choice, and reliability requirements to a rule from `01-core-rules.xml`, telling the agent whether to apply the Celery conventions or skip in favour of a different runner or sync handling. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
