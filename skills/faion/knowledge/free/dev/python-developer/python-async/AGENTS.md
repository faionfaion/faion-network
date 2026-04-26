# Python Async Patterns

## Summary

asyncio patterns for I/O-bound Python services: `TaskGroup` (3.11+) for structured fan-out, `asyncio.timeout()` for per-call deadlines, `Semaphore` for concurrency caps, and `httpx.AsyncClient` as a singleton. Core rules: use `TaskGroup` over `gather` for all-or-nothing fan-out; never block the event loop with `time.sleep`, sync DB drivers, or `requests`; always store task references to prevent GC.

## Why

A single blocking call inside `async def` stalls the entire event loop — all other concurrent coroutines freeze until it returns. Ruff `ASYNC` rules catch most blocking patterns statically, but structured concurrency (`TaskGroup`) is the runtime guarantee: if any subtask fails, siblings are cancelled automatically, preventing the orphan-task resource leaks that `asyncio.gather` leaves behind.

## When To Use

- Building or extending an async API server (FastAPI, aiohttp, Litestar).
- Concurrent network I/O — many HTTP/DB/queue operations within one request or worker tick.
- WebSocket / SSE / long-lived connection handlers.
- Async ORM/driver work — asyncpg, aiosqlite, motor, redis-py async.
- Replacing `threading`-based concurrency that exists only for I/O parallelism.

## When NOT To Use

- CPU-bound work — use `multiprocessing` or `ProcessPoolExecutor`; asyncio gives no speedup.
- Linear scripts with one or two I/O calls — overhead exceeds benefit.
- Codebases where critical libs are sync-only (heavy ML stacks) — `run_in_executor` for each call adds friction.
- Mixing sync Django ORM inside `async def` handlers without `sync_to_async` — blocks the loop.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | `TaskGroup` vs `gather`; `Semaphore` usage; `asyncio.timeout`; async generators; `run_in_executor`. |
| `content/02-http-clients.xml` | `httpx.AsyncClient` singleton pattern; httpx vs aiohttp selection; mocking with respx. |
| `content/03-antipatterns.xml` | Blocking the loop; orphan tasks; swallowing `CancelledError`; sync wrappers inside libraries; `asyncio.timeout(None)`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/concurrent-fetch.py` | Bounded concurrent HTTP fan-out: TaskGroup + Semaphore + per-call timeout + ordered results. |
