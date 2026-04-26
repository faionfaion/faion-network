# Agent Integration — Integration Testing

## When to use
- Validating ORM behavior against a real database (Postgres, MySQL, SQLite-in-memory only as fallback).
- API endpoint tests with full request/response cycle through the HTTP framework (FastAPI, Django, Express, Fastify).
- Message-queue producers and consumers (Kafka, RabbitMQ, SQS) where serialization and routing matter.
- Cache integration (Redis / Valkey / Memcached) — race conditions, TTL behavior, eviction.
- Auth/authorization flows that span middleware + DB + token issuer.
- Service-to-service calls inside a single deployable (e.g., Django view calling internal Celery task).
- File storage (S3, GCS, MinIO) with real client + LocalStack / Testcontainers.

## When NOT to use
- Pure business logic — unit test, no real dependencies needed.
- UI / browser flows — that's E2E, use Playwright/Cypress.
- Cross-service contract verification — use Pact / consumer-driven contracts.
- Performance/load testing — wrong tool; use k6 / Locust / Gatling.
- Production smoke tests — use synthetic monitoring instead (Datadog Synthetics, Checkly).
- Code that's just a thin pass-through (controller → service → repo with no logic) — integration test gives confidence at lower cost than unit + integration both.

## Where it fails / limitations
- README's "Transaction Rollback" pattern won't catch commit-time errors (unique constraints, deferred FK checks); agents apply it universally and miss commit bugs.
- `Testcontainers` startup is slow (5–20s per container); agents create one per test instead of session-scoped.
- README mentions Postgres / MongoDB / Redis but no guidance on **schema migration** in tests — agents either run full migrations every test (slow) or none (drift).
- No mention of test data isolation strategies for parallel test runs (per-worker schema, per-test prefix).
- Async drivers (asyncpg, motor) need different fixture lifecycles than sync; agents copy sync patterns.
- Snapshot or "golden file" tests for API responses are not covered; agents accept any 2xx as passing.
- Container orchestration in CI: agents over-provision (separate Postgres per test job) instead of shared compose stack.
- Time-zone bugs hide between app server and DB server clocks; tests rarely cover this.

## Agentic workflow
Default to **session-scoped Testcontainers** + **per-test transaction rollback** for fast tests. Per integration target: (1) start container in `conftest.py` session fixture; (2) apply migrations once at session start; (3) per-test fixture opens a transaction, yields a connection, rolls back on teardown; (4) test makes real HTTP calls via `TestClient`/`httpx.AsyncClient` to the running app. CI: run integration tests separately from unit (`pytest -m integration`) so unit feedback stays sub-30s. For commit-time-error tests, opt in to "truncate" isolation per test class.

### Recommended subagents
- `faion-test-agent` (custom) — emit integration tests with proper container lifecycle.
- `faion-software-architect` — decides which seams are integration-tested vs unit-tested.
- Reviewer subagent — checks for missing `@pytest.mark.integration`, container leaks, hard-coded ports.
- `faion-devops-engineer` — wires Testcontainers / docker-compose into CI, manages volumes/network.
- `faion-sdd-executor-agent` — when integration tests are part of SDD acceptance gates.

### Prompt pattern
```
Integration test target: api/orders.py POST /orders.
Use:
- pytest + pytest-asyncio + httpx.AsyncClient
- testcontainers Postgres 16 (session-scoped)
- alembic upgrade head ONCE at session start
- per-test transaction with rollback on teardown
- factory-boy for User and Product fixtures
Cover:
- 201 happy path; persisted row matches input.
- 401 when no auth header.
- 422 when product_id missing.
- 409 when stock insufficient (commit-time check; do not roll back, use truncate fixture).
Mark with @pytest.mark.integration.
```

```
Audit: scan tests/integration/ for:
- Function-scope Testcontainer fixtures (slow).
- Missing migration step.
- Hard-coded host:port (use container.get_connection_url()).
- Tests that hit real network beyond the container.
Output table with file:line, smell, fix. Do not edit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `testcontainers-python` | Programmatic Docker containers in Python | https://testcontainers-python.readthedocs.io |
| `testcontainers-go` | Go variant | https://golang.testcontainers.org |
| `testcontainers-node` | JS/TS variant | https://node.testcontainers.org |
| `pytest-postgresql` | Lightweight pg fixture (template DB) | https://github.com/dbfixtures/pytest-postgresql |
| `pytest-redis` | Redis fixture | https://github.com/dbfixtures/pytest-redis |
| `httpx` / `httpx.AsyncClient` | Real HTTP calls into TestClient | https://www.python-httpx.org |
| `respx` / `pytest-httpx` | Mock outbound HTTP in integration tests | https://lundberg.github.io/respx |
| `alembic` / `flyway` / `goose` | Schema migrations | https://alembic.sqlalchemy.org |
| `LocalStack` | Local AWS API for S3/SQS/SNS integration tests | https://localstack.cloud |
| `wiremock` | Stand-alone HTTP mock for upstream services | https://wiremock.org |
| `factory_boy` / `@faker-js/faker` | Test data factories | https://factoryboy.readthedocs.io |
| `tilt` / `docker compose` | Local stack orchestration for integration | https://tilt.dev / https://docs.docker.com/compose |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Testcontainers Cloud | SaaS | Yes — Docker context | Offload containers from CI runner; faster on small runners |
| GitHub Actions services | CI | Yes — `services:` block | Postgres / Redis as ephemeral side-services |
| GitLab CI services | CI | Yes — `services:` block | Same model as GH |
| LocalStack | OSS + Pro | Yes — REST + boto3 | Replace mocking AWS SDK calls; closer to real |
| Mockoon CLI | OSS | Yes — CLI + Docker | Mock upstream APIs your service calls during integration |
| Pact Broker | OSS + SaaS | Yes — REST | Pair with integration: integration tests verify your impl, contract tests verify shape with consumers |

## Templates & scripts
See `templates.md` for full Testcontainers + Alembic + transaction-rollback fixtures. Inline session-scoped Postgres fixture:

```python
# tests/integration/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer
from alembic import command
from alembic.config import Config

@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as pg:
        url = pg.get_connection_url().replace("psycopg2", "psycopg")
        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", url)
        command.upgrade(cfg, "head")
        yield url

@pytest.fixture
def db_session(postgres_url):
    engine = create_engine(postgres_url)
    conn = engine.connect()
    txn = conn.begin()
    session = Session(bind=conn)
    try:
        yield session
    finally:
        session.close()
        txn.rollback()
        conn.close()
```

## Best practices
- **Session-scoped containers, function-scoped data isolation.** Containers are expensive; rollbacks are cheap.
- **Run migrations once per session.** Test failures from forgotten migrations are the #1 cause of CI red runs.
- **Mark integration tests** (`@pytest.mark.integration`, `//go:build integration`) and run separately from unit.
- **Use the real HTTP client** (`httpx.AsyncClient` for FastAPI, `Django Test Client`, `supertest` for Express) — exercises middleware, serializers, auth.
- **Don't mock the integration target.** If you need to mock the DB in a "DB integration test", you've left integration territory.
- **Parallel-safe data**: use UUIDs / sequence prefixes per test worker to avoid PK collisions; or use per-worker schemas.
- **Pin Docker image tags** (`postgres:16.4-alpine`), not `latest` — surprise upgrades break tests.
- **Keep one upstream-service mock per test** — multiple Wiremock instances per test are fragile.
- **Volume cleanup**: `tmpfs` for Postgres data dir is faster and self-cleans.
- **Time-zone**: run containers with `TZ=UTC` and assert all timestamps in UTC.
- **Network**: prefer `network_mode=host` is tempting but breaks parallelism; use Testcontainers default bridge.

## AI-agent gotchas
- **Function-scope Testcontainers**: agents create per-test containers, suite balloons to 30+ minutes. Force session scope and explain why.
- **Missing migration step**: empty DB, all queries fail with `relation does not exist`. Run migrations once at session start.
- **Hard-coded `localhost:5432`** instead of `container.get_connection_url()` — works locally, fails in CI where Docker uses bridge networks.
- **Async fixture forgetfulness**: `@pytest.fixture async def` requires `pytest-asyncio` >= 0.23 with `asyncio_mode = "auto"`; agents miss the config and fixtures hang.
- **Transaction rollback + commit-time errors**: rollback masks unique-constraint violations because the test never commits. Switch to truncate isolation when testing constraint behavior.
- **Connection pool leaks**: agents create engines per test without disposing; PG connection limit hits in long suites.
- **`TestClient` vs real HTTP server**: FastAPI's `TestClient` doesn't run lifespan handlers in older versions; agents use it for tests requiring startup events and they don't fire.
- **LocalStack vs real S3**: signed-URL behavior, eventual consistency, ACL semantics differ; agents write tests passing on LocalStack that fail in prod.
- **Parallel xdist + shared DB**: agents skip per-worker isolation, tests interfere intermittently, get marked "flaky" instead of "wrong".
- **Migration runs on every test**: agents place `alembic upgrade head` in function-scope fixture; multiplies suite time by N.
- **Mocking the DB inside an integration test** to "make it faster" — defeats the test type. Reject.
- **Time zone hidden**: app uses `localtime`, container uses UTC, `created_at` differs by hours; assertions on dates flake.
- **Human-in-loop checkpoint**: review fixture scope (session vs module vs function) before merging — wrong scope is the most expensive bug to fix later.

## References
- README: `./README.md`
- Sibling: `../unit-testing/`, `../e2e-testing/`, `../mocking-strategies/`, `../testing-pytest/`
- Testcontainers: https://testcontainers.com
- Testcontainers Python: https://testcontainers-python.readthedocs.io
- LocalStack: https://localstack.cloud
- Pact: https://docs.pact.io
- Martin Fowler — Integration Test: https://martinfowler.com/bliki/IntegrationTest.html
- Brandur Leach — Postgres test isolation: https://brandur.org/fragments/postgres-test-isolation
- Sam Newman — Testing Microservices: https://samnewman.io/talks/microservice-testing/
