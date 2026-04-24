# Agent Integration — C# Background Services

## When to use
- Long-running in-process workers in ASP.NET Core: queue consumers, periodic cleanups, cache warmers, file watchers.
- Need bounded resource use and graceful shutdown via `IHostedService` / `BackgroundService` with `CancellationToken stoppingToken`.
- In-memory work queues using `System.Threading.Channels` for back-pressure between web request and worker.
- Moderate-throughput scheduled jobs where you don't want a separate process (Hangfire/Quartz overkill).

## When NOT to use
- Cross-process or durable jobs that must survive app restarts — use Hangfire, Quartz.NET with persistence, Azure Functions, or a real broker (RabbitMQ, Azure Service Bus).
- Heavy CPU work — a `BackgroundService` runs in the host process and can starve the request thread pool. Use a separate worker host or queue.
- Distributed scheduling across replicas — `BackgroundService` runs on every instance; you'll get N concurrent timers unless you add leader election.
- Critical "exactly-once" semantics — channels are in-memory and lost on shutdown.

## Where it fails / limitations
- `ExecuteAsync` exceptions silently kill the service in older .NET versions; .NET 6+ respects `BackgroundServiceExceptionBehavior` but defaults can stop the whole host.
- `IServiceProvider.CreateScope()` inside the loop is required for scoped DI (DbContext); forgetting it causes captive-dependency bugs and connection leaks.
- `PeriodicTimer` drift on long pauses — a 1h timer doesn't catch up missed ticks if the host paused (e.g., k8s evict + restart).
- Channels with unbounded capacity become memory bombs under producer spikes.
- Health checks don't see worker progress unless you wire `IHealthCheck` to track last-run timestamp.

## Agentic workflow
A subagent should generate three files together: the `BackgroundService`, an `IXQueue` abstraction (channel writer wrapper), and the `Program.cs`/extension method that registers both as singletons plus the `Channel<T>` factory. Then add an integration test using `WebApplicationFactory` that enqueues an item and asserts side-effects within a timeout. For periodic services, prompt explicitly for `PeriodicTimer` over `Task.Delay` loops, plus a health check.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the test-first cycle for hosted services.
- A project-local `aspnet-worker` subagent — generates `BackgroundService` + queue + DI registration + xUnit test in one diff.

### Prompt pattern
```
Add MyApp.Services.EmailDispatcherService as a BackgroundService consuming
Channel<EmailJob>. Use bounded capacity 1000, BoundedChannelFullMode.Wait.
Resolve IEmailSender via CreateScope. Log at Information on dequeue and
Error on send failure (no rethrow). Register in Program.cs via
AddHostedService + AddSingleton<Channel<EmailJob>>. Add xUnit test using
WebApplicationFactory that posts /send and asserts IEmailSender.SendAsync
was invoked.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet new worker` | Scaffolds a Worker host (BackgroundService + Program.cs) | `dotnet new worker -n MyWorker` |
| `dotnet add package` | Add `Microsoft.Extensions.Hosting`, `System.Threading.Channels` | https://learn.microsoft.com/dotnet/core/extensions/workers |
| `dotnet test` | Run xUnit tests; combine with `WebApplicationFactory<TProgram>` | https://learn.microsoft.com/aspnet/core/test |
| `dotnet-counters` | Live monitor of `dotnet-runtime` and custom EventCounters | `dotnet tool install -g dotnet-counters` |
| `dotnet-trace` | Capture hangs / starvation in worker loops | `dotnet tool install -g dotnet-trace` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hangfire | OSS (free + Pro) | Yes | Persistent jobs in SQL/Redis; better than `BackgroundService` for cross-restart durability |
| Quartz.NET | OSS | Yes | Cron-style scheduling with cluster support |
| Azure Service Bus / AWS SQS | SaaS | Yes | Replace `Channel<T>` for cross-instance, durable queues |
| Application Insights / OpenTelemetry .NET | SaaS / OSS | Yes | Auto-instrument `IHost` and HTTP; add custom `Activity` per dequeue |
| Polly | OSS | Yes | Retry/circuit-breaker around the work delegate inside the service |

## Templates & scripts
See `templates.md` for full hosted-service skeleton. Health-check wiring snippet:

```csharp
// Program.cs
builder.Services.AddSingleton<EmailDispatcherHealth>();
builder.Services.AddHostedService<EmailDispatcherService>();
builder.Services.AddHealthChecks()
    .AddCheck<EmailDispatcherHealth>("email-dispatcher");

// EmailDispatcherHealth.cs
public class EmailDispatcherHealth : IHealthCheck
{
    public DateTime LastSuccess { get; set; } = DateTime.UtcNow;
    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext _, CancellationToken __)
        => Task.FromResult(
            DateTime.UtcNow - LastSuccess > TimeSpan.FromMinutes(5)
                ? HealthCheckResult.Unhealthy("No successful run in >5min")
                : HealthCheckResult.Healthy());
}
```

## Best practices
- Always pass `stoppingToken` into every `await` call inside `ExecuteAsync` — without it, shutdown blocks for 30s before forced kill.
- Wrap the work item handler in try/catch; never let exceptions bubble to `ExecuteAsync`'s loop.
- Use `Channel.CreateBounded<T>(...)` with `FullMode.Wait` (back-pressure) or `DropOldest` (lossy ok). Avoid `Unbounded`.
- Set `WaitForShutdownTimeout`/`ShutdownTimeout` to the worst-case in-flight work duration.
- For periodic work, prefer `PeriodicTimer` over `Task.Delay` — it doesn't accumulate drift.
- One `BackgroundService` per concern; avoid stuffing email + cleanup + cache warm into one class.
- Emit OpenTelemetry/Activity spans around each dequeue so APM shows "request → enqueue → background work" as a linked trace.

## AI-agent gotchas
- LLMs default to `Task.Run(async () => { while (true) ... })` instead of `BackgroundService` — explicitly require the base class.
- They forget `using var scope = _serviceProvider.CreateScope();` and inject `DbContext` directly, which breaks under parallel processing. Reject diffs that inject scoped services into a singleton service constructor.
- Agents create unbounded channels — pin `BoundedChannelOptions(1000) { FullMode = Wait }` in the prompt.
- Agents skip `stoppingToken.ThrowIfCancellationRequested()`; verify shutdown actually exits the loop in the integration test.
- Human-in-loop checkpoint: confirm the worker is run in-host (alongside ASP.NET) vs as separate Worker host; the right answer depends on scaling needs and is hard to LLM-decide.

## References
- .NET docs — Background tasks with hosted services: https://learn.microsoft.com/aspnet/core/fundamentals/host/hosted-services
- Stephen Toub — "An Introduction to System.Threading.Channels": https://devblogs.microsoft.com/dotnet/an-introduction-to-system-threading-channels/
- David Fowler — Async guidance: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios
- Hangfire docs: https://docs.hangfire.io
