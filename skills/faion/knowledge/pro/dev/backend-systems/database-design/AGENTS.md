---
slug: database-design
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Relational schema design for PostgreSQL: normalize to 3NF first, derive indexes from stated query workload (not assumptions), enforce integrity at the database layer (FK, CHECK, NOT NULL, UNIQUE), and emit both forward and backward migrations in the project's migration tool.
content_id: "4637ec007df638a6"
tags: [postgresql, schema, database, migrations, indexing]
---
# Database Design (PostgreSQL)

## Summary

**One-sentence:** Relational schema design for PostgreSQL: normalize to 3NF first, derive indexes from stated query workload (not assumptions), enforce integrity at the database layer (FK, CHECK, NOT NULL, UNIQUE), and emit both forward and backward migrations in the project's migration tool.

**One-paragraph:** Relational schema design for PostgreSQL: normalize to 3NF first, derive indexes from stated query workload (not assumptions), enforce integrity at the database layer (FK, CHECK, NOT NULL, UNIQUE), and emit both forward and backward migrations in the project's migration tool. PK type, ON DELETE semantics, and TIMESTAMPTZ vs TIMESTAMP are decided globally and consistently.

## Applies If (ALL must hold)

- Greenfield schema design for a relational backend (PostgreSQL, MySQL, MariaDB).
- Adding a new bounded context / aggregate needing its own tables.
- Refactoring a denormalized "god table" into 3NF.
- Designing audit trails, soft-delete, partitioning, materialized views.
- Generating migrations (Alembic, Flyway, sqlx, Goose, Prisma) from a target schema.
- Choosing indexes for a known query workload via pg_stat_statements.

## Skip If (ANY kills it)

- Pure document/event-sourced systems — use nosql-patterns/ instead.
- Graph-heavy domains (social, fraud, bill-of-materials) — use Neo4j/Postgres-AGE patterns.
- Time-series with billions of rows/day — TimescaleDB/InfluxDB design rules dominate.
- Wide-column analytical workloads — ClickHouse/BigQuery patterns instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/backend-systems/`
