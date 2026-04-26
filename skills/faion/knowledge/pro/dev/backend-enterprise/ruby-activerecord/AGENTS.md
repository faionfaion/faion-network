# ActiveRecord Patterns (Rails)

## Summary

Patterns for Rails ActiveRecord optimization: Query Objects for complex filter chains, named scopes for simple primitives, eager loading with `includes`/`preload`/`eager_load`, and N+1 prevention. Covers model callbacks, `find_each` for bulk operations, and mandatory eager-load-by-default in controllers. Use the `bullet` + `prosopite` gems to gate N+1 regressions in CI.

## Why

Lazy loading is ActiveRecord's primary production trap. A missing `includes` in a controller that renders a list fires N additional SELECT statements — invisible in code review and undetected without a dedicated N+1 detector. Query Objects extract complex filter logic from controllers into testable, composable units under `app/queries/`.

## When To Use

- Rails apps where models exceed ~150 lines and inline `where` chains scatter across controllers.
- Multi-tenant Rails apps where global scopes and tenant-aware queries must be enforced consistently.
- Measured ORM hot paths (>30% of request time in AR) — query objects + eager loading measurably improve.
- LLM-driven feature work where each AR query must be reviewable in isolation.

## When NOT To Use

- Simple CRUD admin (Rails Admin / ActiveAdmin) — the framework manages queries; query objects add ceremony.
- Rails apps under 1k LOC — direct AR scope blocks plus thin controllers are fine.
- Read-replicas or sharded DBs needing raw `connected_to(role: :reading)` — query object DSL hides the switch.
- Background workers operating on enqueued IDs via `find_each` — no benefit from a chained query object.
- Reporting/analytics — drop to `ActiveRecord::Base.connection.execute` with explicit SQL.

## Content

| File | What's inside |
|------|---------------|
| `content/01-query-object.xml` | Query Object pattern with fluent builder, paginate, and results method. |
| `content/02-model-scopes-callbacks.xml` | Named scopes, callbacks, and eager loading rules. |
| `content/03-rules-and-gotchas.xml` | Mandatory rules and AI-agent gotchas for AR query safety. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ar-budget.sh` | CI gate: fail on N+1 (Bullet/Prosopite) and per-spec query budget. |
