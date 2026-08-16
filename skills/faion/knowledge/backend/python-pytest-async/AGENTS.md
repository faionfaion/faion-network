# pytest Async Testing

## Summary

**One-sentence:** pytest-asyncio for async tests: asyncio_mode=auto, pytest_asyncio.fixture, AsyncMock, httpx ASGITransport for FastAPI.

**One-paragraph:** pytest-asyncio adds an event loop and async test/fixture support. asyncio_mode='auto' treats every async def test and fixture as a coroutine automatically. Use pytest_asyncio.fixture for async fixtures, AsyncMock for async callables, and httpx.AsyncClient + ASGITransport for FastAPI app tests.

**Ефективно для:** інженера, який тестує FastAPI/asgi/async-функції — закриває петлю між сирим async def і робочим тестом, без silently-passing 'тестів', які повертають корутину.

## Applies If (ALL must hold)

- Testing FastAPI or any ASGI application with httpx.AsyncClient and ASGITransport.
- Testing async functions that call async libraries: httpx, asyncpg, aioredis, motor.
- Testing asyncio.gather, asyncio.TaskGroup, or ExceptionGroup handling.
- Testing timeout and cancellation behaviour with asyncio.timeout.
- Any test that contains await expressions.

## Skip If (ANY kills it)

- Pure sync code — pytest-asyncio adds no value.
- Mixing sync Django ORM directly in async tests — wrap in sync_to_async or write a sync test.
- Sync adapters of an otherwise async service — call them synchronously.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pytest-asyncio installed | package | uv add --dev pytest-asyncio |
| Async code under test | Python | src/ |
| pyproject pytest config | TOML | repo root |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-pytest-setup` | Defines pytest config conventions. |
| `free/dev/python-developer/python-pytest-fixtures` | Async fixtures extend the sync fixture model. |
| `free/dev/python-developer/python-pytest-mocking` | AsyncMock semantics. |
| `free/dev/python-developer/python-async` | asyncio primitives this tests. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: asyncio_mode='auto' in pyproject, pytest_asyncio.fixture for async fixtures, AsyncMock for async callables, ASGITransport for FastAPI, never mix sync ORM in async tests. | ~1000 |
| `content/02-output-contract.xml` | essential | Shape: pyproject [tool.pytest.ini_options] asyncio_mode='auto' + pytest_asyncio.fixture decorators + AsyncClient(transport=ASGITransport(app=app)). Forbidden: @pytest.fixture on async def, plain MagicMock on async callable. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: @pytest.fixture on async, MagicMock for async, sync ORM in async test, missing asyncio_mode. | ~700 |
| `content/04-procedure.xml` | medium | Steps: enable asyncio_mode='auto' → write async fixtures → write async tests → mock with AsyncMock → wire ASGITransport for FastAPI. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: async code? → pytest-asyncio. FastAPI app? → ASGITransport. Async callable to mock? → AsyncMock. Else: regular pytest. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-async-test` | sonnet | Async fixtures + AsyncMock composition. |
| `audit-asyncio-mode` | haiku | Check pyproject and fixture decorators. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | Async fixtures: async_client, app_client (FastAPI via ASGITransport), async database fixture. |
| `templates/test_async.py` | Async test skeleton with AsyncMock + pytest_asyncio.fixture. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-pytest-async.py` | Check asyncio_mode='auto', no @pytest.fixture on async def, no MagicMock on async callables. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[python-pytest-setup]]
- [[python-pytest-fixtures]]
- [[python-pytest-mocking]]
- [[python-async]]

## Decision tree

The tree at content/06-decision-tree.xml decides auto vs strict mode, AsyncMock vs MagicMock, and ASGITransport vs httpx live URL. Walk it whenever an async test fails silently or hangs.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/conftest.py`

```python
"""

import pytest
from pytest_factoryboy import register


# Register your factories here:
# from tests.factories import UserFactory
# register(UserFactory)


@pytest.fixture
def api_client():
    """DRF APIClient (override per project)."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authed_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def staff_client(api_client, user_factory):
    staff_user = user_factory(is_staff=True)
    api_client.force_authenticate(user=staff_user)
    return api_client
```

### `templates/test_async.py`

```python
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
```
