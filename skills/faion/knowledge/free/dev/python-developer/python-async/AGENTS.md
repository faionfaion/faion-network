---
slug: python-async
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: asyncio patterns for I/O-bound Python services: TaskGroup (3.
content_id: "883a430d17c007f9"
tags: [asyncio, async-await, concurrency, httpx, structured-concurrency]
---
# Python Async Patterns

## Summary

**One-sentence:** asyncio patterns for I/O-bound Python services: TaskGroup (3.

**One-paragraph:** asyncio patterns for I/O-bound Python services: TaskGroup (3.11+) for structured fan-out, asyncio.timeout() for per-call deadlines, Semaphore for concurrency caps, and httpx.AsyncClient as a singleton. Core rules: use TaskGroup over gather for all-or-nothing fan-out; never block the event loop with time.sleep, sync DB drivers, or requests; always store task references to prevent GC.

## Applies If (ALL must hold)

- Building or extending an async API server (FastAPI, aiohttp, Litestar).
- Concurrent network I/O — many HTTP/DB/queue operations within one request or worker tick.
- WebSocket / SSE / long-lived connection handlers.
- Async ORM/driver work — asyncpg, aiosqlite, motor, redis-py async.
- Replacing threading-based concurrency that exists only for I/O parallelism.

## Skip If (ANY kills it)

- CPU-bound work — use multiprocessing or ProcessPoolExecutor; asyncio gives no speedup.
- Linear scripts with one or two I/O calls — overhead exceeds benefit.
- Codebases where critical libs are sync-only (heavy ML stacks) — run_in_executor for each call adds friction.
- Mixing sync Django ORM inside async def handlers without sync_to_async — blocks the loop.

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
