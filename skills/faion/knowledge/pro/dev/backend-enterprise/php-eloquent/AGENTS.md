---
slug: php-eloquent
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for Eloquent model definition, query optimization, and repository abstraction in Laravel.
content_id: "6c795d163de7888d"
tags: [eloquent, laravel, orm, database, performance]
---
# Eloquent ORM Patterns (Laravel)

## Summary

**One-sentence:** Patterns for Eloquent model definition, query optimization, and repository abstraction in Laravel.

**One-paragraph:** Patterns for Eloquent model definition, query optimization, and repository abstraction in Laravel. Covers $fillable whitelisting, named scopes, Attribute::make() accessors, eager loading to prevent N+1, DB::transaction() for multi-write paths, and query budget enforcement. Repository pattern is optional — adopt only when you have a real swap-out case.

## Applies If (ALL must hold)

- Laravel API or web app with non-trivial data layer (5+ related entities, soft deletes, polymorphic relations).
- Refactoring controllers or services that build raw queries inline — extract to scopes, repositories, or query objects.
- Adding read-side optimizations (eager loading, chunking) after measuring an N+1 problem.
- Multi-tenant or role-gated apps where global scopes + policies enforce data boundaries at the model layer.
- LLM-driven greenfield work where models are the primary "schema-of-truth" the agent reasons about.

## Skip If (ANY kills it)

- Read-heavy analytics workloads — use raw DB:: query builder, chunkById, or jump to Postgres directly. Eloquent hydration is the bottleneck.
- High-throughput event ingestion (>5k req/s on a single box) — bypass Eloquent for inserts; use DB::table()->insert() or LazyCollection.
- Cross-database joins or non-RDBMS backends (Cassandra, DynamoDB, ClickHouse). Eloquent's relation API assumes a single SQL connection per query.
- Microservices where each service is less than 1k LOC and a single repository class adds more ceremony than it saves.

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
