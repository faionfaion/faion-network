// purpose: Hosted-service registration snippet for Program.cs (channel + worker + health check)
// consumes: see AGENTS.md Prerequisites
// produces: C# Background Services composition-root snippet
// depends-on: content/02-output-contract.xml schema, templates/queue-consumer.cs
// token-budget-impact: ~500 tokens when filled

// Program.cs — registration for Channel<T>, queue abstraction, hosted services and health check.
// Adjust TItem, TQueue, and TProcessor to your domain types.

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
