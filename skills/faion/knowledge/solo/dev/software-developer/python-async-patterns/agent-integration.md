# Agent Integration — Python Async Patterns

## When to use
- Building I/O-bound services with FastAPI, Starlette, aiohttp, or Litestar where concurrency requirements > thread pool capacity.
- Fan-out / fan-in workloads: dozens-to-thousands of concurrent HTTP / DB / Redis / S3 calls per request.
- Long-lived clients (WebSocket, SSE, gRPC streaming, MQTT) where each connection is cheap.
- Background workers using `asyncio` + Redis Streams / NATS / RabbitMQ where blocking workers would need huge thread pools.
- LLM-driven Python: agents are best when async usage follows tight rules (TaskGroup, semaphores, never-block-the-loop) — gives a checkable shape.

## When NOT to use
- CPU-bound workloads (image processing, ML inference, parsing huge XML) — async doesn't help; use multiprocessing or move to a process pool / Rust extension.
- Scripts and one-off tools where `asyncio.run` + `gather` is overkill — `requests` + threads is simpler and equivalent.
- Codebases with deep sync dependencies (legacy ORMs, blocking SDKs) where every call needs `run_in_executor` — the async sugar is a net negative.
- Django request handlers without ASGI deployment / async views — partial async leaks blocking calls and serializes everything.
- Pre-3.11 codebases — TaskGroup, `except*`, and improved cancellation make 3.11+ the practical baseline.

## Where it fails / limitations
- Hidden blocking: a single sync call (psycopg2, requests, time.sleep, json on huge payload) freezes the entire event loop for everyone.
- Library asymmetry: many SDKs only ship sync clients; wrapping them in `run_in_executor` reintroduces thread limits.
- Cancellation correctness: `asyncio.CancelledError` mishandling leaks tasks, files, sockets, transactions.
- Backpressure: unbounded `gather` over a queue can spawn 100k tasks, consuming RAM and crushing downstreams.
- Debugging: stack traces inside `gather`/TaskGroup are noisier; without `tracemalloc` and `--debug`, leaks are invisible.
- Mixing sync and async test runners (pytest-asyncio modes, anyio plugin); fixtures that work in one mode break in another.
- Connection pool exhaustion on `httpx.AsyncClient` instantiated per request — a common bug LLMs introduce.
- Subtle data races on shared mutable state (an `asyncio.Lock` is required even though only one task runs at a time — across `await` points).
- `asyncio` ≠ `trio` ≠ `anyio`; agents conflate APIs, importing `trio.sleep` into asyncio code.
- Logging / structured tracing libraries that aren't context-aware lose request-id across `await`.

## Agentic workflow
A four-stage pattern. (1) **Boundary check**: an agent classifies each new function as I/O-bound, CPU-bound, or mixed; CPU work goes to `run_in_executor` / `concurrent.futures.ProcessPoolExecutor`. (2) **Concurrency primitive**: agent picks `TaskGroup` for structured concurrency, `gather` only when fire-and-forget, with mandatory `asyncio.Semaphore` to bound concurrency on any external call. (3) **Resource lifecycle**: agent ensures shared `httpx.AsyncClient` / DB pool / Redis client are app-scoped, not request-scoped. (4) **Test gate**: an agent emits both happy-path and cancellation tests (`asyncio.timeout`, `task.cancel()`); coverage tool flags any async function without a cancel path.

### Recommended subagents
- `faion-sdd-executor-agent` — gates: no `requests`, `time.sleep`, or `psycopg2` in async modules; every external call has a semaphore; every TaskGroup has a timeout.
- A **sync-leak detector** subagent (worth creating): scans async modules with AST for blocking calls (`requests.*`, `time.sleep`, `open()` without `aiofiles`, `psycopg2.*`, `boto3` without aiobotocore). Returns line numbers + remediation.
- A **TaskGroup converter**: rewrites legacy `gather` patterns into `TaskGroup` for Python 3.11+, preserving semantics.
- `faion-feature-executor` (skill) — sequence design → boundary check → impl → cancellation test → load test.

### Prompt pattern
Boundary classification:
```
For each function in <module>, classify as IO_BOUND, CPU_BOUND, MIXED.
For each, propose the concurrency primitive (await, TaskGroup,
run_in_executor, ProcessPoolExecutor) and any required Semaphore.
Output a markdown table with columns: function, classification,
primitive, semaphore_needed, rationale.
```

Sync-leak audit:
```
Scan <path>/**/*.py for blocking calls inside async def: requests.*,
urllib3.*, urllib.*, time.sleep, psycopg2.*, sqlalchemy sync engines,
boto3 (when aiobotocore exists), open() without aiofiles, json.dumps
on payloads > 1MB. Output JSON list of {file, line, snippet,
remediation}. Do NOT auto-fix; emit SDD tasks instead.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest-asyncio` | Async test support | `pip install pytest-asyncio` |
| `anyio` | Cross-runtime async (asyncio + trio) | `pip install anyio` |
| `httpx` | Async HTTP client (request/response parity with `requests`) | `pip install httpx` |
| `aiohttp` | Async HTTP server + client | `pip install aiohttp` |
| `aiofiles` | Async filesystem access | `pip install aiofiles` |
| `aiobotocore` / `aioboto3` | Async AWS SDK | `pip install aioboto3` |
| `aiocache` | Async caching primitives | `pip install aiocache` |
| `aiomonitor` | Inspect running event loop | `pip install aiomonitor` |
| `asyncpg` | Postgres async driver (fastest) | `pip install asyncpg` |
| `aiosqlite` | SQLite async wrapper | `pip install aiosqlite` |
| `uvloop` | Fast event loop replacement (Linux/macOS) | `pip install uvloop` |
| `arq` / `dramatiq` (with asyncio backend) | Async background workers | `pip install arq` |
| `faulthandler` / `tracemalloc` | Diagnose hangs and leaks | stdlib |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| FastAPI | OSS framework | Yes — code-first | Standard async API stack. |
| Litestar | OSS framework | Yes | Faster than FastAPI for some workloads, similar API. |
| Starlette | OSS framework | Yes | The toolkit FastAPI is built on. |
| Uvicorn / Hypercorn / Granian | OSS ASGI servers | Yes | Production runners; pick one and stick. |
| Sentry | SaaS | Yes — SDK | Sentry's async SDK propagates trace context. |
| Datadog APM | SaaS | Yes — SDK | Auto-instruments asyncio + FastAPI. |
| OpenTelemetry Python (auto-instrument) | OSS | Yes — CLI | `opentelemetry-instrument uvicorn ...` |
| Grafana Tempo / Jaeger | OSS | Yes | Trace backends; pair with OTel. |
| RabbitMQ / NATS / Kafka | OSS | Yes — async clients | All have asyncio-native clients. |

## Templates & scripts
See `templates.md` and `examples.md`. Inline blocking-call detector (≤50 lines):

```python
# detect_sync_leaks.py — find blocking calls inside async functions.
import ast, sys, pathlib

BLOCKING = {
    "requests.get", "requests.post", "requests.put", "requests.delete",
    "urllib.request.urlopen", "urllib3.PoolManager",
    "time.sleep",
    "psycopg2.connect",
    "sqlalchemy.create_engine",  # sync engine; asyncio code should use create_async_engine
    "boto3.client", "boto3.resource",
}

def name_of(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr); node = node.value
    if isinstance(node, ast.Name): parts.append(node.id)
    return ".".join(reversed(parts))

def scan(path):
    issues = []
    for f in pathlib.Path(path).rglob("*.py"):
        try: tree = ast.parse(f.read_text(), filename=str(f))
        except SyntaxError: continue
        async_funcs = [n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)]
        for fn in async_funcs:
            for node in ast.walk(fn):
                if isinstance(node, ast.Call):
                    n = name_of(node.func)
                    if any(n.startswith(b) for b in BLOCKING):
                        issues.append((str(f), node.lineno, n))
    return issues

for f, line, n in scan(sys.argv[1] if len(sys.argv) > 1 else "."):
    print(f"{f}:{line}: blocking call '{n}' inside async def")
sys.exit(1 if scan else 0)
```

Wire as a pre-commit hook on async modules.

## Best practices
- Standardize on Python 3.11+ and use `asyncio.TaskGroup` for any concurrent set; it propagates cancellation and exceptions correctly.
- Bound every external-call fan-out with `asyncio.Semaphore`. Unbounded `gather` is an outage waiting to happen.
- Reuse a single `httpx.AsyncClient` per app (or per host pool); creating a client per request leaks sockets and breaks HTTP/2.
- Use `asyncpg` over `psycopg2`; for SQLAlchemy pick `create_async_engine` and async sessions, never mix sync + async sessions.
- Run CPU work in `loop.run_in_executor(None, fn)` (default thread pool) for short tasks; use `ProcessPoolExecutor` for tasks > ~50ms.
- Always pair `await` calls with timeouts: `asyncio.timeout(5)` (3.11+) wraps any block.
- Propagate context with `contextvars`. Logging libraries (`structlog`, `loguru`) and OTel use this; ad-hoc globals don't survive `await`.
- Use `anyio` if you need to support both asyncio and trio, or if you want better cancellation semantics.
- Add `--debug` event-loop in dev (`PYTHONASYNCIODEBUG=1`); it surfaces forgotten awaits and slow callbacks.
- Profile with `py-spy --idle` or `aiomonitor`; standard sampling profilers under-attribute event-loop time.
- Treat `CancelledError` as control flow: catch only to clean up, then re-raise.

## AI-agent gotchas
- Agents add `async def` everywhere even in CPU code, expecting performance — all that gives you is overhead and event-loop blocking. Force the I/O-vs-CPU classification step.
- LLMs love `asyncio.run` inside library code; this breaks composition (only the entry script should call it). Lint for it.
- Agents create `httpx.AsyncClient()` per call inside loops; require an app-scoped fixture/dep.
- They mix `requests` and `httpx` in the same async function; reject unconditionally in async modules.
- Agents forget to cancel children on parent timeout → "shielded zombies". Prefer `TaskGroup` so cancellation is automatic.
- Trio / anyio confusion: agents import `trio.sleep` while using asyncio. Pin the runtime in the system prompt.
- Tests pass under `pytest-asyncio` mode `auto` but break under `strict`; agents don't surface this. Pin mode and CI.
- Concurrency limits hallucinated: agents pick `Semaphore(100)` arbitrarily. Require the limit to be derived from downstream capacity (max conns / max QPS) and documented.
- Logging context lost: agents use `print` or non-context-aware loggers in async code; require `structlog` with `contextvars` integration.
- Cancellation mishandling: agents catch `Exception` (which includes `CancelledError` on 3.7) and swallow shutdowns. On 3.8+ `CancelledError` no longer inherits Exception; some agents are still using older patterns.
- Human-in-loop checkpoint: any change to global semaphores, pool sizes, or the event-loop policy must be human-approved with a load-test result.

## References
- Python `asyncio` docs — https://docs.python.org/3/library/asyncio.html
- "Using Asyncio in Python" — Caleb Hattingh (O'Reilly, 2020).
- "Architecture Patterns with Python" — Cosmic Python (Percival & Gregory).
- Yury Selivanov — `uvloop` and asyncio internals talks. https://github.com/MagicStack/uvloop
- "Notes on structured concurrency, or: Go statement considered harmful" — Nathaniel J. Smith. https://vorpus.org/blog/notes-on-structured-concurrency/
- AnyIO docs — https://anyio.readthedocs.io
- FastAPI async docs — https://fastapi.tiangolo.com/async/
- Sibling methodologies in this repo: `python-async-patterns/`, `free/dev/python-developer/python-async/`, `nodejs-service-layer/`, `message-queues/`.
