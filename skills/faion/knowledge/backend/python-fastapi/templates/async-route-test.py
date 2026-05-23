# purpose: Async FastAPI route test skeleton (httpx + ASGITransport)
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/01-core-rules.xml
# token-budget-impact: small
"""
Async route test skeleton using httpx.AsyncClient + ASGITransport.
Tests routes in-process without a running server.
Location: tests/test_<domain>.py
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_user() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/api/v1/users", json={"email": "a@b.com", "name": "Alice"})
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "a@b.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_not_found() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_unauthenticated_returns_401() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/v1/users/me")
    assert r.status_code == 401
