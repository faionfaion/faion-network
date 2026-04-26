# Database Design (PostgreSQL)

## Summary

Relational schema design for PostgreSQL: normalize to 3NF first, derive indexes from stated query workload (not assumptions), enforce integrity at the database layer (FK, CHECK, NOT NULL, UNIQUE), and emit both forward and backward migrations in the project's migration tool. PK type, `ON DELETE` semantics, and `TIMESTAMPTZ` vs `TIMESTAMP` are decided globally and consistently.

## Why

Schema decisions are nearly irreversible on production databases. Missing FK enforcement leads to orphaned rows; missing `ON DELETE` semantics lead to unexpected cascade wipes; `TIMESTAMP` without timezone causes cross-timezone bugs; `CREATE INDEX` without `CONCURRENTLY` locks large tables. Agents that skip these decisions create technical debt that costs more than the original feature.

## When To Use

- Greenfield schema design for a relational backend (PostgreSQL, MySQL, MariaDB).
- Adding a new bounded context / aggregate needing its own tables.
- Refactoring a denormalized "god table" into 3NF.
- Designing audit trails, soft-delete, partitioning, materialized views.
- Generating migrations (Alembic, Flyway, sqlx, Goose, Prisma) from a target schema.
- Choosing indexes for a known query workload via `pg_stat_statements`.

## When NOT To Use

- Pure document/event-sourced systems — use `nosql-patterns/` instead.
- Graph-heavy domains (social, fraud, bill-of-materials) — use Neo4j/Postgres-AGE patterns.
- Time-series with billions of rows/day — TimescaleDB/InfluxDB design rules dominate.
- Wide-column analytical workloads — ClickHouse/BigQuery patterns instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-patterns.xml` | E-commerce schema example, indexing strategy, soft deletes, audit trail, partitioning. |
| `content/02-migrations.xml` | Alembic up/down example, migration safety rules (CONCURRENTLY, TIMESTAMPTZ). |
| `content/03-rules.xml` | PK type decision, ON DELETE semantics, antipatterns (VARCHAR(255), missing downgrade). |

## Templates

| File | Purpose |
|------|---------|
| `templates/ecommerce_schema.sql` | Complete e-commerce DDL: users, products, orders, order_items with constraints + indexes. |
| `templates/audit_trigger.sql` | Audit log table + trigger function for INSERT/UPDATE/DELETE tracking. |
| `templates/alembic_migration.py` | Alembic migration template with upgrade/downgrade. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/schema_diff.sh` | Diffs a proposed DDL file against a live DB and prints the delta. |
