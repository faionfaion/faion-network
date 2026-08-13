# Django Pytest

## Summary

**One-sentence:** Produces a Django test suite on pytest + pytest-django: fixtures (not setUp), factory_boy for data, APIClient.force_authenticate for auth, db fixture for database access, mocks only at process boundaries.

**One-paragraph:** Produces a Django test suite on pytest + pytest-django: fixtures (not setUp), factory_boy for data, APIClient.force_authenticate for auth, db fixture for database access, mocks only at process boundaries. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Project uses Django 5.x (or 4.2 LTS) with Python 3.12+.
- Code in question lives under `apps/<app>/` or `core/` per the django-coding-standards layout.
- A test runner is configured (`pytest + pytest-django`).
- The team has agreed to enforce service-layer logic separation.

## Skip If (ANY kills it)

- Project is not on Django (FastAPI, Flask, or other) — load the framework-specific methodology instead.
- Tiny throwaway tool with no growth horizon — overhead exceeds payoff.
- Codebase has not adopted the apps/core/config layout and refactoring it is out of scope right now.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `pyproject.toml` | TOML | repo root |
| `apps/<app>/` layout | directory tree | repo source |
| Target Django version | string | `pyproject.toml` |
| Existing test runner config | TOML | `pyproject.toml` `[tool.pytest.ini_options]` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-typing` | Type-checker baseline for Django code. |
| `free/dev/software-developer/django-coding-standards` | Layout standard that gates placement of files produced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to django-pytest | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold model/serializer/view/test from spec | sonnet | Mechanical code generation. |
| Design service-layer boundaries | opus | Needs domain judgement. |
| Audit existing code for layering violations | sonnet | Pattern matching with deterministic output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | pytest-django conftest with db, factories, APIClient. |
| `templates/factories.py` | factory_boy factories template for the BaseModel inheritors. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-pytest.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[django-coding-standards]] — see methodology AGENTS.md for context.
- [[django-models]] — see methodology AGENTS.md for context.
- [[django-api]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/conftest.py`

```python
"""
Minimal root conftest.py for Django + pytest projects.
Copy to tests/conftest.py, add project-specific fixtures as needed.
"""
import socket
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated DRF API test client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Basic test user. Replace UserFactory with your factory."""
    from apps.users.tests.factories import UserFactory
    return UserFactory()


@pytest.fixture
def auth_client(api_client, user) -> APIClient:
    """API client authenticated as the default test user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(autouse=True)
def _disable_external_calls(monkeypatch):
    """Block real network calls in all tests. Fail loudly instead of timing out."""
    def guard(*args, **kwargs):
        raise RuntimeError(
            "Network access in tests is forbidden. Mock the dependency."
        )
    monkeypatch.setattr(socket, "create_connection", guard)
```

### `templates/factories.py`

```python
"""
factory_boy DjangoModelFactory scaffolds.
Location: apps/<domain>/tests/factories.py
"""
import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "users.User"  # Replace with actual model path

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = "orders.Order"  # Replace with actual model path

    user = factory.SubFactory(UserFactory)
    status = "pending"
    # Use factory.LazyAttribute for computed fields:
    # total = factory.LazyAttribute(lambda o: Decimal("9.99"))
```
