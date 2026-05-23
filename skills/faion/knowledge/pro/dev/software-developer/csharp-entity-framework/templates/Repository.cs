// purpose: Repository with PagedResult + AsNoTracking + AsSplitQuery
// consumes: AppDbContext + paging params
// produces: persistence boundary returning materialized DTOs
// depends-on: content/01-core-rules.xml, templates/Entity.cs
// token-budget-impact: ~350 tokens when loaded as reference

using Microsoft.EntityFrameworkCore;

namespace Faion.Infrastructure.Orders;

public sealed record OrderDto(int Id, string CustomerName, decimal Total);
public sealed record PagedResult<T>(IReadOnlyList<T> Items, int TotalCount, int Page, int PageSize);

public interface IOrderRepository
{
    Task<PagedResult<OrderDto>> ListAsync(int page, int pageSize, CancellationToken ct);
    Task<Order?> GetAsync(int id, CancellationToken ct);
    Task AddAsync(Order order, CancellationToken ct);
    Task SaveChangesAsync(CancellationToken ct);
}

public sealed class OrderRepository : IOrderRepository
{
    private readonly AppDbContext _db;

    public OrderRepository(AppDbContext db) => _db = db;

    public async Task<PagedResult<OrderDto>> ListAsync(int page, int pageSize, CancellationToken ct)
    {
        var query = _db.Orders
            .AsNoTracking()
            .Include(o => o.Items)
            .AsSplitQuery();

        var total = await query.CountAsync(ct);
        var items = await query
            .OrderBy(o => o.Id)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(o => new OrderDto(o.Id, o.CustomerName, o.Total))
            .ToListAsync(ct);

        return new PagedResult<OrderDto>(items, total, page, pageSize);
    }

    public Task<Order?> GetAsync(int id, CancellationToken ct) =>
        _db.Orders.Include(o => o.Items).FirstOrDefaultAsync(o => o.Id == id, ct);

    public async Task AddAsync(Order order, CancellationToken ct)
    {
        await _db.Orders.AddAsync(order, ct);
    }

    public Task SaveChangesAsync(CancellationToken ct) => _db.SaveChangesAsync(ct).ContinueWith(_ => { }, ct);
}

public sealed class AppDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public AppDbContext(DbContextOptions<AppDbContext> opt) : base(opt) { }
    protected override void OnModelCreating(ModelBuilder modelBuilder) =>
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
}
