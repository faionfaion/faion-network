---
slug: python-async-patterns
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Async/await patterns for Python 3.
content_id: "ffd0eff26fa6bdff"
tags: [async, asyncio, concurrency, python, fastapi]
---
# Python Async Patterns for I/O-Bound Services

## Summary

**One-sentence:** Async/await patterns for Python 3.

**One-paragraph:** Async/await patterns for Python 3.11+ I/O-bound services. Uses asyncio.TaskGroup for structured concurrency, asyncio.Semaphore to bound fan-out, and app-scoped httpx.AsyncClient / DB pools. CPU-bound work goes to run_in_executor or ProcessPoolExecutor. Blocking calls inside async def (requests, time.sleep, psycopg2) are a hard violation.

## Applies If (ALL must hold)

- FastAPI, Starlette, aiohttp, or Litestar services with high concurrent I/O (HTTP, DB, Redis, S3).
- Fan-out/fan-in: dozens-to-thousands of concurrent external calls per request.
- Long-lived connections: WebSocket, SSE, gRPC streaming, MQTT.
- Background workers consuming Redis Streams / NATS / RabbitMQ.

## Skip If (ANY kills it)

- CPU-bound workloads (ML inference, image processing) — async adds overhead without benefit.
- One-off scripts where requests + threads is simpler and equivalent.
- Codebases with deep sync dependencies (legacy ORMs, blocking SDKs) requiring run_in_executor everywhere.
- Django request handlers without ASGI deployment — partial async serializes everything.
- Python < 3.11 — TaskGroup and improved cancellation are the practical baseline.

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

- parent skill: `solo/dev/software-developer/`
