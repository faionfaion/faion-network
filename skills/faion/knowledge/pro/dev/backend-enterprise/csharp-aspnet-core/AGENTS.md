# ASP.NET Core Patterns

## Summary

Layered architecture for ASP.NET Core 8/9 APIs: `[ApiController]` → `IXService` → `IXRepository` → EF Core. Covers controller/service interface split, AutoMapper DTO projection, `CancellationToken` on every async signature, `AsNoTracking` for reads, and `ProblemDetails` (RFC 7807) error responses. Feature-folder organization (`Features/Users/`) is recommended over technical-layer folders.

## Why

Without explicit DI-based service interfaces, agents couple controllers directly to `DbContext` and lose testability. Missing `CancellationToken` plumbing causes thread-pool starvation under load in ASP.NET Core. AutoMapper runtime errors (unmapped properties) appear only at request time, not at compile time, unless `AssertConfigurationIsValid()` is added to a unit test.

## When To Use

- New ASP.NET Core 8/9 API with clear controller/service/repository separation.
- Migrating legacy ASP.NET MVC or WCF services to modern Web API.
- Multi-tenant or B2B SaaS in .NET where DI scopes and middleware are central.
- Codebase shared between humans and LLMs — explicit interfaces stabilize completions.
- Stepping stone before adopting CQRS/MediatR later.

## When NOT To Use

- Tiny internal tools or webhooks with fewer than 10 endpoints — Minimal APIs are sufficient.
- Microservices that publish only to a queue — three layers around one method call is overkill.
- gRPC-only services — service-method-per-RPC layering is more appropriate.
- Apps on .NET Framework 4.x — Generic Host, async-by-default, and DI container assumptions do not hold.

## Content

| File | What's inside |
|------|---------------|
| `content/01-controller-service.xml` | [ApiController] + IXService interface + implementation with AutoMapper, IPasswordHasher, and CancellationToken. |
| `content/02-rules-and-gotchas.xml` | Mandatory rules, async hygiene, and common AI-agent mistakes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dotnet-gate.sh` | CI gate: dotnet build -warnaserror, coverage threshold check, Roslynator analysis. |
