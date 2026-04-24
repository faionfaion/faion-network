# Agent Integration — Entity Framework Core Patterns

## When to use
- Designing or refactoring EF Core data layer for a .NET 6+ service: entity configurations via `IEntityTypeConfiguration<T>`, repository abstractions, paged query objects.
- Generating migrations from a clean domain model rather than database-first scaffolding, so an agent can iterate Schema → Migration → Test → Apply.
- Performance-tuning N+1 queries, projection vs. tracking decisions, and adding compiled queries.
- Splitting read vs. write concerns (CQRS-lite) where commands use `DbContext.SaveChanges` and queries use `AsNoTracking()` projections.

## When NOT to use
- The codebase uses Dapper or raw ADO.NET intentionally for hot paths — don't insert EF; treat it as off-limits.
- Read-only data warehouse / OLAP — use Dapper/ClickHouse client; EF Core's change tracking is pure overhead.
- Cross-database migrations where EF's provider gaps matter (e.g., Postgres-specific JSONB ops, advisory locks) — drop to raw SQL via `FromSqlInterpolated`.
- Sub-millisecond latency requirements — EF's expression-tree compilation and tracking can add 5–10 ms even with `AsNoTracking`.

## Where it fails / limitations
- LLM-generated `Include` chains explode into Cartesian joins; an agent must check the generated SQL, not just the LINQ. Use `AsSplitQuery()` or projection.
- Migrations created by agents on top of pending model changes accumulate "shadow" properties or rename mistakes when the agent didn't read the prior `ModelSnapshot.cs`.
- `OnDelete(DeleteBehavior.Cascade)` defaults silently create cycles in SQL Server; agent must inspect the generated migration before applying.
- Tracking and identity-map collisions: agents that fetch the same entity twice and call `Update` produce `InvalidOperationException` unless `AsNoTracking` is used on the read.
- EF Core 8/9 changed JSON column behavior, complex types, and primitive-collection mapping; agents trained on EF 6 / EF Core 3 advice produce wrong code.

## Agentic workflow
A subagent generates the entity, configuration, and repository in one pass, then runs `dotnet ef migrations add` against a SQLite scratch DB to validate the schema before producing the SQL Server / Postgres migration. A second sonnet pass reviews the generated SQL via `dotnet ef migrations script` for cascade cycles, missing indexes on FKs, and oversized varchar defaults. Performance audits use `dotnet ef dbcontext optimize` and `EF.CompileQuery` for hot reads.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrates "design → migration → test → review" with quality gates that block on raw SQL diff.
- `faion-backend-agent` — domain model design (aggregate boundaries, value objects, owned entities).
- A custom `ef-migrations-reviewer` (sonnet) scoped to `Read` + `Bash(dotnet ef migrations script:*)` — can't apply destructive migrations.

### Prompt pattern
```
Add entity <Name> with fields <...>. Write IEntityTypeConfiguration<Name>
in Data/Configurations. Create migration AddName against SQLite scratch DB,
then output `dotnet ef migrations script` SQL. Do NOT apply to production.
Flag any cascade delete that creates a cycle.
```

```
Optimize <Repository.GetX>. Read current generated SQL via
`dotnet ef dbcontext optimize` or QueryString. Replace Include chains
with projection where possible. Justify each AsNoTracking / AsSplitQuery.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet ef` | Migrations, scaffolding, dbcontext info | `dotnet tool install -g dotnet-ef` |
| `dotnet ef migrations script` | Generate idempotent SQL | bundled with `dotnet-ef` |
| `dotnet ef dbcontext optimize` | Pre-compile model, find issues | EF Core 7+ |
| `EFCore.NamingConventions` | snake_case / camelCase auto-config | NuGet |
| `Npgsql.EntityFrameworkCore.PostgreSQL` | Postgres provider | NuGet |
| `Microsoft.EntityFrameworkCore.Sqlite` | Scratch DB for migration tests | NuGet |
| `EFCore.BulkExtensions` | Bulk insert/update/delete | NuGet |
| `Respawn` | Reset DB state between tests | NuGet |
| `dotnet ef database update` | Apply migrations (HUMAN-IN-LOOP for prod) | bundled |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Azure SQL / Postgres Flexible | SaaS | Yes | EF connects via standard providers; `dotnet ef` works against both. |
| RDS Postgres / Aurora | SaaS | Yes | Same. Use IAM auth tokens via Npgsql data source. |
| Liquibase / DbUp | OSS | Partial | Sometimes preferred over `dotnet ef` for prod migrations; agent emits SQL, ops applies. |
| Azure Data Studio / pgAdmin | App | Human-only | Visual review of migration SQL. |
| Datadog APM, MiniProfiler | SaaS / OSS | Yes | Captures EF SQL + duration; agents can read traces. |

## Templates & scripts
See `templates.md` for `IEntityTypeConfiguration<T>` and repository skeletons. Inline migration-safety check:

```bash
#!/usr/bin/env bash
# safe-migration.sh - block agent from applying without script review
set -euo pipefail
NAME="${1:?migration name}"
PROJ="${2:?project path}"
dotnet ef migrations add "$NAME" --project "$PROJ" --no-build
SCRIPT=$(mktemp).sql
dotnet ef migrations script --idempotent --project "$PROJ" -o "$SCRIPT"
echo "=== Review SQL: $SCRIPT ==="
grep -iE 'DROP|CASCADE|TRUNCATE|RENAME COLUMN' "$SCRIPT" && {
  echo "DESTRUCTIVE OPS DETECTED — human approval required"; exit 2;
} || echo "Migration looks safe (auto-check)"
```

## Best practices
- Always extract `IEntityTypeConfiguration<T>` into separate files; `OnModelCreating` becomes unmaintainable past 5 entities.
- Use `HasConversion` for value objects (Money, Email) — keeps the domain pure without infra leakage.
- Add `[ConcurrencyCheck]` or `RowVersion` on aggregate roots; without it, last-write-wins silently corrupts data.
- Prefer projection (`Select(x => new Dto { ... })`) over `Include` + manual mapping — fewer columns, no tracking overhead.
- Index FKs explicitly; EF 6 added them automatically, EF Core does not for some cases.
- Pool `DbContext` via `AddDbContextPool` for high-throughput APIs; not for scoped services holding state.
- Owned types for value objects; inheritance (`HasDiscriminator`) only when you really need polymorphism in queries.

## AI-agent gotchas
- Agents conflate EF 6 (`DbSet.Find` + `SaveChanges` semantics) with EF Core; pin the EF Core major version in the prompt.
- LLMs love `_context.Users.FirstOrDefault(u => u.Email == email)` without `.ToLower()` on both sides — case-sensitivity bugs silently differ between SQL Server (CI) and Postgres.
- Generated `OnDelete(DeleteBehavior.Cascade)` on multiple paths produces SQL Server `FK_...` cycle errors; agent must compile + apply migration to verify.
- `async`/`await` on every EF call, including `await _context.SaveChangesAsync()` inside `Task.Run` — cargo cult; agent should keep `await` but never wrap in `Task.Run` for I/O.
- Cross-cutting concerns (audit fields, soft delete) are often inserted ad-hoc per entity; agent should propose a `SaveChangesInterceptor` instead.
- Human-in-loop checkpoint: any migration that touches > 1 table or includes `RENAME` / `DROP COLUMN` — review before apply.
- Agents tend to use `_context.Database.ExecuteSqlRaw` with string concatenation; force `ExecuteSqlInterpolated` for parameterization.

## References
- EF Core docs: https://learn.microsoft.com/ef/core/
- Migrations: https://learn.microsoft.com/ef/core/managing-schemas/migrations/
- Performance: https://learn.microsoft.com/ef/core/performance/
- Jon P. Smith, "Entity Framework Core in Action" (3rd ed., EF Core 7+)
- Andrew Lock — "Configuring DbContext with options" series: https://andrewlock.net
- Npgsql for EF Core: https://www.npgsql.org/efcore/
