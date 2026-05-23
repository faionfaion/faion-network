# Django + Celery Background Jobs

## Summary

**One-sentence:** Configures Celery with Django: idempotent tasks keyed by business id, transaction.on_commit dispatch, retry policy with exponential backoff and jitter, and a dead-letter strategy.

**One-paragraph:** Configures Celery with Django: idempotent tasks keyed by business id, transaction.on_commit dispatch, retry policy with exponential backoff and jitter, and a dead-letter strategy. Every task is keyed by a business id, dispatched via transaction.on_commit, retries with bounded backoff+jitter, and routes to a dead-letter queue after max retries. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Django app needs to run side-effects outside the request cycle (email, webhook, export).
- External call latency or rate limits make in-request execution unacceptable.
- Already running or planning to run Celery with Redis or RabbitMQ broker.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Django app needs to run side-effects outside the request cycle (email, webhook, export).
- External call latency or rate limits make in-request execution unacceptable.
- Already running or planning to run Celery with Redis or RabbitMQ broker.

## Skip If (ANY kills it)

- Single-process Django with no broker — use sync calls or threadpool first.
- Task volume < 100/day where Celery overhead exceeds benefit.
- Workload requires sub-second job dispatch — use a lighter queue (rq) or in-process executor.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Broker URL | redis:// or amqp:// URL | settings.py / env |
| Result backend | string | Redis or DB |
| Existing tasks list | list of dotted paths | git grep @shared_task |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[django-services]] | Tasks call services; tasks are not the place for business logic. |
| [[logging-patterns]] | Structured logging with task id + business id correlation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-task` | sonnet | Mechanical: write task signature + service call + retry decorator. |
| `design-retry-policy` | opus | Per-task backoff/jitter/max-retries decision; cross-cutting. |
| `dead-letter-design` | opus | DLQ topology + alerting; non-obvious. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task.py` | Python scaffold realising the artefact in code. |
| `templates/celery_app.py` | Python scaffold realising the artefact in code. |
| `templates/conftest.py` | Python scaffold realising the artefact in code. |
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-celery.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[django-services]]
- [[decomposition-django]]
- [[logging-patterns]]
- [[feature-flags-rollout-targeting]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the workload high-volume async work compatible with at-least-once delivery?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
