// purpose: repository pattern that materialises results before returning across the boundary
// consumes: DbContext + entity type T
// produces: repository implementation conforming to asnotracking-on-reads rule
// depends-on: content/01-core-rules.xml rule asnotracking-on-reads
// token-budget-impact: ~400 tokens when loaded as context
// IRepository interface + implementation with paged query and email lookup.
// Replace: TEntity, TDto, property names as needed.
// List methods return PagedResult<TDto> — never IQueryable (no-iqueryable-return).

namespace MyApp.Repositories;

public sealed record ExampleDto(int Id, string Name, string Email);
public sealed record PagedResult<T>(IReadOnlyList<T> Items, int TotalCount, int Page, int PageSize);

public interface IExampleRepository
{
    Task<ExampleEntity?> GetByIdAsync(int id, CancellationToken ct);
    Task<ExampleDto?> GetByEmailAsync(string email, CancellationToken ct);
    Task<PagedResult<ExampleDto>> GetPagedAsync(int page, int pageSize, CancellationToken ct);
    Task AddAsync(ExampleEntity entity, CancellationToken ct);
    void Remove(ExampleEntity entity);
    Task SaveChangesAsync(CancellationToken ct);
}

public class ExampleRepository : IExampleRepository
{
    private readonly AppDbContext _context;

    public ExampleRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<ExampleEntity?> GetByIdAsync(int id, CancellationToken ct)
    {
        // Tracked on purpose: the caller will mutate and save this aggregate.
        return await _context.Examples
            .Include(e => e.Tags)
            .FirstOrDefaultAsync(e => e.Id == id, ct);
    }

    public async Task<ExampleDto?> GetByEmailAsync(string email, CancellationToken ct)
    {
        // Normalize case — SQL Server is CI by default, Postgres is not
        return await _context.Examples
            .AsNoTracking()
            .Where(e => e.Email == email.ToLower())
            .Select(e => new ExampleDto(e.Id, e.Name, e.Email))
            .FirstOrDefaultAsync(ct);
    }

    public async Task<PagedResult<ExampleDto>> GetPagedAsync(
        int page, int pageSize, CancellationToken ct)
    {
        var query = _context.Examples
            .AsNoTracking()
            .Include(e => e.Tags)
            .Include(e => e.Items)
            // Two collection navigations: without this the JOIN multiplies rows.
            .AsSplitQuery()
            .OrderByDescending(e => e.CreatedAt);

        var totalCount = await query.CountAsync(ct);
        var items = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(e => new ExampleDto(e.Id, e.Name, e.Email))
            .ToListAsync(ct);

        return new PagedResult<ExampleDto>(items, totalCount, page, pageSize);
    }

    public async Task AddAsync(ExampleEntity entity, CancellationToken ct) =>
        await _context.Examples.AddAsync(entity, ct);

    public void Remove(ExampleEntity entity) =>
        _context.Examples.Remove(entity);

    public async Task SaveChangesAsync(CancellationToken ct) =>
        await _context.SaveChangesAsync(ct);
}
