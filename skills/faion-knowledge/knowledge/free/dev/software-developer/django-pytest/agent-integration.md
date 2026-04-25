# Agent Integration — Django Testing with pytest

## When to use
- Any new Django project — pytest + pytest-django is the modern default over Django's `TestCase`.
- Adding tests to legacy Django apps where the existing `TestCase` style limits fixture reuse.
- Cross-cutting fixtures (API client, authenticated user, factory) that need to be reused across hundreds of tests.
- Integration tests against DRF endpoints with `APIClient` and JWT/session auth.

## When NOT to use
- Projects that already invested heavily in `TestCase` and where mixed style is causing more confusion than gain — pick one.
- Test environments without DB access (pure-logic units) — `pytest` alone is enough; `pytest-django` adds startup overhead.
- Async test suites that need to use `httpx.AsyncClient` against ASGI directly — the `db` fixture and Django's sync ORM complicate things; use `pytest-asyncio` with manual setup.
- Code paths that depend on management commands and `call_command`-style test isolation — sometimes `TestCase`'s built-in transaction handling is simpler.

## Where it fails / limitations
- `db` fixture wraps each test in a transaction (fast) but breaks if the code-under-test calls `transaction.on_commit` — those callbacks never fire. Use `transactional_db` and pay the speed cost.
- pytest-django's `live_server` fixture spawns a real server; flaky on CI without explicit `wait_for_port` and parallel-port allocation.
- `pytest-xdist` parallel runs trip on shared DB state; need `--create-db` per-worker plus DB name templating (`pytest-xdist` + `pytest-django` `--create-db` + `--reuse-db` is finicky).
- Auto-discovery of `conftest.py` cascades — duplicate fixtures in nested conftests silently shadow each other.
- `factory_boy` + DRF + recursive relations (User → Profile → User) cause infinite recursion if `SubFactory` cycles aren't broken with `LazyAttribute`.
- `pytest-mock` `mocker.patch("module.attr")` patches the wrong scope when the code under test imports the symbol differently than the test does — silent test pass with no real coverage.

## Agentic workflow
A test-writing subagent reads the spec/test-plan, lists test cases per acceptance criterion, then generates pytest functions using shared fixtures from `conftest.py`. The agent NEVER assumes a fixture exists — it greps `conftest.py` first. A test-runner subagent runs `pytest --junitxml=results.xml -q --cov=src --cov-fail-under=80`, parses results, and feeds failures back. A code-review agent enforces "no `@pytest.mark.django_db` without `db` fixture if you only read", "no `transactional_db` if `db` is enough", and "no `setUp` style — use fixtures."

### Recommended subagents
- `faion-sdd-executor-agent` — task-level driver, gates on test pass.
- `faion-feature-executor` — sequential test execution with quality gates.
- A purpose-built `factory-builder` subagent — given a model schema, generates `factory_boy` factory + parametrized fixtures.
- A `coverage-gap-finder` subagent — runs coverage, lists uncovered lines per file, and emits a draft test list.

### Prompt pattern
```
Generate pytest tests for apps/<app>/services/<file>.py.
Use existing fixtures from tests/conftest.py (read it first).
For each public function: 1 happy-path + 1 boundary + 1 error case.
Use APIClient and the `user` fixture. Mark integration tests
@pytest.mark.integration. Output the full file. Stop.
```
```
Run: pytest --junitxml=/tmp/r.xml --cov=src --cov-report=term-missing -q
Parse failures. For each: test name, root cause (code/test/fixture/flake),
proposed fix as a unified diff. Do not apply yet.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Test runner | `pip install pytest` |
| `pytest-django` | Django integration: `db`, `client`, `settings` | `pip install pytest-django` |
| `pytest-cov` | Branch coverage | `pip install pytest-cov` |
| `pytest-xdist` | `-n auto` parallel runs | `pip install pytest-xdist` |
| `pytest-mock` | `mocker` fixture | `pip install pytest-mock` |
| `pytest-asyncio` | Async tests | `pip install pytest-asyncio` |
| `pytest-factoryboy` | Auto-register factories as fixtures | `pip install pytest-factoryboy` |
| `factory_boy` | Test data factories | `pip install factory_boy` |
| `pytest-randomly` | Randomize order to expose hidden coupling | `pip install pytest-randomly` |
| `freezegun` / `time-machine` | Freeze time in tests | `pip install time-machine` |
| `responses` / `respx` | Mock HTTP at the requests/httpx layer | `pip install respx` |
| `pytest-django-queries` | Snapshot SQL for N+1 regression | `pip install pytest-django-queries` |
| `coverage` | Standalone coverage tool | `pip install coverage` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Codecov / Coveralls | SaaS | Yes | Upload coverage XML; PR comments. |
| GitHub Actions | SaaS | Yes | Built-in pytest matrix; `actions/setup-python` + Postgres service. |
| GitLab CI | SaaS | Yes | Same. |
| TestRail / Allure | SaaS/OSS | Partial | Useful only if humans triage results. |
| Sentry | SaaS | Yes | Catches errors that escape tests in staging. |
| ngrok / mockoon | SaaS/OSS | Yes | Mock external services for integration tests. |

## Templates & scripts
See `templates.md` for full conftest. Inline minimal `conftest.py` agents can extend:

```python
# tests/conftest.py
import pytest
from rest_framework.test import APIClient
from apps.users.tests.factories import UserFactory

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture(autouse=True)
def _disable_external_calls(monkeypatch):
    """Fail loudly if test code reaches the network."""
    import socket
    def guard(*a, **k):
        raise RuntimeError("network access in tests is forbidden")
    monkeypatch.setattr(socket, "create_connection", guard)
```

```python
# apps/users/tests/factories.py
import factory
from apps.users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
```

## Best practices
- Use `@pytest.mark.django_db` (or the `db` fixture) only where DB is needed; pure logic tests should not touch DB.
- Prefer `factory_boy` over fixtures-as-functions — easier overrides (`UserFactory(email="x")`).
- Keep `conftest.py` close to where the fixture is used; project-root conftest only for truly global fixtures.
- Add `pytest-randomly` so order-dependent tests fail loud locally before CI.
- Snapshot queries with `pytest-django-queries` to catch N+1 regressions in PR.
- Mark slow tests; CI runs `pytest -m "not slow"` per push, full suite nightly.
- Force-authenticate with DRF's `force_authenticate` instead of issuing real login requests in unit tests — much faster.
- Use `freezegun` / `time-machine` rather than monkey-patching `datetime.now`.
- Test settings: separate `config/settings/test.py` with `DEBUG = False`, in-memory cache, fake email backend, `PASSWORD_HASHERS = ["MD5PasswordHasher"]` (test-only).
- Block real network calls (`autouse` socket monkey-patch) — agents that forget to mock will see clear failures, not 30s timeouts.

## AI-agent gotchas
- LLMs write `def test_x():` without the `db` marker, then rely on the `User.objects.create()` call which raises a clear error — but agents waste tokens iterating. Add `pytest --strict-markers` and a CI lint that finds DB-touching tests without the marker.
- LLM-generated tests often re-create the same fixture inline instead of reusing `conftest`. Prompt: "Read tests/conftest.py first. Reuse `user`, `api_client`, `auth_client`."
- `mocker.patch("apps.foo.bar.baz")` vs `mocker.patch("apps.qux.baz")` — agents patch the import path of the module they read, not where the SUT imports from. Verify with `assert mock.called` AND with a real assertion on the result.
- Agents call `transaction.on_commit(...)` in code under test, then assert on the side effect — but `db` fixture rolls back so commit never fires. Use `transactional_db` or `pytest-django`'s `django_capture_on_commit_callbacks` (3.4+).
- Agents leave the fast-but-insecure password hasher in dev settings; pre-commit must reject `MD5PasswordHasher` outside `settings/test.py`.
- LLMs forget to clean up `factory.django.DjangoModelFactory` `_post_save` side effects (signal handlers fire). Use `factory.django.mute_signals(post_save)` selectively.
- `pytest --reuse-db` is fast but masks migration drift — agents update models without re-running migrations. CI should always `--create-db`.
- LLMs over-mock: every dependency mocked → tests prove nothing. Rule: mock at the I/O boundary (HTTP, mail, payment), test the rest with real DB and real serialization.
- `pytest-asyncio` + `pytest-django` interaction: `db` fixture is sync, so async tests need explicit `@pytest.mark.django_db(transaction=True)` plus `@sync_to_async` wrappers around ORM calls.
- Coverage misses async branches in DRF view handlers — agent's "100% coverage" claim is optimistic; verify with `coverage report -m` and read missing lines.

## References
- https://pytest-django.readthedocs.io/ — pytest-django docs
- https://factoryboy.readthedocs.io/ — factory_boy
- https://docs.pytest.org/en/latest/ — pytest
- https://github.com/HackSoftware/Django-Styleguide#testing — HackSoft Django testing guide
- https://www.cosmicpython.com/book/chapter_05_high_gear_low_gear.html — testing strategy in services-style Django
- https://docs.djangoproject.com/en/stable/topics/testing/ — Django's own testing docs
- https://martinfowler.com/articles/practical-test-pyramid.html — Fowler on the test pyramid
- https://github.com/pytest-dev/pytest-randomly — randomize order plugin
