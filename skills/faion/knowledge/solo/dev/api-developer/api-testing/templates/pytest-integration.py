# purpose: Template helper for API Testing (pytest-integration.py).
# consumes: see content/02-output-contract.xml inputs for api-testing
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
"""
pytest fixtures for API integration tests.
Provides: authenticated client, database transaction reset, factory-based user creation.
Usage: drop into tests/conftest.py or import in test modules.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from app.database import Base, get_db


TEST_DATABASE_URL = "postgresql://test:test@localhost/test_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(db_engine):
    """Each test gets a transaction that is rolled back on teardown."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Obtain a bearer token for test user."""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_factory(db):
    """Create users with unique emails to avoid collision across tests."""
    import uuid
    from app.models import User

    def make_user(**kwargs):
        defaults = {
            "email": f"user-{uuid.uuid4()}@example.com",
            "name": "Test User",
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db.add(user)
        db.flush()
        return user

    return make_user
