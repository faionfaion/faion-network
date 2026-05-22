---
slug: ruby-activerecord
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Efficient database access with proper query optimization via Query Objects for chainable filters, scopes as lambdas for composition, eager loading via includes() to prevent N+1, and lifecycle callbacks (before_validation, after_create_commit).
content_id: "1c7fa592ad35b975"
tags: [ruby, activerecord, rails, database, orm]
---
# ActiveRecord Patterns

## Summary

**One-sentence:** Efficient database access with proper query optimization via Query Objects for chainable filters, scopes as lambdas for composition, eager loading via includes() to prevent N+1, and lifecycle callbacks (before_validation, after_create_commit).

**One-paragraph:** Efficient database access with proper query optimization via Query Objects for chainable filters, scopes as lambdas for composition, eager loading via includes() to prevent N+1, and lifecycle callbacks (before_validation, after_create_commit). Validate presence, uniqueness with case_insensitive, and length constraints. Use has_one/has_many/has_many through for association semantics. Normalize data in callbacks (email lowercasing). Dispatch async work via deliver_later and callbacks.

## Applies If (ALL must hold)

- Any Rails application shipping to production with a relational database.
- Building a complex domain with associations, scopes, and validation rules.
- Extracting reusable query logic that appears in multiple controllers.
- Performance optimization: identifying N+1 queries and using includes/joins.

## Skip If (ANY kills it)

- NoSQL/document stores — use a different ORM pattern (Mongoid, etc.).
- Raw SQL is more efficient — use find_by_sql for complex analytical queries.
- Data migration/ETL scripts where overhead of the full Rails stack is unnecessary.

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
