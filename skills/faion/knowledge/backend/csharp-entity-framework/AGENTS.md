# Entity Framework Core Patterns

## Summary

**One-sentence:** EF Core data-layer methodology for .NET 6+ services — `IEntityTypeConfiguration<T>` per entity, repository abstractions, paged query objects, AsNoTracking discipline, and migration safety.

**One-paragraph:** EF Core data layer for .NET 6+ services: every entity gets its own `IEntityTypeConfiguration<T>`; `OnModelCreating` calls `ApplyConfigurationsFromAssembly(...)` and nothing else. Read paths use `AsNoTracking()`. Aggregate roots carry `RowVersion`/`[ConcurrencyCheck]`. Bulk writes use `ExecuteUpdateAsync`/`ExecuteDeleteAsync`. Cross-cutting audit fields (CreatedAt, UpdatedBy) live in a `SaveChangesInterceptor`, never per-entity. Migrations are reviewed as SQL via `dotnet ef migrations script` before any prod apply.

**Ефективно для:**

- Designing or refactoring the EF Core data layer for a .NET 6+ service.
- Generating migrations from a clean domain model (not database-first scaffolding).
- Performance-tuning N+1 queries, projection vs tracking trade-offs, compiled queries.
- Splitting read/write concerns (CQRS-lite) where commands use SaveChanges and queries use `AsNoTracking()` projections.

## Applies If (ALL must hold)

- Designing or refactoring the EF Core data layer for a .NET 6+ service.
- Generating migrations from a clean domain model (not database-first scaffolding).
- Splitting read/write concerns where commands use SaveChanges and queries use `AsNoTracking()` projections.

## Skip If (ANY kills it)

- Codebase uses Dapper or raw ADO.NET intentionally for hot paths — do not insert EF.
- Read-only OLAP / data warehouse — change tracking is pure overhead; use Dapper.
- Cross-database migrations where EF provider gaps matter (Postgres JSONB ops, advisory locks) — drop to `FromSqlInterpolated` for those paths.
- Sub-millisecond latency requirements — EF expression-tree compilation adds 5-10 ms even with `AsNoTracking`.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Domain entity model | C# classes or ERD | domain modelling |
| Target DB provider | `Npgsql` / `SqlServer` / `Sqlite` | platform |
| Migration safety policy | Markdown checklist | DBA / SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Umbrella covering DI lifetimes that govern DbContext scope. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: entity-config-per-entity, asnotracking-on-reads, no-iqueryable-return, splitquery-multi-include, entity-private-setters, append-only-migrations, concurrency-token-on-aggregates, bulk-execute-update-delete, savechanges-interceptor-for-audit, migration-sql-review | 1800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the EF data-layer manifest incl. per-entity and per-repository flags + migration append check, with valid/invalid examples | 1100 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom/root-cause/fix, incl. lazy-loading-proxies and edited-migration | 1200 |
| `content/04-procedure.xml` | essential | 7-step procedure: scope DbContext → entities → configurations → repositories → split-query audit → audit interceptor + tokens → migration safety | 1100 |
| `content/05-examples.xml` | essential | Entity, configuration, repository read path, bulk write, and the two query shapes the rules prevent | 1300 |
| `content/06-decision-tree.xml` | essential | Scope gate on workload shape + flat defect router mapping signals to a rule from 01-core-rules.xml | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-entity` | sonnet | Translating domain entity to `IEntityTypeConfiguration<T>` requires judgment. |
| `optimise-query` | sonnet | N+1 + projection trade-offs need analysis. |
| `review-migration` | opus | Destructive migration risk — needs careful reasoning. |
| `audit-asnotracking` | haiku | Mechanical scan for read paths missing AsNoTracking. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Entity.cs` | POCO entity with private setters, EF parameterless constructor and read-only collections. |
| `templates/entity-configuration.cs` | `IEntityTypeConfiguration<T>` skeleton for one aggregate. |
| `templates/repository.cs` | Repository returning `PagedResult<TDto>` with AsNoTracking, AsSplitQuery and CancellationToken threading. |
| `templates/safe-migration.sh` | Wrapper around `dotnet ef migrations script` for SQL review before apply. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-entity-framework.py` | Validate the EF data-layer manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[csharp-dotnet]]
- [[csharp-dotnet-patterns]]
- [[csharp-xunit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (read vs write path, latency budget, provider, concurrency requirement) to a rule from `01-core-rules.xml`. Use it before scaffolding a new entity or refactoring a hot query.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/entity-configuration.cs`

```csharp
// IEntityTypeConfiguration<T> skeleton
// One file per entity. Replace: TEntity, table name, property names.

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace MyApp.Data.Configurations;

public class ExampleEntityConfiguration : IEntityTypeConfiguration<ExampleEntity>
{
    public void Configure(EntityTypeBuilder<ExampleEntity> builder)
    {
        builder.ToTable("example_entities");

        builder.HasKey(e => e.Id);

        builder.Property(e => e.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(e => e.Email)
            .IsRequired()
            .HasMaxLength(255);

        builder.HasIndex(e => e.Email).IsUnique();

        builder.Property(e => e.CreatedAt)
            .HasDefaultValueSql("CURRENT_TIMESTAMP");

        // Optimistic concurrency: required on aggregate roots
        builder.Property(e => e.RowVersion)
            .IsRowVersion();

        // Many-to-many via junction table
        builder.HasMany(e => e.Tags)
            .WithMany(t => t.Entities)
            .UsingEntity<Dictionary<string, object>>(
                "entity_tags",
                j => j.HasOne<Tag>().WithMany().HasForeignKey("TagId"),
                j => j.HasOne<ExampleEntity>().WithMany().HasForeignKey("EntityId")
            );

        // One-to-many (SetNull on parent delete — avoid Cascade to prevent cycles)
        builder.HasMany(e => e.Items)
            .WithOne(i => i.Entity)
            .HasForeignKey(i => i.EntityId)
            .OnDelete(DeleteBehavior.SetNull);

        // Explicitly index FK — EF Core does not always add these
        builder.HasIndex(e => e.CategoryId);
    }
}
```

### `templates/repository.cs`

```csharp
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
```

### `templates/safe-migration.sh`

```bash
# safe-migration.sh — generate migration + block on destructive SQL ops
# Usage: bash safe-migration.sh <MigrationName> <project-path>
# Example: bash safe-migration.sh AddUserEmailIndex src/MyApp.Data/
set -euo pipefail

NAME="${1:?migration name required}"
PROJ="${2:?project path required}"

echo "=== Adding migration: $NAME ==="
dotnet ef migrations add "$NAME" --project "$PROJ" --no-build

SCRIPT=$(mktemp --suffix=.sql)
echo "=== Generating idempotent SQL to: $SCRIPT ==="
dotnet ef migrations script --idempotent --project "$PROJ" -o "$SCRIPT"

echo "=== Checking for destructive operations ==="
if grep -iE 'DROP TABLE|DROP COLUMN|TRUNCATE|RENAME COLUMN|CASCADE' "$SCRIPT"; then
    echo ""
    echo "DESTRUCTIVE OPERATIONS DETECTED — human approval required before apply"
    echo "Review: $SCRIPT"
    exit 2
fi

echo "Migration looks safe (auto-check). Review SQL before applying to non-dev environments."
echo "SQL script: $SCRIPT"
echo ""
echo "To apply: dotnet ef database update --project $PROJ"
```

### `templates/Entity.cs`

```csharp
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
```
