# Django + Celery Background Jobs

## Summary

**One-sentence:** Configures Celery with Django: idempotent tasks keyed by business id, transaction.on_commit dispatch, retry policy with exponential backoff and jitter, and a dead-letter strategy.

**One-paragraph:** Configures Celery with Django: idempotent tasks keyed by business id, transaction.on_commit dispatch, retry policy with exponential backoff and jitter, and a dead-letter strategy. Every task carries an explicit dotted name, is keyed by a business id, is dispatched via transaction.on_commit, declares max_retries with bounded backoff+jitter and both time limits, lands on a named queue with a known worker pool, and routes to a dead-letter queue after max retries. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Django app needs to run side-effects outside the request cycle (email, webhook, export).
- External call latency or rate limits make in-request execution unacceptable.
- Already running or planning to run Celery with Redis or RabbitMQ broker.
- Designing predictable retry + failure semantics across many task types.
- Onboarding engineers to a Celery codebase with consistent conventions.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Django app needs to run side-effects outside the request cycle (email, webhook, export).
- External call latency or rate limits make in-request execution unacceptable.
- Already running or planning to run Celery 5+ with a Redis or RabbitMQ broker.

## Skip If (ANY kills it)

- Single-process Django with no broker — use sync calls or threadpool first.
- Task volume < 100/day where Celery overhead exceeds benefit.
- Workload requires sub-second job dispatch — use a lighter queue (rq) or in-process executor.
- The use case is a single cron job — django-extensions runscript or crontab is simpler.
- The project runs a different runner (RQ, Dramatiq, Huey) — the conventions here do not transfer.
- Long-running orchestrated pipelines belong in Airflow / Prefect / Temporal, not Celery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Broker URL | redis:// or amqp:// URL | settings.py / env |
| Result backend | string | Redis or DB |
| Existing tasks list | list of dotted paths | git grep @shared_task |
| Task inventory: name, trigger, payload shape, frequency | table | tech-lead |
| Queue topology decision: per-priority or per-domain queues | ADR | tech-lead |
| Alerting integration (PagerDuty, Slack) for DLQ events | endpoint | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[django-services]] | Tasks call services; tasks are not the place for business logic. |
| [[logging-patterns]] | Structured logging with task id + business id correlation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules (incl. run-the-checklist + skip-this-methodology) with rationale + source | 1500 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden patterns + allowed transformations | 1300 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with symptom + root-cause + fix | 1200 |
| `content/04-procedure.xml` | essential | 8-step end-to-end procedure with input/action/output per step | 1300 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip and run leaves always reachable | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-task` | sonnet | Mechanical: write task signature + service call + retry decorator. |
| `design-retry-policy` | opus | Per-task backoff/jitter/max-retries decision; cross-cutting. |
| `queue-topology-design` | opus | Cross-cutting decision about isolation + priority per queue. |
| `dead-letter-design` | opus | DLQ topology + alerting; non-obvious. |
| `dlq-alerting-wire-up` | sonnet | Plumbing exporters + alert routes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task.py` | Python scaffold realising the artefact in code. |
| `templates/celery_app.py` | Python scaffold realising the artefact in code. |
| `templates/conftest.py` | Python scaffold realising the artefact in code. |
| `templates/task-idempotent.py` | Celery task template with idempotency, retry, time limits |
| `templates/celery-worker.service` | systemd unit for a single-queue worker |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-celery.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-services]]
- [[decomposition-django]]
- [[logging-patterns]]
- [[message-queues]]
- [[feature-flags-rollout-targeting]]

Runtime notes for agents — when to reach for Celery, where it fails, CLI tools, services and AI-agent
gotchas — live in `agent-integration.md` beside this file.

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the workload high-volume async work on Celery 5+ compatible with at-least-once delivery?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly, and the run-the-checklist branch is the all-gates-green approval leaf. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
