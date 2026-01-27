# Integration Testing Examples

## Database Integration Tests

### PostgreSQL with Testcontainers

```python
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from testcontainers.postgres import PostgresContainer

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

# Session-scoped container (starts once per test session)
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def engine(postgres_container):
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

class TestUserRepository:

    def test_create_user(self, session):
        user = User(email="test@example.com", name="Test User")
        session.add(user)
        session.flush()

        assert user.id is not None
        assert user.email == "test@example.com"

    def test_find_by_email(self, session):
        user = User(email="find@example.com", name="Find Me")
        session.add(user)
        session.flush()

        result = session.query(User).filter_by(email="find@example.com").first()

        assert result is not None
        assert result.name == "Find Me"

    def test_unique_constraint(self, session):
        from sqlalchemy.exc import IntegrityError

        session.add(User(email="dup@example.com", name="First"))
        session.flush()

        session.add(User(email="dup@example.com", name="Second"))

        with pytest.raises(IntegrityError):
            session.flush()
```

### MongoDB with Testcontainers

```python
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
    database = mongo_client.test_db
    yield database
    # Clean up after each test
    for collection in database.list_collection_names():
        database[collection].delete_many({})

class TestProductRepository:

    def test_insert_product(self, db):
        products = db.products
        result = products.insert_one({
            "name": "Widget",
            "price": 19.99,
            "category": "electronics"
        })

        assert result.inserted_id is not None

    def test_find_by_category(self, db):
        products = db.products
        products.insert_many([
            {"name": "Widget", "category": "electronics"},
            {"name": "Gadget", "category": "electronics"},
            {"name": "Book", "category": "media"},
        ])

        result = list(products.find({"category": "electronics"}))

        assert len(result) == 2
        assert all(p["category"] == "electronics" for p in result)
```

### Redis with Testcontainers

```python
import pytest
from testcontainers.redis import RedisContainer
import redis
import json

@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7-alpine") as container:
        yield container

@pytest.fixture
def redis_client(redis_container):
    client = redis_container.get_client()
    yield client
    client.flushdb()  # Clean up after each test

class TestCacheService:

    def test_set_and_get(self, redis_client):
        redis_client.set("user:1", json.dumps({"id": 1, "name": "Test"}))

        result = json.loads(redis_client.get("user:1"))

        assert result["id"] == 1
        assert result["name"] == "Test"

    def test_expiration(self, redis_client):
        redis_client.setex("temp_key", 1, "temp_value")

        assert redis_client.get("temp_key") == b"temp_value"

        import time
        time.sleep(1.1)

        assert redis_client.get("temp_key") is None

    def test_hash_operations(self, redis_client):
        redis_client.hset("user:1", mapping={
            "email": "test@example.com",
            "name": "Test User"
        })

        email = redis_client.hget("user:1", "email")
        assert email == b"test@example.com"

        all_fields = redis_client.hgetall("user:1")
        assert len(all_fields) == 2
```

## API Integration Tests

### FastAPI with TestClient

```python
import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

@app.post("/api/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Tests
@pytest.fixture
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

class TestUserAPI:

    def test_create_user_success(self, client):
        response = client.post("/api/users", json={
            "email": "new@example.com",
            "name": "New User"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert "id" in data

    def test_create_user_invalid_email(self, client):
        response = client.post("/api/users", json={
            "email": "",  # Invalid
            "name": "User"
        })

        assert response.status_code == 422  # Validation error

    def test_get_user_success(self, client, session):
        # Setup
        user = User(email="existing@example.com", name="Existing")
        session.add(user)
        session.flush()

        # Test
        response = client.get(f"/api/users/{user.id}")

        assert response.status_code == 200
        assert response.json()["email"] == "existing@example.com"

    def test_get_user_not_found(self, client):
        response = client.get("/api/users/99999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
```

### FastAPI Async Tests with httpx

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
async def test_async_create_user(async_client):
    response = await async_client.post("/api/users", json={
        "email": "async@example.com",
        "name": "Async User"
    })

    assert response.status_code == 201
    assert response.json()["email"] == "async@example.com"

@pytest.mark.anyio
async def test_async_list_users(async_client, session):
    # Setup
    for i in range(3):
        session.add(User(email=f"user{i}@example.com", name=f"User {i}"))
    session.flush()

    # Test
    response = await async_client.get("/api/users")

    assert response.status_code == 200
    assert len(response.json()) == 3
```

### Django REST Framework Tests

```python
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
@pytest.mark.django_db
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123"
    )

@pytest.mark.django_db
class TestProductAPI:

    def test_list_products(self, authenticated_client):
        Product.objects.create(name="Widget", price=19.99)
        Product.objects.create(name="Gadget", price=29.99)

        response = authenticated_client.get("/api/products/")

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_create_product(self, authenticated_client):
        response = authenticated_client.post("/api/products/", {
            "name": "New Product",
            "price": 39.99
        })

        assert response.status_code == 201
        assert Product.objects.filter(name="New Product").exists()

    def test_unauthenticated_access(self, api_client):
        response = api_client.get("/api/products/")

        assert response.status_code == 401
```

## External Service Integration Tests

### Mocking HTTP with respx

```python
import pytest
import respx
from httpx import Response, AsyncClient

class PaymentGateway:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def charge(self, amount: float, token: str) -> dict:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/charge",
                json={"amount": amount, "token": token}
            )
            response.raise_for_status()
            return response.json()

@pytest.mark.anyio
@respx.mock
async def test_payment_success():
    respx.post("https://api.payments.com/charge").mock(
        return_value=Response(200, json={
            "payment_id": "pay_123",
            "status": "success"
        })
    )

    gateway = PaymentGateway("https://api.payments.com")
    result = await gateway.charge(100.00, "tok_visa")

    assert result["status"] == "success"
    assert result["payment_id"] == "pay_123"

@pytest.mark.anyio
@respx.mock
async def test_payment_declined():
    respx.post("https://api.payments.com/charge").mock(
        return_value=Response(400, json={
            "error": "card_declined",
            "message": "Your card was declined"
        })
    )

    gateway = PaymentGateway("https://api.payments.com")

    with pytest.raises(Exception):
        await gateway.charge(100.00, "tok_declined")

@pytest.mark.anyio
@respx.mock
async def test_payment_timeout():
    import httpx

    respx.post("https://api.payments.com/charge").mock(
        side_effect=httpx.TimeoutException("Connection timed out")
    )

    gateway = PaymentGateway("https://api.payments.com")

    with pytest.raises(httpx.TimeoutException):
        await gateway.charge(100.00, "tok_visa")
```

### WireMock for Complex Scenarios

```python
import pytest
import requests
from testcontainers.core.container import DockerContainer
import time

@pytest.fixture(scope="session")
def wiremock_container():
    container = DockerContainer("wiremock/wiremock:3.3.1")
    container.with_exposed_ports(8080)
    container.start()

    base_url = f"http://{container.get_container_host_ip()}:{container.get_exposed_port(8080)}"

    # Wait for WireMock to be ready
    for _ in range(30):
        try:
            requests.get(f"{base_url}/__admin/mappings")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    yield base_url
    container.stop()

@pytest.fixture
def mock_inventory_service(wiremock_container):
    # Setup mock for inventory check
    requests.post(f"{wiremock_container}/__admin/mappings", json={
        "request": {
            "method": "GET",
            "urlPathPattern": "/inventory/.*"
        },
        "response": {
            "status": 200,
            "jsonBody": {"available": True, "quantity": 10},
            "headers": {"Content-Type": "application/json"}
        }
    })

    yield wiremock_container

    # Cleanup
    requests.delete(f"{wiremock_container}/__admin/mappings")

def test_order_with_inventory_check(mock_inventory_service):
    order_service = OrderService(inventory_url=mock_inventory_service)

    result = order_service.place_order(product_id="WIDGET-001", quantity=2)

    assert result["status"] == "confirmed"
```

## Message Queue Integration Tests

### RabbitMQ with Testcontainers

```python
import pytest
from testcontainers.rabbitmq import RabbitMqContainer
import pika
import json

@pytest.fixture(scope="session")
def rabbitmq_container():
    with RabbitMqContainer("rabbitmq:3-management-alpine") as rabbitmq:
        yield rabbitmq

@pytest.fixture
def rabbitmq_channel(rabbitmq_container):
    params = pika.ConnectionParameters(
        host=rabbitmq_container.get_container_host_ip(),
        port=rabbitmq_container.get_exposed_port(5672)
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="test_queue", durable=True)

    yield channel

    channel.queue_delete(queue="test_queue")
    connection.close()

class TestMessageProducer:

    def test_publish_order_event(self, rabbitmq_channel):
        producer = OrderEventProducer(rabbitmq_channel)

        producer.publish_order_created({
            "order_id": "ORD-123",
            "customer_id": "CUST-456",
            "total": 99.99
        })

        # Verify message was published
        method, properties, body = rabbitmq_channel.basic_get("test_queue")
        assert method is not None

        message = json.loads(body)
        assert message["order_id"] == "ORD-123"
        assert message["event_type"] == "order_created"

    def test_message_persistence(self, rabbitmq_channel):
        producer = OrderEventProducer(rabbitmq_channel)

        producer.publish_order_created(
            {"order_id": "ORD-789"},
            persistent=True
        )

        method, properties, body = rabbitmq_channel.basic_get("test_queue")
        assert properties.delivery_mode == 2  # Persistent
```

### Kafka with Testcontainers

```python
import pytest
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer
import json

@pytest.fixture(scope="session")
def kafka_container():
    with KafkaContainer("confluentinc/cp-kafka:7.5.0") as kafka:
        yield kafka

@pytest.fixture
def kafka_producer(kafka_container):
    producer = KafkaProducer(
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        value_serializer=lambda v: json.dumps(v).encode()
    )
    yield producer
    producer.close()

@pytest.fixture
def kafka_consumer(kafka_container):
    consumer = KafkaConsumer(
        "test-topic",
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode()),
        consumer_timeout_ms=5000
    )
    yield consumer
    consumer.close()

def test_produce_and_consume(kafka_producer, kafka_consumer):
    # Produce
    kafka_producer.send("test-topic", {"event": "test", "data": 123})
    kafka_producer.flush()

    # Consume
    messages = list(kafka_consumer)

    assert len(messages) == 1
    assert messages[0].value["event"] == "test"
```

## Authentication Integration Tests

```python
import pytest
from datetime import timedelta
from jose import jwt

@pytest.fixture
def auth_headers(user):
    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(hours=1)
    )
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(admin_user):
    token = create_access_token(
        data={"sub": str(admin_user.id), "role": "admin"},
        expires_delta=timedelta(hours=1)
    )
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def expired_headers(user):
    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(seconds=-1)  # Already expired
    )
    return {"Authorization": f"Bearer {token}"}

class TestAuthenticatedEndpoints:

    def test_valid_token_access(self, client, auth_headers):
        response = client.get("/api/profile", headers=auth_headers)
        assert response.status_code == 200

    def test_expired_token_rejected(self, client, expired_headers):
        response = client.get("/api/profile", headers=expired_headers)
        assert response.status_code == 401
        assert "expired" in response.json()["detail"].lower()

    def test_invalid_token_rejected(self, client):
        response = client.get(
            "/api/profile",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401

    def test_missing_token_rejected(self, client):
        response = client.get("/api/profile")
        assert response.status_code == 401

    def test_admin_route_requires_admin(self, client, auth_headers):
        response = client.get("/api/admin/users", headers=auth_headers)
        assert response.status_code == 403

    def test_admin_route_with_admin(self, client, admin_headers):
        response = client.get("/api/admin/users", headers=admin_headers)
        assert response.status_code == 200
```
