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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/conftest.py`

```python
"""

import pytest
from pytest_factoryboy import register


# Register your factories here:
# from tests.factories import UserFactory
# register(UserFactory)


@pytest.fixture
def api_client():
    """DRF APIClient (override per project)."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authed_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def staff_client(api_client, user_factory):
    staff_user = user_factory(is_staff=True)
    api_client.force_authenticate(user=staff_user)
    return api_client
```

### `templates/test_api.py`

```python
"""

import pytest


@pytest.mark.django_db
def test_endpoint_unauth_returns_401(api_client):
    response = api_client.get("/api/v1/example/")
    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture,expected_status",
    [
        ("api_client", 401),
        ("authed_client", 200),
        ("staff_client", 200),
    ],
    ids=["unauth", "user", "staff"],
)
def test_endpoint_permission_matrix(request, client_fixture, expected_status):
    client = request.getfixturevalue(client_fixture)
    response = client.get("/api/v1/example/")
    assert response.status_code == expected_status
```

### `templates/pyproject.toml.fragment`

```toml
[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "T20", "S", "ASYNC"]

[tool.mypy]
python_version = "3.13"
strict = true

[tool.pytest.ini_options]
addopts = "--strict-markers --cov --cov-fail-under=80 -n auto"
testpaths = ["tests"]
markers = ["integration: requires external services"]
```
