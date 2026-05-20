---
slug: csharp-aspnet-core
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ASP.
content_id: "bfacac58d0d6aa80"
tags: [aspnet-core, dotnet, architecture, entity-framework, dependency-injection]
---
# ASP.NET Core Patterns

## Summary

**One-sentence:** ASP.

**One-paragraph:** ASP.NET Core (.NET 8/9) layered architecture: record DTOs → IService + impl → [ApiController] controller → EF Core repository → AutoMapper/Mapperly → IExceptionHandler with ProblemDetails (RFC 7807). Enforces CancellationToken threading, TimeProvider injection, scoped DI for DbContext, and integration tests via WebApplicationFactory + Testcontainers.

## Applies If (ALL must hold)

- Building HTTP APIs in .NET 8/9 with [ApiController], DI-injected services, EF Core.
- Layered architecture (Controller → Service → Repository) with AutoMapper or Mapperly.
- JWT/cookie authenticated APIs using [Authorize].
- OpenAPI-first endpoints via Swashbuckle or NSwag with strongly-typed DTOs.

## Skip If (ANY kills it)

- Microservices that fit Minimal API style — use app.MapGroup(...) instead of controllers.
- Reactive/streaming endpoints — switch to gRPC or SignalR.
- CQRS-heavy domains — use MediatR + handlers per command/query instead.
- AOT-compiled apps — AutoMapper and generic filters break in Native AOT; use Mapperly (source-gen).

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
