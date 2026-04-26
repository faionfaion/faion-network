# Laravel Queues

## Summary

Durable async job processing for Laravel using Redis (Horizon) or SQS. Every job must be idempotent (at-least-once delivery), pass IDs not model instances, declare explicit `$tries`/`$backoff`/`$timeout`, implement `failed()` for terminal-failure logging, and use `WithoutOverlapping($id)` to prevent duplicate concurrent runs on the same resource.

## Why

Moving slow IO (email, PDF, third-party API calls) off the request lifecycle keeps p99 response times predictable. Laravel's job retry + backoff handles transient failures without manual polling. `Bus::batch` provides fan-out with progress tracking and then/catch/finally lifecycle hooks. Passing model IDs instead of Eloquent instances avoids stale-model bugs and keeps payloads small.

## When To Use

- Slow IO must leave the request lifecycle (email, PDF, webhooks, image processing).
- Bulk import/export via `Bus::batch` with per-chunk jobs and progress polling.
- External services with flaky availability that need retry with exponential backoff.
- Webhook receiver pattern: receive → push to queue → return 200 immediately.

## When NOT To Use

- Sub-millisecond pub/sub between services — use Redis pub/sub or NATS.
- Strict global event ordering across many producers — use Kafka with partition keys.
- High-throughput streaming (>10k msg/s sustained) — use a real broker directly.
- Cross-language consumers — Laravel job payload is PHP-serialized; other languages cannot read it.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Idempotency requirement, ID-over-model rule, retry/backoff/timeout configuration, `failed()` contract. |
| `content/02-examples.xml` | `ProcessOrderJob` with `WithoutOverlapping`, `Bus::batch` for chunked export. |
| `content/03-antipatterns.xml` | Full model in payload, missing `failed()`, try/catch swallowing exceptions, Horizon balancing defaults. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ProcessOrderJob.php` | Job skeleton: `ShouldQueue`, retry/backoff/timeout, `WithoutOverlapping`, idempotency check, `failed()`. |
| `templates/laravel-worker.service` | systemd unit for production queue worker with `--max-time` and `--max-jobs` bounds. |
