// purpose: POCO entity with private setters and constructor invariants
// consumes: domain constructor inputs
// produces: entity type for EF Core mapping
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200 tokens when loaded as reference

using System.Collections.Generic;

namespace Faion.Domain.Orders;

public sealed class Order
{
    private readonly List<OrderItem> _items = new();

    public int Id { get; private set; }
    public string CustomerName { get; private set; } = "";
    public decimal Total { get; private set; }
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();

    private Order() { }

    public Order(string customerName)
    {
        if (string.IsNullOrWhiteSpace(customerName))
            throw new ArgumentException("customer name required", nameof(customerName));
        CustomerName = customerName;
    }

    public void AddItem(OrderItem item)
    {
        _items.Add(item);
        Total += item.Price * item.Quantity;
    }
}

public sealed class OrderItem
{
    public int Id { get; private set; }
    public string Sku { get; private set; } = "";
    public decimal Price { get; private set; }
    public int Quantity { get; private set; }
    private OrderItem() { }
    public OrderItem(string sku, decimal price, int quantity)
    {
        Sku = sku; Price = price; Quantity = quantity;
    }
}
