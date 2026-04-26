# Agent Integration — Python FastAPI (python-developer)

## When to use
- New async REST API project where I/O concurrency dominates.
- Adding endpoints to an existing FastAPI project, vertical slice at a time (schema → router → service → repo → test).
- Migrating Flask/DRF endpoints to FastAPI route-by-route while sharing the database.
- Adding Pydantic v2 schemas to a project that previously hand-validated.
- Wrapping ML model inference in an HTTP endpoint with auto-generated OpenAPI.
- Building a microservice that fronts SQLAlchemy 2 async + Postgres + Redis.

## When NOT to use
- Sync-heavy CPU-bound services — FastAPI shines on I/O concurrency, not CPU.
- Apps that need Django's batteries (auth, admin, ORM, contenttypes) — porting cost > benefit.
- Lambda / FaaS where cold-start matters and Pydantic v2 import time hurts.
- Pure WebSockets services — Starlette directly is leaner.
- Codebases that aren't committed to type hints — most of FastAPI's value evaporates.

## Where it fails / limitations
- README's project tree shows `models/` (ORM) and `schemas/` (Pydantic) — agents conflate them and place response models in `models/`.
- `lifespan` is the modern replacement for the deprecated `@app.on_event` decorator. README mentions `lifespan` once but agents still emit `on_event` from training data.
- `Depends()` chains can hide N+1 DB session creation if scope isn't enforced — README doesn't show middleware-level session.
- `BackgroundTasks` runs in the same event loop after the response — agents push long jobs there and exhaust workers.
- README's "Concurrency Patterns" gives `asyncio.gather` examples but doesn't warn that exceptions raised inside one task cancel siblings unless `return_exceptions=True` is set.
- Pydantic v1 → v2 breaking changes (`Config` → `model_config`, `validator` → `field_validator`, `dict()` → `model_dump()`) not covered — agents mix idioms.
- "DB pool: pool_size = concurrency / 2" is a rule of thumb only; ignores PgBouncer, statement timeouts, lambda-style ephemeral workers.
- No content on file uploads (`UploadFile`), streaming responses, SSE, or rate limiting.
- `expire_on_commit=False` recommendation is correct but agents apply it globally, then hit stale-data bugs in long-lived sessions.

## Agentic workflow
Vertical-slice loop: one subagent per slice (schema → router → service → repository → test), with a verifier subagent running `ruff check`, `mypy app`, and `pytest tests/` after each slice. Always require an in-process route test through `httpx.AsyncClient` against the ASGI app — unit-only tests miss `Depends` wiring bugs. Keep agents away from `pyproject.toml` edits unless the SDD task is "dependency change". Never let an agent run `alembic revision --autogenerate` AND `alembic upgrade head` in one shot — review the migration first.

### Recommended subagents
- `faion-sdd-executor-agent` — vertical-slice SDD task pickup.
- `faion-feature-executor` — sequential gate after each slice.
- General-purpose subagent restricted to `app/routers/<domain>.py` + `app/schemas/<domain>.py` + `tests/` for that domain only.
- `password-scrubber-agent` — sweep `app/config.py` and `.env*` before commit.

### Prompt pattern
```
Stack: FastAPI + Pydantic v2 + SQLAlchemy 2 async + uvicorn.
Layout: app/{routers,schemas,models,services,db/repositories}.
Constraints: routes async; Depends() for db session and current user; no business logic in routers;
Pydantic v2 only (model_config, field_validator); explicit response_model on every route.
After edit: run `ruff check`, `mypy app`, `pytest tests/`. Stop on first failure.
```

```
Add endpoint <METHOD> <path>. Vertical slice only:
1) request schema, 2) response schema, 3) router function, 4) service function,
5) repository method, 6) test via httpx.AsyncClient with ASGITransport.
Do not modify other domains. Do not change DB models in this pass.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `uvicorn` | ASGI server | https://www.uvicorn.org/ |
| `gunicorn` (UvicornWorker) | Process manager in prod | https://docs.gunicorn.org/ |
| `fastapi` CLI | Dev/run/openapi commands | https://fastapi.tiangolo.com/fastapi-cli/ |
| `pydantic` v2 | Validation | https://docs.pydantic.dev/latest/ |
| `sqlalchemy` 2.x | ORM (async) | https://docs.sqlalchemy.org/ |
| `alembic` | Migrations | https://alembic.sqlalchemy.org/ |
| `httpx` (`AsyncClient`, `ASGITransport`) | In-process & out-of-process HTTP | https://www.python-httpx.org/ |
| `respx` | Mock httpx in tests | https://lundberg.github.io/respx/ |
| `pytest-asyncio` | Async test support | https://pytest-asyncio.readthedocs.io/ |
| `mypy` / `pyright` | Static typing | https://mypy.readthedocs.io/ , https://github.com/microsoft/pyright |
| `ruff` | Lint + format | https://docs.astral.sh/ruff/ |
| `openapi-python-client` / `datamodel-code-generator` | Generate clients from `/openapi.json` | https://github.com/openapi-generators/openapi-python-client |
| `schemathesis` | Property-based API testing | https://schemathesis.readthedocs.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Postgres + asyncpg | OSS | Yes | Default async DB combo. |
| Redis (`redis.asyncio`) | OSS | Yes | Cache + rate limit + pub/sub. |
| Celery / RQ / Arq / Taskiq | OSS | Yes | Real background jobs. Arq + Taskiq are async-native. |
| Sentry | SaaS | Yes | `sentry-sdk[fastapi]` integration. |
| Logfire (Pydantic) | SaaS | Yes | Structured logging + Pydantic events. |
| OpenTelemetry | OSS | Yes | `opentelemetry-instrumentation-fastapi`. |
| Render / Fly.io / Railway / Modal | SaaS | Yes | Native FastAPI templates. |
| Authentik / Keycloak | OSS | Yes | OIDC; pair with `fastapi-users`. |
| PgBouncer | OSS | Yes | Required for serverless / autoscaled FastAPI to keep PG connection counts sane. |

## Templates & scripts
Inline contract test: fail CI if served OpenAPI drifts from the committed snapshot.

```bash
#!/usr/bin/env bash
# scripts/openapi-snapshot.sh
set -euo pipefail
python - <<'PY' > openapi.new.json
import json
from app.main import app
print(json.dumps(app.openapi(), indent=2, sort_keys=True))
PY
if [[ -f openapi.json ]]; then
  diff -u openapi.json openapi.new.json && rm openapi.new.json && exit 0
  echo "OpenAPI changed. Review and commit openapi.json if intentional."
  mv openapi.new.json openapi.json
  exit 1
fi
mv openapi.new.json openapi.json
```

Async route test skeleton (`httpx.AsyncClient` + `ASGITransport`):

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/api/v1/users", json={"email": "a@b.c", "name": "A"})
    assert r.status_code == 201
    assert r.json()["email"] == "a@b.c"
```

## Best practices
- Pydantic v2 only — pin `pydantic>=2,<3` and `pydantic-settings>=2`.
- Keep route functions thin: validate → call service → serialize. Business logic in `services/`.
- Single `Settings(BaseSettings)` in `app/config.py`; inject via cached `Depends(get_settings)`.
- Async DB: SQLAlchemy 2 async + `AsyncSession`; never call sync ORM in `async def` routes.
- Run uvicorn behind gunicorn `uvicorn.workers.UvicornWorker` in prod; never `--reload` outside dev.
- Group routers per domain under `app/routers/<domain>.py` with explicit `prefix` and `tags`.
- One `AsyncSession` per asyncio task; never share across `asyncio.gather` siblings.
- Eager-load relationships with `selectinload`/`joinedload` to avoid lazy-loading exceptions on serialization.

## AI-agent gotchas
- Agents define `def route(...)` instead of `async def`, blocking the event loop.
- Sync DB code (`session.query(...)`) inside `async def` silently blocks; agents copy from Flask/DRF examples.
- Pydantic v1 idioms (`class Config:`, `@validator`) leak in. Pin v2 explicitly.
- `BackgroundTasks` for long jobs exhausts workers — route to Celery/Arq/Taskiq for >100ms work.
- `response_model` strips fields not in schema (correct) but agents forget and leak server-only fields, OR omit `response_model` and break OpenAPI.
- DI scope: a sync `Depends` in an async route. Use a single async-session dependency.
- Streaming: must use `StreamingResponse` with an async generator; agents return raw `Response` and mishandle backpressure.
- Agents commit a regenerated `openapi.json` snapshot without reviewing the diff — silently ships breaking changes to consumers.
- `expire_on_commit=False` is needed for typical request-scoped sessions but agents apply it to long-lived workers and serve stale rows.
- Human-in-loop checkpoint: any change to `app/main.py` (middleware order, lifespan, CORS) and any new Alembic migration.

## References
- https://fastapi.tiangolo.com/
- https://docs.pydantic.dev/latest/migration/
- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- https://www.uvicorn.org/deployment/
- https://github.com/zhanymkanov/fastapi-best-practices
- https://schemathesis.readthedocs.io/en/stable/
- https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
- https://taskiq-python.github.io/
