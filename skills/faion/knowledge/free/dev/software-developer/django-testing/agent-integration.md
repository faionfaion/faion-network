# Agent Integration — Django Testing Reference

## When to use
- Adding test coverage to a new Django app: `pytest-django` + `model_bakery` (or `factory_boy`) is the canonical default in this skill.
- Reviewing or generating service-layer tests where the rule "test calls real code, not mocks" must be enforced.
- Migrating from Django's `unittest`-based `TestCase` to `pytest` style for parametrize, fixtures, and faster iteration.
- Onboarding LLM-generated test fixtures: the README's quality checklist is the gate.
- Setting up parametrized tests for validation/calculation services where multiple input shapes need coverage.
- Adding API tests with `APIClient` (DRF) without writing the full Django request stack manually.

## When NOT to use
- Non-Django Python projects — these patterns assume `@pytest.mark.django_db`, app-aware fixtures, and Django settings.
- Pure unit tests of pure functions — no DB, no fixtures needed; skip `model_bakery` overhead.
- Browser / E2E tests — use `playwright` (pytest-playwright) instead; `APIClient` won't drive a frontend.
- Performance/load testing — `locust` or `k6`, not pytest.
- Codebases standardized on `unittest.TestCase` (legacy or LTS Django stacks) where moving to pytest is out-of-scope.

## Where it fails / limitations
- **`model_bakery` magic surprises.** Random data hides bugs that only manifest on specific values; tests pass on `baker.make(...)` defaults but fail in prod. Pin critical fields explicitly.
- **`@pytest.mark.django_db` reset cost.** Default rollback strategy slows large suites; without `--reuse-db` or transactional fixtures, suites cross 5 minutes quickly.
- **Fixture coupling.** README's `user` and `item` fixtures are global; growing test files leak state across tests via `db` reuse.
- **No coverage of factories vs. baker trade-off.** README shows both; agents alternate per file, fragmenting the codebase.
- **API tests bypass middleware.** `APIClient.get` skips some middlewares depending on settings; tests pass while the real request fails. Use `Client` (Django) for full pipeline checks where it matters.
- **Authentication tested superficially.** The example `api_client.get('/api/users/{id}/')` doesn't exercise login flows; agents copy this and never test the auth boundary.
- **No async/Celery test guidance.** Modern Django uses async views and Celery for background work; the README is silent on `pytest-asyncio` and `CELERY_TASK_ALWAYS_EAGER`.
- **`assert response.data['email'] == user.email` — silent serializer drift.** Agents lock tests to internal serializer keys; renaming a field breaks tests for the wrong reason.
- **Quality checklist is generic.** "Test calls real code" is good but unenforced; without a custom plugin, mock-heavy tests still pass.

## Agentic workflow
Use Claude subagents in three phases. (1) **Test planner** reads the service/view source and emits a list of test cases with names, inputs, and expected outcomes (no code yet). (2) **Test author** generates `pytest` files using the README templates: fixtures via `baker` for default cases, `factory_boy` for sequence-dependent ones, parametrize for branchy validation. (3) **Test reviewer** runs the suite, verifies coverage gain, applies the quality checklist, and rejects mock-only tests. The reviewer also enforces the `assert` on **specific values** (not just truthiness).

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — gates Django PRs against the SDD test-plan.md; rejects merges that drop coverage on changed lines.
- `faion-feature-executor` (skill, not an agent file) — sequential SDD task execution; the test phase consumes this methodology.
- A purpose-built **django-test-reviewer agent** (worth creating): runs `pytest --cov`, parses the report, applies the quality checklist programmatically (zero mocks for service tests, value assertions, edge cases present).
- `password-scrubber-agent` — when sample fixtures contain plausible-looking emails/tokens that resemble real ones, scrub before sharing.

### Prompt pattern
Test plan pass:
```
Read apps/<app>/services.py and apps/<app>/views.py. For each public
function/view, propose pytest test cases:
- name (test_<unit>_<scenario>)
- preconditions (fixtures needed)
- inputs (concrete values, not "valid" / "invalid")
- expected outcome (specific value or exception)
- edge cases: None, empty, negative, boundary
Output table only. No code. Reject any case that needs mocks for
in-app services; mark them as "needs refactor".
```

Test author pass:
```
Implement the planned tests in apps/<app>/tests/test_<area>.py:
- Use pytest-django (no unittest.TestCase).
- Fixtures via model_bakery.baker; pin all fields that the assertion
  reads. Use factory_boy when sequencing matters.
- Parametrize for value/expected pairs.
- Mark with @pytest.mark.django_db only when DB needed.
- API tests use rest_framework.test.APIClient with proper auth.
- No mocks for in-process service calls. External HTTP only via
  responses / pytest-httpx.
- Asserts MUST check specific values (not just truthy).
Output: file content + run command.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Test runner | `uv pip install pytest` ; https://docs.pytest.org |
| `pytest-django` | Django integration | `uv pip install pytest-django` ; https://pytest-django.readthedocs.io |
| `model_bakery` | Smart Django fixtures | `uv pip install model_bakery` ; https://model-bakery.readthedocs.io |
| `factory_boy` | Factories with sequences | `uv pip install factory_boy` ; https://factoryboy.readthedocs.io |
| `pytest-cov` | Coverage report | `uv pip install pytest-cov` ; https://pytest-cov.readthedocs.io |
| `pytest-xdist` | Parallel execution (`-n auto`) | `uv pip install pytest-xdist` |
| `pytest-randomly` | Random test order to surface state leakage | `uv pip install pytest-randomly` |
| `pytest-asyncio` | Async tests for async views | `uv pip install pytest-asyncio` |
| `pytest-mock` | `mocker` fixture (for external boundaries only) | https://pytest-mock.readthedocs.io |
| `responses` / `pytest-httpx` | Mock outbound HTTP without `unittest.mock` | https://github.com/getsentry/responses |
| `freezegun` | Freeze time | `uv pip install freezegun` |
| `pytest-vcr` / `cassette` | Record/replay HTTP cassettes | https://pytest-vcr.readthedocs.io |
| `coverage report --fail-under=80` | Enforce coverage floor in CI | bundled with `coverage` |
| `ruff check --select T20` | Forbid `print()` in tests | https://docs.astral.sh/ruff/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions / GitLab CI | SaaS / OSS | yes | Run pytest matrix (Python 3.11/3.12, Postgres, Redis); cache `.venv` and `uv.lock`. |
| Codecov / Coveralls | SaaS | yes | Coverage diff on PRs; agents read the diff to prioritize new tests. |
| Sentry | SaaS APM | yes | Cross-reference test failures with prod errors to spot missing coverage. |
| Cypress / Playwright Cloud | SaaS E2E | partial | Out of scope for this skill but pairs naturally for full coverage. |
| Datadog CI Visibility | SaaS | yes | Flake detection; integrates with pytest. |
| Trunk Check | SaaS / OSS | yes | Aggregate linters incl. ruff + mypy + custom. |
| pytest-django plugin community | OSS | yes | Active maintenance; new releases per Django LTS. |

## Templates & scripts

The README ships fixture and parametrize examples but no `conftest.py` skeleton. Inline drop-in (≤50 lines):

```python
# tests/conftest.py — reusable Django + DRF + baker fixtures.
import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def db_keepalive(django_db_setup, django_db_blocker):
    """Allow tests to share data across functions when explicitly requested."""
    with django_db_blocker.unblock():
        yield


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return baker.make("users.User", is_active=True)


@pytest.fixture
def staff_user(db):
    return baker.make("users.User", is_active=True, is_staff=True)


@pytest.fixture
def authed_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(autouse=True)
def _reset_outbound_email(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def freeze_now(monkeypatch):
    """Freeze django.utils.timezone.now to a fixed instant."""
    import datetime as dt
    from django.utils import timezone

    fixed = dt.datetime(2026, 1, 1, 12, 0, tzinfo=dt.timezone.utc)
    monkeypatch.setattr(timezone, "now", lambda: fixed)
    return fixed
```

Pair with `pyproject.toml`:
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
addopts = "-v --tb=short --reuse-db --cov=apps --cov-report=term-missing --cov-fail-under=80"
markers = ["slow", "integration"]
```

## Best practices
- **Test the service, not the model.** Services contain branching; testing model fields is type-checking.
- **Pin fixture values that assertions read.** `baker.make("Item", price=Decimal("9.99"))` — never assert on a random default.
- **Parametrize value tables.** A 10-line parametrized test beats 10 copy-paste test functions.
- **Use `--reuse-db` locally**, drop it in CI when migrations change. Add `--create-db` to the migration-changing PRs.
- **Run `pytest-randomly`.** Order-dependent tests are state leaks; surface them early.
- **Seed factories deterministically per test** (`factory.fuzzy.reseed_random(42)`) when reproducibility matters.
- **Forbid `unittest.mock` in service tests.** Mock only at the process boundary (HTTP, S3, third-party SDK) via `responses` / `pytest-httpx`.
- **API test the contract.** Assert status, response shape (use `jsonschema` if you have one), and absence of leaked fields (`'password' not in response.data`).
- **Use `freezegun` or `monkeypatch` on `timezone.now`** when behavior depends on time. Real clocks make tests flaky.
- **`pytest --collect-only` after generation** to confirm no broken imports before running the full suite.
- **Keep DB tests <5s each.** Anything slower goes behind `@pytest.mark.slow` and runs only in nightly CI.
- **Coverage is signal, not goal.** 80% on services, 50% on views, 0% on migrations is healthier than 95% blanket.

## AI-agent gotchas
- **Mock-everything by default.** Agents trained on Java / .NET examples mock every dependency; the README explicitly forbids this. Reject service tests with `mocker.patch(...)` on in-app modules.
- **Random data assertions.** Agents do `assert user.email` (truthy) — the test always passes. Force value assertions: `assert user.email == "u1@example.com"`.
- **Forgetting `@pytest.mark.django_db`.** Test errors with "Database access not allowed"; agents then add `@pytest.fixture(autouse=True)` hacks. Just mark the function.
- **Fixture overuse.** Agents pull the `user` fixture into tests that don't use it, creating unused DB rows and slowing the suite.
- **Hardcoded URLs in API tests.** Agents write `/api/users/1/`; refactor breaks. Use `reverse("user-detail", args=[user.id])`.
- **Asserting on serializer internals.** `response.data['profile']['bio']` couples to the serializer shape; rename → 100 broken tests. Assert via `jsonschema` or a stable subset.
- **`force_authenticate` everywhere.** Agents skip the actual auth flow; auth bugs slip through. Have at least one happy-path test that exercises `client.login(...)` or token endpoint.
- **Time-dependent tests without freezing.** `assert order.created_at > yesterday` flakes around midnight, in DST transitions, and across CI regions.
- **`baker.make_recipe` confusion.** Agents call `make_recipe` without registering a recipe; runtime error. Stick to `baker.make` unless the recipe exists.
- **`factory_boy` lazy attributes evaluated at import.** Agents define `email = factory.Faker(...)` outside `class Meta`; faker fires once per test session. Use `factory.LazyAttribute` for per-instance.
- **Skipping `--reuse-db` lock.** Schema changes require `--create-db`; agents forget after a migration PR. Add a CI step that detects migration changes and toggles flags.
- **Treating `APIClient` and `Client` as interchangeable.** They handle auth and middleware differently; agents use the wrong one and tests pass while real requests fail.
- **Async view tests with sync client.** Async Django views need `AsyncClient` (Django 4.1+); agents use sync `Client` and miss async-only branches.
- **Cassette drift.** VCR/responses cassettes go stale; agents rerun tests, regenerate cassettes, lose the assertion of "we still call this endpoint." Lock cassettes to specific routes/headers.
- **Coverage gaming.** Agents add tests that import code (raising coverage) without asserting behavior. Reviewer must check assert density per file.

## References
- pytest. https://docs.pytest.org
- pytest-django. https://pytest-django.readthedocs.io
- model_bakery. https://model-bakery.readthedocs.io
- factory_boy. https://factoryboy.readthedocs.io
- Django testing topic. https://docs.djangoproject.com/en/stable/topics/testing/
- DRF testing. https://www.django-rest-framework.org/api-guide/testing/
- responses (HTTP mock). https://github.com/getsentry/responses
- pytest-httpx. https://colin-b.github.io/pytest_httpx/
- freezegun. https://github.com/spulec/freezegun
- "Obey the Testing Goat" — Harry Percival. https://www.obeythetestinggoat.com/
- Sibling methodologies in this repo: `free/dev/software-developer/django-pytest/`, `free/dev/software-developer/django-base-model/`, `free/dev/software-developer/django-coding-standards/`, `free/dev/software-developer/code-coverage/`.
