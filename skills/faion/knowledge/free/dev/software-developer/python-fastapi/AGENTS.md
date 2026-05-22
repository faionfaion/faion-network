---
slug: python-fastapi
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-grade FastAPI: Pydantic v2 schemas define the API contract, `Depends()` injects DB sessions and auth, async routes call service functions, lifespan events manage connection pools.
content_id: "4d9d16a50e38f204"
tags: [fastapi, python, async, pydantic, sqlalchemy]
---
# FastAPI Standards

## Summary

**One-sentence:** Production-grade FastAPI: Pydantic v2 schemas define the API contract, `Depends()` injects DB sessions and auth, async routes call service functions, lifespan events manage connection pools.

**One-paragraph:** Production-grade FastAPI: Pydantic v2 schemas define the API contract, `Depends()` injects DB sessions and auth, async routes call service functions, lifespan events manage connection pools. Separate request schemas (`UserCreate`) from response schemas (`UserResponse`); keep business logic in services, not routers.

## Applies If (ALL must hold)

- Building new REST APIs in Python requiring async/await and auto-generated OpenAPI docs
- Microservices needing high throughput (async I/O, connection pooling)
- Replacing synchronous Flask / Django REST Framework endpoints with async equivalents
- Projects where Pydantic v2 validation and `pydantic-settings` config management are already in use

## Skip If (ANY kills it)

- Existing Django projects with complex ORM relationships — Django REST Framework fits better
- Simple CRUD with no async I/O needs — Flask or Django may be simpler to operate
- Projects where the team is unfamiliar with `async/await` — sync bugs in async code are hard to debug
- GraphQL APIs — FastAPI's OpenAPI tooling conflicts with GraphQL schema conventions

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

- parent skill: `free/dev/software-developer/`
