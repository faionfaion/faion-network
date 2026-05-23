// purpose: repository pattern that materialises results before returning across the boundary
// consumes: DbContext + entity type T
// produces: repository implementation conforming to asnotracking-on-reads rule
// depends-on: content/01-core-rules.xml rule asnotracking-on-reads
// token-budget-impact: ~400 tokens when loaded as context
// IRepository interface + implementation with paged query and email lookup
// Replace: TEntity, TDto, property names as needed

namespace MyApp.Repositories;

public interface IExampleRepository
{
    Task<ExampleEntity?> GetByIdAsync(int id);
    Task<ExampleEntity?> GetByEmailAsync(string email);
    Task<PagedResult<ExampleEntity>> GetPagedAsync(int page, int pageSize);
    Task AddAsync(ExampleEntity entity);
    void Remove(ExampleEntity entity);
    Task SaveChangesAsync();
}

public class ExampleRepository : IExampleRepository
{
    private readonly AppDbContext _context;

    public ExampleRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<ExampleEntity?> GetByIdAsync(int id)
    {
        // Include only when caller will modify navigation; otherwise project
        return await _context.Examples
            .Include(e => e.Tags)
            .FirstOrDefaultAsync(e => e.Id == id);
    }

    public async Task<ExampleEntity?> GetByEmailAsync(string email)
    {
        // Normalize case — SQL Server is CI by default, Postgres is not
        return await _context.Examples
            .AsNoTracking()
            .FirstOrDefaultAsync(e => e.Email == email.ToLower());
    }

    public async Task<PagedResult<ExampleEntity>> GetPagedAsync(int page, int pageSize)
    {
        var query = _context.Examples
            .AsNoTracking()
            .OrderByDescending(e => e.CreatedAt);

        var totalCount = await query.CountAsync();
        var items = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return new PagedResult<ExampleEntity>(items, totalCount, page, pageSize);
    }

    public async Task AddAsync(ExampleEntity entity) =>
        await _context.Examples.AddAsync(entity);

    public void Remove(ExampleEntity entity) =>
        _context.Examples.Remove(entity);

    public async Task SaveChangesAsync() =>
        await _context.SaveChangesAsync();
}
