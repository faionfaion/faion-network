// purpose: Feature folder skeleton with controller/service/repo/dto
// consumes: see AGENTS.md Prerequisites
// produces: ASP.NET Core Patterns code
// depends-on: content/02-output-contract.xml schema
// token-budget-impact: ~500 tokens when filled

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
