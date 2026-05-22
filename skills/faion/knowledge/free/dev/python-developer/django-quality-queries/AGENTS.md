---
slug: django-quality-queries
tier: free
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django ORM query optimization report (N+1 inventory + select_related/prefetch_related fixes + assertNumQueries locks + index recommendations).
content_id: "06f43334ca945422"
complexity: medium
produces: report
est_tokens: 3000
tags: [django, queries, performance, n-plus-one, orm]
---

# Django Query Optimization and N+1 Prevention

## Summary

**One-sentence:** Eliminate Django N+1 queries by adding select_related / prefetch_related at the selector layer, locking query counts with assertNumQueries, and indexing every filtered field.

**One-paragraph:** N+1 queries are the most common performance leak in Django: a single for-loop over a queryset without select_related becomes 1+N database calls. This methodology produces a query-optimization report that inventories N+1 spots (Debug Toolbar / nplusone), applies select_related for FK/OneToOne, prefetch_related (with optional Prefetch objects) for M2M / reverse FK, adds bulk_create / F() expressions for batch writes, indexes hot filter/order fields, and locks each hot endpoint with assertNumQueries regression tests so accidents are caught in CI.

**Ефективно для:** Django list/admin endpoints with FK or M2M access; mobile APIs with strict latency SLAs; pre-launch performance pass; post-incident remediation after a slow-query spike.

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

| Artifact | Format | Source |
|----------|--------|--------|
| Django settings module path | Python module | repo |
| `models.py` / `selectors.py` / `views.py` | Python | repo |
| Optional: Debug Toolbar output / SQL log | text | dev environment |
| Test settings + `pytest-django` install | config + dep | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `django-selectors` | optimisation lives in selector functions, not in views |
| `django-quality-logging` | nplusone alert noise needs structlog `django.db.backends` level discipline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: select_related, prefetch_related, bulk ops, indexes, assertNumQueries | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the query-optimization report + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~700 |
| `content/04-procedure.xml` | medium | 6-step procedure: profile → fix → lock | ~500 |
| `content/05-examples.xml` | optional | full worked example: 1001-query list view → 3-query selector | ~400 |
| `content/06-decision-tree.xml` | essential | route through "is it FK", "is it M2M", "needs index?" | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| N+1 hotspot detection from SQL log | sonnet | pattern match on grouped duplicate queries |
| select_related/prefetch_related plan | sonnet | deterministic from access pattern |
| Index design (composite, partial) | opus | cardinality + access-pattern judgment |
| assertNumQueries test generation | sonnet | template substitution |

## Templates

| File | Purpose |
|------|---------|
| `templates/selector.py` | selector function skeleton centralising query optimisation |
| `templates/test_query_count.py` | pytest skeleton using assertNumQueries to lock counts |
| `templates/audit-report.md` | output skeleton matching `02-output-contract` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-quality-queries.py` | validates the audit report against the schema | after report is generated, before commit |

## Related

- [[django-selectors]] — selector functions own the optimisation
- [[django-quality-logging]] — `django.db.backends` log level affects N+1 detection
- [[django-testing]] — assertNumQueries lives inside the pytest-django stack

## Decision tree

See `content/06-decision-tree.xml`. Routes from "does the queryset cross relationships?" through "ForeignKey / OneToOne vs M2M / reverse FK" to one of: add select_related, add prefetch_related (optionally with Prefetch), bulk_create, F() expression, add composite index, or skip-this-methodology (single-object detail view). Used to keep optimisation focused and avoid the "select_related on every queryset" antipattern.
