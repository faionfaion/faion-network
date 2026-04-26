# Django Testing with pytest

## Summary

pytest with pytest-django is the modern Django test stack. Tests use fixtures (not `setUp`), factory_boy for test data, `APIClient.force_authenticate` for auth, and the `db` fixture for database access. Every test is a function or class method — no `TestCase` inheritance. Block all real network calls with an autouse socket monkeypatch.

## Why

pytest fixtures compose and override cleanly where `TestCase.setUp` does not. Parametrize replaces repeated test methods. factory_boy generates realistic data with field overrides in a single call. `@pytest.mark.django_db` makes DB access explicit, preventing accidental hits. The result is faster, more readable tests that survive refactoring because they test observable behavior, not internal method calls.

## When To Use

- New Django projects — pytest-django is the default over `TestCase`
- Adding cross-cutting fixtures (API client, authenticated user, factory) reused across many tests
- Integration tests against DRF endpoints with `APIClient` and JWT/session auth
- Testing services, models, and database operations
- Adding negative tests (auth failures, validation errors)

## When NOT To Use

- Projects already heavily invested in `TestCase` where mixed styles cause confusion — pick one
- Test environments without DB access (pure logic) — plain `pytest` without pytest-django is lighter
- Async test suites using `httpx.AsyncClient` against ASGI directly — `db` fixture and sync ORM complicate things; use `pytest-asyncio` with manual setup
- Code paths relying on `call_command`-style isolation where `TestCase` transaction handling is simpler

## Content

| File | What's inside |
|------|---------------|
| `content/01-configuration.xml` | pyproject.toml config, directory structure, conftest fixtures, factory pattern |
| `content/02-test-patterns.xml` | Unit tests, integration tests, parametrize, mocking external services |
| `content/03-antipatterns.xml` | Testing implementation details, shared mutable state, LLM gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | Minimal conftest with api_client, user, auth_client, and network-blocking fixture |
| `templates/factories.py` | factory_boy DjangoModelFactory scaffolds for User and related models |
