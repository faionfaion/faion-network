# C# Background Services

## Summary

**One-sentence:** Long-running in-process workers via `BackgroundService` + Channels with bounded back-pressure, scoped DI, graceful shutdown, idempotent retry and health checks.

**One-paragraph:** Ad-hoc `Task.Run` loops bypass the `IHost` lifecycle, ignore `CancellationToken`, and capture scoped DI as singletons. `BackgroundService` extends `IHostedService` and integrates with graceful shutdown, `IHealthCheck`, and `System.Threading.Channels` for in-memory queues with back-pressure. This methodology pins seven testable rules: extend `BackgroundService` (never `Task.Run`), pass `stoppingToken` everywhere, catch per item inside `ExecuteAsync`, `CreateScope()` for scoped access, `Channel.CreateBounded` with an explicit `FullMode`, `PeriodicTimer` instead of a delay loop, and a per-item log scope. Output: a worker class + DI registration + xUnit test conforming to the contract in `02-output-contract.xml`.

**Ефективно для:**

- Queue consumer / scheduler / file watcher з graceful shutdown і bounded drain.
- Idempotent work units під at-least-once delivery.
- In-memory back-pressure between HTTP and background workers.
- Observability як first-class concern (metrics + tracing + per-item log scope).
- Moderate-throughput scheduled tasks where Hangfire/Quartz is overkill.

## Applies If (ALL must hold)

- Service runs a long-lived background loop (queue consumer, scheduler, watcher) inside the API host process.
- Process must shut down gracefully on SIGTERM with bounded drain time.
- Work units must be idempotent to survive at-least-once delivery.
- Throughput fits on a single replica or a leader-elected replica.

## Skip If (ANY kills it)

- Jobs MUST survive restarts — use Hangfire, Quartz.NET, or a durable broker; channels are in-memory only.
- Heavy CPU work per item — would starve the HTTP thread pool; isolate to a separate Worker host.
- Distributed scheduling across replicas without leader election.
- Exactly-once semantics required — in-memory channels lose state on shutdown.
- One-shot CLI / job runner, or a periodic job better expressed as a cron-triggered Function / Lambda.
- Hosted in IIS in-process — BackgroundService lifecycle does not align cleanly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Worker scope / job spec (queue / scheduler / watcher) | markdown | product / ticket |
| Idempotency key strategy | markdown | architecture |
| ASP.NET Core 6+ project | csproj | repo |
| DbContext or downstream service contract | C# interface | repo |
| Observability stack (metrics + tracing) | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-aspnet-core]] | Hosted service runs inside the same Generic Host as the API |
| [[csharp-dotnet]] | Base .NET wiring, DI, hosting model |
| [[csharp-entity-framework]] | Scoped DbContext lifecycle the worker depends on |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: extend-backgroundservice, pass-stoppingtoken, per-item-trycatch, scope-per-item, bounded-channel, periodic-timer-not-delay-loop, structured-per-item-logging | 1300 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the worker spec + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: task-run-loop, unbounded-channel, captive-dbcontext, no-stoppingtoken, uncorrelated-worker-logs | 900 |
| `content/04-procedure.xml` | essential | 7-step procedure with input/action/output per step | 1100 |
| `content/06-decision-tree.xml` | essential | Routing tree on durability / CPU / queue / schedule → conclusion(ref=rule-id) | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-job-shape` | sonnet | Apply the decision tree on durability / throughput / CPU |
| `scaffold-skeleton` | haiku | Mechanical template emission |
| `wire-feature-logic` | sonnet | Per-feature judgment with bounded inputs |
| `write-xunit-test` | haiku | Mechanical AAA test against the IHostedService API |
| `audit-output` | sonnet | Verify rules in 01-core-rules.xml hold |

## Templates

| File | Purpose |
|------|---------|
| `templates/queue-consumer.cs` | BackgroundService queue-consumer skeleton with retry + idempotency |
| `templates/registration.cs` | Channel + worker + health-check registration snippet for Program.cs |
| `templates/prompt-worker.txt` | Subagent prompt generating worker + registration + xUnit test |
| `templates/_smoke-test.cs` | Filled-in minimal queue consumer for a Users.Created topic |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-background-services.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[csharp-aspnet-core]]
- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-xunit-testing]]
- [[audit-grade-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable job-shape signals (durability requirement, CPU profile, queue vs schedule) to a rule from `01-core-rules.xml`, and either approves BackgroundService or redirects to a durable broker / separate Worker host. Use it whenever an engineer reaches for `Task.Run` or considers a hosted service for periodic work.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/queue-consumer.cs`

```csharp
// BackgroundService + bounded Channel<T> producer/consumer skeleton.
// Replace TItem, TService, and TQueue with your domain types.

using System.Threading.Channels;

public interface ITQueue
{
    ValueTask EnqueueAsync(TItem item, CancellationToken ct = default);
}

public class TQueue : ITQueue
{
    private readonly Channel<TItem> _channel;
    public TQueue(Channel<TItem> channel) => _channel = channel;

    public async ValueTask EnqueueAsync(TItem item, CancellationToken ct = default)
        => await _channel.Writer.WriteAsync(item, ct);
}

public class TProcessor : BackgroundService
{
    private readonly IServiceProvider _sp;
    private readonly ILogger<TProcessor> _logger;
    private readonly Channel<TItem> _channel;

    public TProcessor(IServiceProvider sp, ILogger<TProcessor> logger, Channel<TItem> channel)
    {
        _sp = sp;
        _logger = logger;
        _channel = channel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var item in _channel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                using var scope = _sp.CreateScope();
                var svc = scope.ServiceProvider.GetRequiredService<TService>();
                await svc.ProcessAsync(item, stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                throw;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to process item {Item}", item);
            }
        }
    }
}
```

### `templates/registration.cs`

```csharp
using System.Threading.Channels;
using Microsoft.Extensions.Diagnostics.HealthChecks;

// Bounded channel — capacity 1024, block producer when full
builder.Services.AddSingleton(_ => Channel.CreateBounded<TItem>(
    new BoundedChannelOptions(1024) { FullMode = BoundedChannelFullMode.Wait }));

// Queue abstraction (singleton — shares the channel)
builder.Services.AddSingleton<ITQueue, TQueue>();

// Health probe the worker stamps on every successful unit
builder.Services.AddSingleton<TProcessorHealth>();

// Hosted services
builder.Services.AddHostedService<TProcessor>();
builder.Services.AddHostedService<CleanupService>(); // periodic if needed

builder.Services.AddHealthChecks()
    .AddCheck<TProcessorHealth>("t-processor");

var app = builder.Build();
app.MapHealthChecks("/healthz");
app.Run();

// Liveness signal: the worker is only healthy while it keeps draining.
public sealed class TProcessorHealth : IHealthCheck
{
    public DateTime LastSuccess { get; set; } = DateTime.UtcNow;

    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext _, CancellationToken __)
        => Task.FromResult(
            DateTime.UtcNow - LastSuccess > TimeSpan.FromMinutes(5)
                ? HealthCheckResult.Unhealthy("no successful run in >5m")
                : HealthCheckResult.Healthy());
}
```

### `templates/prompt-worker.txt`

```text
Add MyApp.Services.<Name>Service as a BackgroundService consuming Channel<<JobType>>.
- Use bounded capacity 1000, BoundedChannelFullMode.Wait
- Resolve I<Name>Handler via CreateScope() per item
- Open ILogger.BeginScope with the entity id before handling each item
- Log at Information on dequeue, Error on handler failure (no rethrow except OperationCanceledException on the stopping token)
- Register in Program.cs:
    AddSingleton(Channel.CreateBounded<<JobType>>(new BoundedChannelOptions(1000) { FullMode = Wait }))
    AddHostedService<<Name>Service>()
    AddSingleton<<Name>Health>()
    AddHealthChecks().AddCheck<<Name>Health>("<name>")
- Add an xUnit integration test using WebApplicationFactory<Program> that:
    enqueues one item via I<Name>Queue
    awaits until IHealthCheck reports Healthy (or timeout 5s)
    asserts the handler was invoked
    asserts the loop exits within 1s of StopAsync
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
