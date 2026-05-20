---
slug: csharp-dotnet
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Greenfield ASP.
content_id: "90ae5d5bf578c265"
tags: [csharp, dotnet, aspnet-core, entity-framework, backend]
---
# C# .NET Core Backend Development

## Summary

**One-sentence:** Greenfield ASP.

**One-paragraph:** Greenfield ASP.NET Core 8/9 services integrate layered controller/service/repository architecture, Entity Framework Core for data access, xUnit for unit and integration testing, and BackgroundService for async work. All async methods accept CancellationToken. Configure DI to register DbContext as scoped, hosted services as singleton, and resolve scoped dependencies inside background services via IServiceProvider.CreateScope(). Use AutoMapper to project entities to DTOs. Return ProblemDetails for errors. Organize by feature folders (Features/Users/) not technical layers.

## Applies If (ALL must hold)

- Greenfield ASP.NET Core 8/9 service: REST/gRPC API, EF Core data layer, xUnit tests, BackgroundService for async work.
- Brownfield .NET Framework → .NET 8 migration where the agent needs a single map of patterns covering controllers, EF, tests, and hosted services.
- Internal enterprise APIs where DI, options pattern, and configuration binding are part of the contract.

## Skip If (ANY kills it)

- Tiny CLI utilities — dotnet new console is enough; agents should not impose Controller/Service/Repository on a 200-line script.
- Highly dynamic plugin systems — F# or scripting is a better fit; .NET reflection-heavy plugin loading trips up codegen.
- Functional/event-sourced cores — use F# or a CQRS framework (MediatR + Marten/EventStore) directly; this umbrella's Repository pattern fights that grain.

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
