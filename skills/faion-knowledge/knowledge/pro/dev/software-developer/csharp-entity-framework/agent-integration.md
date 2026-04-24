# Agent Integration — Entity Framework Core

## When to use
- ASP.NET Core / .NET worker services that need an ORM with LINQ, change tracking, migrations, and provider portability.
- Domain models with rich relationships (one-to-many, many-to-many, owned types, TPH/TPT inheritance).
- Read paths that benefit from compiled queries and EF 8+ JSON column support.
- CQRS-flavored apps where commands use the tracked context and queries use `AsNoTracking()` projections.
- Greenfield work that needs first-class migration tooling (`dotnet ef migrations add`).

## When NOT to use
- High-throughput analytical workloads — Dapper, plain ADO.NET, or `Microsoft.Data.SqlClient` outperform EF for read-heavy hot paths.
- Stored-procedure-heavy systems where the DBA owns all SQL — EF mapping fights the existing model.
- Streaming / bulk inserts of millions of rows — use `SqlBulkCopy`, `Npgsql COPY`, or `EFCore.BulkExtensions`.
- DBs without a strong EF provider (some NoSQL, niche RDBMSes) — pick a native client.
- Tight memory environments (AOT trimming) where EF reflection footprint matters; consider Dapper + manual mapping.

## Where it fails / limitations
- Lazy loading via proxies (`UseLazyLoadingProxies()`) is the single most-frequent N+1 cause; agents enable it because tutorials do, then performance collapses.
- `DbContext` is not thread-safe and has scoped lifetime — captured by a singleton service or shared across `Task.WhenAll` ⇒ corruption / `InvalidOperationException`.
- `Include` chains over collections explode result sets (Cartesian explosion); EF 5+ `AsSplitQuery()` mitigates but is opt-in.
- Migrations require the project to compile — a half-renamed entity blocks `migrations add`. Agents leave the project in a broken state.
- `Update()` marks every property as modified, including null nav-props; partial updates need attaching + setting `EntityState.Modified` on specific properties.
- Connection pooling (`AddDbContextPool`) caches contexts; mutating `ChangeTracker.Tracked` settings on one request leaks to the next.
- `DbContext.Database.EnsureCreated()` and `migrations` cannot coexist on the same DB — using both corrupts the migrations history table.

## Agentic workflow
A subagent generates the entity, the `IEntityTypeConfiguration<T>` (separate file under `Data/Configurations/`), the migration via `dotnet ef migrations add <Name>`, and the repository / query method. Quality gates: `dotnet build -warnaserror`, `dotnet ef migrations script` to inspect generated SQL, `dotnet test` (with SQLite or Testcontainers Postgres). The agent must verify the migration is idempotent and reversible (`Down()` populated).

### Recommended subagents
- `faion-feature-executor` — slice work where entity, configuration, migration, and repository are produced together.
- `faion-sdd-executor-agent` — gates on build/tests/format.

### Prompt pattern
```
Add EF Core entity <Name> with: <fields>. Place IEntityTypeConfiguration<<Name>> in Data/Configurations/<Name>Configuration.cs. Add unique index on <field>, FK to <Other> with DeleteBehavior.Restrict. Run dotnet ef migrations add Add<Name>, inspect generated SQL via dotnet ef migrations script, ensure idempotency. Add repository method GetBy<Field>Async with AsNoTracking() and Include only when necessary.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet ef migrations add/remove/list/script` | Migration management | `dotnet tool install --global dotnet-ef` |
| `dotnet ef database update/drop` | Apply/revert | Same tool |
| `dotnet ef dbcontext scaffold` | Reverse engineer existing DB | Same tool |
| `dotnet ef dbcontext optimize` | Generate compiled model (.NET 8+) | Same tool |
| `dotnet build -warnaserror` | Catches misconfigured entities | Built-in |
| `EFCore.Visualizer` (Rider/VS extension) | Visualize DbContext model | Marketplace |
| `EFCore.NamingConventions` | snake_case mapping for Postgres | NuGet |
| `EFCore.BulkExtensions` | Bulk insert/update/delete | NuGet |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Npgsql.EntityFrameworkCore.PostgreSQL | OSS | Yes | First-class Postgres provider. |
| Microsoft.EntityFrameworkCore.SqlServer | OSS | Yes | First-party SQL Server provider. |
| Pomelo.EntityFrameworkCore.MySql | OSS | Yes | MySQL/MariaDB provider. |
| Microsoft.EntityFrameworkCore.Sqlite | OSS | Yes | Tests + dev. |
| Testcontainers.PostgreSql / MsSql | OSS | Yes | Real DB integration tests. |
| Respawn | OSS | Yes | Reset DB between tests. |
| Application Insights / Datadog APM | SaaS | Yes | Auto-traces EF queries. |
| MiniProfiler | OSS | Yes | Visualize SQL per request in dev. |

## Templates & scripts
See templates.md and README (Entity Configuration, Repository Pattern). Inline `Program.cs` registration that disables lazy loading and enables sensitive logging only in dev:

```csharp
builder.Services.AddDbContextPool<AppDbContext>((sp, options) =>
{
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default"))
           .UseSnakeCaseNamingConvention();
    if (builder.Environment.IsDevelopment())
    {
        options.EnableSensitiveDataLogging()
               .EnableDetailedErrors()
               .LogTo(Console.WriteLine, LogLevel.Information);
    }
});
```

## Best practices
- Always use `AsNoTracking()` (or `AsNoTrackingWithIdentityResolution()`) for read paths; reserve tracking for writes.
- Place `IEntityTypeConfiguration<T>` per entity in a dedicated `Data/Configurations` folder; call `modelBuilder.ApplyConfigurationsFromAssembly(...)` once.
- Avoid `Include` chains over multiple collections — use `AsSplitQuery()` or projection to a flat DTO.
- Use compiled queries (`EF.CompileAsyncQuery`) for hot read paths in long-lived apps; or `dotnet ef dbcontext optimize` for the compiled model.
- Migrations: name them with verbs (`AddUserTable`, `AlterUserAddIsActive`); never edit a deployed migration in place — add a new one.
- Pair every entity change with a migration in the same PR; CI should run `dotnet ef migrations script` and diff.
- Use `[ConcurrencyCheck]` or `RowVersion` for optimistic concurrency on user-editable rows.
- Configure `DeleteBehavior` explicitly per FK; never accept the default cascade silently.
- Set `QueryTrackingBehavior.NoTracking` as the default at the DbContext level if your app is mostly read.

## AI-agent gotchas
- Agents enable `UseLazyLoadingProxies()` by default — silently triggers N+1. Disable it; force explicit `Include` / projection.
- `DbContextOptions` mis-registration: agents register `Singleton` or `Transient` — `Scoped` is the correct lifetime, `AddDbContextPool` is the right factory for ASP.NET Core.
- New entity but no `DbSet<>` on the context — code compiles, runtime LINQ throws "entity not part of model". Agent must add the `DbSet<T>` AND the configuration.
- Modifying a deployed migration: agents "fix" a generated migration file rather than adding a new one, breaking environments that already applied it. Reject any commit that edits a migration whose timestamp predates the current branch's main merge.
- `dotnet ef migrations add` requires the project to compile. If the agent broke a different file, the migration step silently fails and the agent moves on. Always run `dotnet build` first.
- `Update()` vs targeted property update: agents call `_context.Update(entity)` after mapping a partial DTO and overwrite fields with `null`/defaults. Use `Entry(entity).CurrentValues.SetValues(dto)` only for matching shapes, or set individual properties.
- Human checkpoint: review every `OnDelete(DeleteBehavior.Cascade)` — most should be `Restrict` or `SetNull`.
- Sensitive data in logs: agents enable `EnableSensitiveDataLogging()` and forget to gate it on `IsDevelopment()`, leaking PII to prod logs.

## References
- https://learn.microsoft.com/ef/core/
- https://learn.microsoft.com/ef/core/performance/
- https://github.com/dotnet/efcore
- https://www.thinktecture.com (deep EF performance posts)
- https://github.com/borisdj/EFCore.BulkExtensions
