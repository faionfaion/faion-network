---
slug: django-models
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Django models are thin data containers: fields, indexes, constraints, and __str__.
content_id: "6aae71cded2ec2b2"
tags: [django, models, database-design, querysets, performance]
---
# Django Models

## Summary

**One-sentence:** Django models are thin data containers: fields, indexes, constraints, and __str__.

**One-paragraph:** Django models are thin data containers: fields, indexes, constraints, and __str__. Business logic belongs in services (HackSoft style). Every domain model inherits from BaseModel (uid + timestamps). Status fields use TextChoices/IntegerChoices. ForeignKey on_delete is chosen deliberately — PROTECT for user/account refs, CASCADE only for child rows with no meaning without parent. Every generated migration file is reviewed by a human before migrate.

## Applies If (ALL must hold)

- Adding a new model to a Django app.
- Refactoring a model bloated with business logic into thin model + service functions.
- Audit: scanning for missing db_index, wrong on_delete, missing Meta.constraints.
- Designing status/state fields — converting raw string choices to TextChoices.
- Migrating Django 4.x → 5.x to use db_default and GeneratedField.
- Code review of Django model definitions for design consistency and best practices.

## Skip If (ANY kills it)

- ORM-less projects (FastAPI + SQLAlchemy, Flask + SQLAlchemy) — route to SQLAlchemy methodology.
- Migrating to a different ORM (peewee, Tortoise, SQLModel) — conventions don't translate.
- Quick throwaway prototypes where Django Admin + auto-generated tables are sufficient.
- Reporting/read-only projects backed by views or external warehouses.

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

- parent skill: `free/dev/python-developer/`
