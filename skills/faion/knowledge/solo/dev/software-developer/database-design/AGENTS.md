---
slug: database-design
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design a relational schema (PostgreSQL-first) for integrity, query performance, and zero-downtime migrations.
content_id: "6aef59232670f66a"
complexity: medium
produces: spec
est_tokens: 4500
tags: [database, postgresql, schema, migrations]
---
# Database Design

## Summary

**One-sentence:** Design a relational schema (PostgreSQL-first) for integrity, query performance, and zero-downtime migrations.

**One-paragraph:** Models the domain into 3NF tables (denormalize only with documented justification), declares every FK + check constraint at DB layer (not app), creates indexes only after observing query plans, and treats every schema change as an additive expand-then-contract migration so deploys are reversible. Output is a schema spec + ERD + migration plan that reviewers can validate against acceptance criteria.

**Ефективно для:**

- New service designs with non-trivial relational data.
- Schema reviews before code lands to prevent integrity bugs at the DB edge.
- Migration planning for live systems where downtime windows are scarce.
- Bringing junior developers to schema-quality parity.

## Applies If (ALL must hold)

- Service has multi-table relational data (>=3 entities with FKs).
- Persistence is PostgreSQL or another transactional RDBMS.
- Schema changes need to ship without downtime (live customers).
- Reads and writes both matter (not write-only event store).

## Skip If (ANY kills it)

- Storage is purely key-value or document (DynamoDB, MongoDB without joins) — different patterns.
- Data is throw-away (test fixtures, ETL staging) where integrity is not enforced.
- Table is single-row config (use file or env var).
- OLAP / data-warehouse modelling (star schema needs warehouse-specific methodology).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain entity list + relationships | bullet list or ERD draft | product/domain |
| Expected query patterns (top 5 reads, top 5 writes) | list | tech-lead |
| Read/write QPS estimate + data volume per table | numbers | platform |
| Existing schema if migration (DDL dump) | SQL file | DB owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[sql-optimization]] | Indexing rules consume this schema. |
| [[api-versioning]] | Schema changes drive API version policy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (FK + check at DB, 3NF default, index-after-plan, additive migration, naming convention, no-business-logic-in-DB) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for schema spec artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: model → DDL → constraints → indexes → migration plan → review | 800 |
| `content/05-examples.xml` | essential | Worked example: orders + line-items schema | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `entity_modeling` | opus | Domain-to-relational mapping needs deep synthesis. |
| `constraint_authoring` | sonnet | Mechanical DDL emission once entities decided. |
| `index_plan` | sonnet | Match indexes to query patterns from prereqs. |
| `migration_plan` | opus | Expand-then-contract sequencing needs care. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.sql` | Reference PostgreSQL schema (UUIDs, constraints, indexes, soft-delete, audit trigger) |
| `templates/migration.py` | Alembic migration example: expand-contract pattern |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-database-design.py` | Validate the schema spec artefact metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[sql-optimization]]
- [[api-versioning]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps storage type, change cadence, and downtime tolerance to a rule from `01-core-rules.xml`, telling the agent whether to run the full schema spec methodology or skip when preconditions fail. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
