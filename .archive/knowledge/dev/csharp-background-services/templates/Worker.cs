// purpose: BackgroundService + Channel reader skeleton conforming to 01-core-rules.xml
// consumes: Channel<TItem> + IServiceProvider + ILogger<T>
// produces: code artefact matching 02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~500 tokens when loaded as reference

using System.Threading.Channels;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Faion.Workers;

public sealed class OrderProcessorService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<OrderProcessorService> _logger;
    private readonly Channel<int> _channel;

    public OrderProcessorService(
        IServiceProvider serviceProvider,
        ILogger<OrderProcessorService> logger,
        Channel<int> channel)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
        _channel = channel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var orderId in _channel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                await ProcessAsync(orderId, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed processing order {OrderId}", orderId);
            }
        }
    }

    private async Task ProcessAsync(int orderId, CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var service = scope.ServiceProvider.GetRequiredService<IOrderService>();
        await service.ProcessAsync(orderId, ct);
    }
}

public interface IOrderService
{
    Task ProcessAsync(int orderId, CancellationToken ct);
}
