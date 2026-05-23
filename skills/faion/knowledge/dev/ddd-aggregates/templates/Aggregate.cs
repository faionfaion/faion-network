// purpose: C# aggregate root with private setters + collected events
// consumes: domain constructor inputs
// produces: aggregate class for the Domain project
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~350 tokens when loaded as reference

namespace Faion.Domain.Orders;

public sealed class Order
{
    private readonly List<OrderItem> _items = new();
    private readonly List<object> _events = new();

    public Guid Id { get; private set; }
    public Guid CustomerId { get; private set; }
    public OrderStatus Status { get; private set; } = OrderStatus.Draft;
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();
    public IReadOnlyList<object> Events => _events.AsReadOnly();

    private Order() { }

    public Order(Guid id, Guid customerId)
    {
        if (customerId == Guid.Empty) throw new ArgumentException("customer required", nameof(customerId));
        Id = id;
        CustomerId = customerId;
        Status = OrderStatus.Draft;
    }

    public void AddItem(string sku, decimal price, int quantity)
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException($"cannot modify order in status {Status}");
        _items.Add(new OrderItem(sku, price, quantity));
    }

    public void Place()
    {
        if (_items.Count == 0)
            throw new InvalidOperationException("cannot place empty order");
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException($"cannot place order in status {Status}");
        Status = OrderStatus.Placed;
        _events.Add(new OrderPlaced(Id, CustomerId, DateTime.UtcNow));
    }

    public void Cancel()
    {
        if (Status == OrderStatus.Shipped)
            throw new InvalidOperationException("cannot cancel shipped order");
        Status = OrderStatus.Cancelled;
        _events.Add(new OrderCancelled(Id, DateTime.UtcNow));
    }

    public List<object> CollectEvents()
    {
        var snapshot = _events.ToList();
        _events.Clear();
        return snapshot;
    }
}

public sealed record OrderItem(string Sku, decimal Price, int Quantity);
public enum OrderStatus { Draft, Placed, Shipped, Cancelled }
public sealed record OrderPlaced(Guid OrderId, Guid CustomerId, DateTime OccurredAt);
public sealed record OrderCancelled(Guid OrderId, DateTime OccurredAt);
