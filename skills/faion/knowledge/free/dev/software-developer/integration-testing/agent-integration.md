# Agent Integration — Integration Testing

## When to use
- Verifying ORM queries, migrations, and transactions against a real database (Postgres / MySQL / SQLite).
- Testing API endpoints end-to-end inside the process (TestClient / supertest), bypassing only network and external auth.
- Exercising message-queue producers/consumers (RabbitMQ / Kafka / SQS) with real broker.
- Auth flows: token issuance, role checks, expired/forged tokens.
- Outbound HTTP integrations against WireMock / mockoon / Pact.
- Migration safety: every migration runs in CI on a fresh database before merge.

## When NOT to use
- Pure functions / stateless logic — unit tests are faster and more focused.
- Cross-service end-to-end flows that need browsers / multiple processes — use E2E (Playwright/Cypress) instead.
- Performance benchmarking — use dedicated load tools (k6, Locust).
- Fast inner-loop development feedback — keep these in a separate `tests/integration/` and run on CI + on-demand.

## Where it fails / limitations
- Slow: Testcontainers' first cold start is multi-second; agents writing 200 integration tests will burn CI budget fast.
- Flaky shared state: if two tests both write to the same row, parallel runs collide; transactions help but not for cross-connection state.
- Test isolation in async stacks is tricky — the test client and the app may not share the same DB session unless dependency overrides are set up correctly.
- WireMock / mockoon stubs drift from real upstream; tests pass while production breaks. Pair with contract tests.
- Agents copy fixtures pattern across tests, creating O(N) Postgres connections; container exhaustion under parallel run.
- `testcontainers-python` has version-skew issues with new Docker desktop releases.

## Agentic workflow
A test-fixture subagent owns `conftest.py` / `setup.ts`: it stands up a session-scoped container, builds the schema, and exposes a per-test transaction-rollback session. A feature-test subagent writes one test class per service (`TestUserAPI`, `TestPaymentIntegration`) and is forbidden from re-defining fixtures. CI runs in two passes: unit (sub-second per test, all run on every push) and integration (containers, runs on PR + main). A reviewer subagent enforces the unit/integration split: no Testcontainers / no `TestClient` outside `tests/integration/`.

### Recommended subagents
- `faion-sdd-execution` — already enforces test gates on every change.
- A `fixture-author` subagent (custom) — single-purpose: design DB / queue / HTTP fixtures with proper scoping (session vs function).
- `faion-feature-executor` — sequentially exercise integration tests for a feature task.
- A `flake-hunter` subagent — runs the integration suite N times, flags tests with non-zero failure count, opens issues per flake.

### Prompt pattern
```
Write integration tests for <module> in tests/integration/test_<module>.py. Constraints:
1. Use existing fixtures from conftest.py (db_session, client, auth_headers); do not redefine.
2. Each test must roll back via the transaction-scoped fixture.
3. No mocks for the database; mocks ONLY for outbound HTTP via WireMock or respx.
4. Assert HTTP status AND body shape AND that no orphan rows remain (count check at end if relevant).
```

```
Review fixtures. Block if: fixture scope is `session` for stateful resources, missing `yield + cleanup`, container started outside a `with` / context manager, or tests share a single connection without transaction isolation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `testcontainers-python` | Spin up Postgres/RabbitMQ/Redis/etc. in tests | https://testcontainers-python.readthedocs.io |
| `testcontainers` (Node) | Same for JS/TS | https://node.testcontainers.org |
| `pytest-postgresql` | Lightweight Postgres-only fixtures | https://pypi.org/project/pytest-postgresql/ |
| `httpx` + `respx` | Mock outbound HTTP for httpx clients | https://github.com/lundberg/respx |
| `vcrpy` / `polly.js` | Record-replay HTTP cassettes | https://vcrpy.readthedocs.io |
| `WireMock` (CLI/Docker) | Standalone HTTP stub server | https://wiremock.org |
| `mockoon` | GUI/CLI mock server | https://mockoon.com |
| `pact-broker` (Pact CLI) | Consumer-driven contract testing | https://docs.pact.io |
| `pytest-xdist` | Parallel test runs (`-n auto`) | https://pytest-xdist.readthedocs.io |
| `pytest-asyncio` / `pytest-anyio` | Async test support | https://pytest-asyncio.readthedocs.io |
| `factoryboy` / `model-bakery` | Factories for test data | https://factoryboy.readthedocs.io / https://model-bakery.readthedocs.io |
| `hypothesis` | Property-based testing add-on | https://hypothesis.works |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions services | SaaS | yes | `services: postgres:` / `redis:` for cheaper CI than full Testcontainers in Linux runners. |
| LocalStack | OSS | yes | Local AWS emulator for S3/SQS/DynamoDB integration tests. |
| Pact / PactFlow | OSS+SaaS | yes | Contract test broker; pairs with WireMock to detect drift. |
| Codecov | SaaS | yes | Track integration vs unit coverage separately. |
| Datadog Test Visibility | SaaS | yes | Flake tracking and per-test runtime. |
| Buildkite / CircleCI | SaaS | yes | Better Docker-in-Docker support than older GHA runners. |

## Templates & scripts
See `templates.md` for full pytest/Supertest fixture templates. Inline minimum-viable Postgres fixture pair:

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from app.db import Base

@pytest.fixture(scope="session")
def _engine():
    with PostgresContainer("postgres:16") as pg:
        eng = create_engine(pg.get_connection_url())
        Base.metadata.create_all(eng)
        yield eng

@pytest.fixture
def db_session(_engine):
    conn = _engine.connect()
    tx = conn.begin()
    Session = sessionmaker(bind=conn)
    s = Session()
    try:
        yield s
    finally:
        s.close()
        tx.rollback()
        conn.close()
```

CI snippet (GitHub Actions, faster than Testcontainers for small suites):

```yaml
services:
  postgres:
    image: postgres:16
    env: { POSTGRES_PASSWORD: ci, POSTGRES_DB: app }
    ports: ['5432:5432']
    options: >-
      --health-cmd pg_isready --health-interval 5s --health-retries 12
```

## Best practices
- Two-tier strategy: unit tests on every save, integration tests on push/PR. Don't merge them.
- Transaction-rollback fixture per test = fastest viable isolation for SQL.
- For async stacks (FastAPI / Litestar / aiohttp), share the DB session via dependency override; otherwise the test client opens a different session and you'll see "where's my row?" failures.
- Use real factories with `factory_boy` / `model-bakery` instead of inline `User(...)` literals — keeps tests readable and cheap to update when models grow columns.
- Pin container image tags (`postgres:16.2`) — `postgres:latest` will break the suite when a new major drops.
- Test failure paths: timeouts, 5xx upstream, retries — most agent-written integration tests cover only the happy path.
- Run the integration suite with `--randomly` (pytest-randomly) once per week to surface order dependencies.

## AI-agent gotchas
- LLMs forget to roll back transactions, leaving rows that break later tests. Standardize on a per-test transaction fixture and ban inline `Session()` creation.
- Agents over-mock: they'll mock the database in "integration" tests, producing tests that prove nothing. Lint with grep: no `unittest.mock` imports in `tests/integration/`.
- Async vs sync confusion: agents mix `TestClient` (sync) with `async def` tests, or call `await client.get()` on a sync client. Fix by standardizing on one (httpx `AsyncClient`).
- Auth headers: agents hardcode tokens into tests; use a fixture that mints a token per test scenario.
- Container leakage: agents spawn a new container per test (function-scope) instead of session-scope. Audit fixture scope explicitly.
- Human-in-loop: review CI runtime growth — integration suites > 5 minutes degrade developer feedback. Force agents to budget runtime in PR descriptions.
- WireMock stubs that pass tests but drift from real upstream → couple with periodic contract verification (Pact) or scheduled real-API smoke tests.
- `pytest -p no:cacheprovider` in CI to avoid stale cache flakes when code generation is in the loop.

## References
- https://martinfowler.com/bliki/IntegrationTest.html — "what is an integration test"
- https://testcontainers-python.readthedocs.io — Testcontainers Python
- https://node.testcontainers.org — Testcontainers Node
- https://fastapi.tiangolo.com/tutorial/testing/ — FastAPI testing
- https://docs.pytest.org/en/stable/how-to/fixtures.html — pytest fixtures
- https://wiremock.org/docs/ — WireMock
- https://docs.pact.io — consumer-driven contract testing
- https://github.com/SeleniumHQ/seleniumhq.github.io/blob/trunk/website_and_docs/content/documentation/test_practices/encouraged/test_pyramid.md — test pyramid background
