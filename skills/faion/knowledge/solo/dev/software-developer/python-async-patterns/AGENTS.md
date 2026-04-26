# Python Async Patterns

## Summary

Async/await patterns for Python 3.11+ I/O-bound services. Uses `asyncio.TaskGroup` for structured concurrency, `asyncio.Semaphore` to bound fan-out, and app-scoped `httpx.AsyncClient` / DB pools. CPU-bound work goes to `run_in_executor` or `ProcessPoolExecutor`. Blocking calls inside `async def` (requests, time.sleep, psycopg2) are a hard violation.

## Why

A single blocking call inside an async function freezes the entire event loop for all concurrent requests. TaskGroup propagates cancellation and exceptions automatically, closing the zombie-task leak that plagues `asyncio.gather`. Bounding concurrency with Semaphore prevents resource exhaustion on downstreams.

## When To Use

- FastAPI, Starlette, aiohttp, or Litestar services with high concurrent I/O (HTTP, DB, Redis, S3).
- Fan-out/fan-in: dozens-to-thousands of concurrent external calls per request.
- Long-lived connections: WebSocket, SSE, gRPC streaming, MQTT.
- Background workers consuming Redis Streams / NATS / RabbitMQ.

## When Not To Use

- CPU-bound workloads (ML inference, image processing) — async adds overhead without benefit.
- One-off scripts where `requests` + threads is simpler and equivalent.
- Codebases with deep sync dependencies (legacy ORMs, blocking SDKs) requiring `run_in_executor` everywhere.
- Django request handlers without ASGI deployment — partial async serializes everything.
- Python < 3.11 — TaskGroup and improved cancellation are the practical baseline.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concurrency.xml` | TaskGroup, gather, Semaphore, timeouts, async generators. |
| `content/02-resources.xml` | App-scoped clients, async context managers, background task tracking. |
| `content/03-antipatterns.xml` | Blocking calls in async, unawaited coroutines, fire-and-forget without tracking. |

## Templates

| File | Purpose |
|------|---------|
| `templates/detect_sync_leaks.py` | AST scanner — finds blocking calls (requests, time.sleep, psycopg2) inside async def. |
