# Agent Integration — Database Design

## When to use
- Greenfield schema for a new product (3NF first, denormalize later with evidence).
- Adding a major feature that touches >2 tables; need ER diagram + migration plan.
- Performance regression triaged to schema (missing index, wrong type, hot row).
- Migrating between engines (Postgres ⇄ MySQL, monolith → sharded, OLTP → OLAP mirror).
- Designing audit trails, soft deletes, multi-tenancy, time-series partitioning.

## When NOT to use
- "Move fast" prototypes where you'll throw away the schema in a week — SQLite + a single denormalized table is fine.
- Read-mostly content sites — a CMS or static generator covers it without a relational model.
- Append-only event logs — pick a time-series DB (TimescaleDB, ClickHouse) instead of fighting Postgres indexes.
- Graph-heavy domains (recommendation, social) — relational JOIN explosions hurt; use Neo4j / dgraph.
- When the team has no ops capacity for migrations / backups — a managed KV (DynamoDB, Firestore) trades schema rigour for zero-ops.

## Where it fails / limitations
- Premature denormalization: agents replicate `user.email` into 5 tables; updates become a fanout consistency problem.
- Hot row contention: a `counters` table with one row per app gets `UPDATE` storms; needs sharded counters or atomic increments.
- Composite indexes ordered wrong: `(status, created_at)` doesn't serve `WHERE created_at > ? ORDER BY status` — column order matters.
- Soft-delete leaks: `deleted_at IS NULL` filter forgotten in JOINs → ghost data resurfaces in admin views.
- Foreign keys with `ON DELETE CASCADE` chained 3+ deep — accidental mass deletes; use `RESTRICT` defaults and explicit cleanup jobs.
- Auto-incrementing PKs leak business info (count of records, growth rate); UUID v4 has random distribution → cold cache; UUID v7 / ULID is the modern compromise.
- Migrations that lock big tables (`ALTER TABLE ADD COLUMN NOT NULL DEFAULT`) cause prod outages; use `pg_repack`, `gh-ost`, or expand-contract pattern.

## Agentic workflow
Schema-first: agent produces an ER diagram (Mermaid or `dbml`) from the spec, gets human sign-off, then generates DDL + migration. Reviewer agent runs `sqlfluff` + `squawk` (Postgres migration linter) and rejects locking statements. Each migration must be reversible (`up` + `down`) and tested against a fixture DB. For indexing, agent profiles top 10 slow queries (`pg_stat_statements`) and proposes indexes only after measuring; never invent indexes from imagination.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → DDL → migration → seeds → tests sequentially with quality gates.
- A custom `migration-reviewer` agent gating any `ALTER TABLE` for locking risk (`squawk`).
- `simplify` skill — strips over-normalized junk (e.g., 1:1 split tables) and over-indexed schemas.

### Prompt pattern
```
Design schema for <feature>.
Inputs:
- Domain: <bounded context>
- Read patterns: <queries with frequency>
- Write patterns: <inserts/updates with rate>
Output:
1. dbml diagram (text).
2. PostgreSQL DDL with CHECK constraints + FKs (ON DELETE explicit).
3. Index plan keyed to read patterns; justify each index.
4. Migration up/down (reversible, no NOT NULL DEFAULT on existing big tables).
Constraints: ULID primary keys, created_at/updated_at on every entity, soft-delete only where business-justified.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| sqlfluff | Multi-dialect SQL linter / formatter | `pip install sqlfluff` |
| squawk | Postgres migration linter (catches locking ALTERs) | `npm i -g squawk-cli` |
| dbmate / sqlx-cli / Alembic / Flyway / Liquibase | Migration tooling | per stack |
| atlas (ariga) | Declarative schema migrations across engines | atlasgo.io |
| pg_repack | Online table rewrite without long locks | apt/yum |
| pgbadger | Postgres log analyser | github.com/darold/pgbadger |
| pg_stat_statements + pgss view | Slow-query enumeration | enable in postgresql.conf |
| dbml-cli | Compile dbml diagrams | `npm i -g @dbml/cli` |
| schemaspy / SchemaCrawler | Reverse-engineer ER diagrams | open source |
| pgtap | TAP-style schema/constraint tests | pgxn |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Postgres (RDS / Aurora / Cloud SQL / Supabase / Neon) | SaaS | Yes — psql + REST | Default OLTP choice. Neon has branching for ephemeral test DBs the agent can spin up per PR. |
| MySQL / PlanetScale / Vitess | SaaS | Yes — CLI + branching | PlanetScale's deploy requests fit agent workflows nicely. |
| TimescaleDB | OSS / SaaS | Yes | Postgres extension for time-series partitioning. |
| ClickHouse | OSS / SaaS (Cloud) | Yes — clickhouse-client | OLAP / analytics counterpart. |
| DynamoDB | SaaS | Yes — IaC | Single-table design — totally different mental model; brief the agent explicitly. |
| Atlas Cloud (ariga) | SaaS | Yes | Schema as code with CI integration. |
| dbdocs.io | SaaS | Yes — `dbdocs build` | Hosts dbml diagrams for review. |
| pganalyze / Datadog DB | SaaS | Yes — REST | Index recommendations, slow-query trend; agent can ingest reports. |

## Templates & scripts
See `templates.md` for E-commerce schema, indexing strategy, audit trail, soft-delete views. Index sanity script:

```sql
-- scripts/unused_indexes.sql (PostgreSQL)
SELECT schemaname, relname, indexrelname,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size,
       idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Best practices
- Start at 3NF; denormalize only with a measured query showing the join is the bottleneck. Document the reason in a comment.
- Every entity table: `id` (ULID/UUIDv7), `created_at`, `updated_at` (timestamptz, default `now()`), updated by trigger.
- Foreign keys explicit `ON DELETE` (default `RESTRICT`); never rely on app-layer cascades.
- CHECK constraints on enums or use Postgres `ENUM` / lookup table; never validate in app only.
- Indexes sized to read patterns; review `pg_stat_user_indexes.idx_scan` quarterly and drop the zeroes.
- Migrations are expand → backfill → contract: add nullable column, backfill in batches, then add `NOT NULL` constraint when 100% populated.
- Backups + PITR tested by restoring monthly; an untested backup is no backup.
- For multi-tenancy: row-level security (RLS) in Postgres or schema-per-tenant; never just `WHERE tenant_id = ?` in app code (one missing filter = data leak).

## AI-agent gotchas
- LLMs default to `INTEGER PRIMARY KEY AUTOINCREMENT`; in Postgres prefer `BIGINT GENERATED ALWAYS AS IDENTITY` or ULID. Pin the choice in the prompt.
- Agents add `ON DELETE CASCADE` everywhere "to be safe"; the result is a single accidental delete wiping half the DB.
- Migrations generated by agents often combine `ALTER TABLE ... NOT NULL` with `DEFAULT` on huge tables → full rewrite + lock. Run `squawk` against every migration.
- Indexes on every column "for performance" — bloats writes. Force a "list query → index" mapping in the spec.
- Agents skip `down` migrations or stub them with `pass`; CI must enforce a real reverse path or explicit irreversible flag.
- Soft-delete added without updating queries: stale data appears. Agent must produce a `_active` view or update every query in the same PR.
- Decimals for money: agents reach for `FLOAT`/`DOUBLE`. Force `NUMERIC(12,2)` (or BIGINT cents) and check constraints `>= 0`.
- Human-in-loop checkpoint: any migration that drops a column, drops a table, or runs >5s on prod-sized data must require explicit human approval.

## References
- "Database Design for Mere Mortals" — Hernandez (still the clearest 3NF intro).
- "Designing Data-Intensive Applications" — Kleppmann (replication, partitioning, consistency).
- Use The Index, Luke — https://use-the-index-luke.com/
- Postgres docs (constraints, indexes, RLS) — https://www.postgresql.org/docs/current/
- squawk — https://squawkhq.com/
- pganalyze index advisor — https://pganalyze.com/docs/index-advisor
- Atlas migration tool — https://atlasgo.io/
