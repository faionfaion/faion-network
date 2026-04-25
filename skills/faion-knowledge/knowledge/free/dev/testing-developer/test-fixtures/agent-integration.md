# Agent Integration — Test Fixtures

## When to use

- Designing the test-data layer for a new repo: pick fixtures, factories, builders, or object mothers per use case.
- Refactoring a `setUp`/`tearDown` heavy `unittest` suite to pytest fixtures with explicit dependency injection.
- Introducing Factory Boy / Fishery / FactoryBot to replace ad-hoc dict-based fixtures.
- Diagnosing flake or order-dependence: scope mismatch between fixture lifetime and test mutation patterns.
- Cleaning up `conftest.py` God-fixtures that set up everything for everyone.
- Standardising fixture cleanup: yield+rollback, request finalizers, transactional savepoints.
- Setting up integration tests with Testcontainers (real Postgres/Redis/Kafka) and reusing connections across the session.

## When NOT to use

- Trivial inline data (single string, small dict) — inline beats fixture overhead.
- One-off tests where data is the story — keep the data visible in the test body.
- Cross-cutting setup that's better as a module-level constant (e.g. `EMPTY_PAYLOAD = {}`).
- E2E browser tests where fixture state is owned by Playwright/Cypress (`storageState`, network mocks); see `e2e-testing`.
- When the team has standardised on a different test-data tool (ObjectFaker, mimesis, model_bakery) — don't introduce a second.

## Where it fails / limitations

- **Scope mismatches**. Session-scoped DB fixture with function-scoped Factory Boy creating rows = silent state accumulation, order-coupled tests.
- **Mystery Guest anti-pattern.** Data created in conftest but used implicitly by tests three folders away — agents can't trace where the row came from.
- **God Fixture.** A `seed_full_db` fixture used by 50 tests where each touches 10% — slow, opaque, brittle.
- **Builder verbosity.** Builders shine for complex objects but get noisy for simple ones; agents copy patterns blindly.
- **Object Mother drift.** `UserMother.admin()` semantics evolve over time and tests asserting "admin can do X" stop matching the current real `admin`.
- **Factory Boy + post-save signals**. Factory creating a model triggers `post_save` (e.g. send email) — every test sends fake emails unless `mute_signals` wraps it.
- **Sequence collisions in xdist**. Factory `Sequence(...)` is process-local; two workers generate the same sequence and break unique constraints.
- **`assert_all_requests_are_fired=True`** on `responses` fixtures fail tests when an unrelated path triggers a network call; agents fight that flag with `add_passthru` until tests are weakened.
- **Cleanup in `addfinalizer`** runs even on collection error, sometimes before resource exists. Prefer yield-based fixtures.
- **`conftest.py` discovery rules** are bottom-up but with caveats around plugins; agents move conftest and break fixture resolution.

## Agentic workflow

Pick the fixture style per case: **factories** for domain objects, **fixtures** for resource lifecycle, **builders** for complex object trees, **object mothers** for repeated business scenarios. The agent generates factories from model definitions, registers them via `pytest-factoryboy`, scopes resource fixtures (DB, HTTP mocks) at session and pins data fixtures at function. `conftest.py` lives in `tests/` (root), `tests/unit/`, `tests/integration/`, `tests/e2e/` — each with its own fixtures, never duplicating.

### Recommended subagents

- `faion-testing-developer` (`test-fixtures`, `testing-pytest`, `mocking-strategies`) — Owns the fixture methodology.
- `faion-python-developer` — Pairs to write factories that respect base-model defaults and signals.
- `faion-backend-developer` — Validates DB fixture transactional patterns (nested savepoints, isolation level).
- `faion-sdd-executor-agent` — Treats "factory exists for new model" as part of `done` for any model-introducing task.
- `faion-improver` — Audits for God fixtures, unused fixtures (`pytest --collect-only --co -q | grep used by 0`), shared mutable state.
- General-purpose `Task` subagent for `unittest setUp → pytest fixture` migration.

### Prompt pattern

Generate a Factory Boy factory + register:

```
Model: <App.Model>(<fields...>).
Tasks:
1. tests/factories/<app>.py: DjangoModelFactory with Faker, SubFactory for FKs, mute_signals(post_save) if signals fire.
2. Register via pytest_factoryboy.register(<Factory>) in tests/conftest.py.
3. Demo: in test_<model>.py, use <model>_factory fixture; assert at least one round-trip property of the persisted row.
Do NOT use Sequence(...) for fields with global uniqueness across xdist; use Faker(<provider>, unique=True).
```

Resource fixture for a real Postgres via Testcontainers (≤25 lines):

```
Add tests/conftest.py session-scoped:
- pg_container: Testcontainers Postgres started once per session.
- engine: SQLAlchemy engine bound to pg_container; tear down on session end.
- db_session: function-scoped, opens nested savepoint, rolls back on yield.
Tests use only db_session; do not import engine.
Goal: no test writes survive function teardown.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Runner with built-in fixture system | https://docs.pytest.org |
| `pytest-factoryboy` | Factory Boy auto-register as fixtures | https://pytest-factoryboy.readthedocs.io |
| `factory-boy` | Python test-data factories | https://factoryboy.readthedocs.io |
| `Faker` | Realistic fake data | https://faker.readthedocs.io |
| `model-bakery` | Lighter-weight Django factories | https://model-bakery.readthedocs.io |
| `mimesis` | Faster, multilingual fake data | https://mimesis.name |
| `pytest-mock` | `mocker` fixture | https://github.com/pytest-dev/pytest-mock |
| `pytest-asyncio` | Async fixtures via `async def` | https://pytest-asyncio.readthedocs.io |
| `pytest-xdist` | Parallel execution; needs per-worker isolation | https://pytest-xdist.readthedocs.io |
| `responses` / `respx` | HTTP fixtures (sync/async) | https://github.com/getsentry/responses / https://lundberg.github.io/respx/ |
| `freezegun` / `time-machine` | Time fixtures | https://github.com/spulec/freezegun / https://github.com/adamchainz/time-machine |
| `Testcontainers (Python)` | Real services in fixtures | https://testcontainers-python.readthedocs.io |
| `LocalStack` | AWS mocks; agent-driven session-scoped fixture | https://docs.localstack.cloud |
| `Hypothesis` | Property-based; complements fixtures | https://hypothesis.readthedocs.io |
| `Fishery` (TS) | Type-safe factories | https://github.com/thoughtbot/fishery |
| `FactoryBot` (Ruby) | Rails canonical factories | https://github.com/thoughtbot/factory_bot |
| `go-factory` / `gofactory` | Go struct factories | https://github.com/oleiade/gofactory |
| `dbcleaner` / `truncate` SQL | Hard-reset fixtures for stubborn integration tests | https://github.com/khaiql/dbcleaner |
| `mocker.spy` / `mocker.patch` | Assertion fixtures around external boundaries | pytest-mock docs |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes — `services: postgres/redis` for backed fixtures | Standard CI |
| GitLab CI | SaaS/self-host | Yes — `services:` keyword | Mirror of GH workflow |
| Testcontainers Cloud | SaaS | Yes — drop-in for local Docker | Useful when CI doesn't allow privileged Docker |
| Atomicjar / Testcontainers Desktop | SaaS | Yes — local UI for inspecting fixture containers | Dev experience |
| LocalStack Cloud | SaaS | Yes — REST | Fixture-grade AWS mocks at scale |
| WireMock Cloud | SaaS | Yes — REST | Hosted HTTP mocks reusable across suites |
| Mockoon | OSS+SaaS | Yes — REST | Lightweight HTTP fixtures |
| MailHog / MailDev / Mailpit | OSS | Yes — REST + SMTP | Email fixtures for integration tests |
| Stripe Mock / Stripe CLI | OSS | Yes — REST | Payment-fixture surrogate |
| HiveMQ Cloud / Mosquitto | OSS+SaaS | Yes — MQTT | Pub/sub fixtures |
| MinIO | OSS | Yes — S3 API | Object-storage fixtures |
| Redpanda / Kafka in Docker | OSS | Yes — Testcontainers | Streaming fixtures |
| Datadog CI Visibility | SaaS | Yes — agent | Track fixture-induced flake |
| Allure | OSS | Yes — `allure-pytest` | Surface fixture chains in reports |

## Templates & scripts

See methodology `templates.md` for full factory + conftest examples. Inline minimal Factory Boy registration (≤25 lines):

```python
# tests/factories/users.py
import factory
from factory.django import DjangoModelFactory, mute_signals
from django.db.models.signals import post_save
from apps.users.models import User

@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)
    email = factory.Faker("unique.email")
    name = factory.Faker("name")
    is_active = True

# tests/conftest.py
from pytest_factoryboy import register
from .factories.users import UserFactory
register(UserFactory)  # exposes fixtures: user, user_factory
```

Inline transactional DB fixture (SQLAlchemy, ≤30 lines):

```python
# tests/conftest.py (session-scoped engine, function-scoped session)
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture(scope="session")
def engine(pg_container):
    e = create_engine(pg_container.get_connection_url(), future=True)
    yield e
    e.dispose()

@pytest.fixture()
def db_session(engine):
    conn = engine.connect()
    trans = conn.begin()
    session = Session(bind=conn, future=True)
    nested = conn.begin_nested()
    try:
        yield session
    finally:
        session.close()
        if nested.is_active:
            nested.rollback()
        trans.rollback()
        conn.close()
```

Inline xdist-safe sequence fixture (≤15 lines):

```python
import os, factory

class WorkerScopedSequence(factory.Sequence):
    def evaluate(self, instance, step, extra):
        worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
        return f"{super().evaluate(instance, step, extra)}-{worker}"
```

## Best practices

- **Default to function scope.** Increase only when (a) setup is provably expensive and (b) the resource is immutable across tests.
- **Resource fixtures session-scoped, data fixtures function-scoped.** Don't mix.
- **Yield + cleanup**: `yield x; cleanup()` over `request.addfinalizer`; cleanup runs in correct LIFO order.
- **One factory per model**, named `<Model>Factory`. Cross-model relationships via `SubFactory`, not by hand-passing FKs.
- **`mute_signals`** wraps factories whose models trigger post_save side effects; assert side effects in dedicated tests.
- **Object Mother as a thin layer over factories**, not a parallel hierarchy. `UserMother.admin()` returns `UserFactory(role="admin")`.
- **`conftest.py` per directory**: root, `unit/`, `integration/`, `e2e/` — each scoped to its layer.
- **No God Fixtures.** If a fixture sets up >3 unrelated entities, split it.
- **Factory Boy `Sequence` is process-local** — wrap with worker scope or use `Faker` with `unique=True` for xdist.
- **Avoid `autouse`** unless the setup is universal across the file/dir; document each instance.
- **Test data tells the story**: domain-relevant fields visible in the test, factory fills the irrelevant rest.
- **Pin `responses` / `respx` strict mode**: `assert_all_requests_are_fired=True` catches mock drift.

## AI-agent gotchas

- **Agents reach for fixtures by default.** They invent fixtures for trivial dicts; reviewer rule: ≤2 lines of inline data → no fixture.
- **Scope-up to "make tests faster"** without confirming immutability. A `session`-scoped factory that mutates row count silently breaks downstream tests.
- **`autouse=True` mocks** that suppress real exceptions globally — agents add them to "fix" 5 tests, break 50 silently.
- **Mystery Guest re-introduction.** Agents move data into a fixture in conftest, deleting setup from the test body; reviewers can't follow.
- **Sequence collisions in xdist.** Agents use `factory.Sequence(lambda n: f"user-{n}")` and tests fail intermittently when two workers pick `user-1`. Worker-scope or `Faker(... unique=True)`.
- **post_save side effects** trigger Celery tasks during fixture creation. Agents wonder why "test sent emails". Wrap factories in `mute_signals`.
- **`session`-scoped DB without rollback**. Agents introduce a session DB fixture without a per-function transaction; rows accumulate, tests pass on first run, fail on rerun.
- **Cleanup leaks via `addfinalizer`.** Agents add finalizers to objects whose creation may fail; finalizer runs on a half-built object and crashes. Use yield + try/finally.
- **`responses.activate` + real network call** — agents disable strict mode and `add_passthru('https://')`, defeating the point.
- **Factory `LazyAttribute` referencing other factory fields** in wrong order causes `AttributeError`; agents miss the field-resolution sequence.
- **Tests that mutate shared fixture objects.** Agents add `.append(...)` to a list returned by a session fixture; next test sees stale state. Always copy or scope down.
- **Object Mother behavior baked into the test.** Agents use `UserMother.with_active_subscription()` for tests that don't care about subscription; the Mother semantics drift and tests start asserting on irrelevant invariants.
- **`tmp_path` shared across workers** if scoped wrong. Always function-scoped or `tmp_path_factory`-derived per worker.
- **Faker locale leakage.** Agents pick `Faker("uk_UA")` for one factory; downstream tests asserting on English-format strings break. Pin Faker locale at session level.
- **Forgotten mute_signals**: factory creates a User → post_save sends a welcome email via real SMTP in CI. Always block by default in test settings.

## References

- Methodology README: `./README.md`
- pytest fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html
- pytest fixture reference: https://docs.pytest.org/en/stable/reference/fixtures.html
- pytest-factoryboy: https://pytest-factoryboy.readthedocs.io
- Factory Boy: https://factoryboy.readthedocs.io
- Faker: https://faker.readthedocs.io
- mimesis: https://mimesis.name
- model-bakery (Django): https://model-bakery.readthedocs.io
- Fishery (TS): https://github.com/thoughtbot/fishery
- FactoryBot (Ruby): https://github.com/thoughtbot/factory_bot
- Testcontainers (Python): https://testcontainers-python.readthedocs.io
- LocalStack: https://docs.localstack.cloud
- responses: https://github.com/getsentry/responses
- respx: https://lundberg.github.io/respx/
- Hypothesis: https://hypothesis.readthedocs.io
- pytest-with-eric — Fixture Scopes: https://pytest-with-eric.com/fixtures/pytest-fixture-scope/
- "Replace Fixtures with Builders": https://dev.to/everlyhealth/replace-your-test-fixtures-with-builders-4602
- Test Data Builder pattern: https://ericvruder.dk/20191209/test-data-builder-pattern/
- Software Testing Anti-patterns: https://blog.codepipes.com/testing/software-testing-antipatterns.html
