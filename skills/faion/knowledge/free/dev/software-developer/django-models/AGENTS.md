---
slug: django-models
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Django model design following the BaseModel abstract pattern (integer PK + UUID field + timestamps), with explicit on_delete on every ForeignKey, TextChoices enums in per-app constants.
content_id: "6aae71cded2ec2b2"
tags: [django, models, database, design, architecture]
---
# Django Models

## Summary

**One-sentence:** Django model design following the BaseModel abstract pattern (integer PK + UUID field + timestamps), with explicit on_delete on every ForeignKey, TextChoices enums in per-app constants.

**One-paragraph:** Django model design following the BaseModel abstract pattern (integer PK + UUID field + timestamps), with explicit on_delete on every ForeignKey, TextChoices enums in per-app constants.py, and composite Meta.indexes for query-driven indexing. Django 5 db_default is supported for database-computed defaults.

## Applies If (ALL must hold)

- Creating a new Django app's models/ package.
- Refactoring ad-hoc models to the canonical BaseModel + Meta.indexes shape.
- Adding ForeignKey relations and choosing on_delete policy.
- Introducing per-app constants.py with TextChoices enums.
- Adding Django 5 db_default / computed fields.

## Skip If (ANY kills it)

- Async ORM workflows (.asave(), .aget()) — async manager patterns are not covered here.
- Multi-database routing, sharding, or replicas — out of scope.
- Heavy JSONField / ArrayField document-style data — methodology assumes relational schema.
- Tenant isolation (django-tenants, schema-per-tenant) — needs additional methodology.

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
