# Agent Integration — Django Testing with pytest

## When to use

- New Django repos: bootstrap pytest + pytest-django + pytest-cov + pytest-xdist + Factory Boy as the canonical test stack.
- Migrating a legacy `django.test.TestCase` suite to pytest fixtures + parametrize, in stages, app by app.
- Writing API tests against DRF/Django Ninja endpoints with `APIClient`/`TestClient` driven by an authenticated fixture.
- Generating Factory Boy factories for new models so tests stop hand-crafting fixtures.
- Speeding up a slow Django suite (parallel workers, `--reuse-db`, `MD5PasswordHasher`, session-scoped fixtures).
- Debugging flaky tests: identify shared state, transactional vs non-transactional fixtures, ordering dependencies.

## When NOT to use

- Pure unit tests of helpers/pure functions with no Django dependency — plain `pytest` (no `pytest-django`) is faster and clearer.
- One-off scripts, ad-hoc `manage.py shell` exploration — fast and disposable beats fixture infrastructure.
- Tests that *must* run inside `manage.py test` (legacy CI gates, third-party plugins assuming Django runner) until that constraint is removed.
- Throughput-critical end-to-end tests against a deployed environment — use Playwright/Cypress; pytest is for API/unit/integration only.
- When the project has standardised on `unittest`/`django.test` and the cost of dual stacks isn't justified.

## Where it fails / limitations

- **`@pytest.mark.django_db` vs `transactional_db`** confusion — the former wraps in transaction (rollback), the latter doesn't. Test commits, signals, post-commit hooks, async tasks each pick a different one. Mismatch causes flaky `TransactionManagementError` or persistent state leaking.
- **Fixture scope mismatches.** A `session`-scoped DB fixture combined with `function`-scoped Factory Boy fixtures works only if every write rolls back; otherwise data accumulates and tests get order-dependent.
- **`pytest-xdist` + `--reuse-db`** can race on migrations on the first run; explicit `--create-db` on cold start is needed.
- **`pytest-factoryboy` magic.** `register(UserFactory)` injects two fixtures (`user`, `user_factory`) — naming collisions with explicit fixtures cause silent overrides.
- **Async views (Django 5)** need `pytest-asyncio` + `async_to_sync` adapter; many examples online still target sync.
- **Signals/post-save side effects** can leak across tests because Django doesn't undo connected signals automatically. `mute_signals()` decorator (Factory Boy) is required around model-creating fixtures.
- **`override_settings`** does not nest cleanly with session-scoped fixtures; agents that compose them lose the override silently.
- **Database vendor differences.** Tests passing on SQLite (in-memory) fail on Postgres because `JSONField` ordering, FK integrity timing, partial indexes differ. Run CI against the prod DB engine.
- **Coverage gaming.** `pytest-cov` reports include test code; agents auto-add `assert True` to bump %. Mutation testing (`mutmut`) is a corrective.
- **DRF Browsable API in tests** is slow and pulls Jinja2 errors; use `format='json'` always.

## Agentic workflow

Drive Django tests as three layers under `tests/`: `unit/` (no DB, no I/O), `integration/` (DB via `db` fixture + factories), `api/` (DRF/Ninja TestClient). The agent generates factories from model definitions, then writes parametrized tests per acceptance criterion. Each test must follow Arrange-Act-Assert with one logical assertion focus. CI runs `pytest -n auto --reuse-db --cov` with a per-file coverage threshold. The agent never edits `pytest.ini`/`pyproject.toml` mid-run; surfaces config issues as findings.

### Recommended subagents

- `faion-python-developer` — Owns Django pytest setup (`conftest.py`, factories, settings module split for tests).
- `faion-testing-developer` (`testing-pytest`, `test-fixtures`) — Authoritative for fixture scoping, parametrize, mocking patterns.
- `faion-sdd-executor-agent` — Treats tests as the SDD acceptance gate; blocks task `done` until tests for the AC pass.
- `faion-code-quality` — Runs `pytest --cov --cov-fail-under=80` and rejects PRs that lower file-level coverage.
- `faion-improver` — Periodic audits: slowest tests, flake hot list, redundant fixtures, suspect `mark.django_db(transaction=True)` usage.
- General-purpose `Task` subagent for `unittest → pytest` migration: mechanical, scoped per app.

### Prompt pattern

Generate factories + first tests for a new model:

```
Model: <App.Model> with fields [...].
Tasks:
1. Add tests/factories/<app>.py with Factory Boy DjangoModelFactory.
   - Use Faker for realistic data; SubFactory for FKs; mute_signals where post_save side-effects exist.
2. Register factory in tests/conftest.py via pytest-factoryboy.register(...).
3. Write tests/integration/test_<model>.py with:
   - test_creation_persists (happy path)
   - test_str_returns_<expected>
   - test_unique_<field>_constraint (parametrized)
   - test_soft_delete (only if SoftDeleteMixin present)
4. Run pytest -q --cov=apps.<app>; report coverage.
Use db fixture (not transactional_db) unless the test asserts on commit/signals.
```

API endpoint tests:

```
Endpoint: POST /api/v1/<resource>/, auth required, returns 201 + JSON.
Generate tests/api/test_<resource>.py with:
- authenticated_client fixture (force_authenticate via APIClient).
- parametrize valid/invalid payloads.
- assert response.status_code AND response.json() shape (one row).
- separate test for permissions (401 anonymous, 403 wrong tenant).
Format='json' on every request. No browsable API.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Test runner | https://docs.pytest.org |
| `pytest-django` | Django integration (`db`, `transactional_db`, `client`, `admin_client`) | https://pytest-django.readthedocs.io |
| `pytest-asyncio` | `async def` test support | https://pytest-asyncio.readthedocs.io |
| `pytest-xdist` | Parallel execution (`-n auto`) | https://pytest-xdist.readthedocs.io |
| `pytest-cov` | Coverage reporting | https://pytest-cov.readthedocs.io |
| `pytest-mock` | `mocker` fixture (thin unittest.mock wrapper) | https://github.com/pytest-dev/pytest-mock |
| `pytest-randomly` | Randomise test order to surface order-dependence | https://github.com/pytest-dev/pytest-randomly |
| `pytest-rerunfailures` | Retry transient failures (use sparingly, mark.flaky) | https://github.com/pytest-dev/pytest-rerunfailures |
| `pytest-timeout` | Hard timeout per test (catch hangs) | https://github.com/pytest-dev/pytest-timeout |
| `pytest-sugar` / `pytest-instafail` | Better progress / fail-fast UX | https://github.com/Teemu/pytest-sugar |
| `pytest-factoryboy` | Auto-register Factory Boy factories as fixtures | https://pytest-factoryboy.readthedocs.io |
| `factory-boy` | Test-data factories for Django models | https://factoryboy.readthedocs.io |
| `Faker` | Realistic fake data | https://faker.readthedocs.io |
| `responses` | Mock `requests`/`httpx` HTTP calls | https://github.com/getsentry/responses |
| `respx` | Mock `httpx` async | https://lundberg.github.io/respx/ |
| `freezegun` | Mock `datetime`/`timezone.now` | https://github.com/spulec/freezegun |
| `time-machine` | Faster freezegun alternative | https://github.com/adamchainz/time-machine |
| `mutmut` | Mutation testing — exposes weak assertions | https://mutmut.readthedocs.io |
| `coverage` | Lower-level coverage tool | https://coverage.readthedocs.io |
| `django-debug-toolbar` (off in tests, on locally) | N+1 hunting | https://django-debug-toolbar.readthedocs.io |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes — matrix Python/Django, `actions/cache` for `.tox`/venv | Standard Django CI |
| GitLab CI | SaaS/self-host | Yes — same | Mirror of GH workflow |
| Codecov | SaaS | Yes — `codecov-action` uploads `coverage.xml` | PR coverage diff comments |
| Coveralls | SaaS | Yes — REST + CLI | Alternative to Codecov |
| Postgres in CI (services container) | OSS | Yes — `services: postgres` | Run tests on prod-equivalent DB |
| Redis in CI | OSS | Yes — `services: redis` | For Channels/Celery integration tests |
| Testcontainers (Python) | OSS | Yes — Python API | Real Postgres/Redis/Kafka in tests |
| LocalStack | OSS | Yes — REST/CLI | Mock AWS for `boto3` integration tests |
| WireMock / MockServer | OSS | Yes — REST | Mock external HTTP APIs |
| Sentry | SaaS | Yes — REST | Track which tests trigger errors in CI |
| Datadog CI Visibility | SaaS | Yes — agent | Flaky test surface area + duration trends |
| Allure | OSS | Yes — `allure-pytest` | Rich HTML reports for stakeholders |
| Renovate | SaaS | Yes — `pyproject.toml` aware | Auto-PR for pytest plugin upgrades |

## Templates & scripts

See methodology `templates.md` for full `pyproject.toml`, `conftest.py`, factories, and CI examples. Inline minimal `conftest.py` (≤30 lines):

```python
# tests/conftest.py
import pytest
from rest_framework.test import APIClient
from pytest_factoryboy import register
from .factories.users import UserFactory
from .factories.orders import OrderFactory

register(UserFactory)
register(OrderFactory)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authed_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture(autouse=True)
def _media_root(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path / "media"
```

Inline `pyproject.toml` pytest section (≤25 lines):

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py", "*_test.py"]
testpaths = ["tests"]
addopts = [
  "-ra", "--strict-markers", "--strict-config",
  "--reuse-db", "--cov=apps", "--cov-report=term-missing",
  "--cov-fail-under=80",
]
markers = [
  "slow: tests that hit network/DB heavily",
  "integration: tests requiring external services",
]
filterwarnings = ["error"]
```

## Best practices

- **Default to `db` fixture** (transactional rollback). Switch to `transactional_db` only when the test asserts on commit semantics, post-commit signals, or `select_for_update`.
- **One factory per model** in `tests/factories/<app>.py`; one row per test, no shared mutable state.
- **`mute_signals(post_save)`** when a factory creates a model that triggers email/Celery side effects; assert side effects in dedicated tests.
- **`force_authenticate` over login flows** for API tests unless the test is *about* the login flow.
- **`format='json'` always**, no browsable API. Assert on `response.json()`, not `response.content`.
- **Parametrize edge cases** (`@pytest.mark.parametrize`) instead of duplicating tests; one parameter set = one bug surface.
- **Run with `pytest-randomly`** in CI so order-dependence shows up early. Local dev can disable.
- **Coverage threshold per file** (`--cov-fail-under=80` plus `coverage.py` per-file rules), not global, to prevent gaming.
- **Add a `pytest --collect-only` smoke check** in CI to catch syntax errors and bad imports before running anything.
- **Pin pytest plugin versions** in `pyproject.toml`; one minor mismatch (`pytest-asyncio`) breaks the suite.
- **Test settings module separate** from dev/prod (`config.settings.test`): faster password hasher, in-memory cache, eager Celery, disable migrations only when justified (`--no-migrations`).
- **`tmp_path` for files**, never `/tmp` directly. Auto-cleanup, parallel-safe.

## AI-agent gotchas

- **Agents copy `db` everywhere.** Tests that "work" but secretly need `transactional_db` for signal/commit assertions will be flaky in CI. Reviewer checklist: any `transaction.on_commit`, `signals`, `post_save`, `select_for_update` → `transactional_db`.
- **Factory Boy + Faker unique values** drift across test runs; tests asserting on Faker outputs become flaky. Always derive expected from the factory instance, not from a Faker call.
- **`pytest-factoryboy` registers `<model>` and `<model>_factory`.** Agents writing their own `@pytest.fixture def user` shadow it silently. Force a single source.
- **`override_settings` inside fixtures** doesn't cascade unless the fixture itself is a context manager. Use `settings` fixture from `pytest-django` instead.
- **`assert response.status_code == 200`** without checking body lets bugs through. Always assert payload shape with at least one field.
- **Time leakage.** Tests that compute `datetime.now()` at module load fail at midnight UTC. Use `freezegun`/`time-machine` or relative comparisons.
- **`tmp_path` recreated per function** but session-scoped fixtures pin their own `tmp_path` to the first-test session, leaking files across tests. Scope-match tmp directories to fixture scope.
- **`pytest-xdist` + DB fixture** without `--dist=loadscope`/`loadfile` can split tests in the same class across workers, breaking class-scoped setups. Use `--dist=loadfile` for safety.
- **`MEDIA_ROOT` not overridden** in tests writes to the real disk; tests pollute each other and the host. Always override via `settings` autouse fixture.
- **Async tests without `pytest-asyncio`** silently warn-and-skip on pytest 8.3, hard-fail on 8.4. Pin both, mark with `@pytest.mark.asyncio`, and configure `asyncio_mode = "auto"`.
- **Mocking `time.sleep`** to "speed up" rate-limit tests can mask real bugs. Patch the rate-limiter directly, not `sleep`.
- **`assert True` / `assert response is not None`** — agents add these to satisfy coverage. Reviewer rule: every test has at least one assertion that compares to a literal or a derived expected value.
- **Re-running flaky tests with `--lf`** masks ordering issues. Force at least one `--randomly-dont-shuffle=false` run before merging.
- **`bulk_create` skips signals**, so factories using it don't trigger `post_save`. Tests that depend on signals will silently see no side effect.

## References

- Methodology README: `./README.md`
- pytest docs: https://docs.pytest.org
- pytest-django: https://pytest-django.readthedocs.io
- pytest-factoryboy: https://pytest-factoryboy.readthedocs.io
- Factory Boy: https://factoryboy.readthedocs.io
- Faker: https://faker.readthedocs.io
- pytest-xdist: https://pytest-xdist.readthedocs.io
- pytest-cov: https://pytest-cov.readthedocs.io
- pytest-asyncio: https://pytest-asyncio.readthedocs.io
- pytest-randomly: https://github.com/pytest-dev/pytest-randomly
- responses: https://github.com/getsentry/responses
- freezegun: https://github.com/spulec/freezegun
- time-machine: https://github.com/adamchainz/time-machine
- mutmut: https://mutmut.readthedocs.io
- DRF testing guide: https://www.django-rest-framework.org/api-guide/testing/
- "Making Django Tests Faster": https://schegel.net/posts/making-your-django-tests-faster/
- Real Python on pytest fixtures: https://realpython.com/django-pytest-fixtures/
