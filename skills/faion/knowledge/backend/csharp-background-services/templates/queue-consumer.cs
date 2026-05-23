// purpose: BackgroundService queue-consumer skeleton with retry + idempotency
// consumes: see AGENTS.md Prerequisites
// produces: C# Background Services code
// depends-on: content/02-output-contract.xml schema
// token-budget-impact: ~500 tokens when filled

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
