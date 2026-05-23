# Laravel Queues

## Summary

**One-sentence:** Laravel queue system for offloading background work: ShouldQueue job classes, named queues for priority, WithoutOverlapping for dedup, configured retry/backoff/timeout, and Bus::batch for parallel work.

**One-paragraph:** Laravel's queue system runs background jobs on Redis / SQS / RabbitMQ workers via the ShouldQueue interface. Jobs must be idempotent (check isProcessed early), pass primitive IDs not Eloquent models, declare timeout/retries/backoff with jitter, implement failed() for visibility, and use middleware like WithoutOverlapping to prevent duplicate runs. Use Bus::batch for fan-out work; pin queue names for priority routing; run separate worker pools per queue.

**Ефективно для:**

- Email-sending, notification fan-out, image processing, webhook delivery.
- Long-running tasks (>5s) які повинні бути поза HTTP request.
- Bus::batch для дата-обробки (10k items → batched + monitored).
- Pinning critical queues на окремі pools (priority-mail, default, low).

## Applies If (ALL must hold)

- Laravel 10/11/12 project with Redis/SQS/RabbitMQ broker configured.
- Background tasks identified that don't fit in HTTP response time.
- Operators ready to run + monitor queue workers (supervisord / Horizon).
- Idempotency story exists (or can be added) for each job.

## Skip If (ANY kills it)

- Synchronous CLI scripts run via cron — no queue needed.
- Sub-second background work — queue overhead > benefit; use @Async-style in process.
- Strict in-order processing required — queues don't guarantee FIFO across workers.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Broker | Redis / SQS / RabbitMQ connection | ops |
| Job inventory | list of (job, idempotency key, retry policy) | developer |
| Horizon / supervisord config | worker config file | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Laravel framework basics (providers, config) assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: primitive-ids-only, idempotent-handle, timeout-retries-backoff, failed-method, named-queue-per-priority | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-idempotency-key` | opus | Idempotency design needs domain understanding. |
| `scaffold-job` | sonnet | Templated artisan generation. |
| `lint-model-in-job-ctor` | haiku | Mechanical regex. |

## Templates

| File | Purpose |
|------|---------|
| `templates/job.php` | Queue job skeleton with tries+timeout+backoff+failed+idempotent handle |
| `templates/batch-job.php` | Bus::batch fan-out for parallel processing of N records |
| `templates/supervisor.ini` | Supervisor config for Horizon-managed queue workers per named queue |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-laravel-queues.py` | Validate the job artefact against the schema | Pre-commit + CI |

## Related

- [[php-laravel]]
- [[php-laravel-patterns]]
- [[php-eloquent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
