---
slug: django-testing
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest-django test patterns for Django and Django REST Framework projects.
content_id: "f5886eaa8721df0f"
tags: [django, testing, pytest, factories, drf]
---
# Django Testing with pytest

## Summary

**One-sentence:** pytest-django test patterns for Django and Django REST Framework projects.

**One-paragraph:** pytest-django test patterns for Django and Django REST Framework projects. Core patterns: one Factory Boy factory per model, registered via pytest_factoryboy; @pytest.mark.django_db for database access with savepoint rollback; APIClient.force_authenticate for authenticated API tests; parametrized permission matrices for comprehensive coverage. Key principle: use real database fixtures (not over-mocked ORM) and save mocking for actual external service boundaries.

## Applies If (ALL must hold)

- Setting up pytest-django from scratch: conftest.py, pyproject.toml config, factory registration
- Writing model, service, selector, view, and DRF API tests for a new feature
- Migrating from django.test.TestCase (unittest-style) to pytest-style fixture tests
- Adding parametrized tests for permission matrices, status transitions, validation rules
- Configuring coverage gates and wiring CI

## Skip If (ANY kills it)

- Pure unit tests of standalone Python helpers (no DB, no Django imports) — plain pytest; pytest-django adds boot cost
- Integration suites hitting external SaaS — separate tests/integration/ lane gated by env var
- Performance / load testing — use locust, k6, or pytest-benchmark
- Snapshot/visual testing of admin or templates — playwright, percy

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
