---
slug: django-base-model
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Base Model pattern provides a consistent foundation for all Django models with common fields (UUID, timestamps) and behaviors.
content_id: "9e74f42a3d843126"
tags: [django, models, base-pattern, uuid, soft-delete]
---
# Django Base Model Pattern

## Summary

**One-sentence:** The Base Model pattern provides a consistent foundation for all Django models with common fields (UUID, timestamps) and behaviors.

**One-paragraph:** The Base Model pattern provides a consistent foundation for all Django models with common fields (UUID, timestamps) and behaviors. This methodology covers abstract base models, mixins, custom managers, and advanced patterns for production Django applications. Complexity: Intermediate. Django Version: 5.0+ (with 5.2 LTS features). Key Libraries: django-model-utils, django-simple-history, django-tenants.

## Applies If (ALL must hold)

- Bootstrapping a new Django project: define BaseModel, TimestampMixin, SoftDeleteMixin, manager/queryset patterns once at the start.
- Refactoring a legacy Django app where every model duplicates created_at, updated_at, ad-hoc soft-delete flags, or auto-increment IDs leak through APIs.
- Adding UUIDs to public APIs without rewriting primary keys (the uid separate-field pattern).
- Introducing soft-delete to a domain that needs an "undo" (orders, posts, accounts) — done as one migration plus manager swap.
- Adding audit trail (django-simple-history) to compliance-relevant models.
- Multi-tenant SaaS migration: introducing TenantAwareModel + middleware-driven tenant scoping.
- Code review of new models: ensuring they inherit from the right base, use the right on_delete, and don't reinvent timestamps.
- Starting a new Django project.
- Refactoring legacy models to a consistent base structure.
- Building APIs that expose external IDs (never expose auto-increment integers).
- Multi-tenant SaaS applications requiring row-level isolation.
- Systems requiring audit trails and compliance tracking of changes.

## Skip If (ANY kills it)

- Tiny one-off scripts or admin commands that don't define new models.
- Models for ephemeral data (cache, signed tokens, throwaway joins) where timestamps and soft delete add noise.
- Tables managed outside Django (managed = False for legacy DB views) — the base model's Meta.abstract = True doesn't combine cleanly with managed = False.
- Performance-critical analytical tables where every byte counts; adding a 16-byte UUID + indexes per row is wasteful.
- When introducing PostgreSQL UUID v7 / k-sortable IDs — the UUID v4 advice is partially obsolete; reassess before applying.
- Mixing this pattern in a repo that already standardised on django-model-utils's TimeStampedModel etc. — pick one set of bases.

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
