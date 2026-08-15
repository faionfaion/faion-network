# Agent Integration — C# .NET Backend

## When to use
- Enterprise / B2B backends where Microsoft stack (Azure, AD, SQL Server) is already in place.
- High-throughput APIs needing AOT-friendly perf, async/await, and minimal-allocation hot paths.
- Long-running services (worker / hosted services) and gRPC microservices.
- Domain-rich applications where strong static typing + records + nullable refs prevent whole bug classes.
- Teams comfortable with Visual Studio / Rider tooling and willing to invest in `dotnet` CLI in CI.

## When NOT to use
- Tiny scripts, glue code, one-off cron jobs — Python/Node ship in fewer lines.
- Frontend BFFs in TypeScript-first orgs (the type-sharing story is weaker than tRPC/Hono).
- When deploy targets exclude Linux/x64 — historically still common but mostly resolved on .NET 8+.
- Greenfield startups where hire-ability of senior C# devs is a constraint.
- Edge runtimes with hard cold-start budgets (<50ms) — Node/Bun/Workers win until AOT is fully adopted.

## Where it fails / limitations
- DI container in ASP.NET Core silently treats missing registrations as runtime errors — `AddScoped<I, X>()` typos surface only at first request.
- `async void` (outside event handlers) swallows exceptions; agents copy-paste it from old samples.
- EF Core's tracking + lazy-loading-proxies combination produces N+1 worse than ORMs that disable lazy by default; always force `AsNoTracking()` for queries.
- Configuration binding from `appsettings.json` is loose — typos in section names result in default-valued objects, not exceptions.
- `Task.Run` inside ASP.NET Core handlers steals from the request thread pool and degrades throughput. It's rarely the right tool.

## Agentic workflow
A subagent should drive a full vertical: minimal/controller endpoint → DTO + validator (FluentValidation) → service interface + impl → EF entity + configuration + migration → xUnit feature test using `WebApplicationFactory<Program>`. Quality gates: `dotnet build -warnaserror`, `dotnet test`, `dotnet format --verify-no-changes`. For complex domains, brainstorm a record/aggregate model first, then have the agent generate code.

### Recommended subagents
- `/faion` (sdd-batch-orchestrator workflow) — slice-by-slice; works well with the controller/service/repo split.
- `faion-sdd-executor-agent` — runs `dotnet test`, format, and analyzers as gates.

### Prompt pattern
```
Add endpoint <METHOD /path> for <feature>. Generate: DTO + FluentValidation rule, service interface in /Services, impl with constructor DI, EF entity + Configuration + migration named <Verb><Noun>, controller action returning ActionResult<T>, xUnit test using WebApplicationFactory + in-memory SQLite. Run dotnet test + dotnet format and report.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet new` / `add` / `restore` / `build` / `run` / `test` / `publish` | Core SDK | https://learn.microsoft.com/dotnet |
| `dotnet ef` | EF Core migrations CLI | `dotnet tool install --global dotnet-ef` |
| `dotnet format` | Roslyn-based formatter + analyzer fixer | Built-in (.NET 6+) |
| `dotnet watch run` | Hot reload during dev | Built-in |
| `dotnet user-secrets` | Local-only secrets (no .env file) | Built-in |
| `dotnet publish -c Release -p:PublishAot=true` | Native AOT build | .NET 8+ |
| Roslyn analyzers (`Microsoft.CodeAnalysis.NetAnalyzers`, `Roslynator`) | Static analysis | NuGet |
| `BenchmarkDotNet` | Microbenchmarks | NuGet |
| Aspire CLI (`dotnet aspire`) | Local orchestration of microservices + deps | .NET 8+ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Azure App Service / Container Apps | SaaS | Yes | First-class .NET deploy; `az webapp deploy`. |
| .NET Aspire | OSS | Yes | Local + cloud orchestration with C# manifests. |
| Serilog + Seq | OSS / SaaS | Yes | Structured logging that pairs with `ILogger<T>`. |
| OpenTelemetry .NET | OSS | Yes | Built into ASP.NET Core; one-line wiring. |
| Hangfire / Quartz.NET | OSS | Yes | Background jobs / cron alternatives to `BackgroundService`. |
| MassTransit + RabbitMQ/Azure SB | OSS | Yes | Saga + messaging on top of message brokers. |
| Sentry, Raygun, Application Insights | SaaS | Yes | Auto-instrumentation for ASP.NET Core. |
| GitHub Actions `setup-dotnet` | OSS | Yes | CI wiring; matrix on `dotnet-version`. |

## Templates & scripts
See templates.md and README (Controller, Service, EF entity + configuration, xUnit). Inline `Program.cs` skeleton to anchor agent output:

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(o =>
    o.UseNpgsql(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddAutoMapper(typeof(Program));
builder.Services.AddFluentValidationAutoValidation();
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddOpenApi();

var app = builder.Build();
app.MapOpenApi();
app.MapControllers();
app.Run();
public partial class Program;
```

## Best practices
- Use nullable reference types project-wide (`<Nullable>enable</Nullable>`); treat `CS8` warnings as errors.
- Prefer minimal APIs for small services, controllers for >10 endpoints with cross-cutting filters.
- Constructor DI only — avoid `IServiceProvider` parameter (service locator antipattern) except inside `BackgroundService`s where scopes must be created manually.
- Configure EF Core with `AsNoTracking()` for read paths; use `AsSplitQuery()` when joining many `Include`s.
- Use `record` types for DTOs (value semantics, immutability, `with`-expressions).
- Adopt `IOptions<T>` + `[ConfigurationKeyName]` and validate on startup with `ValidateOnStart()`.
- For background work, pick `BackgroundService` + `Channel<T>` for in-process; Hangfire/MassTransit for cross-process or persistent.
- Pin `<TargetFramework>net9.0</TargetFramework>` (or current LTS) and the SDK in `global.json` so CI and local match.

## AI-agent gotchas
- Agents emit `async void` outside of event handlers — exceptions are unobserved. Reject all `async void` except known event handler signatures.
- Constructor parameter list grows unbounded ("god class" smell); the agent silently injects 8+ services. Set a soft cap of 4-5 dependencies and refactor to mediator/handler.
- EF migrations go stale fast — agents may modify the entity but not run `dotnet ef migrations add`. Pre-commit hook should fail if `Migrations/*` is out of sync with the `OnModelCreating` snapshot.
- `WebApplicationFactory<Program>` requires `public partial class Program;` at the bottom of `Program.cs`. Agents often leave it off → "Cannot find Program" test errors. Verify in scaffolding.
- DI lifetimes: agents register `Singleton` for things holding `DbContext` — captures a scoped dependency and crashes under load. Always lifecheck DbContext-touching services as `Scoped`.
- Human checkpoint: review every new `[AllowAnonymous]`, `[Authorize(Roles = "Admin")]` and CORS policy — agents err toward permissive.
- Configuration: agents drop secrets into `appsettings.json`. Force `dotnet user-secrets` locally and env vars / Key Vault in prod; pre-commit should grep for connection strings.

## References
- https://learn.microsoft.com/aspnet/core/
- https://learn.microsoft.com/ef/core/
- https://learn.microsoft.com/dotnet/core/extensions/
- https://github.com/dotnet/aspire
- https://andrewlock.net (long-form blog on ASP.NET Core internals)
