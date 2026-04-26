# PHP Eloquent Patterns

## Summary

Eloquent ORM patterns for Laravel 10/11: model with `$fillable`, enum casts, scopes, accessors/mutators; optional thin Repository or Query Object for multi-condition filters; eager loading via `with()`/`loadMissing()`; `Model::preventLazyLoading()` in development; pagination enforced on all user-facing endpoints.

## Why

Eloquent's Active Record style silently produces N+1 queries, mass-assignment vulnerabilities (empty `$fillable`), and hydration overhead on bulk operations. Without `Model::preventLazyLoading()` in dev, agents ship N+1 undetected. Query Objects give a chainable, testable alternative to repositories for multi-condition report queries without the dead abstraction overhead.

## When To Use

- Laravel 10/11 models gaining scopes, accessors/mutators, relationships that need eager loading
- Migrating raw query builder to Eloquent for readability and relationship loading
- Standardizing `$fillable`, `$casts`, soft deletes, observers vs events across models
- API resources backed by paginated Eloquent collections

## When NOT To Use

- High-throughput hot paths where Eloquent hydration cost matters — use `DB::table(...)` builder
- Reporting/OLAP queries — Eloquent over-fetches; use raw SQL or a read model
- Bulk inserts/updates over 10k rows — use `upsert`, `LazyCollection`, or chunked raw SQL
- DDD aggregates with strict invariants — Active Record fights immutability and value objects

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-patterns.xml` | Model conventions: fillable, casts, scopes, accessors, soft deletes, ULID PKs |
| `content/02-query-patterns.xml` | Repository vs Query Object, eager loading rules, pagination enforcement, N+1 prevention |
| `content/03-examples.xml` | Model, repository, query object, controller wiring examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/query-object.php` | Fluent Query Object skeleton with active/search/role filters and paginate() |
| `templates/prompt-resource.txt` | Subagent prompt for generating model + migration + factory + resource + test in one diff |
