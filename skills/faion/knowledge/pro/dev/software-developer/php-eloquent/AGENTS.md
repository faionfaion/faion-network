---
slug: php-eloquent
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Eloquent ORM patterns for Laravel 10/11: model with $fillable, enum casts, scopes, accessors/mutators; optional thin Repository or Query Object for multi-condition filters; eager loading via with()/loadMissing(); Model::preventLazyLoading() in development; pagination enforced on all user-facing endpoints.
content_id: "6c795d163de7888d"
tags: [eloquent, laravel, orm, php, query-optimization]
---
# PHP Eloquent Patterns

## Summary

**One-sentence:** Eloquent ORM patterns for Laravel 10/11: model with $fillable, enum casts, scopes, accessors/mutators; optional thin Repository or Query Object for multi-condition filters; eager loading via with()/loadMissing(); Model::preventLazyLoading() in development; pagination enforced on all user-facing endpoints.

**One-paragraph:** Eloquent ORM patterns for Laravel 10/11: model with $fillable, enum casts, scopes, accessors/mutators; optional thin Repository or Query Object for multi-condition filters; eager loading via with()/loadMissing(); Model::preventLazyLoading() in development; pagination enforced on all user-facing endpoints.

## Applies If (ALL must hold)

- Laravel 10/11 models gaining scopes, accessors/mutators, relationships that need eager loading
- Migrating raw query builder to Eloquent for readability and relationship loading
- Standardizing $fillable, $casts, soft deletes, observers vs events across models
- API resources backed by paginated Eloquent collections

## Skip If (ANY kills it)

- High-throughput hot paths where Eloquent hydration cost matters — use DB::table(...) builder
- Reporting/OLAP queries — Eloquent over-fetches; use raw SQL or a read model
- Bulk inserts/updates over 10k rows — use upsert, LazyCollection, or chunked raw SQL
- DDD aggregates with strict invariants — Active Record fights immutability and value objects

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
