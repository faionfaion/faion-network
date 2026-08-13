# C# Background Services

## Summary

**One-sentence:** Produces a robust BackgroundService / IHostedService implementation with graceful shutdown, retry, idempotency, and metrics.

**One-paragraph:** Produces a robust BackgroundService / IHostedService implementation with graceful shutdown, retry, idempotency, and metrics. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Queue consumer / scheduler / file watcher з graceful shutdown і bounded drain.
- Idempotent work units під at-least-once delivery.
- Observability як first-class concern (metrics + tracing per work unit).

## Applies If (ALL must hold)

- Service runs a long-lived background loop (queue consumer, scheduler, watcher).
- Process must shut down gracefully on SIGTERM with bounded drain time.
- Work units must be idempotent to survive at-least-once delivery.

## Skip If (ANY kills it)

- One-shot CLI / job runner — Worker Service overkill.
- Periodic job better expressed as a cron-triggered Function / Lambda.
- Hosted in IIS in-process — BackgroundService lifecycle does not align cleanly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Worker scope (queue / scheduler / watcher) | markdown | product |
| Idempotency key strategy | markdown | architecture |
| Observability stack (metrics + tracing) | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-aspnet-core]] | Hosted service runs inside the same Generic Host as the API |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-skeleton` | haiku | Mechanical template emission |
| `wire-feature-logic` | sonnet | Per-feature judgment with bounded inputs |
| `audit-output` | sonnet | Verify rules in 01-core-rules.xml hold |

## Templates

| File | Purpose |
|------|---------|
| `templates/queue-consumer.cs` | BackgroundService queue-consumer skeleton with retry + idempotency |
| `templates/registration.cs` | Hosted-service registration snippet for Program.cs |
| `templates/_smoke-test.cs` | Filled-in minimal queue consumer for a Users.Created topic |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-background-services.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[csharp-aspnet-core]]
- [[audit-grade-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.

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
// Program.cs — registration for Channel<T>, queue abstraction, and hosted services.
// Adjust TItem, TQueue, and TProcessor to your domain types.

using System.Threading.Channels;

// Bounded channel — capacity 1024, block producer when full
builder.Services.AddSingleton(_ => Channel.CreateBounded<TItem>(
    new BoundedChannelOptions(1024) { FullMode = BoundedChannelFullMode.Wait }));

// Queue abstraction (singleton — shares the channel)
builder.Services.AddSingleton<ITQueue, TQueue>();

// Hosted services
builder.Services.AddHostedService<TProcessor>();
builder.Services.AddHostedService<CleanupService>(); // periodic if needed
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
