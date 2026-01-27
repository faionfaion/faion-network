# Integration Testing

## Overview

Integration testing verifies that multiple components work correctly together using real dependencies (databases, APIs, message queues, external services) or realistic test doubles.

**Key difference from other test types:**

| Test Type | Scope | Dependencies | Speed |
|-----------|-------|--------------|-------|
| **Unit** | Single function/class | Mocked | Milliseconds |
| **Integration** | Multiple components | Real (containerized) | Seconds |
| **E2E** | Full user flow | Production-like | Minutes |

## When to Use Integration Tests

- Database interactions (ORM, queries, transactions)
- API endpoints with real request/response cycles
- Message queue producers and consumers
- Service-to-service communication
- Authentication and authorization flows
- Cache interactions (Redis, Memcached)
- File storage operations

## Test Isolation Strategies

### 1. Transaction Rollback (Recommended for Speed)

Wrap each test in a transaction that rolls back after completion.

```python
@pytest.fixture
def db_session(engine):
    """Fresh session per test with automatic rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

**Pros:** Fast, no cleanup needed
**Cons:** Won't catch commit-time errors (unique constraints)

### 2. Database Reset (Recommended for Accuracy)

Truncate tables or recreate database between tests.

```python
@pytest.fixture(autouse=True)
def reset_db(db_session):
    """Truncate all tables before each test."""
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
```

**Pros:** Catches all errors, realistic behavior
**Cons:** Slower than rollback

### 3. Testcontainers (Recommended for CI/CD)

Spin up real Docker containers per test session.

```python
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres
```

**Pros:** Real database behavior, isolated, reproducible
**Cons:** Requires Docker, slower startup

### 4. Unique Test Data (Recommended for Parallel Tests)

Generate unique identifiers for each test run.

```python
@pytest.fixture
def unique_email():
    return f"test-{uuid.uuid4()}@example.com"
```

**Pros:** Tests can run in parallel
**Cons:** Database accumulates test data

## Database Testing Patterns

### Pattern 1: Session-Scoped Container + Transaction Rollback

Best balance of speed and isolation.

```python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16-alpine") as container:
        yield container

@pytest.fixture(scope="session")
def engine(postgres):
    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### Pattern 2: pytest-django Integration

```python
import pytest

@pytest.mark.django_db
def test_create_user():
    """Uses Django's test database with transaction rollback."""
    user = User.objects.create(email="test@example.com")
    assert user.pk is not None

@pytest.mark.django_db(transaction=True)
def test_with_transaction():
    """For tests that need real transaction commits."""
    pass

@pytest.mark.django_db(reset_sequences=True)
def test_with_fresh_ids():
    """Reset auto-increment sequences."""
    user = User.objects.create(email="test@example.com")
    assert user.pk == 1
```

### Pattern 3: Factory Fixtures

Use factories for consistent test data creation.

```python
import factory
from factory.django import DjangoModelFactory

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
    return UserFactory(is_admin=True)
```

## API Testing with httpx

### Synchronous Testing

```python
from fastapi.testclient import TestClient

@pytest.fixture
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_create_user(client):
    response = client.post("/api/users", json={
        "email": "new@example.com",
        "name": "New User"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "new@example.com"
```

### Async Testing

```python
import pytest
from httpx import ASGITransport, AsyncClient

@pytest.fixture
async def async_client(session):
    app.dependency_overrides[get_db] = lambda: session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.mark.anyio
async def test_async_endpoint(async_client):
    response = await async_client.get("/api/health")
    assert response.status_code == 200
```

## External Service Testing

### WireMock for HTTP Mocking

```python
from testcontainers.core.container import DockerContainer

@pytest.fixture(scope="session")
def wiremock():
    container = DockerContainer("wiremock/wiremock:3.3.1")
    container.with_exposed_ports(8080)
    container.start()

    base_url = f"http://{container.get_container_host_ip()}:{container.get_exposed_port(8080)}"
    wait_for_wiremock(base_url)

    yield base_url
    container.stop()

@pytest.fixture
def mock_payment_gateway(wiremock):
    requests.post(f"{wiremock}/__admin/mappings", json={
        "request": {"method": "POST", "urlPath": "/charge"},
        "response": {
            "status": 200,
            "jsonBody": {"payment_id": "pay_123", "status": "success"}
        }
    })
    yield wiremock
    requests.delete(f"{wiremock}/__admin/mappings")
```

### respx for httpx Mocking

```python
import respx
from httpx import Response

@respx.mock
async def test_external_api():
    respx.get("https://api.example.com/users/1").mock(
        return_value=Response(200, json={"id": 1, "name": "Test"})
    )

    result = await fetch_user(1)
    assert result["name"] == "Test"
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Testing against production | Data corruption | Use Testcontainers |
| Shared test data | Tests affect each other | Transaction rollback |
| No cleanup | Data accumulates | Reset fixtures |
| Slow tests | Developer friction | Session-scoped containers |
| Mocking integrations | Defeats purpose | Use real services |
| Ignoring timeouts | Flaky tests | Set explicit timeouts |

## Folder Structure

```
integration-testing/
├── README.md           # This file
├── checklist.md        # Pre-test checklist
├── examples.md         # Real-world examples
├── templates.md        # Copy-paste templates
└── llm-prompts.md      # AI generation prompts
```

## Resources

### Official Documentation

- [Testcontainers Python](https://testcontainers-python.readthedocs.io/) - Docker containers for tests
- [pytest-django](https://pytest-django.readthedocs.io/) - Django testing with pytest
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) - Official testing guide
- [httpx Testing](https://www.python-httpx.org/advanced/testing/) - HTTPX test utilities

### Best Practices

- [Martin Fowler - Integration Test](https://martinfowler.com/bliki/IntegrationTest.html) - Testing principles
- [Testcontainers Best Practices](https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/) - Container testing guide

### Related Skills

- [faion-python-developer](../faion-python-developer/CLAUDE.md) - pytest, Django, FastAPI
- [faion-api-developer](../faion-api-developer/CLAUDE.md) - REST, GraphQL testing
- [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) - CI/CD integration
