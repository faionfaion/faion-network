---
slug: python-pytest-async
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest-asyncio adds an event loop and @pytest.
content_id: "1ddb287151f294aa"
tags: [pytest, async, asyncio, pytest-asyncio, fastapi]
---
# pytest Async Testing — pytest-asyncio, Async Fixtures, and FastAPI

## Summary

**One-sentence:** pytest-asyncio adds an event loop and @pytest.

**One-paragraph:** pytest-asyncio adds an event loop and @pytest.mark.asyncio support so async def test functions run as coroutines. In auto mode every async test and fixture is treated as asyncio automatically. Use pytest_asyncio.fixture for async fixtures and AsyncMock for async callables.

## Applies If (ALL must hold)

- Testing FastAPI or any ASGI application with httpx.AsyncClient and ASGITransport.
- Testing async functions that call async libraries: httpx, asyncpg, aioredis, motor.
- Testing asyncio.gather, asyncio.TaskGroup, or ExceptionGroup handling.
- Testing timeout and cancellation behavior with asyncio.wait_for or asyncio.timeout.
- Any test that contains await expressions.

## Skip If (ANY kills it)

- Pure sync code — installing pytest-asyncio adds no value and asyncio_mode="auto" silently wraps sync tests in no-op coroutine handling.
- Mixing sync Django ORM calls directly in async tests — the ORM blocks the event loop and looks like a hang; use sync_to_async or a separate sync test.
- Tests that only call sync adapters of an otherwise async service — call the sync adapter synchronously.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/python-developer/`
