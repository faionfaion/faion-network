---
slug: ruby-sidekiq-jobs
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Sidekiq job patterns for Rails apps: job class with `include Sidekiq::Job`, explicit `sidekiq_options` (queue, retry, dead), idempotency check at the top of `perform`, primitive IDs in arguments (never ActiveRecord objects), custom retry backoff via `sidekiq_retry_in`, and RSpec tests using `Sidekiq::Testing.
content_id: "33266403dd680be0"
tags: [sidekiq, background-jobs, rails, async, queuing]
---
# Sidekiq Background Jobs

## Summary

**One-sentence:** Sidekiq job patterns for Rails apps: job class with `include Sidekiq::Job`, explicit `sidekiq_options` (queue, retry, dead), idempotency check at the top of `perform`, primitive IDs in arguments (never ActiveRecord objects), custom retry backoff via `sidekiq_retry_in`, and RSpec tests using `Sidekiq::Testing.

**One-paragraph:** Sidekiq job patterns for Rails apps: job class with `include Sidekiq::Job`, explicit `sidekiq_options` (queue, retry, dead), idempotency check at the top of `perform`, primitive IDs in arguments (never ActiveRecord objects), custom retry backoff via `sidekiq_retry_in`, and RSpec tests using `Sidekiq::Testing.inline!`. Jobs must survive re-execution; errors must be captured and re-raised so retries fire correctly. Sidekiq's threaded model delivers ~10x the throughput of forking workers on the same box. Redis-backed queuing decouples user requests from slow work (mailers, webhooks, image pipelines). Idempotency, explicit retry policies, and the Dead set provide durability without requiring a separate durable queue system.

## Applies If (ALL must hold)

- Rails apps needing background processing: mailers, webhooks, third-party API calls, image/video pipelines
- High-throughput job execution where Redis is already part of the stack
- Scheduled / cron-style jobs via `sidekiq-cron` or `sidekiq-scheduler`
- Workflows with batches, callbacks, and unique-job semantics (Sidekiq Pro or `sidekiq-unique-jobs`)

## Skip If (ANY kills it)

- Single-threaded code that mutates global state — Sidekiq runs N jobs concurrently and will trigger races
- Low-volume one-shot tasks where Rails 8's Solid Queue / ActiveJob async adapter is enough
- Serverless environments without persistent compute — choose a queue-as-a-service (SQS + ECS task) instead
- When jobs must persist beyond Redis durability — use GoodJob (Postgres-backed) or Solid Queue instead
- Strict FIFO requirements per partition — Sidekiq is best-effort ordering

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

- parent skill: `pro/dev/software-developer/`
