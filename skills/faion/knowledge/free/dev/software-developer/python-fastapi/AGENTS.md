# FastAPI Standards

## Summary

Production-grade FastAPI: Pydantic v2 schemas define the API contract, `Depends()` injects DB
sessions and auth, async routes call service functions, lifespan events manage connection pools.
Separate request schemas (`UserCreate`) from response schemas (`UserResponse`); keep business logic
in services, not routers.

## Why

FastAPI's Pydantic + `Depends()` system enforces schema-first design and makes routes thin by
construction. Async I/O (SQLAlchemy 2.0 async, `httpx.AsyncClient`) avoids blocking the event loop.
`lru_cache` on settings reads `.env` once. Separating request/response schemas prevents accidental
write-field exposure and makes partial-update (`PATCH`) clean via `model_dump(exclude_unset=True)`.

## When To Use

- Building new REST APIs in Python requiring async/await and auto-generated OpenAPI docs
- Microservices needing high throughput (async I/O, connection pooling)
- Replacing synchronous Flask / Django REST Framework endpoints with async equivalents
- Projects where Pydantic v2 validation and `pydantic-settings` config management are already in use

## When NOT To Use

- Existing Django projects with complex ORM relationships — Django REST Framework fits better
- Simple CRUD with no async I/O needs — Flask or Django may be simpler to operate
- Projects where the team is unfamiliar with `async/await` — sync bugs in async code are hard to debug
- GraphQL APIs — FastAPI's OpenAPI tooling conflicts with GraphQL schema conventions

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-structure.xml` | `app/` layout, `main.py` with lifespan, CORS middleware, router inclusion |
| `content/02-schemas-deps.xml` | Pydantic v2 schema patterns, `pydantic-settings` config, `Depends()`, type aliases |
| `content/03-service-layer.xml` | Async service functions, SQLAlchemy 2.0 async queries, paginated responses |
| `content/04-antipatterns.xml` | Sync ops in async routes, business logic in routes, mutable default args |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.py` | FastAPI app with lifespan, CORS, and router wiring |
| `templates/schemas.py` | `UserBase` / `UserCreate` / `UserUpdate` / `UserResponse` Pydantic v2 schema set |
| `templates/dependencies.py` | `get_db`, `get_current_user`, `CurrentUser` / `DBSession` type aliases |
