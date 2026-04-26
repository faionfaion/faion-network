# Agent Integration — Django Testing

Methodology covers pytest-django, Factory Boy, model_bakery, DRF APIClient, and pytest-cov for Django/DRF projects. Use this file when an agent bootstraps a Django test suite, writes new tests, or migrates legacy `unittest.TestCase`-based tests to pytest fixtures.

## When to use
- Setting up pytest-django from scratch — `conftest.py`, `pytest.ini`/`pyproject.toml` config, factory registration.
- Writing model, service, selector, view, and DRF API tests for a new feature.
- Migrating from `django.test.TestCase` (unittest-style) to `pytest`-style fixture tests.
- Adding parameterized tests for permission matrices, status transitions, validation rules.
- Configuring coverage gates (e.g., 80% overall, 90% on `services/`).
- Wiring CI: GitHub Actions matrix across Python/Django versions with coverage upload.

## When NOT to use
- Pure unit tests of standalone Python helpers (no DB, no Django imports) — plain pytest is enough; pytest-django adds boot cost.
- Integration suites that hit external SaaS — those go in a separate `tests/integration/` lane gated by env, not the main pytest run.
- Performance / load testing — use locust, k6, or pytest-benchmark, not pytest-django.
- Codebases on Django < 4.2 — many examples assume modern features (`select_related` typing, async views) that older versions don't support.
- Snapshot/visual testing of admin or templates — different stack (playwright, percy).

## Where it fails / limitations
- README's "Factory Boy vs model_bakery" table is correct but agents pick model_bakery for everything to save typing — leads to brittle tests when complex relationships need explicit factories.
- `@pytest.mark.django_db(transaction=True)` is needed for code that calls `transaction.atomic` / `on_commit`; README mentions it but doesn't explain when subtle on_commit hooks won't fire under standard `django_db`.
- DRF `APIClient` examples skip token/JWT auth setup — every project differs, agents copy-paste broken auth.
- No coverage of `pytest-django` `--reuse-db` and migration replay nuances; first-run vs cached-run timing differs 5-10x.
- Async view testing (Django async views, channels) not covered — needs `pytest-asyncio` + `AsyncClient`.
- `pytest-xdist` parallel runs can break tests that share fixtures with mutable state — agents enable `-n auto` and see flakes.
- Coverage on Django models often inflates because `__str__` and `Meta` are auto-counted; meaningful coverage needs `--cov-config` excludes.
- Factory Boy's `SubFactory` with circular relationships requires `LazyAttribute` patterns not shown.

## Agentic workflow
Bootstrap: (1) `uv add --dev pytest pytest-django pytest-cov factory-boy faker model-bakery`, (2) create `pytest.ini`/`[tool.pytest.ini_options]` with `DJANGO_SETTINGS_MODULE = "config.settings.test"`, (3) write `tests/conftest.py` registering factories via `pytest_factoryboy.register`, (4) per app: `tests/factories.py`, `tests/test_<entity>.py`, (5) coverage config in `pyproject.toml` (`omit = ["*/migrations/*", "*/admin.py"]`). Per-feature: write factory first, then test for service/selector, then API test using `APIClient`. CI: cache `.pytest_cache` + `.tox` keyed on lockfile; run on PR with `--cov-fail-under=80`.

### Recommended subagents
- `faion-test-agent` — Default for writing tests, factories, conftest fixtures.
- `faion-code-agent` — When test failures reveal a bug in services/selectors and a paired fix is needed.
- `faion-devtools-developer` — Owns pytest config, coverage thresholds, CI matrix.
- `faion-software-architect` — Decides factory granularity, when to extract shared fixtures, async test policy.
- `faion-feature-executor` — Per-feature TDD loop: failing test → service → selector → API → done.

### Prompt pattern

Test a service:

```
Write pytest-django tests for apps/<app>/services.py::<service> per
free/dev/python-developer/django-testing/README.md.
Setup:
  - Use Factory Boy factory from tests/factories.py (extend if missing fields).
  - Mark with @pytest.mark.django_db; use transaction=True only if code calls on_commit.
  - Cover: happy path, validation failures, permission edge cases (parametrize).
  - Mock external HTTP with respx; mock Celery tasks with `mocker.patch('apps.<app>.tasks.<name>.delay')`.
Assertions: state changes (DB), return value, side effects (Celery .delay called once with kwargs).
Coverage target: 95% on services.py for the touched function.
```

Test a DRF endpoint:

```
Write DRF API test for apps/<app>/apis.py::<view> per
free/dev/python-developer/django-testing/README.md.
Use:
  - pytest fixture `api_client` (APIClient).
  - Auth: force_authenticate(user=factory.UserFactory()).
  - Cover status codes (200, 400, 401, 403, 404, 422), response shape, DB mutations.
  - Parametrize by role (admin, staff, regular) for permission matrix.
Output: `pytest --cov=apps/<app>/apis --cov-report=term-missing` showing 100% on touched lines.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` + `pytest-django` | Test runner with Django integration | https://pytest-django.readthedocs.io |
| `pytest-cov` | Coverage reporting | https://pytest-cov.readthedocs.io |
| `pytest-xdist -n auto` | Parallel test execution | https://pytest-xdist.readthedocs.io |
| `pytest-mock` | mocker fixture wrapping unittest.mock | https://pytest-mock.readthedocs.io |
| `pytest-factoryboy` | Auto-register factories as fixtures | https://pytest-factoryboy.readthedocs.io |
| `pytest-randomly` | Randomize test order, exposes inter-test state leaks | https://github.com/pytest-dev/pytest-randomly |
| `pytest-recording` / `vcrpy` | Record HTTP fixtures | https://github.com/kiwicom/pytest-recording |
| `respx` | httpx mocking | https://lundberg.github.io/respx |
| `freezegun` / `time-machine` | Freeze time for date-sensitive tests | https://github.com/spulec/freezegun |
| `factory-boy` | Test data factories | https://factoryboy.readthedocs.io |
| `model-bakery` | Auto-generate model instances | https://model-bakery.readthedocs.io |
| `coverage erase / report / html` | Coverage CLI | https://coverage.readthedocs.io |
| `pytest --reuse-db --create-db` | Skip migrations on cached test DB | bundled |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions | CI | Yes — services: postgres for real DB tests | Cache .venv keyed on lockfile |
| Codecov / Coveralls | Coverage SaaS | Yes — `coverage xml` + upload | PR comment on coverage delta |
| Sentry | APM | Yes — `pytest-sentry` plugin | Capture test errors with context |
| LocalStack | OSS — local AWS emulator | Yes | For tests against S3, SQS, etc. |
| Testcontainers-python | OSS | Yes — spin up postgres/redis per session | Replaces SQLite-for-tests anti-pattern |
| GitHub PR Annotations | CI integration | Yes — pytest plugins emit annotations | `pytest-github-actions-annotate-failures` |

## Templates & scripts

See `templates.md` for full `conftest.py` and `pytest.ini` examples. Add this minimal Factory Boy + APIClient bootstrap (≤45 lines):

```python
# tests/conftest.py — shared fixtures.
import pytest
from rest_framework.test import APIClient
from pytest_factoryboy import register
from tests.factories import UserFactory, OrderFactory

register(UserFactory)
register(OrderFactory)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authed_client(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client, user

@pytest.fixture
def staff_client(api_client, user_factory):
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)
    return api_client, user

@pytest.fixture(autouse=True)
def _enable_db_access(db):
    """All tests get DB access; remove autouse for tests that should not touch DB."""
```

## Best practices
- **One factory per model**, registered via `pytest_factoryboy.register`. Name fixture as snake_case of model: `user_factory`, `order_factory`.
- **Factory Boy for production codebases** — declarative, reusable, supports `SubFactory`/`LazyAttribute`. model_bakery only for throwaway prototypes.
- **`@pytest.mark.django_db` not `transaction=True` by default** — faster (savepoint rollback). Only set `transaction=True` for code that needs full COMMIT semantics (`on_commit`, raw SQL with savepoint conflicts).
- **`force_authenticate` for unit-level API tests** — skips token/JWT setup. For auth flow tests, use `client.post('/api/token/', ...)`.
- **Parametrize permission matrices** — `@pytest.mark.parametrize("role,expected_status", [("admin", 200), ("user", 403)])`.
- **Mock at the boundary** — Celery `task.delay`, `httpx.AsyncClient`, third-party SDKs. Don't mock your own services from inside their tests.
- **`--reuse-db` locally, `--create-db` once after migrations change** — saves minutes per run. CI uses `--create-db` always for hygiene.
- **`pytest-randomly`** in CI — reveals tests that depend on order or global state.
- **Coverage excludes** for migrations, admin, settings, manage.py — they inflate but are not meaningful test targets.
- **Snapshot DRF response shapes** with `pytest-snapshot` or `syrupy` for stable contract tests.
- **Use `freezegun` / `time-machine`** for any time-sensitive assertion; `time.time()` drift breaks tests randomly.

## AI-agent gotchas
- **`pytest.mark.django_db` missing on a DB-touching test** → `RuntimeError: Database access not allowed`. Agents add `autouse=True` `db` fixture as workaround; that hides which tests need DB.
- **`SubFactory` cycles** (UserFactory → ProfileFactory → UserFactory) — infinite recursion at test time. Use `factory.LazyAttribute` or `factory.Faker` to break.
- **`force_authenticate` does not run middleware/permissions decorators reliably for some custom auth classes** — token-based tests need `client.credentials(HTTP_AUTHORIZATION=...)`.
- **`mocker.patch('apps.<app>.services.task_name.delay')`** — patch where used, not where defined. Agents patch the import target and see the real task fire.
- **`@pytest.mark.django_db(transaction=True)` is incompatible with `pytest-xdist`'s `--reuse-db`** in some setups; fixtures may collide. Pin DB names per worker via `--basetemp`.
- **Test isolation breaks** when models cache classvars (e.g., signals registered globally). Use `--randomly-seed` to repro flake.
- **`assertNumQueries` (django.test.TestCase)** has no direct pytest-django equivalent — use `django-assert-num-queries` (separate package) or `django.test.utils.CaptureQueriesContext`.
- **`tmp_path` fixture vs MEDIA_ROOT** — overriding `MEDIA_ROOT` per test needs `@override_settings(MEDIA_ROOT=tmp_path)` or settings fixture; agents miss this and tests pollute repo dir.
- **`override_settings` does not affect already-imported modules** — settings read at module load (e.g., DRF throttle classes) won't see overrides.
- **Async views need `AsyncClient`** (Django 4.1+) — sync `Client` returns `Coroutine` for async views, raising obscure TypeErrors.
- **`pytest --pdb` + DB transaction rollback** — pdb session sees rolled-back state because the fixture finalizer ran on exception. Use `--pdb` with `--no-rollback`.
- **`pytest-cov` + `pytest-xdist`** — coverage merges automatically only with `--cov-config`'s `parallel = true`. Otherwise CI shows half coverage.
- **Coverage on `from __future__ import annotations`** files: type-only branches under `if TYPE_CHECKING:` count as uncovered unless excluded via `# pragma: no cover`.
- **`responses` lib (sync) vs `respx` (httpx)** — agents use `responses` for async code; doesn't intercept httpx.

## References
- README: `./README.md`
- Sibling: `../django-pytest/`, `../python-testing-pytest/`, `../django-coding-standards/`
- pytest-django: https://pytest-django.readthedocs.io
- pytest-cov: https://pytest-cov.readthedocs.io
- factory-boy: https://factoryboy.readthedocs.io
- model-bakery: https://model-bakery.readthedocs.io
- pytest-factoryboy: https://pytest-factoryboy.readthedocs.io
- DRF testing: https://www.django-rest-framework.org/api-guide/testing/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io
- coverage.py: https://coverage.readthedocs.io
- testcontainers-python: https://testcontainers-python.readthedocs.io
