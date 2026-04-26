# Eloquent ORM Patterns (Laravel)

## Summary

Patterns for Eloquent model definition, query optimization, and repository abstraction in Laravel. Covers `$fillable` whitelisting, named scopes, `Attribute::make()` accessors, eager loading to prevent N+1, `DB::transaction()` for multi-write paths, and query budget enforcement. Repository pattern is optional — adopt only when you have a real swap-out case.

## Why

Eloquent's lazy loading is the primary source of N+1 regressions in Laravel apps. Relations are loaded on first access unless eager-loaded via `->with()`. `$fillable` misconfiguration is a recurring mass-assignment CVE source. The `Attribute::make()` API replaces legacy `getXAttribute()` but the two cannot be mixed without undefined behavior.

## When To Use

- Laravel API or web app with non-trivial data layer (5+ related entities, soft deletes, polymorphic relations).
- Refactoring controllers or services that build raw queries inline — extract to scopes, repositories, or query objects.
- Adding read-side optimizations (eager loading, chunking) after measuring an N+1 problem.
- Multi-tenant or role-gated apps where global scopes + policies enforce data boundaries at the model layer.

## When NOT To Use

- Read-heavy analytics workloads — use raw `DB::` query builder or Postgres directly; Eloquent hydration is the bottleneck.
- High-throughput event ingestion (>5k req/s) — bypass Eloquent for inserts; use `DB::table()->insert()`.
- Cross-database joins or non-RDBMS backends (Cassandra, DynamoDB, ClickHouse).
- Microservices where each service is under 1k LOC — repository pattern adds more ceremony than value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-definition.xml` | Model with $fillable, $casts, relationships, scopes, and Attribute::make() accessor. |
| `content/02-repository-pattern.xml` | Optional repository layer with paginate, findOrFail, create/update/delete, and eager loading. |
| `content/03-rules-and-gotchas.xml` | Mandatory rules and AI-agent gotchas for Eloquent N+1, mass assignment, and soft deletes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/query-budget.sh` | CI gate: fail if any feature test exceeds N queries (integrates with Debugbar/query log). |
