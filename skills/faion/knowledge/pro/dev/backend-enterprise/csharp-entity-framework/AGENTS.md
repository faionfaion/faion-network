# Entity Framework Core Patterns

## Summary

EF Core data-layer methodology for .NET 6+ services: entity configuration via
`IEntityTypeConfiguration<T>`, repository abstractions, paged query objects, and
migration safety checks. The testable rule: every entity gets its own configuration
class; `OnModelCreating` must not contain inline `builder` calls beyond
`ApplyConfigurationsFromAssembly`.

## Why

Keeping entity configs in separate files prevents `OnModelCreating` from becoming
unmaintainable past 5 entities. `AsNoTracking()` on reads eliminates identity-map
collisions. Reviewing migration SQL before apply catches cascade-delete cycles (SQL
Server) and missing FK indexes that EF Core skips in some providers. Projection over
`Include` chains avoids Cartesian joins on multi-level navigation properties.

## When To Use

- Designing or refactoring the EF Core data layer for a .NET 6+ service.
- Generating migrations from a clean domain model (not database-first scaffolding).
- Performance-tuning N+1 queries, projection vs. tracking trade-offs, compiled queries.
- Splitting read/write concerns (CQRS-lite) where commands use `SaveChanges` and
  queries use `AsNoTracking()` projections.

## When NOT To Use

- Codebase uses Dapper or raw ADO.NET intentionally for hot paths — do not insert EF.
- Read-only OLAP / data warehouse — change tracking is pure overhead; use Dapper.
- Cross-database migrations where EF provider gaps matter (Postgres JSONB ops, advisory
  locks) — drop to `FromSqlInterpolated` for those paths.
- Sub-millisecond latency requirements — EF expression-tree compilation adds 5-10 ms
  even with `AsNoTracking`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-entity-configuration.xml` | `IEntityTypeConfiguration<T>` pattern, indexes, relationships, owned types. |
| `content/02-repository-pattern.xml` | `IRepository<T>` interface, paged queries, `AsNoTracking`, `SaveChangesAsync`. |
| `content/03-rules-and-gotchas.xml` | Agent-critical rules: cascade cycles, Include vs projection, migration safety, version drift. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity-configuration.cs` | `IEntityTypeConfiguration<T>` skeleton with table, keys, indexes, relations. |
| `templates/repository.cs` | `IRepository<T>` interface + implementation with paged query. |
| `templates/safe-migration.sh` | Run `dotnet ef migrations add`, generate SQL, block on destructive ops. |
