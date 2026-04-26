# Python FastAPI

## Summary

FastAPI production patterns with Pydantic v2 and SQLAlchemy 2 async. Routes are thin: validate input via Pydantic schema → call service → return response model. One `AsyncSession` per asyncio task — never share across `asyncio.gather` siblings. Background tasks via FastAPI `BackgroundTasks` are for short work only (&lt;100ms); route longer jobs to Celery/Arq/Taskiq. Snapshot `openapi.json` per PR to catch schema drift.

## Why

FastAPI's value comes from the type-hint-to-OpenAPI pipeline, automatic validation, and native async I/O. That value evaporates if routes contain business logic, if Pydantic v1 idioms leak in, or if sync DB calls run inside `async def` handlers. A vertical-slice discipline (schema → router → service → repo → test per endpoint) keeps each change reviewable and rollback-safe.

## When To Use

- New async REST API project where I/O concurrency dominates
- Adding endpoints to an existing FastAPI project (one vertical slice at a time)
- Migrating Flask/DRF endpoints to FastAPI route-by-route while sharing the database
- Adding Pydantic v2 schemas to a project that hand-validated before
- Wrapping ML model inference in an HTTP endpoint with auto-generated OpenAPI
- Microservice fronting SQLAlchemy 2 async + Postgres + Redis

## When NOT To Use

- Sync-heavy CPU-bound services — FastAPI shines on I/O concurrency, not CPU
- Apps needing Django batteries (auth, admin, ORM, contenttypes) — porting cost exceeds benefit
- Lambda/FaaS where Pydantic v2 import time hurts cold start
- Pure WebSocket services — Starlette directly is leaner
- Codebases not committed to type hints — most of FastAPI's value disappears

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-structure.xml` | Layout, key principles, dependency injection patterns, yield dependencies |
| `content/02-async-patterns.xml` | When to use async, blocking the event loop, gather, BackgroundTasks limits |
| `content/03-sqlalchemy-pydantic.xml` | Async engine + session factory, one-session-per-task rule, eager loading, Pydantic v2 schemas |
| `content/04-antipatterns.xml` | Sync routes, v1 idioms, BackgroundTasks abuse, response_model omission, LLM gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-snapshot.sh` | CI script: diff served openapi.json against committed snapshot, fail on change |
| `templates/async-route-test.py` | Async route test skeleton via httpx.AsyncClient + ASGITransport |
