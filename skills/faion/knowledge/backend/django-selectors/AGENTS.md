# Django Selectors Pattern

## Summary

**One-sentence:** Centralise every Django read operation in a keyword-only `selectors.py` function that returns an optimised QuerySet so views, tasks, admin, and management commands all inherit the same N+1-safe query.

**One-paragraph:** Selectors (HackSoft styleguide) are pure read functions placed in `apps/<app>/selectors.py`, take keyword-only arguments, return `QuerySet[Model]` for list shapes or `Model` (raising DoesNotExist) for single-object shapes, and own every `select_related` / `prefetch_related` / `Prefetch(...)` the caller needs. The result: one place to apply optimisation, one place to test query counts, one place to evolve when the data model grows.

**Ефективно для:** any list/detail endpoint with filtering, ordering, or related data; cross-cutting reuse across views + Celery tasks + admin; new HackSoft-style Django services; refactor of services-tangled-with-queries.

## Applies If (ALL must hold)

- Any list query with filtering, ordering, or pagination.
- Fetching a single object by ID or unique field, especially with related data.
- Queries with select_related or prefetch_related for related model data.
- Queries used in more than one place (view, task, admin, management command).
- Queries that need N+1 prevention guaranteed across all usage points.

## Skip If (ANY kills it)

- Simple `Model.objects.get(pk=pk)` with no related data used in exactly one place — inline is fine.
- Write operations — those belong in `services.py`.
- Annotations purely for display (computed fields in serializers via `SerializerMethodField`).

## Prerequisites

| Artifact | Format | Source |
|----------|--------|--------|
| `apps/<app>/models.py` | Python | repo |
| Optional existing query call site | Python | repo (views/tasks/admin) |
| pytest-django configured | config | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `django-quality-queries` | rule set on select_related / prefetch_related / assertNumQueries |
| `django-service-layer` | selectors are the read-half of the services/selectors split |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: kwarg-only, QuerySet return, prefetch ownership, .exists(), N+1 test | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for selector code metadata + valid/invalid Python signature examples | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: locate query → extract → optimise → test → wire | ~400 |
| `content/05-examples.xml` | optional | full worked example: order-list selector + N+1 test | ~400 |
| `content/06-decision-tree.xml` | essential | route between extract, inline-OK, services.py | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Selector signature design | sonnet | deterministic kwarg pattern |
| Prefetch shape (FK vs M2M vs Prefetch object) | sonnet | rule-driven |
| Annotation / aggregation design | opus | Q/F/Count/Subquery composition is judgement-heavy |
| N+1 test generation | sonnet | template substitution |

## Templates

| File | Purpose |
|------|---------|
| `templates/selector_list.py` | list selector skeleton: kwarg-only, QuerySet return, optional filters |
| `templates/selector_get.py` | single-object selector skeleton: kwarg-only, raises DoesNotExist |
| `templates/test_selector.py` | pytest skeleton asserting query count via django_assert_num_queries |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-selectors.py` | static check: selector signature uses keyword-only, returns QuerySet/Model, lives in selectors.py | pre-commit / CI |

## Related

- [[django-service-layer]] — write half of the read/write split
- [[django-quality-queries]] — selector is the canonical home for N+1 prevention
- [[django-testing]] — django_assert_num_queries fixture lives here

## Decision tree

See `content/06-decision-tree.xml`. Routes from "is this a read?" through "is it used more than once?" and "does it cross relationships?" to one of: extract into selector, leave inline, or place in services.py (write). The "used more than once" check exists because premature extraction of single-use simple queries is its own antipattern.
