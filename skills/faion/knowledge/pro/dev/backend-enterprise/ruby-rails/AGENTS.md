---
slug: ruby-rails
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Build production-grade Rails applications by extracting multi-step business logic into Service Objects, using Query Objects for efficient database access, and leveraging Sidekiq for asynchronous processing.
content_id: "218f2d3386bb58f2"
tags: [ruby, rails, backend, activerecord, sidekiq]
---
# Ruby on Rails Backend Development

## Summary

**One-sentence:** Build production-grade Rails applications by extracting multi-step business logic into Service Objects, using Query Objects for efficient database access, and leveraging Sidekiq for asynchronous processing.

**One-paragraph:** Build production-grade Rails applications by extracting multi-step business logic into Service Objects, using Query Objects for efficient database access, and leveraging Sidekiq for asynchronous processing. Wrap multi-step writes in transactions, move side effects outside transactions, and use RSpec with FactoryBot for comprehensive testing.

## Applies If (ALL must hold)

- Rails 7+ applications where controllers or ActiveRecord callbacks have grown unwieldy.
- Multi-step writes that must be transactional plus side effects (mailers, audit logs, webhooks).
- Applications needing a uniform success/failure return shape so controllers do not sniff exceptions.
- Refactoring fat controllers and fat models toward service-centric architecture.
- Asynchronous processing of slow workflows with Sidekiq jobs and retry policies.

## Skip If (ANY kills it)

- Tiny single-step writes where wrapping in a service is excessive ceremony.
- Read-only endpoints where services add no value over a query object or scope.
- Apps using Hanami, Sinatra, or pure Rack where Rails conventions do not transfer.
- High-throughput message processing (>10k msg/s) where Sidekiq hits ceiling; use Karafka or dedicated Go/Rust worker.
- Rails 5/6 LTS where some patterns (after_create_commit, encrypted attributes) require Rails 7+.

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
