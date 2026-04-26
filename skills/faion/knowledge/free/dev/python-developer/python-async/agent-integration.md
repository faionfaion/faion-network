# Agent Integration — Python Async Patterns

Methodology covers asyncio fundamentals plus structured concurrency (Python 3.11+ `TaskGroup`, `asyncio.timeout`), HTTP client selection (httpx vs aiohttp), and async testing (pytest-asyncio). This file is the runbook for an agent introducing or refactoring async code in a Python service (FastAPI, aiohttp, async Django, standalone workers).

## When to use
- Building or extending an async API server (FastAPI, aiohttp, Litestar, Sanic).
- Concurrent network I/O — many HTTP/DB/queue operations within one request or worker tick.
- WebSocket / SSE / long-lived connection handlers.
- Async ORM/driver work — asyncpg, aiosqlite, motor (Mongo), redis-py async.
- Replacing legacy `threading`-based concurrency that exists only for I/O parallelism.
- Migrating callback-style code (`Twisted`, `tornado.gen.coroutine`) to native `async`/`await`.

## When NOT to use
- CPU-bound work — use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`. asyncio gives no speedup; can hurt latency.
- Linear scripts with one or two I/O calls — async overhead and complexity > benefit.
- Codebases where critical libs are sync-only (heavy ML, scientific stacks) — wrapping each call in `run_in_executor` adds friction without parallelism.
- Mixing sync ORM (Django sync ORM, SQLAlchemy sync) inside `async def` request handlers — blocks the event loop. Use `sync_to_async` (Django) or sync workers instead.
- Educational / introductory codebases — beginners hit "coroutine never awaited" bugs that obscure intent.

## Where it fails / limitations
- README mentions `asyncio.timeout()` (3.11+) but does not warn that timeout context managers swallow `CancelledError` differently than legacy `wait_for`.
- TaskGroup vs gather table is correct, but skips that `gather(return_exceptions=True)` is the right escape hatch when you actually want all-results-then-decide.
- `asyncio.Semaphore` example missing `async with sem:` pattern guidance — agents misuse with bare `acquire()`/`release()`.
- HTTP client comparison says "httpx good, aiohttp excellent" — true at high concurrency, but httpx connection-pool tuning often matches aiohttp for typical service loads. Agents over-rotate to aiohttp.
- No coverage of `anyio` — production-grade structured concurrency lib that bridges asyncio and trio. Used by FastAPI internally.
- `run_in_executor` examples assume default executor; max_workers (default 32 in 3.13) often exhausts under load.
- `ExceptionGroup` / `except*` (PEP 654) only briefly mentioned; agents miss the syntax.
- Cancellation propagation is the #1 footgun in real async code — README under-covers it.
- No mention of `asyncio.Runner` (3.11+) for tighter loop control vs `asyncio.run()`.

## Agentic workflow
Greenfield async service: (1) pick framework (FastAPI default), (2) pin Python ≥ 3.11 to access TaskGroup/timeout, (3) wire httpx `AsyncClient` as a singleton in app state, (4) write each endpoint as `async def`, (5) use `TaskGroup` for fan-out within a request, (6) test with `pytest-asyncio` (`asyncio_mode = "auto"`). Sync→async migration: incremental at the boundary — convert one entry point, then services it calls, then DB layer (with async driver swap). Don't half-convert; partial async with sync DB blocks the loop. CI gate: ruff `ASYNC` rules detect blocking calls inside coroutines.

### Recommended subagents
- `faion-code-agent` — Default for writing/refactoring async code.
- `faion-software-architect` — Decides asyncio vs threading vs multiprocessing for a workload.
- `faion-test-agent` — Owns pytest-asyncio config, async fixtures, mock async clients.
- `faion-devtools-developer` — Wires ruff `ASYNC` lint rules and pytest plugins.
- `faion-api-developer` — FastAPI / aiohttp endpoint design, dependency injection.

### Prompt pattern

Concurrent fan-out:

```
Refactor <function> in <file> to fetch N URLs concurrently per
free/dev/python-developer/python-async/README.md.
Constraints:
  - Python 3.11+; use asyncio.TaskGroup, NOT gather (we need all-or-nothing).
  - HTTP client: httpx.AsyncClient passed in (do not create per-call).
  - Cap concurrency at 10 with asyncio.Semaphore.
  - Per-request timeout 5s via asyncio.timeout(5).
  - On any failure: cancel siblings, raise ExceptionGroup; caller uses except*.
  - Return list ordered by input URL order.
Add pytest-asyncio test using respx to mock httpx.
```

Sync→async migration:

```
Convert <module>.<function> to async per
free/dev/python-developer/python-async/README.md.
  - Keep public signature identical (same args, same return shape).
  - Replace requests with httpx.AsyncClient; replace time.sleep with asyncio.sleep.
  - If callers are sync, expose sync wrapper using anyio.from_thread.run.
  - Do NOT introduce a top-level asyncio.run inside a library function.
Run tests; show before/after timing under concurrent load.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `httpx` | Async + sync HTTP client, HTTP/2 | https://www.python-httpx.org |
| `aiohttp` | High-perf async HTTP client + server | https://docs.aiohttp.org |
| `asyncpg` | Fastest PostgreSQL async driver | https://magicstack.github.io/asyncpg/ |
| `psycopg[binary,pool]` (v3) | Postgres async with sync compat | https://www.psycopg.org/psycopg3/ |
| `aiosqlite` | sqlite3 async wrapper | https://github.com/omnilib/aiosqlite |
| `redis-py` (async) | Redis async client (built-in async since 4.x) | https://redis.readthedocs.io |
| `anyio` | Structured concurrency lib over asyncio/trio (FastAPI uses it) | https://anyio.readthedocs.io |
| `trio` | Alternative async lib focused on structured concurrency | https://trio.readthedocs.io |
| `pytest-asyncio` | Pytest plugin for async tests | https://pytest-asyncio.readthedocs.io |
| `respx` | httpx mocking | https://lundberg.github.io/respx |
| `aioresponses` | aiohttp mocking | https://github.com/pnuckowski/aioresponses |
| `ruff --select ASYNC` | Lint blocking calls in async code | https://docs.astral.sh/ruff/rules/#flake8-async-async |
| `aiomonitor` | Inspect running asyncio tasks via REPL | https://aiomonitor.aio-libs.org |
| `aiodebug` | Detect slow callbacks blocking the loop | https://github.com/qntln/aiodebug |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| FastAPI | OSS framework | Yes — async-native, OpenAPI auto-gen | First choice for new async APIs |
| aiohttp | OSS framework | Yes — server + client, WebSocket | When you need WS/streaming server |
| Starlette | OSS framework | Yes — FastAPI's foundation | Lower-level than FastAPI |
| Sanic | OSS framework | Partial | Less ecosystem than FastAPI |
| Litestar | OSS framework | Yes — modern, async-first | Strong typing, DI |
| Celery | OSS task queue | Partial — async support is recent (5.x) | For async-only, prefer arq or taskiq |
| arq | OSS async task queue (Redis) | Yes | Lightweight |
| taskiq | OSS async task queue (multi-broker) | Yes | Modern alt to arq |
| Sentry | SaaS APM | Yes — supports asyncio | `sentry_sdk.integrations.asyncio` |
| Datadog APM | SaaS APM | Yes | `ddtrace.patch(asyncio=True)` |
| Pyroscope | OSS profiler | Yes | Async-aware sampling |

## Templates & scripts

See `templates.md` for full FastAPI scaffolding and `examples.md` for production-shaped patterns. Add this concurrent fan-out helper (≤45 lines):

```python
# concurrent_fetch.py — bounded concurrent HTTP with TaskGroup + Semaphore.
import asyncio
from typing import Iterable
import httpx

async def fetch_one(client: httpx.AsyncClient, sem: asyncio.Semaphore, url: str) -> dict:
    async with sem:
        async with asyncio.timeout(5):
            r = await client.get(url)
            r.raise_for_status()
            return r.json()

async def fetch_all(urls: Iterable[str], *, concurrency: int = 10) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient(http2=True, timeout=10) as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_one(client, sem, u)) for u in urls]
    return [t.result() for t in tasks]

if __name__ == "__main__":
    import sys
    urls = sys.argv[1:] or ["https://httpbin.org/json"] * 3
    results = asyncio.run(fetch_all(urls))
    print(f"Fetched {len(results)} responses")
```

## Best practices
- **`TaskGroup` is the default for fan-out in 3.11+.** Reach for `gather` only when you genuinely want partial results (`return_exceptions=True`).
- **One `httpx.AsyncClient` per app, not per request.** Connection pooling is its main perf win; per-call clients destroy it.
- **Timeouts are non-negotiable.** Wrap every external call: `async with asyncio.timeout(N): ...`. Default `httpx` timeout is 5s — fine, but be explicit.
- **`Semaphore` bounds concurrency.** Without one, a fan-out over 10k URLs DDoSes both you and the target.
- **Never block the loop.** No `time.sleep`, `requests.*`, sync DB drivers inside `async def`. Use `asyncio.to_thread()` (3.9+) for unavoidable sync calls.
- **Exceptions from TaskGroup come as `ExceptionGroup`.** Use `try: ... except* ValueError as eg: ...` to handle by type.
- **`CancelledError` must propagate.** Never `except Exception:` swallow it; if you catch it for cleanup, re-raise after.
- **Use `asyncio.Runner` (3.11+)** when you need to run multiple `run()`-equivalent contexts in one process.
- **Test with `pytest-asyncio` mode `auto`** — every `async def test_` auto-marked. Reduces boilerplate.
- **Mock at the transport layer**: respx (httpx) / aioresponses (aiohttp) > monkeypatching the call site.
- **Profile with `aiomonitor` or `py-spy --idle`** — async stalls hide in callbacks blocking the loop.

## AI-agent gotchas
- **Forgetting `await`** — coroutine never runs, returns a `<coroutine object>` that warns at GC time. Ruff `ASYNC230`/pyflakes catches some cases.
- **Using `requests` inside `async def`** — silently blocks the loop. Ruff `ASYNC210` flags it.
- **`time.sleep` in async** — same issue; use `asyncio.sleep`. Ruff `ASYNC251`.
- **Running blocking DB queries (Django sync ORM) in `async def`** — works but blocks; either use `sync_to_async` or async ORM.
- **`asyncio.create_task(...)` without storing the task** — task may be GC'd mid-execution. Always retain the reference (TaskGroup does this for you).
- **Fire-and-forget tasks in module scope** — `asyncio.create_task` requires a running loop; hits "no running event loop" at import time.
- **`asyncio.gather` swallows the first exception** unless `return_exceptions=True` — other tasks keep running but are then ignored. TaskGroup cancels siblings instead.
- **`async for` on a non-async iterator** — `TypeError`. Use `async for` only on async generators / async iterables.
- **`async with` on a sync context manager** — `AttributeError: __aenter__`. Mostly handled by libs, but custom CMs need both `__aenter__`/`__aexit__`.
- **Mixing trio and asyncio code** — only via `anyio`. Pure asyncio code in trio runtime crashes at first await.
- **`event_loop = asyncio.get_event_loop()`** is deprecated for top-level use. Use `asyncio.run()` or `asyncio.get_running_loop()` (must be inside a coroutine).
- **`pytest-asyncio` mode mismatch** — `strict` (default) requires `@pytest.mark.asyncio`; `auto` runs all `async def` tests. Agents flipping modes break test collection.
- **`asyncio.timeout(None)`** disables the timeout — agents pass `None` thinking it means "no override" and then wonder why hangs persist.
- **`run_in_executor` with default executor exhausts under load** — bind a custom `ThreadPoolExecutor(max_workers=...)` for heavy sync-bridge use.
- **WebSockets in FastAPI** require `websocket_disconnect` handling; agents leak connections by not catching `WebSocketDisconnect`.
- **Sync wrappers around async code** (`asyncio.run` inside library function) break when called from an existing loop. Use `anyio.from_thread.run` or expose async-only.

## References
- README: `./README.md`
- Sibling: `../python-modern-2026/`, `../python-fastapi/`, `../python-testing-pytest/`
- asyncio docs: https://docs.python.org/3/library/asyncio.html
- TaskGroup: https://docs.python.org/3/library/asyncio-task.html#task-groups
- PEP 654 (Exception Groups): https://peps.python.org/pep-0654/
- httpx: https://www.python-httpx.org
- aiohttp: https://docs.aiohttp.org
- anyio: https://anyio.readthedocs.io
- pytest-asyncio: https://pytest-asyncio.readthedocs.io
- ruff ASYNC rules: https://docs.astral.sh/ruff/rules/#flake8-async-async
- "Async Python 2025" overview: https://medium.com/@hadiyolworld007/async-python-2025-fast-safe-and-under-control-ee2c0e2b2bf6
