# Python Async Patterns

## Summary

**One-sentence:** Spec + scaffold for Python asyncio code: single event loop per process, no sync I/O in async paths, TaskGroups for structured concurrency, timeouts on every await on the wire, bounded semaphores for fan-out.

**One-paragraph:** Python async code breaks in five predictable ways: blocking sync I/O inside async paths (the event loop freezes), unbounded `asyncio.gather` fan-out (memory explosion), missing timeouts (await forever), bare exceptions swallowing cancellation, and mixing thread pools with asyncio without explicit boundaries. This methodology produces a spec naming the async runtime (asyncio + uvloop or plain), the I/O boundary (only async libraries on the hot path), TaskGroup vs gather usage with cardinality caps, timeout per network await, and the sync-thread offload pattern.

**Ефективно для:**

- FastAPI / async Django / aiohttp - спочатку зафіксувати правила.
- Перехід sync→async - визначити boundary і не змішувати.
- Race conditions / deadlocks - діагностувати через TaskGroup.
- Memory leak через unbounded gather - впровадити semaphore.
- Сторонні sync бібліотеки - винести в run_in_executor через guard.

## Applies If (ALL must hold)

- Service uses an async framework (FastAPI, aiohttp, Starlette, async Django).
- Hot path performs network I/O (HTTP, DB, queue) with measurable concurrency.
- Python version is 3.11+ (TaskGroup, asyncio.timeout context manager available).
- Team can ban sync drivers on async code paths via lint or review.

## Skip If (ANY kills it)

- Service is purely CPU-bound batch work - use multiprocessing instead.
- Codebase is sync Django / Flask with no async transition planned.
- All I/O backends are sync-only (legacy driver) and the rewrite cost is unjustified.
- Single-developer one-off script - asyncio overhead exceeds gain.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Async-library inventory | list of HTTP/DB/queue libraries used | engineering |
| Concurrency budget | max parallel tasks per request | perf + product |
| Timeout policy | per-call ms budget | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[performance-testing]] | downstream consumer of latency numbers async code targets. |
| [[rate-limiting]] | shared concurrency caps inform semaphore sizing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: no sync I/O in async, timeouts on network, bounded fan-out, TaskGroup, cancellation respected, sync offload explicit, single loop per process | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: runtime, drivers, timeouts, fanout caps, sync offload | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-drivers` | haiku | Mechanical scan of requirements vs known async libs. |
| `design-fanout-caps` | sonnet | Match semaphore sizes to perf budget. |
| `rewrite-handler` | sonnet | Per-handler translation sync->async. |
| `review-cancellation` | opus | Stakes high; cancellation leaks deadlock shutdown. |

## Templates

| File | Purpose |
|------|---------|
| `templates/async_handler.py` | Async handler skeleton with TaskGroup, timeout, Semaphore, sync-offload pattern. |
| `templates/ruff_async.toml` | Ruff config snippet enabling the ASYNC rule group. |
| `templates/detect_sync_leaks.py` | AST scan for blocking-call leaks inside async def functions (pre-commit hook). |
| `templates/_smoke-test.json` | Minimum viable async-patterns artefact for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-async-patterns.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[performance-testing]]
- [[rate-limiting]]
- [[websocket-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - framework type, driver inventory, timeout policy, fan-out shape - onto a rule from `content/01-core-rules.xml`. Use it before merging async code: it catches sync-on-hot-path, unbounded gather, and missing timeouts upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/async_handler.py`

```python
import asyncio
import httpx

FANOUT_CAP = asyncio.Semaphore(50)

async def fetch_one(client: httpx.AsyncClient, url: str) -> dict:
    async with FANOUT_CAP:
        async with asyncio.timeout(3.0):
            r = await client.get(url)
            r.raise_for_status()
            return r.json()

async def handle(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_one(client, u)) for u in urls]
    return [t.result() for t in tasks]

async def heavy_sync_wrapper(blob: bytes) -> bytes:
    return await asyncio.to_thread(compress_legacy_sync, blob)

def compress_legacy_sync(blob: bytes) -> bytes:
    return blob[::-1]
```

### `templates/ruff_async.toml`

```toml
[tool.ruff.lint]
select = ["E", "F", "ASYNC"]
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ASYNC"]
```

### `templates/detect_sync_leaks.py`

```python
Usage: python detect_sync_leaks.py [path]
Exit 1 if blocking calls found; suitable as pre-commit hook.
"""
import ast
import sys
import pathlib

BLOCKING = {
    "requests.get", "requests.post", "requests.put", "requests.delete", "requests.request",
    "urllib.request.urlopen", "urllib3.PoolManager",
    "time.sleep",
    "psycopg2.connect",
    "sqlalchemy.create_engine",
    "boto3.client", "boto3.resource",
    "open",  # use aiofiles instead
}


def name_of(node: ast.expr) -> str:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value  # type: ignore[assignment]
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def scan(path: str) -> list[tuple[str, int, str]]:
    issues = []
    for f in pathlib.Path(path).rglob("*.py"):
        try:
            tree = ast.parse(f.read_text(), filename=str(f))
        except SyntaxError:
            continue
        async_funcs = [n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)]
        for fn in async_funcs:
            for node in ast.walk(fn):
                if isinstance(node, ast.Call):
                    n = name_of(node.func)
                    if any(n.startswith(b) for b in BLOCKING):
                        issues.append((str(f), node.lineno, n))
    return issues


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    found = scan(target)
    for filepath, line, name in found:
        print(f"{filepath}:{line}: blocking call '{name}' inside async def")
    sys.exit(1 if found else 0)
```

### `templates/_smoke-test.json`

```json
{
  "runtime": "asyncio",
  "async_drivers": [
    "httpx"
  ],
  "timeout_policy": {
    "default_ms": 3000
  },
  "fanout_caps": {
    "max_parallel": 50,
    "mechanism": "TaskGroup"
  },
  "sync_offload_pattern": "to_thread"
}
```
