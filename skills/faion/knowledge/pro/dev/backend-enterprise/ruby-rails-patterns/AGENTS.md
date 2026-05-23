---
slug: ruby-rails-patterns
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Rails 7+ Service Object + ServiceResult patterns — single canonical ServiceResult class, services accept params:+current_user:, side effects via after_commit, Pundit verify_authorized, Bullet+Brakeman+bundler-audit gates in CI.
content_id: "e9e3bf1a49df9765"
complexity: deep
produces: code
est_tokens: 4500
tags: [rails, service-objects, transactions, patterns]
---
# Rails Patterns (Service Objects and ServiceResult)

## Summary

**One-sentence:** Rails 7+ Service Object + ServiceResult patterns — single canonical ServiceResult class, services accept params:+current_user:, side effects via after_commit, Pundit verify_authorized, Bullet+Brakeman+bundler-audit gates in CI.

**One-paragraph:** Rails 7.x application patterns extracting multi-step business logic into Service Objects. Exactly one `ServiceResult` class (`app/services/service_result.rb`) is shared across the codebase; CI fails on duplicates. Services accept `params:` and `current_user:` in `initialize`, expose `call` returning the canonical `ServiceResult`. Writes wrap in `ActiveRecord::Base.transaction`; side effects (mail, webhooks, search-index update) fire from `after_commit` / outbox / chained Sidekiq jobs — never inside the transaction. `ApplicationController` calls `verify_authorized` + `verify_policy_scoped` (Pundit). Migrations with `remove_column` / `rename_column` require a backfill plan + human checkpoint. Bullet, Brakeman, bundler-audit gate every PR.

**Ефективно для:**

- Rails 7.x app where controllers or ActiveRecord callbacks have grown unwieldy.
- Multi-step writes that must be transactional plus side effects (mailers, audit logs, webhooks).
- Defining a uniform success/failure return shape so controllers do not rescue exceptions.
- Refactoring fat controllers and models toward service-centric architecture.
- Enforcing Pundit authorization on every endpoint.

## Applies If (ALL must hold)

- Rails 7.x app on Ruby 3.1+.
- Multi-step business logic or transactional writes with side effects.
- Service-centric architecture is acceptable to the team.

## Skip If (ANY kills it)

- Tiny single-step writes (`User.create!(params)`) — wrapping in a service is ceremony.
- Read-only endpoints — services add no value over a query object or scope.
- Background jobs that already encapsulate one action — nesting Service inside Sidekiq inside Service is over-engineering.
- Apps using Trailblazer / Interactor / `Dry::Transaction` — stick to one paradigm.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case catalogue | Markdown verb list | product |
| Pundit policy plan | Markdown | security |
| Migration policy | text | DBA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ruby-rails]] | Umbrella for the broader Rails patterns. |
| [[ruby-activerecord]] | ORM discipline. |
| [[decomposition-rails]] | Service / Query / Form decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: single-serviceresult, service-signature-params-current-user, side-effects-after-commit, strong-params-not-into-service, pundit-verify-authorized, ci-gates-bullet-brakeman-audit | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Rails-patterns manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: serviceresult-shape-drift, deliver-later-inside-transaction, pundit-no-verify, callback-business-logic, missing-bullet-brakeman | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: define ServiceResult → write services → after_commit side effects → Pundit verify_authorized → CI gates | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-service-with-result` | sonnet | Service signature + result shape design. |
| `audit-pundit-coverage` | haiku | Mechanical scan for missing `authorize` calls. |
| `harden-ci-gates` | sonnet | Multi-tool CI wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bullet-rspec.rb` | RSpec configuration enabling Bullet in test runs. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rails-patterns.py` | Validate the Rails-patterns manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[ruby-rails]]
- [[ruby-activerecord]]
- [[decomposition-rails]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (service shape, authorization layer, CI gate presence) to a rule from `01-core-rules.xml`. Use it before extracting a service or wiring authorization.
