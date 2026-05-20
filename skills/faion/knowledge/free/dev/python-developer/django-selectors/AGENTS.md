---
slug: django-selectors
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Keyword-only functions in selectors.
content_id: "6d0f8786b07e4160"
tags: [django, selectors, queryset, n-plus-one]
---
# Django Selectors Pattern

## Summary

**One-sentence:** Keyword-only functions in selectors.

**One-paragraph:** Keyword-only functions in selectors.py that encapsulate read operations, return QuerySet with select_related/prefetch_related, and prevent N+1 queries. Query logic belongs in selectors, not in views, serializers, or tests.

## Applies If (ALL must hold)

- Any list query with filtering, ordering, or pagination.
- Fetching a single object by ID or unique field, especially with related data.
- Queries with select_related or prefetch_related for related model data.
- Queries used in more than one place (view, task, admin, management command).
- Queries that need N+1 prevention guaranteed across all usage points.

## Skip If (ANY kills it)

- Simple Model.objects.get(pk=pk) with no related data — inline is fine if only used once.
- Write operations — those belong in services.
- Annotations purely for display (computed fields in serializers via SerializerMethodField).

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
