# Sidekiq Background Jobs for Rails

## Summary

**One-sentence:** Produces a Sidekiq job spec: idempotent `perform`, IDs not records, explicit retry/dead settings, custom backoff for transient errors, RecordNotFound handling, thin job class delegating to a service.

**Ефективно для:**

- Rails apps offloading email / webhooks / file uploads to background.
- Workloads needing at-least-once durability backed by Redis.
- Per-queue concurrency tuning (default / critical / mailers).
- LLM agents generating job classes from service signatures.

**One-paragraph:** Durable async job processing for Rails with Sidekiq + Redis. Jobs MUST be idempotent (at-least-once delivery), accept IDs not ActiveRecord objects, declare `sidekiq_options retry: N, dead: true`, implement `sidekiq_retry_in` for transient errors, and handle `ActiveRecord::RecordNotFound` gracefully. Job classes stay thin and delegate to a service object so business logic is unit-testable.

## Applies If (ALL must hold)

- Rails app with Sidekiq + Redis already wired (or scoped to be added).
- Async work requires durability beyond in-process `Thread.new`.
- Jobs need typed retries and dead-letter handling.
- Production has a monitored Sidekiq Web UI or equivalent dashboard.

## Skip If (ANY kills it)

- Sub-second fire-and-forget (use `ActiveJob` inline or a goroutine in Go).
- Cron-only scheduled work — use `sidekiq-cron` separately, not bare jobs.
- Single-process apps with no Redis — use `delayed_job` or `good_job`.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Sidekiq Gemfile + config | Gemfile + config/sidekiq.yml | team |
| Redis URL + concurrency budget | ENV | SRE |
| Queue taxonomy (default / critical / mailers) | decision doc | tech lead |
| Service object the job delegates to | Ruby class | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[ruby-rails]]` | host framework conventions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-job-class` | haiku | Mechanical template fill from service signature. |
| `review-idempotency` | sonnet | Judgement: which side effects need uniqueness guards. |
| `tune-retry-budget` | sonnet | Maps error taxonomy to retry / dead settings. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ruby-sidekiq-jobs.json` | JSON Schema for the Sidekiq Background Jobs for Rails output contract |
| `templates/ruby-sidekiq-jobs.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a ruby-sidekiq-jobs record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-sidekiq-jobs.py` | Enforce the Sidekiq Background Jobs for Rails output contract | After subagent returns, before downstream consumer reads |

## Related

- [[ruby-rails-patterns]]
- [[ruby-activerecord]]
- [[ruby-rspec-testing]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
