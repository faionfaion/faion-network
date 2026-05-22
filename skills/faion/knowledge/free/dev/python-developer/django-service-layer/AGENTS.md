---
slug: django-service-layer
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: All write operations (create, update, delete, side effects) belong in service functions, not in views, serializers, or model save() overrides.
content_id: "6ed563d8a9d30ed4"
tags: [django, service-layer, architecture, transactions]
---
# Django Service Layer Pattern

## Summary

**One-sentence:** All write operations (create, update, delete, side effects) belong in service functions, not in views, serializers, or model save() overrides.

**One-paragraph:** All write operations (create, update, delete, side effects) belong in service functions, not in views, serializers, or model save() overrides. Services take keyword-only arguments, wrap multi-model writes in transaction.atomic(), call full_clean() before save(), and raise domain exceptions instead of HTTP exceptions. This makes business logic independently testable and reusable across views, tasks, admin actions, and management commands.

## Applies If (ALL must hold)

- Any write operation that modifies one or more models.
- Business logic that spans multiple models (create order + create order items).
- Operations with side effects (send email, queue background task, write to audit log).
- Admin actions, Celery tasks, and management commands that implement business rules.
- Any logic that needs to be called from more than one entry point (view + task + management command).

## Skip If (ANY kills it)

- Trivial wrappers that do nothing but Model.objects.create() — add no value, just boilerplate.
- Read-only operations — those belong in selectors.
- View-only glue (getting request data, setting HTTP headers) — that stays in the view.
- Function-style scripts / management commands that orchestrate existing services — those call services, they are not services themselves.

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
