---
slug: ruby-sidekiq-jobs
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Sidekiq job patterns for Rails apps: explicit sidekiq_options, idempotency-first perform, primitive-ID arguments, custom retry backoff, and RSpec testing.
content_id: "33266403dd680be0"
complexity: medium
produces: code
est_tokens: 4100
tags: [sidekiq, background-jobs, rails, async, queuing]
---
# Sidekiq Background Jobs

## Summary

**One-sentence:** Sidekiq job patterns for Rails apps: explicit sidekiq_options, idempotency-first perform, primitive-ID arguments, custom retry backoff, and RSpec testing.

**One-paragraph:** Sidekiq job patterns for Rails apps: explicit sidekiq_options, idempotency-first perform, primitive-ID arguments, custom retry backoff, and RSpec testing. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-ruby-sidekiq-jobs.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Rails 6+ app з Redis на стеку, де потрібен async-throughput >100 jobs/min.
- Mailers / webhooks / third-party API calls, які не можна тримати в request-response cycle.
- Idempotency-critical pipelines (payments, notifications): дублікати delivery лиш через at-least-once Redis.
- Custom retry backoff (linear / exponential per error class) — не дефолтний 25-retry expo.

## Applies If (ALL must hold)

- Rails app з Redis уже в стеку та async job throughput ≥100 jobs/min
- Idempotent perform body можна гарантувати (DB unique constraint, version flag, або memoized check)
- Job arguments serializable до primitive IDs (Integer / String / UUID), не AR-objects
- RSpec test infra налаштована з Sidekiq::Testing.fake! та drain support

## Skip If (ANY kills it)

- Strict FIFO per partition — Sidekiq best-effort ordering; обери Kafka/SQS-FIFO
- Jobs мають persistance beyond Redis durability — обери GoodJob (Postgres-backed) або Solid Queue
- Serverless без persistent compute — обери queue-as-a-service (SQS + ECS task)
- Low-volume one-shot mailers — Rails 8 Solid Queue / ActiveJob async adapter достатньо

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-ruby-sidekiq-jobs` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/job.rb` | Canonical Sidekiq job example (idempotent perform, retry backoff) |
| `templates/sidekiq.service` | systemd unit template for running Sidekiq in production |
| `templates/sidekiq.yml` | Sidekiq config skeleton (queues, concurrency) |
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.rb` | Language skeleton implementing the canonical rule set |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-sidekiq-jobs.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[ruby-rails-patterns]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
