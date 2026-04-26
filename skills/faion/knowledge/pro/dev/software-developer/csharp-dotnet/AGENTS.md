# C# ASP.NET Core + Entity Framework

## Summary

Production .NET backend patterns: `[ApiController]` controllers with typed route parameters, service interfaces with constructor DI, EF Core entities with `IEntityTypeConfiguration`, repository interfaces, and xUnit tests via `WebApplicationFactory`. Use nullable reference types project-wide, `record` types for DTOs, `AsNoTracking()` for read paths, and `BackgroundService` + `Channel<T>` for in-process async work.

## Why

ASP.NET Core's DI container enforces constructor injection, making every dependency explicit and swappable. Strong static typing + records + nullable references prevent whole bug classes at compile time. EF Core's `IEntityTypeConfiguration` keeps mapping logic out of entity classes. The controller/service/repository split is testable at each layer with xUnit + `WebApplicationFactory<Program>` for integration tests without a real HTTP server.

## When To Use

- Enterprise / B2B backends where Microsoft stack (Azure, AD, SQL Server) is already in place.
- High-throughput APIs needing `async/await`, minimal allocation, and eventual AOT.
- Long-running services (worker / hosted services) and gRPC microservices.
- Domain-rich applications where strong static typing prevents whole categories of bugs.
- Teams comfortable with `dotnet` CLI and willing to invest in Roslyn analyzers in CI.

## When NOT To Use

- Tiny scripts or one-off cron jobs — Python/Node ship in fewer lines.
- Frontend BFFs in TypeScript-first orgs — the type-sharing story is weaker than tRPC/Hono.
- Edge runtimes with hard cold-start budgets (<50ms) — Node/Bun win until AOT is fully adopted.
- Greenfield startups where hiring senior C# developers is a real constraint.

## Content

| File | What's inside |
|------|---------------|
| `content/01-controller-service.xml` | Controller routing, ActionResult<T> patterns, service interface + impl, constructor DI rules |
| `content/02-ef-core.xml` | Entity definition, IEntityTypeConfiguration, repository interface + impl, AsNoTracking, paging |
| `content/03-background-services.xml` | BackgroundService + Channel<T> for in-process queue, PeriodicTimer for scheduled cleanup |
| `content/04-testing.xml` | xUnit unit tests with Mock<T>, WebApplicationFactory integration tests, Program partial class |
| `content/05-antipatterns.xml` | async void, god-class DI, Singleton capturing DbContext, missing Program partial, secrets in appsettings |

## Templates

| File | Purpose |
|------|---------|
| `templates/program-cs.cs` | Program.cs skeleton with DI registration, EF Core, AutoMapper, FluentValidation |
| `templates/entity-config.cs` | IEntityTypeConfiguration with table, indexes, FK cascade, many-to-many |
