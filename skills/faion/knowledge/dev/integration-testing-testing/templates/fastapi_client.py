# purpose: FastAPI sync + async client fixtures with dependency overrides
# consumes: app object, get_db dependency, session fixture
# produces: client + async_client fixtures with proper override.clear() teardown
# depends-on: r3-clear-overrides (overrides MUST be cleared in teardown)
# token-budget-impact: ~250 tokens
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
