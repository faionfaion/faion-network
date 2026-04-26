# C# .NET Clean Architecture + CQRS Patterns

## Summary

Clean Architecture for .NET 8/9 with MediatR/CQRS: Domain (entities, value objects, domain events) → Application (Commands, Queries, Handlers, Validators) → Infrastructure (EF Core, configurations) → API (controllers or Minimal API, composition root only). One Command/Query per folder. Domain behavior in entity methods, not Application handlers. Architecture fitness enforced by NetArchTest in CI.

## Why

Without layer enforcement, agents add EF Core imports to the Application layer within weeks. CQRS (MediatR) separates reads and writes cleanly, but only delivers value when Domain entities hold real behavior — otherwise you get an anemic layered monolith with extra indirection. NetArchTest catches layer violations at compile time, which agents would otherwise silently introduce.

## When To Use

- .NET 8/9 service with non-trivial domain (3+ aggregate roots, multiple bounded contexts, business rules beyond CRUD).
- Multi-team enterprise codebase where Application/Domain/Infrastructure separation enables parallel work.
- Microservices with event-driven integration — domain events + MediatR Notification pattern for cross-aggregate hand-offs.
- Apps targeting native AOT / containerized deploys where layering trims Infrastructure dependencies.

## When NOT To Use

- Simple CRUD apps (&lt;20 endpoints, no business rules) — four projects are pure overhead.
- Lambda/Functions with cold-start budget — DI graph + MediatR add 100-300ms startup; use Minimal API + direct DbContext.
- Teams unfamiliar with DDD — pattern's value depends on rich domain models; without that, you have a layered anemic codebase.
- Pure read-side services (reporting, dashboards) — CQRS is overkill; one project with SELECT queries is fine.

## Content

| File | What's inside |
|------|---------------|
| `content/01-domain-layer.xml` | BaseEntity, rich domain entity, and Value Object with factory method and domain events. |
| `content/02-application-cqrs.xml` | MediatR Command + Validator + Handler, and Query + Handler with AsNoTracking projection. |
| `content/03-infrastructure-api.xml` | EF Core DbContext with domain event dispatch, entity configuration, and API controller. |
| `content/04-rules-and-gotchas.xml` | Architecture rules, MediatR licensing note, and AI-agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/arch-tests.cs` | NetArchTest xUnit tests asserting Domain has zero references to outer layers. |
