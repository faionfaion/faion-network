---
slug: csharp-aspnet-core
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement layered architecture in ASP.
content_id: "bfacac58d0d6aa80"
tags: [aspnet-core, architecture, csharp, api, di]
---
# ASP.NET Core Patterns

## Summary

**One-sentence:** Implement layered architecture in ASP.

**One-paragraph:** Implement layered architecture in ASP.NET Core 8/9: [ApiController] routes to IXService interfaces, which delegate to repositories, which wrap Entity Framework Core. Thread CancellationToken through every async signature. Use AutoMapper to project entities to DTOs. Return ProblemDetails (RFC 7807) for errors. Organize by feature folders (Features/Users/) not technical layers. Mandatory: AsNoTracking on all read queries, [Authorize] and [ProducesResponseType] on every action, AssertConfigurationIsValid() test for AutoMapper.

## Applies If (ALL must hold)

- New ASP.NET Core 8/9 API with clear controller/service/repository separation.
- Migrating legacy ASP.NET MVC or WCF services to modern Web API.
- Multi-tenant or B2B SaaS in .NET where DI scopes and middleware are central.
- Codebase shared between humans and LLMs — explicit interfaces stabilize completions.
- Stepping stone before adopting CQRS/MediatR later.

## Skip If (ANY kills it)

- Tiny internal tools or webhooks with fewer than 10 endpoints — Minimal APIs are sufficient.
- Microservices that publish only to a queue — three layers around one method call is overkill.
- gRPC-only services — service-method-per-RPC layering is more appropriate.
- Apps on .NET Framework 4.x — Generic Host, async-by-default, and DI container assumptions do not hold.

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
