# Sidekiq Background Jobs

## Summary

Durable async job processing for Rails using Sidekiq + Redis. Every job must be idempotent (at-least-once delivery), accept IDs not ActiveRecord objects, declare explicit `sidekiq_options retry: N, dead: true`, implement custom `sidekiq_retry_in` per-exception class, and handle `ActiveRecord::RecordNotFound` gracefully. Keep job classes thin — `perform` delegates to a service object for unit testability.

## Why

Sidekiq is at-least-once; retries are the default, not the exception. Passing IDs avoids stale-model bugs and works with Sidekiq 7 strict args mode which rejects non-JSON-serializable objects. Custom `sidekiq_retry_in` gives linear backoff for rate-limit errors (payment gateways) and exponential for transient failures — the default 25-retry curve rarely matches real SLA needs. Thin job classes let the service object be unit-tested without Sidekiq's testing module.

## When To Use

- Rails app needing durable async work: emails, webhooks, file processing, third-party API fan-out.
- Bulk processing with `find_each` chunking and per-chunk jobs.
- Reliable retry/backoff for flaky external integrations (payment gateways, email providers).
- Cron-like scheduling via `sidekiq-cron` or `sidekiq-scheduler`.

## When NOT To Use

- Sub-second latency between action and effect — Sidekiq pickup latency is 50-500ms even idle.
- Cross-language consumers — Sidekiq conventions are Ruby-specific even though payload is JSON.
- Strict global ordering — Sidekiq is parallel; use a single-thread queue or Kafka with partition keys.
- Exactly-once semantics — Sidekiq is at-least-once; design for idempotency or use `sidekiq-unique-jobs` carefully.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Idempotency, ID-over-record, explicit retry/dead, `sidekiq_retry_in`, thin job rule. |
| `content/02-examples.xml` | `ProcessOrderJob` with per-exception retry curve, `BatchExportJob` with `find_each`. |
| `content/03-antipatterns.xml` | ActiveRecord args, swallowed exceptions, ActiveJob API confusion, missing `retry:`/`dead:`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/process_order_job.rb` | Job skeleton: `include Sidekiq::Job`, `sidekiq_options`, custom `sidekiq_retry_in`, idempotency check. |
| `templates/sidekiq.yml` | Production Sidekiq config: concurrency, weighted queues, retry cap, dead-set limits. |
| `templates/sidekiq.service` | systemd unit with `WatchdogSec`, `TSTP` reload, `KillMode=mixed`. |
