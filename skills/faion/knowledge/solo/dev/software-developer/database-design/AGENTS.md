---
slug: database-design
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Relational schema design for integrity, performance, and maintainability.
content_id: "4637ec007df638a6"
tags: [database, postgresql, schema, migrations]
---
# Database Design

## Summary

**One-sentence:** Relational schema design for integrity, performance, and maintainability.

**One-paragraph:** Relational schema design for integrity, performance, and maintainability. Core rules: normalize to 3NF first and denormalize only with a measured query showing the join is the bottleneck; use ULID or UUIDv7 primary keys (not auto-increment integers that leak row counts); every entity needs created_at and updated_at (timestamptz); foreign keys must have explicit ON DELETE (default RESTRICT, never implicit CASCADE).

## Applies If (ALL must hold)

- Greenfield schema for a new product (3NF first, denormalize with evidence later).
- Major feature touching more than 2 tables — needs ER diagram + migration plan.
- Performance regression traced to schema (missing index, wrong column type, hot row contention).
- Designing audit trails, soft deletes, multi-tenancy, or time-series partitioning.
- Migrating between engines (Postgres to MySQL, monolith to sharded, OLTP to OLAP mirror).

## Skip If (ANY kills it)

- Move fast prototypes you will throw away in a week — SQLite + single table is fine.
- Read-mostly content sites — a CMS or static generator covers it without a relational model.
- Append-only event logs — use TimescaleDB or ClickHouse instead of fighting Postgres indexes.
- Graph-heavy domains (recommendation, social) — relational JOIN explosions hurt; use Neo4j or dgraph.
- When the team has no ops capacity for migrations / backups — a managed KV (DynamoDB, Firestore) trades schema rigour for zero-ops.

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

- parent skill: `solo/dev/software-developer/`
