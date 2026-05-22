---
slug: python-async
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: asyncio patterns for I/O-bound Python: TaskGroup, asyncio.timeout, Semaphore, httpx.AsyncClient singleton.
content_id: "883a430d17c007f9"
complexity: medium
produces: code
est_tokens: 3500
tags: [asyncio, async-await, concurrency, httpx, structured-concurrency]
---
# Python Async Patterns

## Summary

**One-sentence:** asyncio patterns for I/O-bound Python: TaskGroup, asyncio.timeout, Semaphore, httpx.AsyncClient singleton.

**One-paragraph:** asyncio patterns for I/O-bound Python services: TaskGroup (3.11+) for structured fan-out, asyncio.timeout for per-call deadlines, Semaphore for concurrency caps, and httpx.AsyncClient as a singleton. Use TaskGroup over gather for all-or-nothing fan-out; never block the event loop with time.sleep, sync drivers, or requests; always store task references to prevent GC.

**Ефективно для:** інженера, який пише async API/handler і потребує детермінованої поведінки fan-out + cancel + timeout, без orphan-tasks і блокувань event-loop.

## Applies If (ALL must hold)

- Building or extending an async API server (FastAPI, aiohttp, Litestar).
- Concurrent network I/O — many HTTP/DB/queue operations within one request or worker tick.
- WebSocket / SSE / long-lived connection handlers.
- Async ORM/driver work — asyncpg, aiosqlite, motor, redis-py async.
- Replacing threading-based concurrency that exists only for I/O parallelism.

## Skip If (ANY kills it)

- CPU-bound work — use multiprocessing or ProcessPoolExecutor; asyncio gives no speedup.
- Linear scripts with one or two I/O calls — overhead exceeds benefit.
- Codebases where critical libs are sync-only (heavy ML stacks).
- Mixing sync Django ORM inside async def handlers without sync_to_async — blocks the loop.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python 3.11+ interpreter | binary | system / uv-managed |
| httpx or other async client | package | pyproject dependencies |
| ruff with ASYNC ruleset enabled | lint config | pyproject.toml [tool.ruff] |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-modern-2026` | Defines the 3.11+ baseline and tooling required for TaskGroup/asyncio.timeout. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: TaskGroup over gather, Semaphore inside task, asyncio.timeout over wait_for, no blocking calls in async def, store task refs. | ~900 |
| `content/02-output-contract.xml` | essential | Shape of an async module: async def signatures + TaskGroup blocks + per-call timeout + bounded Semaphore. Forbidden: time.sleep, requests in async def, fire-and-forget create_task without reference. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: blocking call in coroutine, orphaned create_task, gather without cancel, mixing sync ORM under async. | ~700 |
| `content/04-procedure.xml` | medium | Steps: identify I/O fan-out → wrap in TaskGroup → add Semaphore for caps → add timeout per call → lint with ASYNC. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: is this CPU-bound? → no asyncio. Need all-or-nothing fan-out? → TaskGroup. Need cap? → Semaphore inside task. Else: don't add async. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `introduce-taskgroup` | sonnet | Code rewrite with judgment on cancellation semantics. |
| `audit-blocking-calls` | haiku | Pattern match: time.sleep, requests, sync ORM inside async def. |

## Templates

| File | Purpose |
|------|---------|
| `templates/concurrent-fetch.py` | Bounded fan-out: TaskGroup + Semaphore + asyncio.timeout over httpx.AsyncClient. |
| `templates/asgi-handler.py` | FastAPI-style handler showing TaskGroup composition inside a request. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-async.py` | Scan a module for blocking calls in async def and missing task references. | Pre-commit and CI. |

## Related

- [[python-fastapi]]
- [[python-pytest-async]]
- [[python-modern-2026]]

## Decision tree

The tree at content/06-decision-tree.xml triages: CPU vs I/O, all-or-nothing vs partial-success fan-out, capped vs uncapped concurrency. Walk it before introducing asyncio into a module that wasn't already async.
