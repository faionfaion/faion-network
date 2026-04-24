# Agent Integration — C# Background Services (Hosted Service / IHostedService)

## When to use
- ASP.NET Core or .NET Worker Service that needs in-process background processing: queue consumers, periodic cleanup, scheduled syncs.
- Bridging an HTTP request to async post-processing via an in-memory `Channel<T>` producer/consumer.
- Recurring jobs ≤ a few minutes apart on a single instance using `PeriodicTimer` (preferred over `Task.Delay` loops).
- Adding `IHostApplicationLifetime` integration so background work shuts down cleanly under SIGTERM/Kubernetes.
- Wiring `ILogger<T>`, `IServiceProvider` scopes, and OpenTelemetry instrumentation around background work.

## When NOT to use
- Distributed scheduling (multiple replicas needing leader election) — use Hangfire, Quartz.NET, or external schedulers (K8s CronJob, Azure Functions Timer).
- Durable, retry-able jobs with persistence — use Hangfire, MassTransit, or a queue (RabbitMQ, Service Bus, SQS).
- Long-running CPU-bound work that should not block the host pipeline — use a separate Worker Service deployment.
- Cron-style "every Tuesday at 3 AM" — `PeriodicTimer` is fixed-interval; use Quartz.NET or platform schedulers.

## Where it fails / limitations
- `Channel<T>` is in-memory only; if the host crashes, queued work is lost. Agents miss this and treat it as durable.
- Singletons resolving scoped services panics at runtime — agents forget the `IServiceProvider.CreateScope()` pattern inside `BackgroundService`.
- Unhandled exceptions in `ExecuteAsync` silently terminate the service in older runtimes; .NET 6+ logs but still stops. Agents skip the try/catch around the inner loop.
- `PeriodicTimer.WaitForNextTickAsync(stoppingToken)` cancellation is correct, but agents often `Task.Delay` instead, which leaks on shutdown.
- `Channel.Writer.WriteAsync` blocks when the channel is bounded and full — agents pick `Channel.CreateUnbounded` "to avoid blocking" and create memory leaks.
- Logging from background services without correlation IDs makes triage impossible; OpenTelemetry must be wired explicitly.

## Agentic workflow
Treat each background service as a small subsystem: define the queue interface, the processor (`BackgroundService`), and registration in `Program.cs`. The coding subagent registers the singleton `Channel<T>`, the `IXQueue` abstraction, and the `BackgroundService`. Reviewer enforces: bounded channels with a sane capacity, scoped DI inside `ExecuteAsync`, try/catch around the per-item loop, graceful shutdown via `stoppingToken`. Long-term: if requirements gain durability or distribution, escalate to Hangfire/MassTransit rather than evolving the in-process service.

### Recommended subagents
- `faion-sdd-executor-agent` — implement queue + processor + tests in sequence.
- General reviewer subagent — flag unbounded channels, unscoped DI, missing per-item try/catch, `Task.Delay` instead of `PeriodicTimer`.
- `password-scrubber-agent` — strip secrets from log scopes around background work.

### Prompt pattern
Plan: "Add `IOrderQueue` (writes to bounded `Channel<int>` capacity 1024) and `OrderProcessor : BackgroundService` (reads via `ReadAllAsync(stoppingToken)`). Resolve `IOrderService` per-item via `IServiceProvider.CreateScope()`. Wrap per-item work in try/catch logging the error. Register both in `Program.cs`. Add an integration test using `Host.CreateDefaultBuilder` and `TestServer`."

Review: "Audit `Services/*.cs`: any `Channel.CreateUnbounded` (justify or convert to bounded), any singleton resolving a scoped service, any `BackgroundService` without per-item try/catch, any `Task.Delay` used as a timer."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet` SDK | Build/run/test | dot.net |
| `dotnet new worker` | Scaffold Worker Service template | `dotnet new worker -n MyWorker` |
| `dotnet format` | Style + analyzers fixes | bundled |
| `dotnet test` | xUnit/NUnit/MSTest runner | bundled |
| Roslyn analyzers + .NET 8 analyzers | Detect async/await mistakes, dispose patterns | NuGet `Microsoft.CodeAnalysis.NetAnalyzers` |
| StyleCop.Analyzers | Style enforcement | NuGet |
| `dotnet-counters` | Live perf counters (queue depth, GC) | `dotnet tool install --global dotnet-counters` |
| `dotnet-trace` | Tracing for queue stalls | `dotnet tool install --global dotnet-trace` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Hangfire | OSS (paid Pro) | Yes | Replaces in-process when durability/retries are needed |
| Quartz.NET | OSS | Yes | Cron expressions, clustering |
| MassTransit + RabbitMQ/Azure Service Bus | OSS | Yes | Real distributed processing; complex setup |
| Azure Functions Timer | SaaS | Yes | Replace `PeriodicTimer` if hosted on Azure |
| AWS Lambda + EventBridge | SaaS | Yes | Same idea on AWS |
| Application Insights | SaaS | Yes | Auto-instruments `BackgroundService` via OpenTelemetry |
| Datadog .NET APM | SaaS | Yes | Tracer attaches via env vars |

## Templates & scripts
See `templates.md` for `BackgroundService` skeleton, bounded `Channel<T>` registration, scoped service resolution. Sample registration:

```csharp
// Program.cs
builder.Services.AddSingleton(_ => Channel.CreateBounded<int>(
    new BoundedChannelOptions(1024) { FullMode = BoundedChannelFullMode.Wait }));
builder.Services.AddSingleton<IOrderQueue, OrderQueue>();
builder.Services.AddHostedService<BackgroundOrderProcessor>();
builder.Services.AddHostedService<CleanupService>();
```

Per-item resilience pattern (40 lines):

```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    await foreach (var id in _channel.Reader.ReadAllAsync(stoppingToken))
    {
        try
        {
            using var scope = _sp.CreateScope();
            var svc = scope.ServiceProvider.GetRequiredService<IOrderService>();
            await svc.ProcessAsync(id, stoppingToken);
        }
        catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested) { throw; }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Order {OrderId} failed", id);
        }
    }
}
```

## Best practices
- Always bound your `Channel<T>` with backpressure semantics (`Wait`, `DropOldest`, `DropWrite`) chosen explicitly.
- Resolve scoped dependencies inside `ExecuteAsync` via `IServiceProvider.CreateScope()`; never inject scoped services directly into a `BackgroundService`.
- Wrap per-item processing in try/catch so one bad item does not kill the loop; rethrow `OperationCanceledException` only on shutdown.
- Use `PeriodicTimer.WaitForNextTickAsync(stoppingToken)` for fixed-interval work; do not use `Task.Delay` in a loop.
- Log structured fields (`{OrderId}`) and use `BeginScope` per item for correlation.
- Add integration tests that spin up `Host.CreateDefaultBuilder().Build()` and assert end-to-end queue→handler flow.
- Prefer Hangfire/Quartz/MassTransit when work needs durability, distribution, or cron-style schedules — do not retrofit in-process.

## AI-agent gotchas
- LLMs default to `Channel.CreateUnbounded<T>()` — silently builds an unbounded memory leak under load. Reject in review.
- Agents inject `DbContext` (scoped) into a `BackgroundService` (singleton) and run; this throws at runtime on first access. Force the scope pattern.
- Generated `ExecuteAsync` often lacks try/catch around the loop body; one transient exception terminates the host.
- `Task.Delay(period, stoppingToken)` is common in AI output; replace with `PeriodicTimer` for shutdown correctness.
- Agents commonly forget to register the `BackgroundService` in `Program.cs` (`AddHostedService<T>()`) — service compiles but never runs.
- For multi-instance deploys, agents may run `BackgroundService` on every replica and double-process; gate with leader election or move to Hangfire.
- Logging without `BeginScope` or correlation IDs makes triage impossible — agents need explicit prompting.

## References
- .NET BackgroundService docs — https://learn.microsoft.com/en-us/dotnet/core/extensions/workers
- Channels — https://learn.microsoft.com/en-us/dotnet/core/extensions/channels
- IHostApplicationLifetime — https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.hosting.ihostapplicationlifetime
- Hangfire — https://www.hangfire.io
- Quartz.NET — https://www.quartz-scheduler.net
- MassTransit — https://masstransit.io
- OpenTelemetry .NET — https://opentelemetry.io/docs/instrumentation/net/
