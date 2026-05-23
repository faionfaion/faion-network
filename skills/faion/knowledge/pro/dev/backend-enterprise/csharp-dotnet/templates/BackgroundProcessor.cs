// purpose: BackgroundService skeleton resolving scoped deps via IServiceScopeFactory
// consumes: Channel<T> bounded queue, IOrderService work unit interface
// produces: hosted service conforming to di-lifetimes rule
// depends-on: content/01-core-rules.xml rule di-lifetimes
// token-budget-impact: ~400 tokens when loaded as context
using System.Threading.Channels;

namespace MyApp.Features.Orders;

public class BackgroundOrderProcessor : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<BackgroundOrderProcessor> _logger;
    private readonly Channel<int> _orderChannel;

    public BackgroundOrderProcessor(
        IServiceScopeFactory scopeFactory,
        ILogger<BackgroundOrderProcessor> logger,
        Channel<int> orderChannel)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
        _orderChannel = orderChannel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Order processor started");

        await foreach (var orderId in _orderChannel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                using var scope = _scopeFactory.CreateScope();
                var svc = scope.ServiceProvider.GetRequiredService<IOrderService>();
                await svc.ProcessAsync(orderId, stoppingToken);
                _logger.LogInformation("Order {OrderId} processed", orderId);
            }
            catch (OperationCanceledException)
            {
                throw;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing order {OrderId}", orderId);
            }
        }
    }
}
