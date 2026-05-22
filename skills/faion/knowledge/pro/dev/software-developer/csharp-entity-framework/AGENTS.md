---
slug: csharp-entity-framework
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Entity Framework Core patterns for ASP.
content_id: "cf3c9b41f6805e01"
tags: [entity-framework, orm, csharp, database, migrations]
---
# Entity Framework Patterns

## Summary

**One-sentence:** Entity Framework Core patterns for ASP.

**One-paragraph:** Entity Framework Core patterns for ASP.NET Core backends: entity definition, IEntityTypeConfiguration, repository interface and implementation, AsNoTracking() for reads, paged queries, migrations, and change tracking management. Covers configuration best practices, N+1 prevention, and concurrency handling.

## Applies If (ALL must hold)

- ASP.NET Core / .NET worker services that need an ORM with LINQ, change tracking, migrations, and provider portability
- Domain models with rich relationships (one-to-many, many-to-many, owned types, TPH/TPT inheritance)
- Read paths that benefit from compiled queries and EF 8+ JSON column support
- CQRS-flavored apps where commands use the tracked context and queries use AsNoTracking() projections
- Greenfield work that needs first-class migration tooling (dotnet ef migrations add)

## Skip If (ANY kills it)

- High-throughput analytical workloads — Dapper, plain ADO.NET, or Microsoft.Data.SqlClient outperform EF for read-heavy hot paths
- Stored-procedure-heavy systems where the DBA owns all SQL — EF mapping fights the existing model
- Streaming / bulk inserts of millions of rows — use SqlBulkCopy, Npgsql COPY, or EFCore.BulkExtensions
- DBs without a strong EF provider (some NoSQL, niche RDBMSes) — pick a native client
- Tight memory environments (AOT trimming) where EF reflection footprint matters; consider Dapper + manual mapping

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
