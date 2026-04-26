# Agent Integration — ASP.NET Core Patterns

## When to use
- Building a new ASP.NET Core 8/9 API where you want clear controller / service / repository boundaries before agents start writing endpoints.
- Migrating a legacy ASP.NET MVC or WCF service to modern Web API; pattern provides target architecture.
- Multi-tenant or B2B SaaS in .NET where DI scopes and middleware are central to the design.
- Codebase shared between humans and Copilot/Claude — the pattern's explicit interfaces make LLM completions stable.
- Apps that will adopt CQRS/MediatR later — the Service Layer here is a stepping stone.

## When NOT to use
- Tiny internal tools or webhooks with <10 endpoints — Minimal APIs are sufficient, this layered pattern is overkill.
- Microservices that publish only to a queue — controller plus repository plus service is three layers around one method call.
- gRPC-only services — the HTTP-action vocabulary in this pattern doesn't map; use service-method-per-RPC layering instead.
- Apps stuck on .NET Framework 4.x — pattern assumes Generic Host, async-by-default, and DI container; backporting is more work than rewriting.

## Where it fails / limitations
- **Anemic services.** Services become passthroughs to repositories, adding indirection without behavior. Agents copy the pattern and never push logic out of the controller.
- **AutoMapper sprawl.** Profiles spread across folders, ambiguous mappings, runtime-only config errors. Agents prefer manual mapping than debug an `AutoMapperConfigurationException`.
- **Repository over EF.** EF Core's `DbContext` is already a Unit-of-Work + Repository; wrapping it adds layers without value unless you have multiple data sources.
- **Async deadlocks.** Agents mix `.Result` / `.Wait()` with `async`; in legacy ASP.NET this deadlocks immediately.
- **DTO duplication.** `CreateUserDto`, `UpdateUserDto`, `UserDto`, `UserResponseDto` — agents copy fields and they drift.
- **Dependency explosion in controllers.** A `UsersController` ends up with 6 services injected; SRP violation invisible to LLMs.
- **PagedResult re-implemented per project.** Agents reinvent pagination types instead of using `Microsoft.EntityFrameworkCore` extensions or `EFCore.PaginatedList`.

## Agentic workflow
Drive ASP.NET Core work as: (1) a planner subagent reads `Program.cs` + existing controllers and emits a target endpoint list (route, verb, request DTO, response DTO, auth policy); (2) a code-writer subagent scaffolds Controller + Service interface + Service impl + DTOs + AutoMapper profile + xUnit/NUnit tests in one pass; (3) a build-and-test subagent runs `dotnet build` + `dotnet test` and feeds compile errors back; (4) a Roslyn analyzer subagent flags missing `CancellationToken`, blocking calls, and missing `[ProducesResponseType]`. Persist generated code split by feature folder (`Features/Users/`) so agents read one folder per task.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — implementer for controllers and services.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = one endpoint plus test; quality gate runs `dotnet build` + `dotnet test`.
- A purpose-built **dotnet-build-loop-agent** (worth creating): wraps `dotnet watch test` and feeds first compile error per file back as the next prompt.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub `appsettings.Development.json` and seeded fixtures (connection strings, JWT secrets) before commit.

### Prompt pattern
Endpoint scaffold:
```
You are an ASP.NET Core 8 backend engineer. Add a GET /api/v1/users
/{id:guid}/posts endpoint. Output: PostsController action +
IPostsService method + impl + GetUserPostsQuery DTO + PostDto +
AutoMapper profile + xUnit test. Use CancellationToken on every
async signature. Add [Authorize] and [ProducesResponseType] for
200/404. Run: dotnet build && dotnet test --filter "Posts".
```

Async/cancellation review:
```
Scan Controllers/ and Services/ for: (1) async methods missing
CancellationToken parameter, (2) .Result / .Wait() / .GetAwaiter()
.GetResult(), (3) async void methods, (4) Task-returning methods
named without "Async" suffix. Output: filepath:line, fix proposal.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet new webapi` / `dotnet new sln` | Scaffold project + solution | bundled with .NET SDK |
| `dotnet ef migrations add` | EF Core migrations | `dotnet tool install -g dotnet-ef` |
| `dotnet watch` | Hot reload + run-on-save tests | bundled |
| `dotnet test --collect:"XPlat Code Coverage"` | Coverage data → coverlet → ReportGenerator | bundled + `dotnet tool install -g dotnet-reportgenerator-globaltool` |
| `dotnet format` | Roslyn-based formatter; runs in pre-commit | bundled |
| `dotnet outdated` | Surface stale NuGet packages | `dotnet tool install -g dotnet-outdated-tool` |
| Roslynator CLI | Extra analyzers; flags `Result`/`Wait` and missing CT | `dotnet tool install -g Roslynator.DotNet.Cli` |
| `gh` CLI | GitHub Actions / PR automation | https://cli.github.com |
| `aspnet-codegenerator` | Scaffold controllers from EF model | `dotnet tool install -g dotnet-aspnet-codegenerator` |
| `swagger-cli` | Validate generated OpenAPI from Swashbuckle | `npm i -g @apidevtools/swagger-cli` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Azure App Service / Container Apps | SaaS PaaS | API yes | First-class .NET deploy; agents drive via `az` CLI. |
| AWS ECS / Lambda (.NET 8 native AOT) | SaaS | API yes | AOT cuts cold-start; agents need to know `[DynamicallyAccessedMembers]` annotations. |
| Application Insights / OpenTelemetry | SaaS APM | API yes | Per-request telemetry; surfaces async-deadlock symptoms agents miss. |
| MediatR | OSS | yes | Common upgrade path from this Service Layer pattern; not free as of v12 — verify license. |
| FluentValidation | OSS | yes | Replaces DataAnnotations; agents handle FluentValidation generators well. |
| AutoMapper | OSS | yes | Source-generator branch; consider Mapster for AOT scenarios. |
| Serilog | OSS | yes | Structured logging; integrate with App Insights/Seq for agent-readable traces. |
| EF Core | OSS | yes | Already implements UoW + Repository; pattern's repos often redundant. |

## Templates & scripts
See `templates.md` for controller + service skeletons. Add an analyzer-driven gate (≤50 lines):

```bash
#!/usr/bin/env bash
# dotnet-gate.sh — fail PR if async hygiene or coverage slips.
# Usage: dotnet-gate.sh path/to/sln.sln [coverage_threshold]
set -euo pipefail
SLN="${1:?usage: dotnet-gate.sh SOLUTION [THRESHOLD]}"
THRESH="${2:-70}"
dotnet build "$SLN" -warnaserror -p:TreatWarningsAsErrors=true
dotnet test "$SLN" --collect:"XPlat Code Coverage" --results-directory /tmp/cov
COV_FILE=$(find /tmp/cov -name 'coverage.cobertura.xml' | head -1)
[ -n "$COV_FILE" ] || { echo "no coverage file"; exit 1; }
python3 - "$COV_FILE" "$THRESH" <<'PY'
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.argv[1]); root = tree.getroot()
rate = float(root.attrib.get("line-rate", 0)) * 100
thr = float(sys.argv[2])
print(f"line coverage: {rate:.1f}% (threshold {thr}%)")
sys.exit(0 if rate >= thr else 1)
PY
roslynator analyze "$SLN" --severity-level info \
  --analyzer-assemblies "$(dotnet --info | grep 'Base Path' | awk '{print $3}')Microsoft.CodeAnalysis.NetAnalyzers.dll" \
  || echo "Roslynator findings (non-blocking)"
```

Wire into GitHub Actions before merge.

## Best practices
- **CancellationToken on every async public API.** Plumb from controller → service → EF Core. Agents skip this; enforce via Roslynator.
- **`AsNoTracking` for all read queries.** Doubles read throughput on Postgres/SQL Server; controllers showing data should never track.
- **Use `ProblemDetails` (RFC 7807) for errors.** Don't return naked strings. Configure `AddProblemDetails()` in `Program.cs`.
- **Source-generated JSON serialization** (`[JsonSerializable]`) for hot endpoints — meaningful win, especially under AOT.
- **Feature folders, not technical folders.** `Features/Users/{Controller, Service, Dtos, Mappings}` reads better for agents than `Controllers/`, `Services/`, `Dtos/`.
- **OpenAPI as the contract.** Generate clients via NSwag/Kiota; agents on the consumer side then never invent endpoint shapes.
- **Static analyzers in csproj.** `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` + `Microsoft.CodeAnalysis.NetAnalyzers` package. Compiler is your linter.
- **Don't inject `DbContext` into controllers** — always go through a service. Otherwise transactions span unclear scopes.
- **Use `Required` keyword on DTOs** (.NET 7+) instead of `[Required]` — surfaces missing fields at compile time.
- **Health checks for every external dep.** `AddHealthChecks().AddNpgSql(...).AddRedis(...)` — agents need a single endpoint to verify deploys.

## AI-agent gotchas
- **`async void` slips in.** Agents reach for `async void` for "fire-and-forget" notifications; one unhandled exception crashes the host. Roslynator + ban via analyzer.
- **`.Result` deadlocks on legacy frameworks.** In .NET Core 6+ this rarely deadlocks but causes thread-pool starvation. Force agents to await all the way down.
- **AutoMapper runtime errors only at request time.** Agents add a property to a DTO without mapping; tests pass, prod 500s. Add `MapperConfiguration.AssertConfigurationIsValid()` to a unit test.
- **DTO/Entity drift.** Agents add `IsActive` to entity, forget DTO; updates silently no-op. Reflection-based parity test (`PropertyInfo` diff) blocks regressions.
- **Missing `[Authorize]`.** Agents copy a public endpoint into a private controller and forget the attribute. Default to `RequireAuthenticatedUser()` in `Program.cs`, opt-out per route.
- **Repository methods leak `IQueryable`.** Agents return `IQueryable<User>` so callers can keep composing — but the DbContext is already disposed by then. Always `ToListAsync` / `ToArrayAsync` inside the repo.
- **PagedResult re-invented.** Each agent ships its own `PagedResult<T>`; fields differ (`TotalCount` vs `Total`, `PageIndex` vs `Page`). Centralize in `Common/Models`.
- **Migration drift across branches.** Agents `dotnet ef migrations add` on parallel branches; merge yields out-of-order migrations. Single-writer migration discipline; PR template asks "did you generate a migration?"
- **`ConfigureServices` ordering matters.** `UseAuthentication` must precede `UseAuthorization`. Agents reorder middleware while refactoring `Program.cs`; runtime fails subtly. Lock middleware order with a comment.
- **HttpClient as singleton/scoped misuse.** Agents `new HttpClient()` per call → socket exhaustion. Inject `IHttpClientFactory` always; lint via Roslynator.
- **Secrets in `appsettings.json`.** Agents paste connection strings into the file checked into git. Use `dotnet user-secrets` in dev, env vars + Key Vault in prod, and add a pre-commit secret scanner.

## References
- Microsoft Learn — ASP.NET Core fundamentals. https://learn.microsoft.com/aspnet/core/fundamentals
- Microsoft Learn — Best practices for async. https://learn.microsoft.com/dotnet/csharp/asynchronous-programming/async-scenarios
- David Fowler — "ASP.NET Core Diagnostic Scenarios." https://github.com/davidfowl/AspNetCoreDiagnosticScenarios
- Steve Smith — Clean architecture template. https://github.com/ardalis/CleanArchitecture
- Microsoft Learn — ProblemDetails / RFC 7807. https://learn.microsoft.com/aspnet/core/web-api/handle-errors
- Roslynator — analyzer rules. https://github.com/dotnet/roslynator
- AutoMapper docs (caveats). https://docs.automapper.org
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/csharp-dotnet/`, `pro/dev/backend-enterprise/csharp-dotnet-patterns/`, `pro/dev/backend-enterprise/csharp-entity-framework/`, `pro/dev/backend-enterprise/csharp-xunit-testing/`.
