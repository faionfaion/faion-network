---
slug: ruby-sidekiq-jobs
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Durable async job processing for Rails using Sidekiq + Redis.
content_id: "33266403dd680be0"
tags: [ruby, sidekiq, background-jobs, async, redis]
---
# Sidekiq Background Jobs

## Summary

**One-sentence:** Durable async job processing for Rails using Sidekiq + Redis.

**One-paragraph:** Durable async job processing for Rails using Sidekiq + Redis. Every job must be idempotent (at-least-once delivery), accept IDs not ActiveRecord objects, declare explicit sidekiq_options retry: N, dead: true, implement custom sidekiq_retry_in for known transient errors, and handle ActiveRecord::RecordNotFound gracefully. Keep job classes thin — perform delegates to a service object for unit testability.

## Applies If (ALL must hold)

- Rails app needing durable async work: emails, webhooks, file processing, third-party API fan-out.
- Bulk processing with find_each chunking and per-chunk jobs.
- Reliable retry/backoff for flaky external integrations (payment gateways, email providers).
- Cron-like scheduling via sidekiq-cron or sidekiq-scheduler.

## Skip If (ANY kills it)

- Sub-second latency between action and effect — Sidekiq pickup latency is 50-500ms even idle.
- Cross-language consumers — Sidekiq conventions are Ruby-specific even though payload is JSON.
- Strict global ordering — Sidekiq is parallel; use a single-thread queue or Kafka with partition keys.
- Exactly-once semantics — Sidekiq is at-least-once; design for idempotency or use sidekiq-unique-jobs carefully.

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

- parent skill: `pro/dev/backend-enterprise/`
