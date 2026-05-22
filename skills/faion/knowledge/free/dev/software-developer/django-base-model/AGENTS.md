---
slug: django-base-model
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every Django domain model must inherit from BaseModel, an abstract model providing uid (UUID), created_at, and updated_at fields.
content_id: "9e74f42a3d843126"
tags: [django, base-model, uuid, timestamps]
---
# Django Base Model Pattern

## Summary

**One-sentence:** Every Django domain model must inherit from BaseModel, an abstract model providing uid (UUID), created_at, and updated_at fields.

**One-paragraph:** Every Django domain model must inherit from BaseModel, an abstract model providing uid (UUID), created_at, and updated_at fields. The integer primary key is kept for join performance; uid is the public identifier exposed in APIs and URLs. This pattern decouples internal DB layout from public API contracts while ensuring all domain entities carry audit timestamps with zero per-model boilerplate. Auto-increment IDs leak table size, enable enumeration attacks, and couple internal schema to external contracts.

## Applies If (ALL must hold)

- Starting any new Django project — define BaseModel before first domain model
- Creating any model that represents a domain entity (user, order, product, post, comment)
- Building REST/GraphQL APIs that must expose a stable, non-enumerable identifier
- Systems requiring audit trails (created_at/updated_at) for compliance or debugging
- Refactoring legacy models to add UUID and timestamp fields retroactively

## Skip If (ANY kills it)

- Internal-only models never exposed externally (M2M through-tables, analytics rollups) — extra UUID column and index are dead weight
- Models inheriting from third-party abstract bases (django-mppt, django-polymorphic) that define their own PK/timestamp scheme — MRO conflicts
- High-write tables in the millions of rows without a migration plan — UUIDv4 has poor B-tree index locality (use UUIDv7 instead)
- Read-replica DBs where every extra index slows replication lag

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

- parent skill: `free/dev/software-developer/`
