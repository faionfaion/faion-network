---
slug: django-api
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Thin views plus service layer plus `drf-spectacular` OpenAPI plus `ViewSet` pattern for Django REST Framework.
content_id: "49b08d0160fba49c"
tags: [django, drf, rest-api, openapi, architecture]
---
# Django REST Framework API

## Summary

**One-sentence:** Thin views plus service layer plus `drf-spectacular` OpenAPI plus `ViewSet` pattern for Django REST Framework.

**One-paragraph:** Thin views plus service layer plus `drf-spectacular` OpenAPI plus `ViewSet` pattern for Django REST Framework. Views validate input and call services; services own all business logic and accept domain types (not `request.user`). Every endpoint gets `@extend_schema` with `summary`, `request`, `responses`, and `tags`. Fat views (business logic in `def post`) are untestable from Celery or management commands and resist refactoring. Separating concerns into serializer → thin view → service → repository lets each layer be tested independently and reused across callers. `drf-spectacular` generates accurate OpenAPI from code; `manage.py spectacular --validate` catches schema regressions before deployment.

## Applies If (ALL must hold)

- New DRF endpoint inside a Django 5 project following apps/(name)/{views,services,serializers,urls}.py
- Refactoring a fat view (business logic in def post) into thin view plus services.py extraction
- Adding OpenAPI docs to existing endpoints via `drf-spectacular`
- Standardizing pagination, permissions, filtering across a `ViewSet`

## Skip If (ANY kills it)

- FastAPI, Starlette, Flask — different idioms; see python-fastapi instead
- Internal-only endpoints used by Django admin or management commands — plain Django views suffice
- Pure GraphQL APIs — `graphene-django` or `strawberry-django` have orthogonal patterns
- Async-first endpoints with heavy I/O concurrency — use Django Ninja or FastAPI
- One-off webhooks needing raw JSON in and out — DRF serializer overhead not justified

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
