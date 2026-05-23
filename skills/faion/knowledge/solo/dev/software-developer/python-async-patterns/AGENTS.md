---
slug: python-async-patterns
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spec + scaffold for Python asyncio code: single event loop per process, no sync I/O in async paths, TaskGroups for structured concurrency, timeouts on every await on the wire, bounded semaphores for fan-out.
content_id: "a1b22a8d23b3f452"
complexity: medium
produces: code
est_tokens: 4800
tags: [python, asyncio, concurrency, asgi]
---
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
| `templates/_smoke-test.json` | Minimum viable async-patterns artefact for validator smoke-test. |

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
