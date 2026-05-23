---
slug: php-eloquent
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Eloquent ORM methodology for Laravel — $fillable whitelist, Attribute::make accessors, eager-load discipline, DB::transaction for multi-write, preventLazyLoading in dev, paired migration+factory+resource on every change.
content_id: "20906c4347c5fc36"
complexity: deep
produces: code
est_tokens: 4400
tags: [eloquent, laravel, orm, database, performance]
---
# Eloquent ORM Patterns (Laravel)

## Summary

**One-sentence:** Eloquent ORM methodology for Laravel — $fillable whitelist, Attribute::make accessors, eager-load discipline, DB::transaction for multi-write, preventLazyLoading in dev, paired migration+factory+resource on every change.

**One-paragraph:** Patterns for Eloquent model definition, query optimisation, and integration in Laravel 10/11. Models declare `$fillable` (never empty `$guarded`). Accessors / mutators use `Attribute::make()`; legacy `getXAttribute()` is forbidden in the same model. Eager-loading is done at the repository / service boundary via `->with(...)`. Multi-write paths run in `DB::transaction(...)`. `Model::preventLazyLoading(! app()->isProduction())` is set in `AppServiceProvider` so N+1 throws in dev. Every entity diff lands paired with a migration, a factory, and an API Resource.

**Ефективно для:**

- Laravel API or web app with 5+ related entities, soft deletes, polymorphic relations.
- Refactoring controllers / services that build raw queries inline — extract to scopes, repositories, or query objects.
- Adding read-side optimisations (eager loading, chunking) after measuring an N+1 problem.
- Multi-tenant or role-gated apps where global scopes + policies enforce data boundaries at the model layer.

## Applies If (ALL must hold)

- Laravel 10/11 app on PHP 8.2+.
- Eloquent is the primary ORM in use.
- Codebase has ≥5 entities with relationships.

## Skip If (ANY kills it)

- Read-heavy analytics workloads — use `DB::` query builder + `chunkById`; Eloquent hydration is the bottleneck.
- High-throughput event ingestion (>5k req/s on a single box) — bypass Eloquent for inserts.
- Cross-database joins or non-RDBMS backends (Cassandra, DynamoDB, ClickHouse).
- Microservices < 1k LOC where a single repository class is heavier than the rest of the code.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eloquent model list | Markdown | data modelling |
| Index policy | text | DBA |
| Migration policy | text | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Umbrella for controller / queue patterns. |
| [[laravel-patterns]] | Enterprise patterns that drive Eloquent discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: fillable-whitelist, attribute-make-only, eager-load-at-boundary, db-transaction-multiwrite, prevent-lazy-loading-in-dev, paired-migration-factory-resource | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Eloquent-discipline manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: guarded-empty-mass-assignment, mixed-accessor-apis, lazy-load-in-controller, single-write-orphan, missing-index-on-where | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: model + migration + factory → relations + accessors → scopes → repository eager-load → preventLazyLoading guard | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-aggregate` | sonnet | Relation + accessor design needs judgment. |
| `audit-n-plus-one` | haiku | Mechanical scan via query-budget assertion. |
| `design-bulk-import` | opus | Hydration vs raw insert trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/query-budget.sh` | CLI helper running query-budget assertions across test suite. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-eloquent.py` | Validate the Eloquent-discipline manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[php-laravel]]
- [[laravel-patterns]]
- [[php-laravel-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (workload shape, write multiplicity, dev-vs-prod) to a rule from `01-core-rules.xml`. Use it before scaffolding a model or refactoring a query.
