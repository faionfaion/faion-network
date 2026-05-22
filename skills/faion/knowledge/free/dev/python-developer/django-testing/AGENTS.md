---
slug: django-testing
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: pytest-django patterns for Django/DRF: Factory Boy factories, django_db marker, APIClient.force_authenticate, parametrized permission matrices.
content_id: "f5886eaa8721df0f"
complexity: medium
produces: code
est_tokens: 4000
tags: [django, testing, pytest, factories, drf]
---
# Django Testing with pytest

## Summary

**One-sentence:** pytest-django patterns for Django/DRF: Factory Boy factories, django_db marker, APIClient.force_authenticate, parametrized permission matrices.

**One-paragraph:** pytest-django patterns for Django and Django REST Framework projects. One Factory Boy factory per model registered via pytest_factoryboy; @pytest.mark.django_db for savepoint rollback; APIClient.force_authenticate for authenticated API tests; parametrized permission matrices. Use real DB fixtures (not over-mocked ORM); reserve mocking for actual external service boundaries.

**Ефективно для:** Django/DRF інженера, який налаштовує тестову інфраструктуру або пише регресійні тести — заміняє розкидану тестову прозу на конкретні фікстури, фабрики і matrix-параметризацію.

## Applies If (ALL must hold)

- Setting up pytest-django from scratch (conftest.py, pyproject.toml, factory registration).
- Writing model, service, selector, view, and DRF API tests for a new feature.
- Migrating from django.test.TestCase to pytest-style fixture tests.
- Adding parametrized tests for permission matrices, status transitions, validation rules.
- Configuring coverage gates and wiring CI.

## Skip If (ANY kills it)

- Pure unit tests of standalone Python helpers with no DB — plain pytest is faster.
- Integration suites hitting external SaaS — separate tests/integration/ lane gated by env var.
- Performance / load testing — use locust, k6, or pytest-benchmark.
- Snapshot/visual testing of admin or templates — use playwright or percy.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Django project layout | code | apps/<app>/ with settings module |
| pyproject.toml | TOML | project root |
| Test environment settings module | Python module | config/settings/testing.py |
| Factory module | Python | tests/factories.py |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-pytest-setup` | Provides base pytest config conventions this methodology extends. |
| `free/dev/python-developer/python-pytest-fixtures` | Defines conftest fixture composition rules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: pyproject pytest config, savepoint vs transaction, conftest fixtures, factory per model, LazyAttribute vs LazyFunction, APIClient + force_authenticate, status + body asserts, parametrized permission matrices | ~1100 |
| `content/02-output-contract.xml` | essential | Output shape: pyproject.toml block + conftest.py block + tests/factories.py + per-feature test module skeleton. Forbidden: ORM mocking, transaction=True as default, bare status_code assertions. | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing django_db marker, ORM mocking, patch-define-site vs use-site, transaction=True default, assert status_code only | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: configure pytest-django → write factories + register → conftest fixtures → write model/service/view tests → add parametrized permission matrix → wire coverage + CI | ~800 |
| `content/06-decision-tree.xml` | essential | Decide: needs DB? → django_db. Needs commit semantics? → transaction=True. Else parametrize. Else patch use-site. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-conftest` | haiku | Boilerplate fixture file from template — low judgement. |
| `author-permission-matrix` | sonnet | Per-endpoint role × status enumeration with business judgement. |
| `review-test-suite` | opus | Cross-cutting: detect over-mocking, transaction misuse, coverage gaps. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | Shared pytest fixtures: api_client, authed_client, staff_client, factory registration. |
| `templates/test_api.py` | Skeleton for DRF API integration test with auth + status + body asserts. |
| `templates/pyproject.toml.fragment` | Pytest-django config block: DJANGO_SETTINGS_MODULE, addopts, markers, coverage. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-testing.py` | Validate that a test file uses django_db marker, format='json', and avoids ORM mocks. | Pre-commit and on every test added. |

## Related

- [[python-pytest-setup]]
- [[python-pytest-fixtures]]
- [[python-pytest-mocking]]
- [[python-pytest-parametrize]]

## Decision tree

The tree at content/06-decision-tree.xml routes the test author between savepoint (default) vs transaction=True, parametrization vs N test functions, and ORM mocking vs real DB fixtures. Walk it before writing any new test module.
