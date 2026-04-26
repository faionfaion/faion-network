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
