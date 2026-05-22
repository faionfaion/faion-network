---
slug: python-fastapi
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a production FastAPI app — @asynccontextmanager lifespan, Pydantic v2 Base/Create/Update/Response schemas, Annotated dependency aliases, async service functions, async SQLAlchemy 2 with flush+refresh, and Depends-based auth.
content_id: "4d9d16a50e38f204"
complexity: medium
produces: code
est_tokens: 4400
tags: [fastapi, pydantic, async, sqlalchemy, depends]
---
# FastAPI Standards

## Summary

**One-sentence:** Produces a production FastAPI app — @asynccontextmanager lifespan, Pydantic v2 Base/Create/Update/Response schemas, Annotated dependency aliases, async service functions, async SQLAlchemy 2 with flush+refresh, and Depends-based auth.

**One-paragraph:** Production-grade FastAPI: Pydantic v2 schemas define the API contract; separate `Base`, `Create`, `Update`, and `Response` schemas (Response uses `ConfigDict(from_attributes=True)`). `@asynccontextmanager` lifespan manages connection pools; never `@app.on_event` (deprecated). Annotated aliases (`DBSession = Annotated[AsyncSession, Depends(get_db)]`) eliminate boilerplate. Routers stay thin; service functions are `async def`, accept typed parameters, return ORM instances. After insert, `await db.flush(); await db.refresh(obj)` to get the generated ID without committing — commit happens in get_db on request success.

**Ефективно для:** new async REST APIs needing OpenAPI docs, microservices wanting high I/O concurrency, replacing sync Flask/DRF endpoints with async equivalents, services adopting Pydantic v2 + SQLAlchemy 2 async.

## Applies If (ALL must hold)

- Python >= 3.11.
- FastAPI >= 0.110 + Pydantic v2.
- async I/O is a real benefit (DB + HTTP clients).
- Team comfortable with `async/await` (or willing to learn).

## Skip If (ANY kills it)

- Existing Django + DRF service with complex ORM — DRF stays simpler.
- Simple CRUD with no async benefit — Flask/DRF easier to operate.
- GraphQL — different schema model.
- Team has zero async experience and timeline is tight — risk of subtle bugs.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| DB driver | string (asyncpg, aiomysql, motor) | infra ADR |
| Auth scheme | JWT / cookie | security ADR |
| Migration tool | alembic / piccolo | infra ADR |
| Settings management | pydantic-settings | config ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[python]]` | Python ecosystem rules apply at the language level. |
| `[[python-poetry-setup]]` | Dep manager pin. |
| `[[error-handling]]` | RFC 7807 envelope for HTTP errors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: lifespan, schema separation, Annotated aliases, async services return ORM, flush+refresh | ~700 |
| `content/01-project-structure.xml` | essential | Recommended directory layout (kept) | ~700 |
| `content/02-output-contract.xml` | essential | App shape + per-endpoint invariants | ~700 |
| `content/02-schemas-deps.xml` | essential | Schemas + Annotated deps (kept) | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: deprecated on_event, schema reuse, logic in router, sync DB call in async route | ~600 |
| `content/03-service-layer.xml` | essential | Service-function patterns (kept) | ~700 |
| `content/04-antipatterns.xml` | essential | Additional FastAPI-specific traps (kept) | ~600 |
| `content/04-procedure.xml` | medium | 6-step scaffold | ~800 |
| `content/06-decision-tree.xml` | essential | Root question on async REST API needing OpenAPI | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold main + lifespan | sonnet | Template. |
| Generate schemas | sonnet | DTO generation. |
| Migrate sync endpoint to async | opus | I/O reasoning. |
| Auth dependency wiring | sonnet | Pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.py` | App + lifespan + router include scaffold. |
| `templates/schemas.py` | Base/Create/Update/Response schema skeletons. |
| `templates/dependencies.py` | Annotated DBSession + CurrentUser aliases. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-fastapi.py` | Greps for @app.on_event, sync DB calls in async routes, schema reuse. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[python]]` — Python language rules
- `[[error-handling]]` — RFC 7807 envelope
- `[[integration-testing]]` — async test session pattern

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: async-benefiting workload, team comfort with async, Pydantic v2 adoptable.
