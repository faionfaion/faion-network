# Ruby on Rails Backend Development

## Summary

**One-sentence:** Production-grade Rails 7+ — Rails conventions (RESTful routing, Strong Parameters, credentials, concerns, invariant-only callbacks) plus Service Objects with a shared ServiceResult, transactional writes with side effects via after_commit, Sidekiq jobs taking IDs only, and RSpec + FactoryBot per-branch tests.

**One-paragraph:** Production-grade Rails 7+ applications. Multi-step business logic extracts into Service Objects (`Users::CreateService` style) sharing a single `ServiceResult` shape (`success?` / `failure?` / `value`). Writes wrap in `ActiveRecord::Base.transaction`; side effects (mail, webhook, search-index update) fire from `after_commit` callbacks or chained Sidekiq jobs — never inside the transaction. Sidekiq jobs accept primitives (IDs, strings) and load fresh records inside `perform`. RSpec + FactoryBot drive per-branch tests; controllers do `params.require(...).permit(...)` before passing to services. The methodology also carries the framework fundamentals the architecture sits on — resourceful routing with `member` / `collection`, secrets in `credentials.yml.enc` rather than ENV, shared model logic in concerns, and callbacks reserved for invariants while every external side effect lives in a service or job.

**Ефективно для:**

- Rails 7+ apps where controllers or ActiveRecord callbacks have grown unwieldy.
- Multi-step writes that must be transactional plus side effects (mailers, audit logs, webhooks).
- Applications needing a uniform success/failure return shape so controllers do not sniff exceptions.
- Refactoring fat controllers and fat models toward service-centric architecture.
- Asynchronous processing of slow workflows with Sidekiq jobs and retry policies.

## Applies If (ALL must hold)

- Rails 7+ on Ruby 3.1+, serving HTML and/or JSON.
- The team commits to Rails conventions rather than a Sinatra-style ad-hoc layout.
- For the service-object half: multi-step business logic or transactional writes with side effects, and a service-centric architecture the team accepts.

## Skip If (ANY kills it)

- Tiny single-step writes where wrapping in a service is excessive ceremony — the convention rules still apply, the service rules do not.
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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ruby-activerecord]] | ORM discipline that Service Objects rely on. |
| [[ruby-rails-patterns]] | ServiceResult shape + transaction patterns. |
| [[decomposition-rails]] | Service / Query / Form decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules — architecture: one-serviceresult-class, service-call-returns-result, after-commit-for-side-effects, strong-params-not-into-service, sidekiq-jobs-take-ids, destructive-migration-checkpoint; framework fundamentals: restful-resources, credentials-not-env, concern-for-shared-multi-model, callback-only-for-invariants | 1900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Rails-app manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns: deliver-later-inside-transaction, service-result-shape-drift, ar-object-in-sidekiq-args, params-leak-to-service, destructive-migration-no-review, callback-side-effect, ad-hoc-routes-explosion, secrets-in-env-leak | 1400 |
| `content/04-procedure.xml` | essential | 7-step procedure: lock ServiceResult → service per verb → transaction + after_commit → Sidekiq IDs + retry → RSpec per-branch → RESTful routes + strong params → callbacks, concerns and credentials | 1100 |
| `content/05-examples.xml` | essential | Worked Orders-module hardening + resourceful routes and controller shapes | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-service` | sonnet | Verb extraction + ServiceResult shape design. |
| `wire-sidekiq-job` | sonnet | Retry policy + idempotency reasoning. |
| `audit-callback-logic` | haiku | Mechanical scan for business logic in callbacks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md.j2` | Minimum viable Rails service / job / spec layout reference. |
| `templates/_smoke-test.md` | Minimum viable Rails service / job / spec layout reference. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rails.py` | Validate the Rails-app manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ruby-activerecord]]
- [[ruby-rails-patterns]]
- [[decomposition-rails]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (write shape, side-effect presence, async need) to a rule from `01-core-rules.xml`. Use it before extracting a service or wiring a job.
