---
slug: ruby-activerecord
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for Rails ActiveRecord optimization: Query Objects for complex filter chains, named scopes for simple primitives, eager loading with includes/preload/eager_load, and N+1 prevention.
content_id: "1c7fa592ad35b975"
tags: [activerecord, rails, query-objects, orm, performance]
---
# ActiveRecord Patterns for Rails

## Summary

**One-sentence:** Patterns for Rails ActiveRecord optimization: Query Objects for complex filter chains, named scopes for simple primitives, eager loading with includes/preload/eager_load, and N+1 prevention.

**One-paragraph:** Patterns for Rails ActiveRecord optimization: Query Objects for complex filter chains, named scopes for simple primitives, eager loading with includes/preload/eager_load, and N+1 prevention. Covers model callbacks, find_each for bulk operations, and mandatory eager-load-by-default in controllers. Use the bullet + prosopite gems to gate N+1 regressions in CI.

## Applies If (ALL must hold)

- Rails apps where models exceed ~150 lines and inline where chains scatter across controllers.
- Multi-tenant Rails apps where global scopes and tenant-aware queries must be enforced consistently.
- Measured ORM hot paths (>30% of request time in AR) — query objects + eager loading measurably improve.
- LLM-driven feature work where each AR query must be reviewable in isolation.
- Codebases adopting Trailblazer / dry-rb partials — Query Objects play nicely as ingest into the new architecture.

## Skip If (ANY kills it)

- Simple CRUD admin (Rails Admin / ActiveAdmin) — the framework manages queries; query objects add ceremony.
- Rails apps under 1k LOC — direct AR scope blocks plus thin controllers are fine.
- Read-replicas or sharded DBs needing raw connected_to(role: :reading) — query object DSL hides the switch.
- Background workers operating on enqueued IDs via find_each — no benefit from a chained query object.
- Reporting/analytics — drop to ActiveRecord::Base.connection.execute with explicit SQL.

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
