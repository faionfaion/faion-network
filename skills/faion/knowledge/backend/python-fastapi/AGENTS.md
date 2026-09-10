# Python FastAPI

## Summary

**One-sentence:** FastAPI production patterns with Pydantic v2 + SQLAlchemy 2 async + thin routes + per-task AsyncSession.

**One-paragraph:** FastAPI production patterns with Pydantic v2 and SQLAlchemy 2 async. Routes are thin: validate input via Pydantic schema → call service → return response model. One AsyncSession per asyncio task — never share across asyncio.gather siblings. Background tasks via FastAPI BackgroundTasks for short work only (<100ms); route longer jobs to Celery/Arq/Taskiq. Snapshot openapi.json per PR to catch schema drift.

**Ефективно для:** інженера, який будує або еволюціонує FastAPI-сервіс — закриває петлю між Pydantic-валідацією, SQLAlchemy-сесіями та чіткими роутами без бізнес-логіки.

## Applies If (ALL must hold)

- New async REST API project where I/O concurrency dominates.
- Adding endpoints to an existing FastAPI project (one vertical slice at a time).
- Migrating Flask/Django REST to FastAPI vertical slices.
- Wiring openapi.json snapshot tests into CI.

## Skip If (ANY kills it)

- Synchronous CPU-bound workloads — use Celery + Flask/Django.
- Tight CRUD-only apps that fit a Django admin — FastAPI's flexibility is overkill.
- GraphQL endpoints — use Strawberry or Ariadne instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python 3.12+ interpreter | binary | uv install |
| FastAPI 0.115+ installed | package | uv add fastapi |
| Pydantic v2 + SQLAlchemy 2 async drivers | package | uv add pydantic 'sqlalchemy[asyncio]' asyncpg |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-async` | Async fundamentals (TaskGroup, asyncio.timeout, no blocking calls). |
| `free/dev/python-developer/python-type-hints` | Pydantic v2 relies on accurate type hints. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 13 rules: thin routes, Pydantic v2 in/out, one AsyncSession per task, BackgroundTasks <100ms only, Depends injection, openapi snapshot, lifespan not on_event, Base/Create/Update/Response quartet, Annotated dependency aliases, services return ORM, flush+refresh never commit, no sync I/O in async, docs guarded in prod. | ~2000 |
| `content/02-output-contract.xml` | essential | Shape: routers/ + services/ + schemas/ + models/ + dependencies.py + main.py. Forbidden: business logic in routes, dict in/out, shared AsyncSession across gather siblings. | ~900 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns: shared session across gather, fat route, BackgroundTasks for slow work, openapi drift, deprecated on_event, one-schema-fits-all, sync I/O in an async route, unguarded /docs in production. | ~1300 |
| `content/04-procedure.xml` | medium | 8 steps: bootstrap the async stack → lifespan + dependency aliases → schema quartet → service function → wire route → register dependencies → snapshot openapi → audit blocking calls → CI gate. | ~1000 |
| `content/06-decision-tree.xml` | essential | Tree: stack in scope? then what is being written — lifespan / schema / route / service / post-response work / fan-out — each to a rule id. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-vertical-slice` | sonnet | schema + service + route + test triplet with judgement. |
| `audit-openapi-drift` | haiku | Diff openapi.json against snapshot. |

## Templates

| File | Purpose |
|------|---------|
| `templates/router.py` | Thin FastAPI router: Depends() for session, Pydantic schema in/out, calls service. |
| `templates/service.py` | Service function skeleton: AsyncSession dependency, returns Pydantic response model. |
| `templates/schemas.py` | Pydantic v2 quartet: <Entity>Base/Create/Update/Response + paginated list response. |
| `templates/main.py` | App entry: asynccontextmanager lifespan, CORS, router includes, docs gated on settings.debug. |
| `templates/dependencies.py` | get_db + get_current_user with the DBSession / CurrentUser Annotated aliases. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-fastapi.py` | Check that routes only call services (no ORM in routes), and openapi.json matches snapshot. | Pre-commit and CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[python-async]]
- [[python-type-hints]]
- [[python-pytest-async]]
- [[error-handling]] — the RFC 7807 envelope this app's exception handler returns.
- [[django-api]] — the DRF/Ninja counterpart when the project is Django rather than FastAPI.

## Decision tree

The tree at content/06-decision-tree.xml decides BackgroundTasks vs job queue, Depends scope, and fan-out strategy inside a request. Walk it before adding any new endpoint or background job.
