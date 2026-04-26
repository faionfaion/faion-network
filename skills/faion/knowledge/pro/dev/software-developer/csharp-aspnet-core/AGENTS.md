# ASP.NET Core Patterns

## Summary

ASP.NET Core (.NET 8/9) layered architecture: record DTOs → `IService` + impl → `[ApiController]` controller → EF Core repository → AutoMapper/Mapperly → `IExceptionHandler` with `ProblemDetails` (RFC 7807). Enforces `CancellationToken` threading, `TimeProvider` injection, scoped DI for `DbContext`, and integration tests via `WebApplicationFactory` + Testcontainers.

## Why

Controller-heavy ASP.NET projects accumulate domain logic in HTTP handlers, inject `DbContext` into singletons (captive dependency), and return tracked EF entities directly (circular refs, information leaks). This methodology enforces the DTO mapping boundary, scoped DI discipline, RFC 7807 error shape, and testability via `TimeProvider`/`WebApplicationFactory` — the patterns that prevent the most common runtime failures.

## When To Use

- Building HTTP APIs in .NET 8/9 with `[ApiController]`, DI-injected services, EF Core
- Layered architecture (Controller → Service → Repository) with AutoMapper or Mapperly
- JWT/cookie authenticated APIs using `[Authorize]`
- OpenAPI-first endpoints via Swashbuckle or NSwag with strongly-typed DTOs

## When NOT To Use

- Microservices that fit Minimal API style — use `app.MapGroup(...)` instead of controllers
- Reactive/streaming endpoints — switch to gRPC or SignalR
- CQRS-heavy domains — use MediatR + handlers per command/query instead
- AOT-compiled apps — AutoMapper and generic filters break in Native AOT; use Mapperly (source-gen)

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | Controller/service/repository layer rules, DI scoping, EF Core guidance, CancellationToken |
| `content/02-rules.xml` | DTO mapping boundary, ProblemDetails error handling, TimeProvider, keyset pagination, LLM gotchas |
| `content/03-examples.xml` | Controller, service, IExceptionHandler, mapper, integration test examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/problem-details-handler.cs` | IExceptionHandler implementation mapping domain exceptions to RFC 7807 responses |
| `templates/prompt-aspnet-slice.txt` | Subagent prompt for generating full vertical slice: DTOs, service, controller, migration, test |
