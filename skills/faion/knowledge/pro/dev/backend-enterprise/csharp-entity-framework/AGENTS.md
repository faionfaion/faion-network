---
slug: csharp-entity-framework
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: EF Core data-layer methodology for.
content_id: "cf3c9b41f6805e01"
tags: [entity-framework, dotnet, orm, data-layer, database]
---
# Entity Framework Core Patterns

## Summary

**One-sentence:** EF Core data-layer methodology for.

**One-paragraph:** EF Core data-layer methodology for .NET 6+ services: entity configuration via IEntityTypeConfiguration<T>, repository abstractions, paged query objects, and migration safety checks. The testable rule: every entity gets its own configuration class; OnModelCreating must not contain inline builder calls beyond ApplyConfigurationsFromAssembly.

## Applies If (ALL must hold)

- Designing or refactoring the EF Core data layer for a .NET 6+ service.
- Generating migrations from a clean domain model (not database-first scaffolding).
- Performance-tuning N+1 queries, projection vs. tracking trade-offs, compiled queries.
- Splitting read/write concerns (CQRS-lite) where commands use SaveChanges and queries use AsNoTracking() projections.

## Skip If (ANY kills it)

- Codebase uses Dapper or raw ADO.NET intentionally for hot paths — do not insert EF.
- Read-only OLAP / data warehouse — change tracking is pure overhead; use Dapper.
- Cross-database migrations where EF provider gaps matter (Postgres JSONB ops, advisory locks) — drop to FromSqlInterpolated for those paths.
- Sub-millisecond latency requirements — EF expression-tree compilation adds 5-10 ms even with AsNoTracking.

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
