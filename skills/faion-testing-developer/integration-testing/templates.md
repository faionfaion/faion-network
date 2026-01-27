# Integration Test Templates

Copy-paste templates for common integration testing scenarios.

## Testcontainers Setup

### PostgreSQL Template

```python
# conftest.py
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
    """Create SQLAlchemy engine and tables."""
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    """Create a fresh session with transaction rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### MySQL Template

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.mysql import MySqlContainer

from app.models import Base

@pytest.fixture(scope="session")
def mysql_container():
    with MySqlContainer("mysql:8") as mysql:
        yield mysql

@pytest.fixture(scope="session")
def engine(mysql_container):
    engine = create_engine(mysql_container.get_connection_url())
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

### MongoDB Template

```python
# conftest.py
import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient

@pytest.fixture(scope="session")
def mongodb_container():
    with MongoDbContainer("mongo:7") as mongo:
        yield mongo

@pytest.fixture(scope="session")
def mongo_client(mongodb_container):
    client = MongoClient(mongodb_container.get_connection_url())
    yield client
    client.close()

@pytest.fixture
def db(mongo_client):
    """Fresh database for each test."""
    database = mongo_client.test_db
    yield database
    # Clean up collections
    for collection in database.list_collection_names():
        database[collection].delete_many({})
```

### Redis Template

```python
# conftest.py
import pytest
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7-alpine") as redis:
        yield redis

@pytest.fixture
def redis_client(redis_container):
    """Fresh Redis client with cleanup."""
    client = redis_container.get_client()
    yield client
    client.flushdb()
```

### Multiple Services Template

```python
# conftest.py
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from testcontainers.rabbitmq import RabbitMqContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16-alpine") as container:
        yield container

@pytest.fixture(scope="session")
def redis():
    with RedisContainer("redis:7-alpine") as container:
        yield container

@pytest.fixture(scope="session")
def rabbitmq():
    with RabbitMqContainer("rabbitmq:3-management-alpine") as container:
        yield container

@pytest.fixture(scope="session")
def app_config(postgres, redis, rabbitmq):
    """Application configuration with all services."""
    return {
        "database_url": postgres.get_connection_url(),
        "redis_url": f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}",
        "rabbitmq_url": f"amqp://{rabbitmq.get_container_host_ip()}:{rabbitmq.get_exposed_port(5672)}"
    }
```

## FastAPI Test Templates

### Sync Client Template

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.deps import get_db

@pytest.fixture
def client(session):
    """Test client with database session override."""
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
```

### Async Client Template

```python
# conftest.py
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.deps import get_db

@pytest.fixture
async def async_client(session):
    """Async test client with database session override."""
    app.dependency_overrides[get_db] = lambda: session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
```

### Authentication Fixtures Template

```python
# conftest.py
import pytest
from datetime import timedelta

from app.auth import create_access_token
from app.models import User

@pytest.fixture
def user(session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=hash_password("testpass123")
    )
    session.add(user)
    session.flush()
    return user

@pytest.fixture
def admin_user(session):
    """Create an admin user."""
    user = User(
        email="admin@example.com",
        name="Admin User",
        hashed_password=hash_password("adminpass123"),
        is_admin=True
    )
    session.add(user)
    session.flush()
    return user

@pytest.fixture
def auth_headers(user):
    """Valid authentication headers."""
    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(hours=1)
    )
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(admin_user):
    """Admin authentication headers."""
    token = create_access_token(
        data={"sub": str(admin_user.id), "role": "admin"},
        expires_delta=timedelta(hours=1)
    )
    return {"Authorization": f"Bearer {token}"}
```

## pytest-django Templates

### Basic Django Test Setup

```python
# conftest.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User"
    )

@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123"
    )

@pytest.fixture
def api_client():
    """DRF API client."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    """Admin authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client
```

### Django Factory Fixtures Template

```python
# conftest.py
import pytest
import factory
from factory.django import DjangoModelFactory

from myapp.models import User, Product, Order

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    sku = factory.Sequence(lambda n: f"SKU-{n:06d}")

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    status = "pending"
    total = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def product(db):
    return ProductFactory()

@pytest.fixture
def order(db, user):
    return OrderFactory(user=user)
```

## API Test Templates

### CRUD Test Template

```python
# test_api_users.py
import pytest

class TestUserAPI:
    """Test user CRUD operations."""

    def test_create_user(self, client):
        """POST /api/users - Create user."""
        response = client.post("/api/users", json={
            "email": "new@example.com",
            "name": "New User",
            "password": "securepass123"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert "id" in data
        assert "password" not in data

    def test_get_user(self, client, user, auth_headers):
        """GET /api/users/{id} - Get user by ID."""
        response = client.get(
            f"/api/users/{user.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["id"] == user.id

    def test_update_user(self, client, user, auth_headers):
        """PATCH /api/users/{id} - Update user."""
        response = client.patch(
            f"/api/users/{user.id}",
            json={"name": "Updated Name"},
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_delete_user(self, client, user, admin_headers):
        """DELETE /api/users/{id} - Delete user (admin only)."""
        response = client.delete(
            f"/api/users/{user.id}",
            headers=admin_headers
        )

        assert response.status_code == 204

    def test_list_users(self, client, auth_headers, session):
        """GET /api/users - List all users with pagination."""
        # Setup: Create multiple users
        from app.models import User
        for i in range(15):
            session.add(User(email=f"user{i}@example.com", name=f"User {i}"))
        session.flush()

        # Test first page
        response = client.get(
            "/api/users?page=1&size=10",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] >= 15
```

### Error Handling Test Template

```python
# test_api_errors.py
import pytest

class TestAPIErrors:
    """Test API error handling."""

    def test_not_found(self, client, auth_headers):
        """GET /api/users/{id} - Non-existent resource."""
        response = client.get(
            "/api/users/99999",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_validation_error(self, client):
        """POST /api/users - Invalid data."""
        response = client.post("/api/users", json={
            "email": "not-an-email",
            "name": ""
        })

        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any(e["loc"][-1] == "email" for e in errors)

    def test_unauthorized(self, client):
        """Protected endpoint without auth."""
        response = client.get("/api/profile")

        assert response.status_code == 401

    def test_forbidden(self, client, auth_headers):
        """Admin endpoint with user auth."""
        response = client.get("/api/admin/users", headers=auth_headers)

        assert response.status_code == 403

    def test_conflict(self, client, user):
        """POST /api/users - Duplicate email."""
        response = client.post("/api/users", json={
            "email": user.email,  # Already exists
            "name": "Duplicate",
            "password": "pass123"
        })

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()
```

## External Service Mock Templates

### respx Mock Template

```python
# test_external_services.py
import pytest
import respx
from httpx import Response

class TestPaymentService:
    """Test payment integration with mocked gateway."""

    @pytest.mark.anyio
    @respx.mock
    async def test_charge_success(self):
        """Successful payment charge."""
        respx.post("https://api.stripe.com/v1/charges").mock(
            return_value=Response(200, json={
                "id": "ch_123",
                "status": "succeeded",
                "amount": 10000
            })
        )

        result = await payment_service.charge(
            amount=100.00,
            currency="USD",
            source="tok_visa"
        )

        assert result["status"] == "succeeded"

    @pytest.mark.anyio
    @respx.mock
    async def test_charge_declined(self):
        """Declined payment."""
        respx.post("https://api.stripe.com/v1/charges").mock(
            return_value=Response(402, json={
                "error": {
                    "type": "card_error",
                    "code": "card_declined"
                }
            })
        )

        with pytest.raises(PaymentDeclinedError):
            await payment_service.charge(
                amount=100.00,
                currency="USD",
                source="tok_declined"
            )

    @pytest.mark.anyio
    @respx.mock
    async def test_service_unavailable(self):
        """Payment service unavailable."""
        import httpx

        respx.post("https://api.stripe.com/v1/charges").mock(
            side_effect=httpx.TimeoutException("Connection timeout")
        )

        with pytest.raises(PaymentServiceUnavailableError):
            await payment_service.charge(
                amount=100.00,
                currency="USD",
                source="tok_visa"
            )
```

### WireMock Template

```python
# conftest.py
import pytest
import requests
import time
from testcontainers.core.container import DockerContainer

@pytest.fixture(scope="session")
def wiremock():
    """Start WireMock container."""
    container = DockerContainer("wiremock/wiremock:3.3.1")
    container.with_exposed_ports(8080)
    container.start()

    base_url = f"http://{container.get_container_host_ip()}:{container.get_exposed_port(8080)}"

    # Wait for WireMock readiness
    for _ in range(30):
        try:
            requests.get(f"{base_url}/__admin/mappings")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    yield base_url
    container.stop()

@pytest.fixture
def mock_email_service(wiremock):
    """Mock email service."""
    requests.post(f"{wiremock}/__admin/mappings", json={
        "request": {
            "method": "POST",
            "urlPath": "/api/v1/send"
        },
        "response": {
            "status": 202,
            "jsonBody": {"message_id": "msg_123", "status": "queued"},
            "headers": {"Content-Type": "application/json"}
        }
    })

    yield wiremock

    requests.delete(f"{wiremock}/__admin/mappings")
```

## Message Queue Templates

### RabbitMQ Template

```python
# conftest.py
import pytest
import pika
from testcontainers.rabbitmq import RabbitMqContainer

@pytest.fixture(scope="session")
def rabbitmq():
    with RabbitMqContainer("rabbitmq:3-management-alpine") as container:
        yield container

@pytest.fixture
def rabbitmq_channel(rabbitmq):
    """Create RabbitMQ channel with test queue."""
    params = pika.ConnectionParameters(
        host=rabbitmq.get_container_host_ip(),
        port=rabbitmq.get_exposed_port(5672)
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="test_queue", durable=True)

    yield channel

    channel.queue_delete(queue="test_queue")
    connection.close()
```

### Kafka Template

```python
# conftest.py
import pytest
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer
import json

@pytest.fixture(scope="session")
def kafka():
    with KafkaContainer("confluentinc/cp-kafka:7.5.0") as container:
        yield container

@pytest.fixture
def kafka_producer(kafka):
    producer = KafkaProducer(
        bootstrap_servers=kafka.get_bootstrap_server(),
        value_serializer=lambda v: json.dumps(v).encode()
    )
    yield producer
    producer.close()

@pytest.fixture
def kafka_consumer(kafka):
    consumer = KafkaConsumer(
        "test-topic",
        bootstrap_servers=kafka.get_bootstrap_server(),
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode()),
        consumer_timeout_ms=5000
    )
    yield consumer
    consumer.close()
```

## pytest.ini Configuration Template

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Async support
asyncio_mode = auto

# Django settings (if using Django)
DJANGO_SETTINGS_MODULE = myproject.settings.test

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests

# Coverage
addopts = --cov=app --cov-report=term-missing --cov-fail-under=80

# Warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

## pyproject.toml Configuration Template

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "e2e: marks tests as end-to-end tests",
]
addopts = "--cov=app --cov-report=term-missing"

[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
