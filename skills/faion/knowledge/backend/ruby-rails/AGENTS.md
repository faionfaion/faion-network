# Ruby on Rails Backend Development

## Summary

**One-sentence:** Production-grade Rails 7+ — Service Objects with shared ServiceResult, transactional writes with side effects via after_commit, Sidekiq jobs taking IDs only, RSpec + FactoryBot per-branch tests.

**One-paragraph:** Production-grade Rails 7+ applications. Multi-step business logic extracts into Service Objects (`Users::CreateService` style) sharing a single `ServiceResult` shape (`success?` / `failure?` / `value`). Writes wrap in `ActiveRecord::Base.transaction`; side effects (mail, webhook, search-index update) fire from `after_commit` callbacks or chained Sidekiq jobs — never inside the transaction. Sidekiq jobs accept primitives (IDs, strings) and load fresh records inside `perform`. RSpec + FactoryBot drive per-branch tests; controllers do `params.require(...).permit(...)` before passing to services.

**Ефективно для:**

- Rails 7+ apps where controllers or ActiveRecord callbacks have grown unwieldy.
- Multi-step writes that must be transactional plus side effects (mailers, audit logs, webhooks).
- Applications needing a uniform success/failure return shape so controllers do not sniff exceptions.
- Refactoring fat controllers and fat models toward service-centric architecture.
- Asynchronous processing of slow workflows with Sidekiq jobs and retry policies.

## Applies If (ALL must hold)

- Rails 7+ on Ruby 3.1+.
- Multi-step business logic or transactional writes with side effects.
- Service-centric architecture is acceptable to the team.

## Skip If (ANY kills it)

- Tiny single-step writes where wrapping in a service is excessive ceremony.
- Read-only endpoints where services add no value over a query object or scope.
- Apps using Hanami, Sinatra, or pure Rack where Rails conventions do not transfer.
- High-throughput message processing (>10k msg/s) where Sidekiq hits ceiling — use Karafka or a Go/Rust worker.
- Rails 5/6 LTS where some patterns (`after_create_commit`, encrypted attributes) require Rails 7+.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case catalogue | Markdown verb list | product |
| Sidekiq cluster + Redis | infra config | platform |
| Migration policy | text | DBA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ruby-activerecord]] | ORM discipline that Service Objects rely on. |
| [[ruby-rails-patterns]] | ServiceResult shape + transaction patterns. |
| [[decomposition-rails]] | Service / Query / Form decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: one-serviceresult-class, service-call-returns-result, after-commit-for-side-effects, strong-params-not-into-service, sidekiq-jobs-take-ids, destructive-migration-checkpoint | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Rails-app manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: deliver-later-inside-transaction, service-result-shape-drift, ar-object-in-sidekiq-args, params-leak-to-service, destructive-migration-no-review | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: lock ServiceResult → service per verb → transaction + after_commit → Sidekiq IDs + retry → RSpec per-branch | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-service` | sonnet | Verb extraction + ServiceResult shape design. |
| `wire-sidekiq-job` | sonnet | Retry policy + idempotency reasoning. |
| `audit-callback-logic` | haiku | Mechanical scan for business logic in callbacks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum viable Rails service / job / spec layout reference. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rails.py` | Validate the Rails-app manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[ruby-activerecord]]
- [[ruby-rails-patterns]]
- [[decomposition-rails]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (write shape, side-effect presence, async need) to a rule from `01-core-rules.xml`. Use it before extracting a service or wiring a job.
