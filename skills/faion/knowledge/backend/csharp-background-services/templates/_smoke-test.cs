// purpose: Filled-in minimal queue consumer for a Users.Created topic
// consumes: see AGENTS.md Prerequisites
// produces: C# Background Services code
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
