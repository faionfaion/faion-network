---
slug: ruby-rails
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rails backend patterns for production-grade applications.
content_id: "218f2d3386bb58f2"
tags: [ruby, rails, rspec, sidekiq, backend]
---
# Ruby on Rails Backend Development

## Summary

**One-sentence:** Rails backend patterns for production-grade applications.

**One-paragraph:** Rails backend patterns for production-grade applications. Service Objects encapsulate business logic (user creation, order processing) with ActiveRecord::Base.transaction for data consistency and ServiceResult for success/failure semantics. RSpec model specs validate constraints, association specs check belongs_to/has_many, scope specs isolate filtering. Service specs exercise the happy path and error cases. Sidekiq background jobs with retry policies (exponential backoff) for async work (email, exports, notifications). Controllers stay thin, delegating to services. Pagination via kaminari.

## Applies If (ALL must hold)

- Any Rails/Ruby backend shipping to production with a database.
- Building multi-user SaaS with proper data isolation, audits, and async notifications.
- Complex domain logic (order processing, payment reconciliation, report generation).
- API backends with strict JSON contracts, validation errors, and fault handling.
- Background job pipelines for email, data export, or data transformation.

## Skip If (ANY kills it)

- Simple static sites or content management — Rails is overkill.
- Real-time systems requiring sub-100ms latency — consider Go or Rust.
- Teams unfamiliar with Rails conventions — the convention overhead requires buy-in.

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
