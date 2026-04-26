# Database Design

## Summary

Relational schema design for integrity, performance, and maintainability. Core rules: normalize to 3NF first and denormalize only with a measured query showing the join is the bottleneck; use ULID or UUIDv7 primary keys (not auto-increment integers that leak row counts); every entity needs `created_at` and `updated_at` (timestamptz); foreign keys must have explicit `ON DELETE` (default `RESTRICT`, never implicit CASCADE).

## Why

Premature denormalization creates update-fanout consistency bugs. Auto-increment integer PKs leak business information (record count, growth rate). Missing `ON DELETE` defaults produce accidental mass deletes when a parent is removed. Migrations combining `ALTER TABLE ADD COLUMN NOT NULL DEFAULT` on large tables cause production lock-outs; the expand-contract pattern eliminates this risk.

## When To Use

- Greenfield schema for a new product (3NF first, denormalize with evidence later)
- Major feature touching more than 2 tables — needs ER diagram + migration plan
- Performance regression traced to schema (missing index, wrong column type, hot row contention)
- Designing audit trails, soft deletes, multi-tenancy, or time-series partitioning

## When NOT To Use

- "Move fast" prototypes you will throw away in a week — SQLite + single table is fine
- Read-mostly content sites — a CMS or static generator covers it without a relational model
- Append-only event logs — use TimescaleDB or ClickHouse instead of fighting Postgres indexes
- Graph-heavy domains (recommendation, social) — relational JOIN explosions hurt; use Neo4j or dgraph

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-patterns.xml` | E-commerce DDL: tables, UUIDs, CHECK constraints, foreign keys, soft deletes, audit trigger |
| `content/02-indexing.xml` | Index strategy keyed to query patterns; partial indexes; composite index column order rules |
| `content/03-migrations.xml` | Alembic migration example; expand-contract pattern; partitioning; denormalization via trigger |
| `content/04-antipatterns.xml` | God tables, missing FKs, over-indexing, EAV abuse, storing stale computed values, FLOAT for money |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.sql` | Reference e-commerce schema with UUIDs, constraints, indexes, soft-delete, audit trigger |
| `templates/migration.py` | Alembic migration with up/down using expand-contract pattern |
