# Django Testing Reference

## Summary

pytest-based testing patterns for Django projects using `model_bakery` (or `factory_boy`) for fixtures, `@pytest.mark.django_db` for DB access, and `APIClient` for DRF endpoint tests. The core rule: service-layer tests must call real code, not mocks; mock only at process boundaries (outbound HTTP, S3, third-party SDKs).

## Why

Agents default to mocking every dependency (Java/.NET style), producing tests that pass while integration is broken. Django's `baker.make(...)` randomises fixture data, which hides value-specific bugs. Prescribing explicit fixture pinning and forbidding in-app mocks prevents both failure modes while keeping the test suite fast and readable.

## When To Use

- Adding test coverage to a new Django app: `pytest-django` + `model_bakery` is the canonical default.
- Generating or reviewing service-layer tests where the "no mocks for in-app code" rule must be enforced.
- Migrating from `unittest.TestCase` to `pytest` style.
- Setting up parametrized tests for validation/calculation services.
- Adding DRF API tests without writing the full request stack manually.

## When NOT To Use

- Non-Django Python projects — patterns assume `@pytest.mark.django_db`, app fixtures, Django settings.
- Pure unit tests of pure functions with no DB access — skip `model_bakery` overhead.
- Browser / E2E tests — use `playwright` (pytest-playwright).
- Performance / load testing — use `locust` or `k6`.
- Codebases standardized on `unittest.TestCase` where migration is out of scope.

## Content

| File | What's inside |
|------|---------------|
| `content/01-fixture-patterns.xml` | `baker.make` vs `factory_boy` rules; mandatory field-pinning rule; `conftest.py` canonical fixtures. |
| `content/02-test-patterns.xml` | Parametrized tests, service-layer test rules, API test patterns with `APIClient`, quality checklist. |
| `content/03-antipatterns.xml` | Mock-everything failure mode, truthy-assertion trap, fixture overuse, async/time-related antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | Reusable Django + DRF + baker fixtures (`api_client`, `user`, `staff_user`, `authed_client`, `freeze_now`). |
| `templates/pyproject-pytest.toml` | pytest.ini_options with `--reuse-db`, coverage floor 80%, randomised order. |
