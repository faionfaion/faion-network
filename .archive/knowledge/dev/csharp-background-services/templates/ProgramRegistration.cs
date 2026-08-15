// purpose: DI registration template for BackgroundService + Channel + IHealthCheck
// consumes: WebApplicationBuilder
// produces: composition root snippet
// depends-on: templates/Worker.cs
// token-budget-impact: ~300 tokens when loaded as reference

using System.Threading.Channels;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Faion.Workers;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton(Channel.CreateBounded<int>(
    new BoundedChannelOptions(1000) { FullMode = BoundedChannelFullMode.Wait }));

builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddSingleton<OrderProcessorHealth>();
builder.Services.AddHostedService<OrderProcessorService>();
builder.Services.AddHealthChecks()
    .AddCheck<OrderProcessorHealth>("order-processor");

var app = builder.Build();
app.MapHealthChecks("/healthz");
app.Run();

public sealed class OrderProcessorHealth : IHealthCheck
{
    public DateTime LastSuccess { get; set; } = DateTime.UtcNow;

    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext _, CancellationToken __)
        => Task.FromResult(
            DateTime.UtcNow - LastSuccess > TimeSpan.FromMinutes(5)
                ? HealthCheckResult.Unhealthy("no successful run in >5m")
                : HealthCheckResult.Healthy());
}
