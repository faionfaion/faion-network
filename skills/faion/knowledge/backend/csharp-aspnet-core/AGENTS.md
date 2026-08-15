# ASP.NET Core Patterns

## Summary

**One-sentence:** Produces a layered ASP.NET Core 8/9 service: feature folders, IXService interfaces, EF Core repos, AutoMapper, ProblemDetails.

**One-paragraph:** Produces a layered ASP.NET Core 8/9 service: feature folders and IXService interfaces, scoped DbContext, CancellationToken threaded to every EF Core call, ProblemDetails (RFC 7807) from a single global IExceptionHandler, record DTOs mapped at the service boundary, TimeProvider instead of DateTime.UtcNow, AsNoTracking + eager .Include() on reads, keyset pagination, explicit transactions on multi-step writes, and WebApplicationFactory + Testcontainers for integration tests. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Новий ASP.NET Core 8/9 API з feature folders і чіткими шарами controller/service/repo.
- Async-by-default з CancellationToken прокинутим до DB layer.
- ProblemDetails (RFC 7807) як єдиний error contract.
- Ревʼю PR-диффа на captive DbContext, зворотний порядок middleware і повернення tracked-ентіті з сервісу.
- Дисципліна запитів EF Core: AsNoTracking, eager .Include(), keyset-пагінація, явні транзакції.
- Інтеграційні тести на WebApplicationFactory + Testcontainers замість EF InMemory.

## Applies If (ALL must hold)

- New ASP.NET Core 8/9 API with clear controller/service/repository separation.
- Migrating legacy ASP.NET MVC or WCF services to modern Web API.
- Multi-tenant or B2B SaaS in .NET where DI scopes and middleware are central.
- Codebase shared between humans and LLMs — explicit interfaces stabilize completions.

## Skip If (ANY kills it)

- Tiny internal tool or webhook with <10 endpoints — Minimal APIs suffice.
- Microservice that publishes only to a queue — three layers around one method is overkill.
- gRPC-only service — service-method-per-RPC layering is more appropriate.
- App on .NET Framework 4.x — Generic Host, async-by-default, DI assumptions do not hold.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| .NET 8 or 9 SDK | tool | dev environment |
| Feature scope brief | markdown | product |
| Data model decision (EF Core vs Dapper) | markdown | architecture |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[audit-grade-api-design]] | API contract defines the controller surface |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 16 testable rules + skip rule, each with rationale + source | 2200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) incl. optional `design_profile` + valid/invalid examples + forbidden patterns | 1300 |
| `content/03-failure-modes.xml` | essential | 12 antipatterns with symptom + detector + root-cause + fix | 1400 |
| `content/04-procedure.xml` | essential | 7-step procedure with input/action/output per step | 1300 |
| `content/05-examples.xml` | essential | Controller / service / IExceptionHandler / transaction examples + end-to-end trace | 1400 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-skeleton` | haiku | Mechanical template emission |
| `wire-feature-logic` | sonnet | Per-feature judgment with bounded inputs |
| `audit-output` | sonnet | Verify rules in 01-core-rules.xml hold |

## Templates

| File | Purpose |
|------|---------|
| `templates/dotnet-gate.sh` | CI gate script enforcing async hygiene and coverage threshold |
| `templates/feature-folder-skeleton.cs` | Feature folder skeleton with controller/service/repo/dto |
| `templates/_smoke-test.cs` | Minimum viable feature: Users CRUD with auth + ProblemDetails |
| `templates/problem-details-handler.cs` | .NET 8+ IExceptionHandler mapping domain exceptions to RFC 7807 |
| `templates/prompt-aspnet-slice.txt` | Prompt skeleton for scaffolding one compliant vertical slice |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-aspnet-core.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[csharp-background-services]]
- [[audit-grade-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/dotnet-gate.sh`

```bash
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
echo "Gate passed"
```

### `templates/feature-folder-skeleton.cs`

```csharp
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Faion.Sample;

public sealed class SampleBackgroundService(ILogger<SampleBackgroundService> log) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // 1. dequeue work unit (idempotency-keyed)
                // 2. process with retry policy
                // 3. ack
                await Task.Delay(TimeSpan.FromSeconds(1), stoppingToken);
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                log.LogError(ex, "work unit failed");
            }
        }
    }
}
```

### `templates/_smoke-test.cs`

```csharp
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Faion.Sample;

public sealed class SampleBackgroundService(ILogger<SampleBackgroundService> log) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // 1. dequeue work unit (idempotency-keyed)
                // 2. process with retry policy
                // 3. ack
                await Task.Delay(TimeSpan.FromSeconds(1), stoppingToken);
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                log.LogError(ex, "work unit failed");
            }
        }
    }
}
```

### `templates/problem-details-handler.cs`

```csharp
// .NET 8+ IExceptionHandler — maps domain exceptions to RFC 7807 ProblemDetails.
// Register in Program.cs:
//   builder.Services.AddProblemDetails();
//   builder.Services.AddExceptionHandler<ProblemDetailsHandler>();
//   app.UseExceptionHandler();
public sealed class ProblemDetailsHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext ctx, Exception ex, CancellationToken ct)
    {
        var pd = ex switch
        {
            NotFoundException nf =>
                new ProblemDetails { Status = 404, Title = nf.Message },
            ValidationException ve =>
                new ProblemDetails { Status = 422, Title = "Validation failed",
                                     Detail = ve.Message },
            _ => new ProblemDetails { Status = 500, Title = "Server error" }
        };
        ctx.Response.StatusCode = pd.Status!.Value;
        await ctx.Response.WriteAsJsonAsync(pd, ct);
        return true;
    }
}
```

### `templates/prompt-aspnet-slice.txt`

```text
Add <Entity> vertical slice in MyApp.Features.<Entities>:
- Records: Create<Entity>Dto(string Name, ...), <Entity>Dto(int Id, string Name, DateTime CreatedAt)
- I<Entity>Service { Task<<Entity>Dto> CreateAsync(Create<Entity>Dto, CancellationToken);
                     Task Delete<Entity>Async(int id, CancellationToken) }
- <Entity>Service uses AppDbContext, maps to DTO via Mapperly, injects TimeProvider
- <Entity>sController: POST/DELETE/GET with [Authorize], CreatedAtAction,
  CancellationToken on all actions, keyset cursor on the list endpoint
- EF migration Add<Entities>
- Integration test using WebApplicationFactory<Program> + Testcontainers Postgres
```
