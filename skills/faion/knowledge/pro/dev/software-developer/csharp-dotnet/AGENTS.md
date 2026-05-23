---
slug: csharp-dotnet
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Production ASP.NET Core + EF Core layout with [ApiController] + service interfaces + scoped DI + nullable refs + record DTOs + AsNoTracking reads.
content_id: "ea9863d5ed2608c8"
complexity: medium
produces: code
est_tokens: 4200
tags: [csharp, aspnet-core, entity-framework, backend, api]
---
# C# ASP.NET Core + Entity Framework

## Summary

**One-sentence:** Production ASP.NET Core + EF Core layout with [ApiController] + service interfaces + scoped DI + nullable refs + record DTOs + AsNoTracking reads.

**One-paragraph:** Greenfield .NET 8 backend conventions: `[ApiController]` controllers with typed route binding, `[Service]` interfaces with constructor DI, `DbContext` registered scoped, EF Core entities with `IEntityTypeConfiguration<T>`, repository interfaces only where DDD requires them, `AsNoTracking()` on read paths, `record` DTOs for transport, nullable reference types project-wide. Output: a feature folder (Controller + Service + DTO + EntityConfig + xUnit slice test) conforming to `02-output-contract.xml`.

**Ефективно для:**

- Enterprise backends on Microsoft stack (Azure, AD, SQL Server).
- High-throughput APIs needing async + minimal allocation.
- Domain-rich apps where strong static typing prevents bugs.
- Long-running services (`BackgroundService`) and gRPC microservices.
- Teams with Roslyn analyzers + nullable-refs already enforced.

## Applies If (ALL must hold)

- Greenfield or refactored ASP.NET Core 6+ project.
- EF Core (any provider) is the persistence layer.
- xUnit (not MSTest / NUnit) is the test framework.
- DI lifetimes (singleton/scoped/transient) are understood across the team.

## Skip If (ANY kills it)

- Tiny scripts or one-off cron — Python/Node ship in fewer lines.
- Frontend BFFs in TypeScript-first orgs — tRPC/Hono wins type-sharing.
- Edge runtimes with sub-50ms cold start — AOT not yet mature enough.
- Greenfield startups where senior C# hiring is a real constraint.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | ticket / SDD task |
| Existing solution layout | .sln + csproj | repo |
| DB schema or entity sketch | C# class or ERD | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-entity-framework]] | EF Core patterns this feature consumes. |
| [[csharp-xunit-testing]] | Test conventions for the slice test. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: apicontroller-required, scoped-dbcontext, nullable-refs-on, record-dtos, asnotracking-reads | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for feature folder + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: anaemic-controller, tracking-leaks, dto-as-entity, missing-cancellationtoken | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: classify → entity+config → service → controller → test | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on stack/runtime → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-feature-folder` | sonnet | Layered judgment on naming + boundaries. |
| `write-controller-service` | sonnet | C# scaffolding within the 5 rules. |
| `write-xunit-slice-test` | haiku | Mechanical AAA test against the controller. |

## Templates

| File | Purpose |
|------|---------|
| `templates/FeatureController.cs` | `[ApiController]` skeleton with typed routes |
| `templates/FeatureService.cs` | Service + DI skeleton |
| `templates/EntityConfiguration.cs` | `IEntityTypeConfiguration<T>` skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-dotnet.py` | Validate feature-folder spec against schema | Pre-commit on spec artefact |

## Related

- [[csharp-entity-framework]]
- [[csharp-background-services]]
- [[csharp-xunit-testing]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (runtime constraints, stack, async needs) to a rule from `01-core-rules.xml`, either approving the ASP.NET Core feature layout or redirecting to a smaller stack (script, edge function, BFF). Use it whenever starting a new .NET feature folder or porting from Web Forms / .NET Framework.
