# Sidekiq Background Jobs

## Summary

Sidekiq job patterns for Rails apps: job class with `include Sidekiq::Job`, explicit `sidekiq_options` (queue, retry, dead), idempotency check at the top of `perform`, primitive IDs in arguments (never ActiveRecord objects), custom retry backoff via `sidekiq_retry_in`, and RSpec tests using `Sidekiq::Testing.inline!`. Jobs must survive re-execution; errors must be captured and re-raised so retries fire correctly.

## Why

Sidekiq's threaded model (N jobs concurrently per process) delivers ~10x the throughput of forking workers on the same box. Redis-backed queuing decouples user requests from slow work (mailers, webhooks, image pipelines). Idempotency, explicit retry policies, and the Dead set provide durability without requiring a separate durable queue system. Passing IDs instead of AR objects avoids stale data and GlobalID re-fetch failures when rows are deleted between enqueue and run.

## When To Use

- Rails apps needing background processing: mailers, webhooks, third-party API calls, image/video pipelines.
- High-throughput job execution where Redis is already part of the stack.
- Scheduled / cron-style jobs via `sidekiq-cron` or `sidekiq-scheduler`.
- Workflows with batches, callbacks, and unique-job semantics (Sidekiq Pro or `sidekiq-unique-jobs`).

## When NOT To Use

- Single-threaded code that mutates global state — Sidekiq runs N jobs concurrently and will trigger races.
- Low-volume one-shot tasks where Rails 8's Solid Queue / ActiveJob async adapter is enough.
- Serverless environments without persistent compute — choose a queue-as-a-service (SQS + ECS task) instead.
- When jobs must persist beyond Redis durability — use GoodJob (Postgres-backed) or Solid Queue instead.
- Strict FIFO requirements per partition — Sidekiq is best-effort ordering.

## Content

| File | What's inside |
|------|---------------|
| `content/01-job-rules.xml` | sidekiq_options, idempotency, primitive args, retry backoff, error capture, queue naming |
| `content/02-batch-processing.xml` | BatchExportJob pattern: find_each, status tracking, error recovery |
| `content/03-antipatterns.xml` | AR objects in args, dispatch inside transaction, retry:false, Thread.sleep in tests, secret args leakage |

## Templates

| File | Purpose |
|------|---------|
| `templates/job.rb` | ProcessOrderJob with sidekiq_options, idempotency check, retry backoff, error handling |
| `templates/sidekiq.yml` | Queue priorities and concurrency for dev and production |
| `templates/sidekiq.service` | Systemd unit for daemonized Sidekiq worker with graceful shutdown |
