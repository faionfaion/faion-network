# Entity Framework Core Patterns

## Summary

**One-sentence:** EF Core data-layer methodology for .NET 6+ services — `IEntityTypeConfiguration<T>` per entity, repository abstractions, paged query objects, AsNoTracking discipline, and migration safety.

**One-paragraph:** EF Core data layer for .NET 6+ services: every entity gets its own `IEntityTypeConfiguration<T>`; `OnModelCreating` calls `ApplyConfigurationsFromAssembly(...)` and nothing else. Read paths use `AsNoTracking()`. Aggregate roots carry `RowVersion`/`[ConcurrencyCheck]`. Bulk writes use `ExecuteUpdateAsync`/`ExecuteDeleteAsync`. Cross-cutting audit fields (CreatedAt, UpdatedBy) live in a `SaveChangesInterceptor`, never per-entity. Migrations are reviewed as SQL via `dotnet ef migrations script` before any prod apply.

**Ефективно для:**

- Designing or refactoring the EF Core data layer for a .NET 6+ service.
- Generating migrations from a clean domain model (not database-first scaffolding).
- Performance-tuning N+1 queries, projection vs tracking trade-offs, compiled queries.
- Splitting read/write concerns (CQRS-lite) where commands use SaveChanges and queries use `AsNoTracking()` projections.

## Applies If (ALL must hold)

- Designing or refactoring the EF Core data layer for a .NET 6+ service.
- Generating migrations from a clean domain model (not database-first scaffolding).
- Splitting read/write concerns where commands use SaveChanges and queries use `AsNoTracking()` projections.

## Skip If (ANY kills it)

- Codebase uses Dapper or raw ADO.NET intentionally for hot paths — do not insert EF.
- Read-only OLAP / data warehouse — change tracking is pure overhead; use Dapper.
- Cross-database migrations where EF provider gaps matter (Postgres JSONB ops, advisory locks) — drop to `FromSqlInterpolated` for those paths.
- Sub-millisecond latency requirements — EF expression-tree compilation adds 5-10 ms even with `AsNoTracking`.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Domain entity model | C# classes or ERD | domain modelling |
| Target DB provider | `Npgsql` / `SqlServer` / `Sqlite` | platform |
| Migration safety policy | Markdown checklist | DBA / SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Umbrella covering DI lifetimes that govern DbContext scope. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: entity-config-per-entity, asnotracking-on-reads, concurrency-token-on-aggregates, bulk-execute-update-delete, savechanges-interceptor-for-audit, migration-sql-review | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the EF data-layer manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: scope DbContext → entity configurations → repositories → audit interceptor → migration safety | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-entity` | sonnet | Translating domain entity to `IEntityTypeConfiguration<T>` requires judgment. |
| `optimise-query` | sonnet | N+1 + projection trade-offs need analysis. |
| `review-migration` | opus | Destructive migration risk — needs careful reasoning. |
| `audit-asnotracking` | haiku | Mechanical scan for read paths missing AsNoTracking. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity-configuration.cs` | `IEntityTypeConfiguration<T>` skeleton for one aggregate. |
| `templates/repository.cs` | Repository pattern that materialises results before returning. |
| `templates/safe-migration.sh` | Wrapper around `dotnet ef migrations script` for SQL review before apply. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-entity-framework.py` | Validate the EF data-layer manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[csharp-dotnet]]
- [[csharp-dotnet-patterns]]
- [[csharp-xunit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (read vs write path, latency budget, provider, concurrency requirement) to a rule from `01-core-rules.xml`. Use it before scaffolding a new entity or refactoring a hot query.
