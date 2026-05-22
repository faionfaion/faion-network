---
slug: csharp-dotnet-patterns
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: TBD — fill from v1 source
content_id: "21bcf93d3bf9d36d"
tags: [csharp, dotnet, aspnet-core, clean-architecture, domain-driven-design]
---
# C# .NET Patterns

## Summary

**One-sentence:** TBD

**One-paragraph:** .NET is a modern, cross-platform framework for building web APIs, microservices, and enterprise applications. This methodology covers ASP.NET Core patterns, clean architecture, domain-driven design, and best practices for C# development including dependency injection, middleware pipelines, configuration management, and async-first design.

## Applies If (ALL must hold)

- Enterprise web applications requiring high performance and scalability.
- Microservices architecture with event-driven communication.
- REST and gRPC APIs with complex business logic.
- Cloud-native applications (Azure, AWS) with tight integration requirements.
- Applications requiring strong typing and compile-time error detection.
- Teams familiar with C# and wanting to leverage the .NET ecosystem.
- Greenfield ASP.NET Core service where Clean Architecture is mandated and scaffolding is needed fast.
- Brownfield migration from legacy .NET Framework or classic Web API to .NET 8/9 minimal APIs with MediatR.
- Cross-cutting addition of MediatR pipelines (validation, logging, transactions, caching) to existing ASP.NET Core.
- Enforcing DTO boundaries when a codebase has leaked EF Core entities through controllers.
- Refactoring anemic services into rich aggregates with private setters, factory methods, and domain events.

## Skip If (ANY kills it)

- Greenfield projects with no prior .NET experience and tight delivery timelines.
- JavaScript-only teams with no C# expertise.
- Applications locked into specific language ecosystems (Java-only, Python-only).
- Simple CRUD applications where Django or Rails may be more lightweight.
- Console apps, single-file utilities, Azure Functions with one HTTP trigger. Clean Architecture's four-project split is overkill.
- Razor Pages or MVC monoliths where teams have no MediatR experience. Adding the bus creates a parallel architecture nobody owns.
- Game or Unity C# work. DI container, MediatR, and EF Core are wrong tools; prefer ECS patterns.
- Lambda or serverless functions with cold-start budgets under 300ms. MediatR and AutoMapper add startup overhead that breaks SLOs.
- Teams without DDD literacy. Rich-domain-model rules degrade into "private setters with no behavior," which is anemic with ceremony.

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
