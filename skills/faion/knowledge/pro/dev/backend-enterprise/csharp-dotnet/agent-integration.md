# Agent Integration — C# .NET (umbrella)

## When to use
- Greenfield ASP.NET Core 8/9 service: REST/gRPC API, EF Core data layer, xUnit tests, BackgroundService for async work.
- Brownfield .NET Framework → .NET 8 migration where the agent needs a single map of patterns covering controllers, EF, tests, and hosted services.
- Internal enterprise APIs where DI, options pattern, and configuration binding are part of the contract.

## When NOT to use
- Tiny CLI utilities — `dotnet new console` is enough; agents should not impose Controller/Service/Repository on a 200-line script.
- Highly dynamic plugin systems — F# or scripting is a better fit; .NET reflection-heavy plugin loading trips up codegen.
- Functional/event-sourced cores — use F# or a CQRS framework (MediatR + Marten/EventStore) directly; this umbrella's Repository pattern fights that grain.

## Where it fails / limitations
- This file is an umbrella aggregating ASP.NET Core, EF Core, xUnit, and BackgroundService snippets from sibling methodologies (`csharp-aspnet-core`, `csharp-entity-framework`, `csharp-xunit-testing`, `csharp-background-services`). Edits should happen in those subdirs.
- Repository over `DbContext` is debatable: `DbContext` already provides `IUnitOfWork` and `IDbSet`. Add a repository only when (a) you need to mock without an in-memory provider, (b) you want to enforce eager-load policies, or (c) you have multiple data sources.
- `IServiceProvider.CreateScope()` inside `BackgroundService` is required; agents often inject scoped services directly into singleton-lifetime hosted services and break startup.
- AutoMapper is not free at scale. For hot paths, use `Mapperly` (source generator) or hand-write mappings.

## Agentic workflow
A coding subagent should plan top-down: minimal API or controller → DTOs (request/response) → service interface + impl → EF entity + configuration → repository (only if justified) → migration → tests. Use `dotnet new`, `dotnet ef migrations add`, `dotnet test` between steps. Pause for human review before: running `ef database update` on shared DBs, adding NuGet packages, changing `Program.cs` middleware order.

### Recommended subagents
- `general-purpose` Claude subagent — scaffolding and DI registration.
- Code-review subagent (Sonnet) — checks DI lifetimes, async/await correctness (no `.Result`/`.Wait()`), nullable-reference compliance.

### Prompt pattern
```
Add resource <Name>: entity + EF Core configuration with explicit table/column names + indexes, DbSet<Name>, migration, repository interface + impl with paged Get, AddAsync, Remove, SaveChangesAsync, service with mapping, controller with 5 REST endpoints, DTOs (CreateXDto, UpdateXDto, XDto), AutoMapper profile, xUnit unit tests for service (Moq), integration tests via WebApplicationFactory + Testcontainers Postgres. Register all DI in Program.cs. Run dotnet build, dotnet test, dotnet ef migrations add Add<Name>.
```
```
Add BackgroundService <Worker>: reads from Channel<T>, processes via scoped IServiceProvider, logs with ILogger<Worker>, honors stoppingToken, max 1 concurrent task. Register Channel<T> and Worker in Program.cs. Add unit test using TestServer + IHostedService.StartAsync.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet new {webapi,classlib,xunit}` | Project scaffolding | bundled |
| `dotnet ef migrations add` / `database update` | Schema migrations | `dotnet tool install -g dotnet-ef` |
| `dotnet test --logger "trx;LogFileName=results.trx"` | Run tests + emit results | bundled |
| `dotnet format` | Style + analyzer fixes | bundled |
| `dotnet outdated` | NuGet package staleness | `dotnet tool install -g dotnet-outdated-tool` |
| `dotnet user-secrets` | Local secret store | bundled |
| `dotnet watch run` | Hot reload | bundled |
| `dotnet trace` / `dotnet-counters` / `dotnet-dump` | Live diagnostics | https://learn.microsoft.com/dotnet/core/diagnostics |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Azure App Service / Container Apps | SaaS | Yes | First-class .NET deploy |
| AWS App Runner / Elastic Beanstalk | SaaS | Yes | Container-based |
| Aspire (.NET Aspire) | OSS | Yes | Local orchestration of multi-service .NET apps; agents can use it for repro |
| Testcontainers .NET | OSS | Yes | Spin up real Postgres/Redis/RabbitMQ in tests |
| Application Insights / OpenTelemetry .NET | SaaS/OSS | Yes | Auto-instrument controllers, EF, HttpClient |
| Hangfire / Quartz.NET | OSS | Yes | Use when `BackgroundService` lacks scheduling/retry/dashboard |

## Templates & scripts
Templates live in sibling methodologies (`csharp-aspnet-core/templates.md`, `csharp-entity-framework/templates.md`, `csharp-xunit-testing/templates.md`, `csharp-background-services/templates.md`). Inline `Directory.Build.props` snippet the agent should drop at the solution root for consistent settings:

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>
</Project>
```

## Best practices
- All public methods that touch IO must be async and accept `CancellationToken`. Agents drop the token frequently — review must enforce.
- Register `DbContext` as `Scoped`, `IHttpClientFactory`-backed clients as `Transient`, hosted services as `Singleton` and resolve scoped deps via `IServiceProvider.CreateScope()`.
- Use `IOptions<T>` pattern for configuration; never read `IConfiguration` deep in services.
- For EF Core: `AsNoTracking()` on read paths, `AsSplitQuery()` when projecting collections, `ExecuteUpdateAsync`/`ExecuteDeleteAsync` for bulk ops.
- xUnit: one assertion concern per test; use `IClassFixture` for shared, `ICollectionFixture` for cross-class shared (sparingly).
- Use `record` for DTOs (immutable, value equality); `class` for entities (EF needs setters).
- Centralize `DateTime.UtcNow` behind `TimeProvider` (.NET 8) so tests can fake clock.

## AI-agent gotchas
- LLMs default to `async void` for event handlers — silent crashes. Force `async Task`.
- `.Result` / `.Wait()` deadlock under sync context; agent code reviewing must reject any sync-over-async.
- AutoMapper profiles are routinely mis-registered (`AddAutoMapper` missing assembly). Verify boot.
- LLM-generated EF queries often miss `await` on `IQueryable.ToListAsync()` — caught by analyzers; ensure `<TreatWarningsAsErrors>true`.
- BackgroundService captures of scoped DI: agent injects `DbContext` directly into singleton; throws on first call. Mandate `IServiceScopeFactory` pattern.
- Migrations against shared dev/prod DB are destructive — human checkpoint before `dotnet ef database update`.
- Source-generated mappers (Mapperly) require `partial class` — agent often forgets the partial keyword.

## References
- https://learn.microsoft.com/aspnet/core
- https://learn.microsoft.com/ef/core
- https://xunit.net/docs/getting-started/v3
- https://learn.microsoft.com/dotnet/core/extensions/workers
- https://github.com/dotnet/aspire
- Sub-methodologies: `csharp-aspnet-core/`, `csharp-entity-framework/`, `csharp-xunit-testing/`, `csharp-background-services/`, `csharp-dotnet-patterns/`
