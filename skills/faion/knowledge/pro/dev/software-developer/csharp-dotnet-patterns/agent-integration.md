# Agent Integration — C# .NET Patterns

## When to use
- Greenfield ASP.NET Core service where Clean Architecture (Api/Application/Domain/Infrastructure) is mandated by the org and you need scaffolding fast.
- Brownfield migration from legacy .NET Framework / classic Web API to .NET 8/9 minimal APIs + MediatR.
- Cross-cutting addition of MediatR pipelines (validation, logging, transactions, caching) to an existing ASP.NET Core codebase.
- Enforcing DTO boundaries when a codebase has been leaking EF Core entities through controllers — agent can sweep and convert.
- Generating EF Core `IEntityTypeConfiguration<T>` from an existing domain model when teams have been using data annotations and want fluent config.
- Refactoring "anemic" services into rich aggregates with private setters, factory methods (`User.Create`), and domain events.

## When NOT to use
- Console apps, single-file utilities, Azure Functions with one HTTP trigger — Clean Architecture's four-project split is overkill; keep it in one project.
- Razor Pages / MVC monoliths where the team has no MediatR experience — adding the bus + behaviors creates a parallel architecture nobody owns.
- Game / Unity C# work — DI container, MediatR, EF Core are wrong tools; prefer ECS patterns.
- Lambda / serverless functions with cold-start budgets <300ms — MediatR + AutoMapper add startup overhead that breaks SLOs.
- Teams without DDD literacy — the rich-domain-model rules degrade into "private setters with no behavior", which is anemic with extra ceremony.

## Where it fails / limitations
- **MediatR became commercial.** v12+ requires a paid license for organizations with >$1M revenue (announced 2024). Plan migration to `Mediator` (source-gen) or hand-rolled mediator before adoption in commercial product.
- **AutoMapper too became commercial.** Same vendor, same license model. The README's `ProjectTo<UserDto>` examples assume AutoMapper — agents must be told to prefer Mapperly (source-gen, free) or manual mapping.
- **`SaveChangesAsync` dispatching domain events is racy.** Events fire after commit in the README sample but inside the same `SaveChangesAsync` — handlers cannot transactionally enlist. Use Outbox pattern for at-least-once delivery; the README does not show this.
- **Owned types (`OwnsOne` for value objects) leak into queries.** EF Core 8 partially fixed this; EF Core 6/7 generates 2x JOINs and breaks `AsNoTracking` projections. Verify generated SQL.
- **Controller bloat returns.** Teams move logic out of controllers into commands but keep DTO mapping, auth, header parsing inline — controllers grow back. Enforce a controller-line-count budget.
- **Pipeline ordering is invisible.** `IPipelineBehavior<,>` order depends on DI registration order; mis-registration silently disables validation. Static composition root + tests for ordering required.
- **Minimal API + MediatR** loses OpenAPI metadata that controllers get for free; teams discover this when they integrate with Swagger UI / NSwag.

## Agentic workflow
Drive .NET pattern application as a four-pass pipeline: (1) a structure agent verifies the four-project split exists, creates missing projects, and wires `DependencyInjection.cs` per layer; (2) a feature-slice agent generates `Command`/`CommandHandler`/`Validator`/`Query`/`QueryHandler`/`DTO`/`Controller` for one vertical (e.g., Users); (3) an EF agent emits `IEntityTypeConfiguration<T>` + migration; (4) an anti-pattern review agent runs the README's anti-patterns checklist (entity returned from controller, public setters on aggregates, business logic in services). Persist the per-feature inventory in `.aidocs/product_docs/dotnet-features.md`. Use `faion-sdd-executor-agent` to drive each vertical slice as one SDD task.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because Clean Architecture decisions (where does X live?) are non-trivial and easy to get wrong.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing `appsettings.*.json` and EF Core seed data; .NET configs leak connection strings, JWT keys, Azure resource IDs constantly.
- A purpose-built **dotnet-clean-arch-lint agent** (worth adding under `agents/`): grep-based linter for the four canonical anti-patterns (controller method returns `Task<User>` instead of `Task<UserDto>`, aggregate with `public set;`, domain project referencing `Microsoft.EntityFrameworkCore`, application project referencing `Microsoft.AspNetCore`).
- For EF Core changes specifically, pair with sibling `pro/dev/software-developer/csharp-entity-framework/` and gate migration generation behind human review.
- Code-review agent reading `dotnet build /warnaserror` output — .NET nullable reference type warnings are signal-rich and agents miss them.

### Prompt pattern
Vertical-slice generation:
```
You are a .NET architect implementing one feature slice in a Clean
Architecture solution (Api/Application/Domain/Infrastructure). Given
the entity <Entity> with fields <fields>, generate exactly these files:
Domain/Entities/<Entity>.cs (rich model, private setters, factory
method, domain events), Application/<Entity>s/Commands/Create<Entity>/*
(Command record, Validator, Handler), Application/<Entity>s/Queries/
Get<Entity>s/* (Query record, Handler, Dto with AutoMapper Profile),
Api/Controllers/<Entity>sController.cs. Use IRequest from MediatR. No
public setters on the entity. Handler returns Guid for Create, Dto for
Get. No EF Core types in Domain or Application.
```

Anti-pattern review:
```
You are reviewing a PR in a .NET Clean Architecture solution. Flag any
of: (1) controller method whose return type is a Domain entity instead
of a Dto; (2) aggregate / entity with `public * set;` other than `Id`;
(3) project file under Domain/ referencing Microsoft.EntityFrameworkCore
or Microsoft.AspNetCore; (4) `services.AddScoped<UserService>` with
business logic that should live on the aggregate; (5) Validator missing
for a Command. Cite file:line. Do not propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet` SDK | Project create, build, test, EF migrations | https://dotnet.microsoft.com/download |
| `dotnet ef` | EF Core migrations, scaffolding, database update | `dotnet tool install --global dotnet-ef` |
| `dotnet new clean-architecture` | Jason Taylor's Clean Architecture template | `dotnet new install Clean.Architecture.Solution.Template` ; https://github.com/jasontaylordev/CleanArchitecture |
| `dotnet new ardalis-cleanarchitecture` | Ardalis variant (different layer naming) | https://github.com/ardalis/CleanArchitecture |
| `dotnet format` | Code style enforcement; pair with `.editorconfig` | built into SDK |
| `dotnet test` + `coverlet.collector` | Test + coverage collection | https://github.com/coverlet-coverage/coverlet |
| `dotnet outdated` | Find stale NuGet refs (MediatR, EF Core) | `dotnet tool install --global dotnet-outdated-tool` |
| `Microsoft.OpenApi.OData` / `Swashbuckle` | OpenAPI generation | https://github.com/domaindrivendev/Swashbuckle.AspNetCore |
| `Aspire` (`dotnet aspire`) | Cloud-native composition for Clean-Arch services | https://learn.microsoft.com/dotnet/aspire |
| `dotnet-counters` / `dotnet-trace` | Runtime perf profiling | https://learn.microsoft.com/dotnet/core/diagnostics |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MediatR (now commercial >$1M revenue) | OSS / commercial | yes | Reference command/query mediator. Verify license for org. |
| Mediator (source-gen) | OSS (MIT) | yes | Free MediatR alternative; compile-time handler resolution. https://github.com/martinothamar/Mediator |
| Mapperly | OSS (Apache-2.0) | yes | Source-gen mapper, free AutoMapper alternative. https://mapperly.riok.app |
| FluentValidation | OSS | yes | Validator chain integrates as MediatR pipeline behavior. https://docs.fluentvalidation.net |
| Serilog + Seq | OSS / SaaS | yes | Structured logging; Seq is the agent-readable sink for local dev. https://serilog.net |
| OpenTelemetry .NET | OSS | yes | Replaces Application Insights SDK in OTel-first orgs. https://opentelemetry.io/docs/languages/net |
| Azure App Service / Container Apps | SaaS | yes | Default deploy target; `az` CLI fully scriptable. |
| AWS Lambda + API Gateway | SaaS | partially | Cold start tax for full Clean Architecture; prefer Container image deploy. |
| Refit / Flurl | OSS | yes | Typed HTTP clients; inject as `IXService` instead of `HttpClient`. |
| MassTransit / Wolverine | OSS | yes | Bus + saga + outbox layer for cross-aggregate work. https://wolverinefx.net |
| EF Core + Postgres / SQL Server | OSS / commercial | yes | Default Infrastructure persistence; agents must NOT add DbContext outside Infrastructure layer. |
| xUnit + FluentAssertions + Testcontainers | OSS | yes | Standard test stack; Testcontainers spins real DB for handler tests. |
| BenchmarkDotNet | OSS | yes | Required for any "this handler is fast" claim. |

## Templates & scripts

The methodology already ships layer/handler/controller code in `README.md` and templates in `templates.md`. The gap is automated lint of the four canonical anti-patterns. Inline drop-in (≤50 lines) — `scripts/dotnet-cleanarch-lint.sh`:

```bash
#!/usr/bin/env bash
# dotnet-cleanarch-lint.sh — flag Clean Architecture anti-patterns.
# Usage: dotnet-cleanarch-lint.sh <solution-root>
set -euo pipefail
root="${1:?usage: dotnet-cleanarch-lint.sh SOLUTION_ROOT}"
fail=0
echo "# .NET Clean Arch lint ($root)"
echo "## Controllers returning Domain entities"
grep -rEn 'public async Task<(User|Order|Product|Organization|Post)>' "$root/src" --include='*Controller.cs' \
  | tee /tmp/da.ctrl-ent || true
[[ -s /tmp/da.ctrl-ent ]] && fail=1
echo "## Aggregates with public setters (other than Id)"
grep -rEn 'public (string|int|Guid|DateTime|decimal|bool) \w+ \{ get; set; \}' "$root/src/*.Domain" --include='*.cs' \
  | grep -v 'Id { get;' | tee /tmp/da.pub-set || true
[[ -s /tmp/da.pub-set ]] && fail=1
echo "## Domain project referencing EF Core or AspNetCore"
grep -rEn 'Microsoft\.(EntityFrameworkCore|AspNetCore)' "$root/src/*.Domain" --include='*.csproj' \
  | tee /tmp/da.dom-leak || true
[[ -s /tmp/da.dom-leak ]] && fail=1
echo "## Application project referencing AspNetCore"
grep -rEn 'Microsoft\.AspNetCore' "$root/src/*.Application" --include='*.csproj' \
  | tee /tmp/da.app-leak || true
[[ -s /tmp/da.app-leak ]] && fail=1
echo "## Commands missing FluentValidation Validator"
for f in $(find "$root/src" -name '*Command.cs'); do
  base="${f%Command.cs}"
  [[ -f "${base}CommandValidator.cs" ]] || echo "missing validator: $f"
done | tee /tmp/da.no-val || true
[[ -s /tmp/da.no-val ]] && fail=1
exit "$fail"
```

Wire into `dotnet build` via a `BeforeTargets="Build"` MSBuild target or a `pre-commit` hook. Pair with `dotnet format --verify-no-changes` to also catch style drift.

## Best practices
- **Composition root in `Program.cs` only.** Per-layer `DependencyInjection.cs` extension methods (`AddApplication`, `AddInfrastructure`) keep `Program.cs` short and make agent-driven service registration deterministic.
- **`IRequest<TResponse>` is your contract.** Reading any handler signature tells the agent the full input/output schema; banned: handlers that read `HttpContext` or `IHttpContextAccessor`.
- **Domain events live on the aggregate, not in services.** `user.AddDomainEvent(new UserCreatedEvent(...))` inside the factory method. Dispatched in `SaveChangesAsync` override, but use Outbox table for at-least-once semantics.
- **EF Core in Infrastructure only.** `IApplicationDbContext` interface in Application, concrete `ApplicationDbContext` in Infrastructure. Agents constantly try to inject `DbContext` directly into handlers — reject in review.
- **`Result<T>` over exceptions for expected failures.** `DomainException` is fine for invariant violations; for "user not found" return `Result.NotFound()` (use FluentResults / ErrorOr). Reduces try/catch cargo-cult in handlers.
- **Pipeline behaviors registered in known order:** Logging → Validation → Authorization → UnitOfWork → Caching → Handler. Wrong order = silent bugs (validator after handler). Test the ordering, don't trust DI.
- **One DTO per query, no shared DTOs.** "GetUsersListItemDto" and "GetUserDetailDto" are two types, even if 80% overlap. Sharing causes over-projection and "I added a field and broke 5 endpoints".
- **`AsNoTracking()` by default in queries.** README does this — keep it. Tracking on read paths is the #1 EF Core perf pitfall.
- **Never expose `IQueryable<T>` from Application.** Agents will return it for "flexibility" — don't. Apply paging + projection inside the handler; return materialized DTOs.
- **Source-gen everything you can.** Mapperly for mapping, Mediator (not MediatR) for the bus, `System.Text.Json` source-gen for serialization. Cuts cold-start, makes generated code visible to grep + agents.

## AI-agent gotchas
- **MediatR / AutoMapper hallucinations.** Agents emit code against APIs from MediatR v9, AutoMapper v10. Pin versions in the prompt and reject `IRequestPostProcessor` etc. that don't exist in target version. Better: tell the agent which library (MediatR vs Mediator vs Wolverine) — they have incompatible APIs.
- **Anemic-domain regression.** Asked to "add a Promote action", agents produce `UserService.Promote(user)` not `user.Promote()`. Constrain with structured output: `where_does_this_live: aggregate|service|handler` and reject `service` for state-transition logic.
- **Public setters returning.** Code-gen agents emit `public string Name { get; set; }` because that's the ASP.NET Core training-data norm. Force `private set;` + factory method via prompt example; lint catches the rest.
- **Controllers with business logic.** Agents inline auth checks, mapping, and side calls into controller actions when the user says "add endpoint X". Always require: action signature → mediator.Send → return — and nothing else.
- **EF Core entity leaks.** Agents return entities directly to skip the DTO step ("simpler"). Always pair the controller change with a Dto + AutoMapper Profile + Query handler; reject PRs that don't.
- **Domain events without dispatch.** Agents call `AddDomainEvent` in the aggregate but forget to override `SaveChangesAsync` to publish. Or override it but don't clear events post-publish, causing re-fires on the next save. Both are common.
- **Migrations auto-created without review.** `dotnet ef migrations add` produces destructive changes (column drops) silently. Hard human-in-the-loop checkpoint — never let an agent run `database update` against any non-throwaway DB.
- **Pipeline behaviors ordered by accident.** Agents register behaviors in the order they see them in the file. Force explicit order in `AddApplication()` and a comment justifying it.
- **`async void` event handlers.** Agents borrow JS-style `async (e) => ...` for `INotificationHandler<T>` and lose exceptions. Force `Task` returns, force `try/catch` + log, and add a Polly retry for handler bodies that talk to external services.
- **Test fakes overstub the bus.** Agents mock `IMediator.Send(...)` and assert call count, missing handler-resolution and pipeline-behavior bugs. Require at least one integration test per feature using `WebApplicationFactory<Program>` + Testcontainers DB.

## References
- Microsoft Architecture Guides — Common web application architectures (Clean Architecture). https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures
- Jason Taylor — Clean Architecture Solution Template. https://github.com/jasontaylordev/CleanArchitecture
- Steve "Ardalis" Smith — Clean Architecture template + book. https://github.com/ardalis/CleanArchitecture
- MediatR. https://github.com/jbogard/MediatR (license change notice 2024)
- Mediator (source-gen). https://github.com/martinothamar/Mediator
- Mapperly. https://mapperly.riok.app
- FluentValidation. https://docs.fluentvalidation.net
- EF Core docs — Modeling, owned types. https://learn.microsoft.com/ef/core
- Vernon, V. "Implementing Domain-Driven Design," ch. 5–10 (rich aggregates, value objects).
- Sibling methodologies: `pro/dev/software-developer/csharp-aspnet-core/`, `csharp-entity-framework/`, `csharp-background-services/`, `cqrs-pattern/`, `clean-architecture/`, `domain-driven-design/`.
