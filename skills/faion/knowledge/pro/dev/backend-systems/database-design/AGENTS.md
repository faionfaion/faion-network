---
slug: database-design
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a PostgreSQL schema spec: 3NF tables, access-pattern indexes, DB-layer constraints (FK / CHECK / NOT NULL / UNIQUE), forward + backward migrations, TIMESTAMPTZ + PK type policy."
content_id: "6aef59232670f66a"
complexity: deep
produces: spec
est_tokens: 4300
tags: [postgresql, schema, database, migrations, indexing]
---

# Database Design (PostgreSQL)

## Summary

**One-sentence:** Produces a PostgreSQL schema spec: 3NF tables, access-pattern indexes, DB-layer constraints (FK / CHECK / NOT NULL / UNIQUE), forward + backward migrations, TIMESTAMPTZ + PK type policy.

**Ефективно для:**

- New entities in an existing PostgreSQL schema.
- Migration from prototype-grade schema to production.
- OLTP workloads with mixed read/write patterns.
- Multi-tenant schemas needing tenant-id discipline.

**One-paragraph:** Relational schema design for PostgreSQL: normalize to 3NF first; derive indexes from a stated query workload, not assumptions; enforce integrity at the database layer (FK, CHECK, NOT NULL, UNIQUE); emit both forward and backward migrations in the project's migration tool. PK type, ON DELETE semantics, and TIMESTAMPTZ vs TIMESTAMP are decided globally and consistently.

## Applies If (ALL must hold)

- Stack uses PostgreSQL ≥14.
- Workload mix is OLTP (transactional, indexable).
- Migration tool present (Alembic, dbmate, Flyway, ActiveRecord, Goose, Atlas).
- Project agreed on global PK type + ON DELETE policy.

## Skip If (ANY kills it)

- Read-heavy analytics workloads — use a columnar store / OLAP.
- Document-oriented schemas — switch to MongoDB / DynamoDB / JSONB.
- Single-table designs — see NoSQL design instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Entity inventory + relationships | domain doc | PM / BA |
| Query workload sample | EXPLAIN report | team |
| Global type policy (UUID v7 vs bigint) | decision record | tech lead |
| Migration tool selection | ADR | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[api-developer]]` | endpoint contracts derive table needs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-tables` | sonnet | 3NF tables from entity inventory. |
| `derive-indexes` | sonnet | Maps workload sample to indexes. |
| `write-migrations` | haiku | Mechanical: forward + backward DDL. |

## Templates

| File | Purpose |
|------|---------|
| `templates/database-design.json` | JSON Schema for the Database Design (PostgreSQL) output contract |
| `templates/database-design.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a database-design record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-database-design.py` | Enforce the Database Design (PostgreSQL) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[caching-invalidation]]
- [[error-handling]]
- [[go-error-handling-patterns]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
