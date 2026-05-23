// purpose: Service + DI skeleton conforming to scoped-dbcontext + asnotracking-reads rules
// consumes: AppDbContext + CancellationToken
// produces: service class behind the controller
// depends-on: content/01-core-rules.xml, templates/FeatureController.cs
// token-budget-impact: ~250 tokens when loaded as reference

using Microsoft.EntityFrameworkCore;

namespace Faion.Features.Orders;

public interface IOrdersService
{
    Task<OrderResponse?> GetAsync(int id, CancellationToken ct);
    Task<OrderResponse> CreateAsync(CreateOrderRequest req, CancellationToken ct);
}

public sealed class OrdersService : IOrdersService
{
    private readonly AppDbContext _db;

    public OrdersService(AppDbContext db) => _db = db;

    public Task<OrderResponse?> GetAsync(int id, CancellationToken ct) =>
        _db.Orders
            .AsNoTracking()
            .Where(o => o.Id == id)
            .Select(o => new OrderResponse(o.Id, o.CustomerName, o.Total))
            .FirstOrDefaultAsync(ct);

    public async Task<OrderResponse> CreateAsync(CreateOrderRequest req, CancellationToken ct)
    {
        var order = new Order(req.CustomerName, req.Total);
        _db.Orders.Add(order);
        await _db.SaveChangesAsync(ct);
        return new OrderResponse(order.Id, order.CustomerName, order.Total);
    }
}

public sealed class Order
{
    public int Id { get; private set; }
    public string CustomerName { get; private set; } = "";
    public decimal Total { get; private set; }
    private Order() { }
    public Order(string customerName, decimal total)
    {
        CustomerName = customerName;
        Total = total;
    }
}

public sealed class AppDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public AppDbContext(DbContextOptions<AppDbContext> opt) : base(opt) { }
}
