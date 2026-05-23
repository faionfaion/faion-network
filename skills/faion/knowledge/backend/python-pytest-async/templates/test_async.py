"""
purpose: Async test skeleton with AsyncMock + pytest_asyncio.fixture.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock


@pytest_asyncio.fixture
async def fake_client():
    client = AsyncMock()
    client.get.return_value = {"id": 1, "name": "demo"}
    yield client


@pytest.mark.asyncio
async def test_async_call_returns_dict(fake_client):
    result = await fake_client.get("/anywhere")
    assert result == {"id": 1, "name": "demo"}
    fake_client.get.assert_awaited_once_with("/anywhere")
