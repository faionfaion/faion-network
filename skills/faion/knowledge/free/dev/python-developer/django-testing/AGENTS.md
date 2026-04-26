# Django Testing

## Summary

pytest-django test patterns for Django/DRF projects: Factory Boy factories, `@pytest.mark.django_db` usage, `APIClient.force_authenticate`, parametrized permission matrices, coverage configuration. Core rules: one Factory Boy factory per model registered via `pytest_factoryboy.register`; use `@pytest.mark.django_db` (savepoint rollback) by default — only add `transaction=True` for code that calls `on_commit`; mock at the boundary (Celery `.delay`, httpx) not inside services.

## Why

Over-mocking (`patch('apps.users.services.User.objects.filter')`) tests the mock, not the code. Using real DB fixtures with transaction rollback gives real SQL behavior while keeping tests isolated. Factory Boy's `SubFactory` pattern makes relationship setup explicit and reusable across the test suite, reducing fixture duplication.

## When To Use

- Setting up pytest-django from scratch: `conftest.py`, `pyproject.toml` config, factory registration.
- Writing model, service, selector, view, and DRF API tests for a new feature.
- Migrating from `django.test.TestCase` (unittest-style) to pytest-style fixture tests.
- Adding parametrized tests for permission matrices, status transitions, validation rules.
- Configuring coverage gates and wiring CI.

## When NOT To Use

- Pure unit tests of standalone Python helpers (no DB, no Django imports) — plain pytest; pytest-django adds boot cost.
- Integration suites hitting external SaaS — separate `tests/integration/` lane gated by env var.
- Performance / load testing — use locust, k6, or pytest-benchmark.
- Snapshot/visual testing of admin or templates — playwright, percy.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pytest-django-setup.xml` | `pyproject.toml` config, `conftest.py` structure, `@pytest.mark.django_db` variants, `--reuse-db`. |
| `content/02-factory-patterns.xml` | Factory Boy vs model_bakery selection; `SubFactory`; `pytest_factoryboy.register`; `LazyAttribute` for cycles. |
| `content/03-api-testing.xml` | `APIClient`, `force_authenticate`, DRF response assertions, permission matrix parametrization. |
| `content/04-antipatterns.xml` | Missing `django_db` marker; over-mocking ORM; patching import target not use site; `transaction=True` overuse. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | Shared fixtures: `api_client`, `authed_client`, `staff_client`, factory registration, db autouse. |
