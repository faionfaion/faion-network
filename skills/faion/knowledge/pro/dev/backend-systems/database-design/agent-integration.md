# Agent Integration — Database Design (PostgreSQL focus)

## When to use
- Greenfield schema design for a relational backend (PostgreSQL, MySQL, MariaDB).
- Adding a new bounded context / aggregate to an existing service that needs its own tables.
- Refactoring a denormalized "god table" into 3NF or extracting a sparse subset into its own table.
- Designing audit trails, soft-delete, partitioning, materialized views for reporting.
- Generating migrations (Alembic, Flyway, sqlx, Goose, golang-migrate, Prisma) from a target schema.
- Choosing indexes for a known query workload identified via `pg_stat_statements`.

## When NOT to use
- Pure document/event-sourced systems — use `nosql-patterns/` and an event store (EventStoreDB, Kafka).
- Graph-heavy domains (social, fraud, bill-of-materials) — Neo4j/Postgres-AGE patterns instead.
- Time-series with billions of rows/day — TimescaleDB/InfluxDB-specific design rules dominate.
- Wide-column analytical workloads — ClickHouse/BigQuery design patterns instead.
- Schemaless ingestion ("we'll figure out the schema later") — that's a debt signal, not a design.

## Where it fails / limitations
- "Normalize first, denormalize for performance" assumes you have a query workload to optimize against; new projects don't have one yet — over-normalizing slows the first 6 months.
- UUID primary keys (especially v4) hurt B-tree locality; prefer UUIDv7 or ULID for time-ordered inserts at scale.
- Triggers (audit, sync) couple business logic to the DB and silently break tests; many shops ban them.
- Materialized views need a refresh strategy (concurrent + lock contention); naive `REFRESH` blocks readers.
- Range partitioning by date helps reads but complicates UPDATE/DELETE across boundaries; default ON CONFLICT semantics differ.
- Soft deletes (`deleted_at IS NULL`) hide data but every query must filter; agents forget.
- Cross-DB portability is a myth: `gen_random_uuid()`, `JSONB`, partial indexes are PG-specific.

## Agentic workflow
The agent should (1) read existing migrations and ER diagram (or extract schema via `pg_dump --schema-only`), (2) propose new tables/columns with constraints (`CHECK`, `NOT NULL`, `UNIQUE`, FK + ON DELETE), (3) propose indexes derived from the stated query patterns, (4) emit a forward+backward migration in the project's migration tool, (5) generate seed/fixture data and a smoke query for each index. The most common failure is choosing PK type and FK ON DELETE semantics late — these are sticky decisions; prompt the agent to surface them up front. For schema audits, the agent should run `EXPLAIN (ANALYZE, BUFFERS)` against representative queries before recommending an index.

### Recommended subagents
- `faion-sdd-executor-agent` — drives schema change as an SDD task; gates: migration applies on a clean DB, downgrade reverses cleanly, all integration tests pass.
- An architect (Opus) for the normalize/denormalize trade-off and partitioning strategy; an implementer (Sonnet) for migration boilerplate.
- A reviewer subagent armed with `pg_stat_statements` snapshots to validate index choices.

### Prompt pattern
```
Design schema for <bounded context>. Entities: <list>. Read access patterns: <queries>.
Write rate: <ops/sec>. Output: (1) DDL with FKs, CHECK, UNIQUE; (2) indexes derived
from access patterns with rationale; (3) Alembic up/down; (4) seed data SQL.
Choose PK type and justify (UUIDv7 vs bigserial). No triggers without explicit ask.
```

```
Audit this schema against these queries from pg_stat_statements (top 20). For each
slow query, propose either an index or a rewrite. Show EXPLAIN before/after.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `psql` | Interactive shell, `\d+`, `EXPLAIN` | bundled with PostgreSQL |
| `pg_dump --schema-only` | Snapshot current schema for diffs | bundled |
| `pgcli` | Better psql with autocomplete | https://www.pgcli.com |
| `alembic` | Python migrations (SQLAlchemy) | https://alembic.sqlalchemy.org |
| `golang-migrate` | Language-agnostic migrations | https://github.com/golang-migrate/migrate |
| `sqlx-cli` | Rust migrations + offline check | https://github.com/launchbadge/sqlx |
| `flyway` / `liquibase` | JVM-world migrations | https://flywaydb.org · https://www.liquibase.org |
| `pgloader` | Migrate from MySQL/SQLite/CSV to PG | https://pgloader.io |
| `pgbadger` | Slow-query log analyzer | https://pgbadger.darold.net |
| `dbdocs` / `schemaspy` | ER diagram from live DB | https://dbdocs.io |
| `pg_repack` | Online table repacking (no exclusive lock) | https://reorg.github.io/pg_repack/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Supabase | SaaS PG | Yes (CLI + REST) | Schema diff + migrations, RLS-first design. |
| Neon | SaaS PG (serverless) | Yes (REST + CLI) | Branching makes agent-driven schema experiments cheap. |
| Crunchy Bridge | SaaS | Yes | PG with extensions exposed. |
| AWS RDS / Aurora | SaaS | Yes (CLI + IaC) | Parameter groups matter; agent must read them. |
| pganalyze | SaaS | Yes (REST API) | Index advisor + query insights consumable by agents. |
| dbdocs.io | SaaS | Yes (DBML) | Agent can emit DBML for review docs. |
| DBeaver | OSS GUI | Indirect | Human-in-loop review of agent-proposed schemas. |
| Atlas | OSS / SaaS | Yes (HCL + CLI) | Declarative schema-as-code; great for agents. |

## Templates & scripts
See `templates.md`. Inline script that diffs DDL against an existing DB and prints proposed migration:

```bash
#!/usr/bin/env bash
# scripts/schema_diff.sh  proposed.sql  postgres://...
set -euo pipefail
PROPOSED="$1"; DB_URL="$2"
TMPDIR=$(mktemp -d); trap 'rm -rf "$TMPDIR"' EXIT
pg_dump --schema-only --no-owner --no-privileges "$DB_URL" \
  | sed -E '/^--/d;/^SET /d;/^SELECT pg_/d' > "$TMPDIR/current.sql"
pg_dump --schema-only --no-owner --no-privileges \
  -d "$(createdb -T template0 _diff_$$)" >/dev/null
psql -d "_diff_$$" -f "$PROPOSED" >/dev/null
pg_dump --schema-only --no-owner --no-privileges -d "_diff_$$" \
  | sed -E '/^--/d;/^SET /d;/^SELECT pg_/d' > "$TMPDIR/proposed.sql"
dropdb "_diff_$$"
diff -u "$TMPDIR/current.sql" "$TMPDIR/proposed.sql" || true
```

## Best practices
- Decide PK type globally (`UUIDv7`, `bigserial`, `ULID`) and stick to it; mixed PK types make joins ugly.
- Always `ON DELETE` explicit (`CASCADE`, `RESTRICT`, `SET NULL`) — the default `NO ACTION` surprises people.
- Prefer `TIMESTAMPTZ` (UTC always) over `TIMESTAMP`; agents picking `TIMESTAMP` is the #1 cross-timezone bug.
- Use `CHECK` constraints for enums via varchar; native ENUMs are hard to alter.
- Index for the queries you have, not the queries you imagine; review `pg_stat_statements` first.
- Partial indexes (`WHERE deleted_at IS NULL`, `WHERE status = 'pending'`) often beat composite indexes for skewed data.
- Run all migrations on a copy of prod before merge; trivial-looking `ALTER TABLE … ADD COLUMN NOT NULL DEFAULT` rewrites the table on PG <11.
- Ban triggers in app schema unless explicitly approved; replace with app-level events or `pgaudit` extension.
- Document every index purpose in a comment (`COMMENT ON INDEX ... IS '...'`); makes future audits cheap.

## AI-agent gotchas
- LLMs default to `VARCHAR(255)` everywhere — the limit is folklore from MySQL pre-5.0.3 and meaningless on PG. Require `TEXT` with explicit `CHECK (length(...))` only when justified.
- Agents drop FKs "for performance" without measuring; schema integrity erodes silently. Force them to keep FKs unless a benchmark shows >10% impact.
- Generated `CASCADE DELETE` chains can wipe terabytes; review every `ON DELETE CASCADE` against business rules.
- Migrations from agents commonly omit `downgrade` or write a no-op; require both directions to apply on a clean DB.
- LLMs use `NOW()` in `DEFAULT` and forget the timezone; insist on `now() AT TIME ZONE 'UTC'` or use `TIMESTAMPTZ`.
- Agents write `CREATE INDEX` synchronously in production migrations; require `CREATE INDEX CONCURRENTLY` outside a transaction for big tables.
- Auto-generated audit triggers reference `current_user`/`session_user` which is the DB role, not the app user. Agent must wire app-level user via `SET LOCAL app.user_id`.
- Human-in-loop checkpoint: every PK-type, partitioning, or sharding decision; these are nearly impossible to reverse on prod.
- Type-mismatch FKs (`INTEGER` referring to `BIGINT`) silently disable index usage on join — require matching types.
- Agents propose materialized views without a refresh job; the view becomes a stale liability. Require a documented refresh strategy.

## References
- PostgreSQL docs: https://www.postgresql.org/docs/current/
- Use The Index, Luke: https://use-the-index-luke.com/
- PostgreSQL Partitioning: https://www.postgresql.org/docs/current/ddl-partitioning.html
- Designing Data-Intensive Applications (Kleppmann)
- The Art of PostgreSQL (Fontaine)
- Atlas (declarative): https://atlasgo.io
- pganalyze blog: https://pganalyze.com/blog
- pg_stat_statements: https://www.postgresql.org/docs/current/pgstatstatements.html
