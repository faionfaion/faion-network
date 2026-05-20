---
slug: csharp-dotnet-patterns
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Clean Architecture for.
content_id: "21bcf93d3bf9d36d"
tags: [clean-architecture, cqrs, dotnet, entity-framework, ddd]
---
# C# .NET Clean Architecture + CQRS Patterns

## Summary

**One-sentence:** Clean Architecture for.

**One-paragraph:** Clean Architecture for .NET 8/9 with MediatR/CQRS: Domain (entities, value objects, domain events) → Application (Commands, Queries, Handlers, Validators) → Infrastructure (EF Core, configurations) → API (controllers or Minimal API, composition root only). One Command/Query per folder. Domain behavior in entity methods, not Application handlers. Architecture fitness enforced by NetArchTest in CI.

## Applies If (ALL must hold)

- .NET 8/9 service with non-trivial domain (3+ aggregate roots, multiple bounded contexts, business rules beyond CRUD).
- Multi-team enterprise codebase where Application/Domain/Infrastructure separation enables parallel work.
- Microservices with event-driven integration — domain events + MediatR Notification pattern for cross-aggregate hand-offs.
- Apps targeting native AOT / containerized deploys where layering trims Infrastructure dependencies.

## Skip If (ANY kills it)

- Simple CRUD apps (<20 endpoints, no business rules) — four projects are pure overhead.
- Lambda/Functions with cold-start budget — DI graph + MediatR add 100-300ms startup; use Minimal API + direct DbContext.
- Teams unfamiliar with DDD — pattern's value depends on rich domain models; without that, you have a layered anemic codebase.
- Pure read-side services (reporting, dashboards) — CQRS is overkill; one project with SELECT queries is fine.

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
