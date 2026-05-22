---
slug: django-quality-queries
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: N+1 queries are the most common performance leak in Django.
content_id: "7023aa13611a4559"
tags: [django, queries, performance, n-plus-one, orm]
---
# Django Query Optimization and N+1 Prevention

## Summary

**One-sentence:** N+1 queries are the most common performance leak in Django.

**One-paragraph:** N+1 queries are the most common performance leak in Django. A single for loop over a queryset without select_related becomes 1 + N database calls. This methodology covers select_related, prefetch_related, custom Prefetch objects, only/defer for large fields, and assertNumQueries to lock query counts as regression tests.

## Applies If (ALL must hold)

- Any Django view that iterates over a queryset and accesses related objects.
- List API endpoints returning more than 10 rows — N+1 impact grows linearly with row count.
- Admin list views that display FK fields (automatic N+1 from list_display).
- Celery tasks that process batches of model instances with relationships.
- Any endpoint where performance targets matter (SLA, dashboard, mobile API).

## Skip If (ANY kills it)

- Single-object detail views accessing only direct fields — no relationship traversal, no N+1 risk.
- Management commands processing one row at a time where simplicity beats efficiency.
- Throwaway scripts where correctness matters more than speed.

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
