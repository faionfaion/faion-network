# Integration Testing

## Summary

**One-sentence:** Produces an integration-test config (pytest + Testcontainers + respx/WireMock) with rollback isolation, FastAPI/Django dependency overrides, and factory fixtures.

**One-paragraph:** Integration tests catch the class of bugs unit tests cannot: ORM query bugs, constraint violations, serialization mismatches between layers, and middleware failures. Without containerised dependencies + rollback isolation they become slow, order-dependent, and flaky in CI. This methodology emits a runnable conftest set, dependency-override fixtures, and a WireMock/respx contract for external HTTP — pinned to the rollback-by-default discipline.

**Ефективно для:** backend team facing growing test suites where order-dependence and flakes from shared DB state are eating PR velocity.

## Applies If (ALL must hold)

- Code under test touches a database, message queue, or external HTTP service.
- pytest is the runner (or Django's pytest-django plugin).
- Docker is available locally and in CI for Testcontainers.
- Test data can be regenerated from factories — no production-data dependencies.
- Suite duration target is ≤5 minutes.

## Skip If (ANY kills it)

- Testing a single pure function with no external calls → unit-testing.
- Full user journey through a browser → e2e-testing.
- Environment cannot run Docker (some sandboxes) — must fall back to in-memory SQLite.
- Test depends on third-party SaaS behaviour that no fixture can model (run a smoke test in staging instead).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `service-graph.yaml` | list of {service, db_engine, external_apis} | operator |
| `framework` | fastapi / django / flask | repo |
| `parallel_target` | integer (worker count) | CI config |
| `secrets-redirect` | env-var names that must never hit real services | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[testing-pytest]] | pytest-fixture scoping and parametrisation. |
| [[test-fixtures]] | factory pattern + scope decisions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: rollback default, Testcontainers scoping, dependency_overrides clear, respx vs WireMock pick, factory uniqueness, no prod data, ban mocking the layer under test. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the integration-test-config artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: prod DB in CI, mocking the integration layer, shared state, missing dependency_overrides.clear(), hard-coded emails. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: inventory services → pick isolation → wire conftest → emit factories → wire external mocks. | ~700 |
| `content/05-examples.xml` | recommended | Postgres rollback + FastAPI client + respx mock end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks rollback vs truncate vs unique-ID; respx vs WireMock. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_service_graph` | haiku | Mechanical YAML→typed list. |
| `pick_isolation_strategy` | sonnet | Tradeoff between speed and constraint-violation accuracy. |
| `audit_dependency_overrides` | opus | Subtle leakage across tests when overrides aren't cleared. |
| `emit_conftest` | sonnet | Mechanical but must be importable. |

## Templates

| File | Purpose |
|---|---|
| `templates/conftest_postgres.py` | Session-scoped Postgres container + function-scoped transaction rollback session. |
| `templates/conftest_django.py` | Django conftest with Factory Boy UserFactory and admin_user fixture. |
| `templates/fastapi_client.py` | FastAPI TestClient and AsyncClient fixtures with dependency override. |
| `templates/_smoke-test.yaml` | Minimum service graph (one Postgres, one FastAPI app). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testing-pytest]]
- [[unit-testing]]
- [[e2e-testing]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `db_engine_required` (yes → Testcontainers + rollback; no → in-memory), then on `parallel_target` (≥2 → unique-ID factories; 1 → sequence-based), then on `external_http_calls` (none → no mock; few/simple → respx; many/complex → WireMock container). Each leaf cites a rule id.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/conftest_postgres.py`

```python
"""
conftest.py — PostgreSQL integration test setup.
Session-scoped Testcontainers container + function-scoped transaction rollback.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.models import Base


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container once per test session."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    """Create SQLAlchemy engine and all tables."""
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Fresh session per test with automatic transaction rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    db = Session()

    yield db

    db.close()
    transaction.rollback()
    connection.close()
```

### `templates/conftest_django.py`

```python
"""
conftest.py — Django integration test setup with Factory Boy.
Requires: pytest-django, factory-boy
"""
import factory
import pytest
from factory.django import DjangoModelFactory

from myapp.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    return UserFactory(is_staff=True, is_superuser=True)
```

### `templates/fastapi_client.py`

```python
"""
FastAPI test client fixtures — sync (TestClient) and async (AsyncClient).
Add to conftest.py; requires httpx.
"""
import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database import get_db


# --- Synchronous ---

@pytest.fixture
def client(session):
    """Sync TestClient with test DB session injected via dependency override."""
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# --- Asynchronous ---

@pytest.fixture
async def async_client(session):
    """Async client — required when app uses async DB drivers (asyncpg, motor)."""
    app.dependency_overrides[get_db] = lambda: session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c
    app.dependency_overrides.clear()
```

### `templates/_smoke-test.yaml`

```yaml
services:
  - service: api
    framework: fastapi
    db_engine: postgres
    external_apis:
      - {name: billing, url: https://billing.example.com}

drivers:
  db_engine_required: true
  commit_time_behavior_under_test: false
  parallel_target: 4
  external_http_calls: few
```
