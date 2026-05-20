---
slug: ruby-rails-patterns
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rails 7.
content_id: "57dfcf0e2bccf665"
tags: [rails, service-objects, transactions, patterns]
---
# Rails Patterns (Service Objects and ServiceResult)

## Summary

**One-sentence:** Rails 7.

**One-paragraph:** Rails 7.x applications extract multi-step business logic into Service Objects that accept params and current_user in initialize and return a single canonical ServiceResult from #call. Wrap multi-step writes in ActiveRecord::Base.transaction. Move mailers, webhooks, and HTTP calls to after_commit callbacks or a transactional outbox — never mid-transaction. One ServiceResult class for the entire codebase.

## Applies If (ALL must hold)

- Rails 7.x app where controllers or ActiveRecord callbacks have grown unwieldy.
- Multi-step writes that must be transactional plus side effects (mailers, audit logs, webhooks).
- Defining a uniform success/failure return shape so controllers do not rescue exceptions.
- Refactoring fat controllers and models toward service-centric architecture.

## Skip If (ANY kills it)

- Tiny single-step writes (User.create!(params)) — wrapping in a service is ceremony.
- Read-only endpoints — services add no value over a query object or scope.
- Background jobs that already encapsulate one action — nesting Service inside Sidekiq inside Service is over-engineering.
- Apps using Trailblazer, Interactor, or Dry::Transaction — stick to one paradigm.

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
