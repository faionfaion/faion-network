---
slug: csharp-dotnet
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production.
content_id: "90ae5d5bf578c265"
tags: [csharp, aspnet-core, entity-framework, backend, api]
---
# C# ASP.NET Core + Entity Framework

## Summary

**One-sentence:** Production.

**One-paragraph:** Production .NET backend patterns: [ApiController] controllers with typed route parameters, service interfaces with constructor DI, EF Core entities with IEntityTypeConfiguration, repository interfaces, and xUnit tests via WebApplicationFactory. Use nullable reference types project-wide, record types for DTOs, AsNoTracking() for read paths, and BackgroundService + Channel for in-process async work.

## Applies If (ALL must hold)

- Enterprise / B2B backends where Microsoft stack (Azure, AD, SQL Server) is already in place
- High-throughput APIs needing async/await, minimal allocation, and eventual AOT
- Long-running services (worker / hosted services) and gRPC microservices
- Domain-rich applications where strong static typing prevents whole categories of bugs
- Teams comfortable with dotnet CLI and willing to invest in Roslyn analyzers in CI

## Skip If (ANY kills it)

- Tiny scripts or one-off cron jobs — Python/Node ship in fewer lines
- Frontend BFFs in TypeScript-first orgs — the type-sharing story is weaker than tRPC/Hono
- Edge runtimes with hard cold-start budgets (less than 50ms) — Node/Bun win until AOT is fully adopted
- Greenfield startups where hiring senior C# developers is a real constraint

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
