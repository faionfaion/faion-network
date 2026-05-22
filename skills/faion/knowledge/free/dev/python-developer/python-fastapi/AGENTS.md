---
slug: python-fastapi
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: FastAPI production patterns with Pydantic v2 and SQLAlchemy 2 async.
content_id: "4d9d16a50e38f204"
tags: [fastapi, pydantic, sqlalchemy, async, rest-api]
---
# Python FastAPI

## Summary

**One-sentence:** FastAPI production patterns with Pydantic v2 and SQLAlchemy 2 async.

**One-paragraph:** FastAPI production patterns with Pydantic v2 and SQLAlchemy 2 async. Routes are thin: validate input via Pydantic schema → call service → return response model. One AsyncSession per asyncio task — never share across asyncio.gather siblings. Background tasks via FastAPI BackgroundTasks are for short work only (<100ms); route longer jobs to Celery/Arq/Taskiq. Snapshot openapi.json per PR to catch schema drift.

## Applies If (ALL must hold)

- New async REST API project where I/O concurrency dominates
- Adding endpoints to an existing FastAPI project (one vertical slice at a time)
- Migrating Flask/DRF endpoints to FastAPI route-by-route while sharing the database
- Adding Pydantic v2 schemas to a project that hand-validated before
- Wrapping ML model inference in an HTTP endpoint with auto-generated OpenAPI
- Microservice fronting SQLAlchemy 2 async + Postgres + Redis

## Skip If (ANY kills it)

- Sync-heavy CPU-bound services — FastAPI shines on I/O concurrency, not CPU
- Apps needing Django batteries (auth, admin, ORM, contenttypes) — porting cost exceeds benefit
- Lambda/FaaS where Pydantic v2 import time hurts cold start
- Pure WebSocket services — Starlette directly is leaner
- Codebases not committed to type hints — most of FastAPI's value disappears

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
