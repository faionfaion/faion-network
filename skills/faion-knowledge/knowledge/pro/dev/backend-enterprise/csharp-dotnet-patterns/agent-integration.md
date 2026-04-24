# Agent Integration — C# .NET Patterns (Clean Architecture + CQRS)

## When to use
- Building a new .NET 8/9 service with non-trivial domain (≥3 aggregate roots, multiple bounded contexts, business rules beyond CRUD).
- Migrating a transactional-script .NET app to a domain-rich model where invariants must be enforced at the entity level.
- Multi-team enterprise codebase where Application/Domain/Infrastructure separation enables parallel work without merge conflicts.
- Microservices with event-driven integration — domain events + MediatR Notification pattern enables clean cross-aggregate hand-offs.
- Apps targeting native AOT / containerized deploys where layering helps trim Infrastructure dependencies from the API layer.

## When NOT to use
- Simple CRUD apps (<20 endpoints, no business rules) — Clean Architecture's four projects are pure overhead.
- Lambda/Functions with cold-start budget — DI graph and MediatR pipeline add 100-300ms startup; use minimal API + direct `DbContext`.
- Codebases on `Newtonsoft.Json` + AutoMapper that haven't moved to System.Text.Json + source generators — pattern compounds the migration debt.
- Teams unfamiliar with DDD — pattern's value depends on rich domain models; without that, you have a layered anemic codebase.
- Pure read-side services (reporting, dashboards) — CQRS is overkill; one project with `SELECT` queries is fine.

## Where it fails / limitations
- **Anemic domain anyway.** Teams adopt the layout but keep behavior in handlers; entities stay property bags. Pattern's value evaporates.
- **MediatR over-use.** Every method becomes a Command/Query; trivial reads pay for handler resolution + pipeline behaviors.
- **CQRS without separate read model.** Pattern hints at separation but most teams query the write DB through projections — read paths still hit aggregate repositories.
- **Domain events firing at SaveChanges.** Exceptions inside handlers roll back the transaction; agents expect "fire-and-forget" and break atomicity.
- **AutoMapper magic.** `ProjectTo<T>` + complex mappings produce runtime-only errors; agents unable to debug map registration issues.
- **Validation duplication.** FluentValidation rules on Commands repeat DataAnnotations on entities and DTOs; agents update one, not all three.
- **Source generation incompatibility.** Reflection-heavy MediatR + AutoMapper fight native AOT; pattern needs Mapster + manual handler dispatch for AOT.
- **Layer violations invisible.** Without ArchUnit-style tests, agents reference Infrastructure types from Application within months.

## Agentic workflow
Drive Clean Architecture work as: (1) a planner subagent reads `Domain/Entities/` + existing aggregates and emits the target Command/Query list (name, request DTO, response DTO, validator, handler, integration events); (2) a code-writer subagent generates Domain entity changes + Application Command/Query/Handler/Validator + Infrastructure Configuration + xUnit tests in one pass per feature folder; (3) an architecture-test subagent runs NetArchTest to verify Domain has zero references to Application/Infrastructure/Api; (4) a build-and-test subagent runs `dotnet build -warnaserror` + `dotnet test`. Keep each Command/Query in its own folder (`Application/Users/Commands/CreateUser/`) so agents read one folder per task.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — implementer for entities, value objects, handlers.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task per Command/Query; quality gate runs `dotnet test` + NetArchTest + Roslynator.
- A purpose-built **arch-fitness-agent** (worth creating): runs NetArchTest assertions ("Domain shall not depend on EFCore") on every PR; outputs failing rule + fix proposal.
- A **domain-event-audit-agent** (worth creating): scans `SaveChangesAsync` overrides and asserts every domain event has a handler; flags orphan events.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub `appsettings.Development.json`, secrets, and seed data before commit.

### Prompt pattern
Add a Command:
```
You are a .NET 8 architect using Clean Architecture +
MediatR/CQRS pattern from csharp-dotnet-patterns/README.md. Add a
"Promote user to admin" use case. Output:
- Domain: User.Promote() with invariant + UserPromotedEvent
- Application/Users/Commands/PromoteUser/: Command, Validator,
  Handler
- Domain event handler in Application/Users/EventHandlers/
- xUnit test covering: success, already-admin, deactivated user
- API controller action mapped to PUT /users/{id}/promote
Run: dotnet build -warnaserror && dotnet test --filter "Promote".
```

Architecture fitness pass:
```
Run NetArchTest with rules:
1. Domain shall not depend on Application, Infrastructure, Api,
   EntityFrameworkCore, AutoMapper, MediatR.
2. Application shall not depend on Infrastructure, EFCore.
3. Api shall not depend on Infrastructure (composition root only).
4. Every IRequestHandler must be in Application namespace.
Output: failing rule, project, type, fix proposal.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet new ca-sln` (template) | Scaffold Clean Architecture sln | `dotnet new install Clean.Architecture.Solution.Template` |
| `dotnet ef migrations` | EF Core migrations | `dotnet tool install -g dotnet-ef` |
| `dotnet test --collect:"XPlat Code Coverage"` | Coverage with coverlet | bundled |
| Roslynator CLI | Analyzers + automated fixes | `dotnet tool install -g Roslynator.DotNet.Cli` |
| NetArchTest / ArchUnitNET | Architecture fitness functions | `dotnet add package NetArchTest.Rules` |
| `dotnet format` | Roslyn formatter (pre-commit) | bundled |
| `dotnet outdated` | Stale NuGet deps | `dotnet tool install -g dotnet-outdated-tool` |
| Mapster CLI | AOT-compatible mapping (alternative to AutoMapper) | `dotnet tool install -g Mapster.Tool` |
| `Verify` | Snapshot testing for handler outputs | `dotnet add package Verify.Xunit` |
| `gh` CLI | PR + CI orchestration | https://cli.github.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| MediatR (v12+) | OSS, paid for commercial | yes | License changed; budget for it or fork pre-v12 OSS. |
| FluentValidation | OSS | yes | Pairs with MediatR pipeline behavior; agents handle DSL well. |
| AutoMapper | OSS, paid for commercial (v13+) | yes | Same license shift as MediatR; consider Mapster. |
| Mapster | OSS | yes | Source-generated mapping; AOT-friendly. |
| MassTransit | OSS | yes | Outbox pattern + integration events; pairs with domain events. |
| Marten | OSS | yes | Document DB on Postgres + event sourcing — replaces this pattern's persistence layer. |
| Wolverine | OSS | yes | MediatR alternative with built-in messaging; reduces ceremony. |
| Azure App Service / AWS ECS | SaaS | API yes | Composition root in Api project deploys cleanly. |
| Application Insights / Honeycomb | SaaS APM | API yes | Trace propagation via OpenTelemetry across handlers. |
| Sentry | SaaS errors | API yes | Tag releases by migration version. |

## Templates & scripts
See `templates.md` for entity, value object, handler skeletons. Add an architecture fitness test (≤50 lines):

```csharp
// tests/MyApp.ArchitectureTests/LayerTests.cs
using NetArchTest.Rules;
using Xunit;
public class LayerTests
{
    private const string Domain = "MyApp.Domain";
    private const string Application = "MyApp.Application";
    private const string Infrastructure = "MyApp.Infrastructure";
    private const string Api = "MyApp.Api";

    [Fact] public void Domain_does_not_reference_outer_layers() =>
        Assert.True(Types.InAssembly(typeof(MyApp.Domain.Entities.User).Assembly)
            .Should().NotHaveDependencyOnAny(Application, Infrastructure, Api,
                "Microsoft.EntityFrameworkCore", "MediatR", "AutoMapper")
            .GetResult().IsSuccessful);

    [Fact] public void Application_does_not_reference_infrastructure() =>
        Assert.True(Types.InAssembly(typeof(MyApp.Application.DependencyInjection).Assembly)
            .Should().NotHaveDependencyOn(Infrastructure)
            .GetResult().IsSuccessful);

    [Fact] public void Handlers_live_in_Application() =>
        Assert.True(Types.InCurrentDomain()
            .That().ImplementInterface(typeof(MediatR.IRequestHandler<,>))
            .Should().ResideInNamespace(Application)
            .GetResult().IsSuccessful);

    [Fact] public void Entities_have_private_setters() =>
        Assert.True(Types.InAssembly(typeof(MyApp.Domain.Entities.User).Assembly)
            .That().Inherit(typeof(MyApp.Domain.Entities.BaseEntity))
            .Should().BeSealed().Or().BeAbstract()
            .GetResult().IsSuccessful);
}
```

Run as part of every CI build; failures block merge.

## Best practices
- **Constructors private, factories static.** `User.Create(...)` returns a constructed aggregate; new-ing entities outside is banned by analyzer.
- **Value objects for every primitive concept** (`Email`, `Money`, `Slug`). Stops "stringly-typed" agent bugs.
- **Domain events raised inside aggregate methods, dispatched at `SaveChangesAsync`.** Side-effects via NotificationHandlers, not inline.
- **No `ToList`/`ToArray` in handlers without pagination.** Always paged + `AsNoTracking` for read.
- **MediatR pipeline behaviors for cross-cutting concerns** (validation, logging, transaction, caching, auth). Don't repeat per-handler.
- **CancellationToken on every async signature.** Plumb from controller → handler → repository. Roslynator + analyzer enforced.
- **`required` keyword + `init` for DTOs** (.NET 7+). Surfaces missing fields at compile time.
- **Migrations checked into Infrastructure project, only.** Api project never references EF — composition root only.
- **One Command/Query per folder.** `Users/Commands/CreateUser/{Command,Validator,Handler,Result}.cs`. Agents read one folder; no scrolling.
- **Architecture tests run in `dotnet test`.** Same gate as unit tests; don't relegate to a separate stage that gets skipped.
- **Source-generated MediatR + Mapster for AOT.** Skip if not AOT-targeting.

## AI-agent gotchas
- **Anemic regression.** Agent adds new behavior to `UserService` (Application) instead of `User` entity (Domain). Force prompts to read `Domain/Entities/<Aggregate>.cs` first; require behavior changes there.
- **Layer leakage.** Agent imports `Microsoft.EntityFrameworkCore` into Application for "convenience". NetArchTest catches; without it, agents drift over time.
- **Domain events vs Integration events confusion.** Agents fire a domain event for cross-service notification; these don't cross process boundaries. Document which is which in `Domain/Events/` vs `Application/IntegrationEvents/`.
- **`DbContext.SaveChangesAsync` ordering.** Domain event handlers running inside the same transaction can deadlock or roll back unexpectedly. Use outbox pattern (MassTransit) for anything crossing aggregates.
- **Validator duplication.** Agent adds `RuleFor(x => x.Email).EmailAddress()` in three places (entity, validator, DTO annotation). Standardize: validators on Commands, invariants in entity factories, no annotations.
- **AutoMapper runtime errors.** Agent adds a property without mapping; tests pass, prod 500s. Add `MapperConfiguration.AssertConfigurationIsValid()` as a unit test.
- **Handler returning `Task`.** Agent forgets `Task<TResponse>`; compile error or wrong return shape. Roslynator rule MA0042 catches.
- **`async void` in event handlers.** Agent uses `async void Handle(...)` for "fire-and-forget"; one exception kills the host. INotificationHandler<T> must return Task.
- **MediatR over-use for trivial paths.** Agent wraps `GET /health` in a Query/Handler. Reserve MediatR for use cases with cross-cutting needs.
- **Entity collection mutation outside aggregate.** Agent does `user.Posts.Add(post)` from a handler. Add via `user.AddPost(post)` — encapsulate.
- **Soft-delete + global query filter forgotten on a query.** Agent uses `IgnoreQueryFilters()` to "see all rows" and ships it; multi-tenant leak. Lint forbids `IgnoreQueryFilters` outside admin tools.
- **Migration generated by agent but not applied to seed/integration tests.** PR builds fail intermittently; agents blame flaky tests. Force `dotnet ef database update` on test container startup.
- **MediatR/AutoMapper license accepted by accident.** Agent adds via `dotnet add package`; commercial license trip wires fire later. Pin SPDX checks in CI.

## References
- Microsoft Learn — Clean Architecture for .NET. https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures
- Steve Smith / Ardalis — Clean Architecture template. https://github.com/ardalis/CleanArchitecture
- Jason Taylor — Clean Architecture template (referenced by README). https://github.com/jasontaylordev/CleanArchitecture
- Vladimir Khorikov — "Domain-Driven Design Fundamentals." https://enterprisecraftsmanship.com
- David Fowler — "ASP.NET Core Diagnostic Scenarios." https://github.com/davidfowl/AspNetCoreDiagnosticScenarios
- Eric Evans — "Domain-Driven Design" book; companion to this pattern.
- NetArchTest README. https://github.com/BenMorris/NetArchTest
- Wolverine — MediatR alternative. https://wolverine.netlify.app
- MediatR licensing change announcement. https://www.jimmybogard.com/automapper-and-mediatr-becoming-commercial-products/
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/csharp-dotnet/`, `pro/dev/backend-enterprise/csharp-aspnet-core/`, `pro/dev/backend-enterprise/csharp-entity-framework/`, `pro/dev/backend-enterprise/csharp-xunit-testing/`.
