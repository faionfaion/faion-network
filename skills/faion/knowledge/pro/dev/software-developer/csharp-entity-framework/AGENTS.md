---
slug: csharp-entity-framework
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: EF Core 8 patterns — fluent `IEntityTypeConfiguration`, `AsNoTracking` reads, `AsSplitQuery` on multi-collection includes, repository paged results, and ordered migrations.
content_id: "dec775197d9ee814"
complexity: medium
produces: code
est_tokens: 4400
tags: [entity-framework, orm, csharp, database, migrations]
---
# Entity Framework Patterns

## Summary

**One-sentence:** EF Core 8 patterns — fluent `IEntityTypeConfiguration`, `AsNoTracking` reads, `AsSplitQuery` on multi-collection includes, repository paged results, and ordered migrations.

**One-paragraph:** EF Core misuse — data annotations on entities, lazy-loading proxies, `IQueryable` returned from repositories, Cartesian explosions from multi-Include — produces the classic "EF Core is slow" complaint. This methodology pins five rules: entities are POCOs with private setters initialized in constructors; mapping lives in `IEntityTypeConfiguration<T>` via fluent API; read paths use `.AsNoTracking()` + DTO projection; multi-collection queries use `.AsSplitQuery()`; migrations are append-only and named with verbs. Output: entity + configuration + repository + migration scaffold per `02-output-contract.xml`.

**Ефективно для:**

- Production EF Core 8 apps with non-trivial domain.
- Read paths under throughput pressure (AsNoTracking + projection).
- Multi-collection queries causing Cartesian explosion.
- Repositories that must hide `IQueryable` from upper layers.
- Teams co-versioning migrations with entity changes.

## Applies If (ALL must hold)

- EF Core 6+ (Code-First) inside an ASP.NET Core or worker project.
- Migrations are the schema-of-record (not a hand-maintained SQL script).
- The team agrees DTOs separate from entities for transport.
- Read/write paths can be distinguished at the repository boundary.

## Skip If (ANY kills it)

- Database-First / `EDMX` legacy project — start with a migration plan first.
- Dapper / micro-ORM is already in place and adequate.
- Trivial CRUD with single-table reads — overhead exceeds benefit.
- Stored-procedure-heavy enterprise app — EF Core sits on top of SP-only contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Entity sketch | C# class or ERD | team |
| DbContext + connection | existing csproj | repo |
| Migration history | `Migrations/` folder | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | ASP.NET Core layout that wires EF in. |
| [[ddd-repositories]] | Repository pattern abstracting EF behind a domain interface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fluent-config-only, asnotracking-reads, no-iqueryable-return, splitquery-multi-include, append-only-migrations | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for entity+config+repo+migration spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: cartesian-explosion, tracking-on-reads, lazy-loading-proxies, edited-migration | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on workload + Include shape → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-entity-and-config` | sonnet | Layered judgment on relationships + indexes. |
| `write-repository-paged` | sonnet | Paged read scaffolding. |
| `audit-existing-queries` | sonnet | Look for AsNoTracking + Include violations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Entity.cs` | POCO entity with private setters |
| `templates/EntityConfiguration.cs` | Fluent mapping skeleton |
| `templates/Repository.cs` | Repository with PagedResult + AsNoTracking |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-entity-framework.py` | Validate entity+config+repo spec against schema | Pre-commit on spec artefact |

## Related

- [[csharp-dotnet]]
- [[ddd-repositories]]
- [[csharp-dotnet-patterns]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (workload — read-heavy vs write-heavy, Include shape) to a rule from `01-core-rules.xml`, either approving the EF Core pattern or routing to Dapper / raw SQL. Use it whenever adding a new entity, a new query, or refactoring a slow page.
