---
slug: django-services
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Pattern for isolating Django business logic into a services/ layer of plain Python functions (or classes only when DI is required).
content_id: "67f1bcbec14acb19"
tags: [django, architecture, services, testing, clean-code]
---
# Django Services Architecture

## Summary

**One-sentence:** Pattern for isolating Django business logic into a services/ layer of plain Python functions (or classes only when DI is required).

**One-paragraph:** Pattern for isolating Django business logic into a services/ layer of plain Python functions (or classes only when DI is required). Services own all DB-mutating operations, outbound API calls, and transactional boundaries; views/serializers stay HTTP-only. Core rule: service functions take domain primitives (never request), use keyword-only optional args, wrap multi-write paths in transaction.atomic(), and raise domain exceptions — never DRF ones.

## Applies If (ALL must hold)

- Adding any DB-mutating logic (create/update/delete) that would otherwise live in a view.
- Coordinating multi-model writes needing a single transactional boundary.
- Wrapping outbound API/SMTP/SMS calls so views/serializers stay thin.
- Making business logic unit-testable without HTTP or DRF context.
- Sharing an operation between a view, Celery task, and management command.

## Skip If (ANY kills it)

- Pure functions (validation, formatting, calculation) — those go in utils/.
- Trivial single-model obj.field = x; obj.save() called from one view.
- Read-only queryset chaining — keep on the manager / objects.
- DRF view-only concerns (permission checks, serializer wiring).

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
