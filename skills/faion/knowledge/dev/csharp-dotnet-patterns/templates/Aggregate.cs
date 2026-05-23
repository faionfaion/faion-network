// purpose: Aggregate root with no public setters, intention-revealing methods
// consumes: order construction inputs
// produces: aggregate type in Domain layer
// depends-on: content/01-core-rules.xml, ddd-aggregates methodology
// token-budget-impact: ~250 tokens when loaded as reference

namespace Faion.Domain.Orders;

public sealed class Order
{
    private readonly List<object> _events = new();

    public int Id { get; private set; }
    public string CustomerName { get; private set; } = "";
    public OrderStatus Status { get; private set; } = OrderStatus.Pending;
    public string? Carrier { get; private set; }
    public DateTime? ShippedAt { get; private set; }

    public IReadOnlyList<object> Events => _events.AsReadOnly();

    private Order() { }

    public Order(string customerName)
    {
        if (string.IsNullOrWhiteSpace(customerName))
            throw new ArgumentException("customer name required", nameof(customerName));
        CustomerName = customerName;
        Status = OrderStatus.Pending;
    }

    public void Ship(string carrier, DateTime when)
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException($"cannot ship order in state {Status}");
        if (string.IsNullOrWhiteSpace(carrier))
            throw new ArgumentException("carrier required", nameof(carrier));
        Status = OrderStatus.Shipped;
        Carrier = carrier;
        ShippedAt = when;
        _events.Add(new OrderShipped(Id, carrier, when));
    }

    public void Cancel()
    {
        if (Status == OrderStatus.Shipped)
            throw new InvalidOperationException("cannot cancel shipped order");
        Status = OrderStatus.Cancelled;
        _events.Add(new OrderCancelled(Id));
    }
}

public enum OrderStatus { Pending, Shipped, Cancelled }
public sealed record OrderShipped(int OrderId, string Carrier, DateTime ShippedAt);
public sealed record OrderCancelled(int OrderId);
