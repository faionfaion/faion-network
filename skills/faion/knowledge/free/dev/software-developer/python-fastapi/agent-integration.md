# Agent Integration — Python FastAPI

## When to use
- New Python REST API where async I/O dominates (DB + HTTP fan-out).
- Migrating Flask / DRF endpoints to FastAPI route-by-route while keeping shared models.
- Building microservices that need automatic OpenAPI + Swagger UI.
- Replacing ad-hoc validators with Pydantic v2 schemas at the boundary.
- Adding background tasks via `BackgroundTasks` or Celery/RQ glue around FastAPI.
- Layered apps following routers → services → repositories where DI via `Depends` is desired.

## When NOT to use
- Sync-heavy CPU-bound services — FastAPI's strengths are I/O concurrency. Use a worker pool or Go/Rust.
- Apps requiring Django's batteries (auth, admin, ORM, migrations, contenttypes) — porting cost exceeds benefit.
- Plain function-as-a-service / Lambda where startup time matters; Pydantic v2 import is heavy.
- WebSockets-only services where Starlette directly is leaner.
- Projects that haven't committed to type hints — FastAPI without types loses its main value.

## Best practices
- Use Pydantic v2 (`model_validate`, `model_dump`) and avoid mixing v1/v2 idioms in the same project.
- Keep route functions thin: validate → call service → serialize. No business logic in routers.
- Define `Settings(BaseSettings)` once in `app/config.py` and inject via `Depends(get_settings)` (cached).
- Async DB: SQLAlchemy 2 async + `AsyncSession`; never call sync ORM in `async def` routes.
- Run uvicorn behind gunicorn `uvicorn.workers.UvicornWorker` in prod; never `--reload` outside dev.
- Group routers per domain under `app/routers/<domain>.py`; mount with explicit `prefix` and `tags`.

## Where it fails / limitations
- README's project tree shows `models/` for ORM and `schemas/` for Pydantic — agents conflate them and put response models in `models/`. Re-state the split.
- `lifespan` context (mentioned in main.py snippet) is the modern replacement for deprecated `@app.on_event`; agents still emit `on_event`.
- `Depends()` chains can hide N+1 DB session creation if not scoped per request — the README doesn't show session middleware.
- Background tasks via `BackgroundTasks` run **after the response** but in the **same event loop**; agents use it for long jobs and block the worker.
- No discussion of CORS preflight nuances, streaming responses, file uploads (`UploadFile` quirks), or rate limiting.
- Pydantic v1 → v2 breaking changes (`Config` → `model_config`, `validator` → `field_validator`) are not covered.

## Agentic workflow
Build FastAPI features in vertical slices: `schema → router → service → repository → test`. One subagent per slice, with a verifier subagent that runs `mypy`, `ruff`, `pytest`, and `uvicorn --check-config` (or boots the app via `httpx.AsyncClient` against `app`). Always require a route test that goes through the full DI chain (`TestClient` or `AsyncClient`) — unit-only tests miss `Depends` wiring bugs. Keep the agent away from `requirements.txt` / `pyproject.toml` edits unless explicitly tasked.

### Recommended subagents
- `faion-sdd-executor-agent` — SDD task pickup; matches well to vertical-slice tasks.
- `faion-feature-executor` — sequential execution with quality gates after each slice.
- General-purpose subagent restricted to `app/routers/<domain>.py` + `app/schemas/<domain>.py` + matching tests.
- `password-scrubber-agent` — sweep `app/config.py` and `.env*` before commit.

### Prompt pattern
```
Stack: FastAPI + Pydantic v2 + SQLAlchemy 2 async + uvicorn.
Layout: app/{routers,schemas,models,services,db/repositories}.
Constraints: routes async; Depends() for db session and current user; no business logic in routers;
Pydantic v2 only (model_config, field_validator); explicit response_model on every route.
After edit: run `ruff check`, `mypy app`, and `pytest tests/`. Stop on first failure.
```

```
Add endpoint <METHOD> <path>. Vertical slice only:
1) schemas (request + response), 2) router function, 3) service function, 4) repository method, 5) test via httpx.AsyncClient.
Do not modify other domains. Do not change DB models in this pass.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `uvicorn` | ASGI server | https://www.uvicorn.org/ |
| `gunicorn` (with UvicornWorker) | Process manager in prod | https://docs.gunicorn.org/ |
| `fastapi` CLI | Built-in dev/run/openapi commands | https://fastapi.tiangolo.com/fastapi-cli/ |
| `pydantic` v2 | Validation | https://docs.pydantic.dev/latest/ |
| `sqlalchemy` 2.x | ORM (async) | https://docs.sqlalchemy.org/ |
| `alembic` | Migrations | https://alembic.sqlalchemy.org/ |
| `httpx` (`AsyncClient`) | Test client + outbound HTTP | https://www.python-httpx.org/ |
| `respx` | Mock httpx in tests | https://lundberg.github.io/respx/ |
| `pytest-asyncio` | async test support | https://pytest-asyncio.readthedocs.io/ |
| `mypy` / `pyright` | Static typing | https://mypy.readthedocs.io/ , https://github.com/microsoft/pyright |
| `ruff` | Lint + format | https://docs.astral.sh/ruff/ |
| `openapi-python-client` / `datamodel-code-generator` | Generate clients from the served `/openapi.json` | https://github.com/openapi-generators/openapi-python-client , https://koxudaxi.github.io/datamodel-code-generator/ |
| `schemathesis` | Property-based API testing from OpenAPI | https://schemathesis.readthedocs.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Postgres + asyncpg | OSS | Yes | Default async DB combo. |
| Redis (`redis.asyncio`) | OSS | Yes | Cache + rate limit + pub/sub. |
| Celery / RQ / Arq / Taskiq | OSS | Yes | Real background jobs (replace `BackgroundTasks` for long work). Arq + Taskiq are async-native. |
| Sentry | SaaS | Yes | First-class FastAPI integration via `sentry-sdk[fastapi]`. |
| Logfire (Pydantic) | SaaS | Yes | Structured logging + Pydantic validation events. |
| OpenTelemetry | OSS | Yes | `opentelemetry-instrumentation-fastapi` auto-instruments routes. |
| Render / Fly.io / Railway / Vercel | SaaS | Yes | Native FastAPI deploy templates. |
| Modal / Beam | SaaS | Yes | Serverless Python with FastAPI app exposure. |
| Authentik / Keycloak | OSS | Yes | OIDC providers; pair with `fastapi-users` or custom `Depends(current_user)`. |

## Templates & scripts
Inline contract test runner — fails CI if served OpenAPI drifts from the committed snapshot:

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

Async test skeleton via `httpx.AsyncClient`:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/v1/users", json={"email": "a@b.c", "name": "A"})
    assert r.status_code == 201
    assert r.json()["email"] == "a@b.c"
```

## AI-agent gotchas
- Agents define `def route(...)` instead of `async def`, blocking the event loop. Lint with a custom rule or require `async def` in the prompt.
- Calling sync DB code (`session.query(...)`) inside `async def` routes silently blocks; agents do this when copy-pasting from Flask/DRF examples. Pin SQLAlchemy 2 async API.
- Pydantic v1 idioms (`class Config:`, `@validator`) creep in from training data. Pin v2 explicitly.
- `BackgroundTasks` runs in the same worker — agents push long jobs there and exhaust workers. Route long jobs to Celery/Arq/Taskiq.
- `response_model` strips fields not in the schema, including helpful error info; agents forget this and leak server data, or omit `response_model` altogether and break the OpenAPI spec.
- DI scope: a session-`Depends` returning a sync session in an async route is a frequent bug. Use a single async-session dependency.
- Streaming responses must use `StreamingResponse` with an async generator; agents return a `Response` with chunked body and mishandle backpressure.
- Human-in-loop checkpoint: review every change to `app/main.py` (middleware order, lifespan, CORS) — small edits have global effects.
- Do not let agents run `alembic revision --autogenerate` then `alembic upgrade head` in one shot; review the generated migration first (same trap as Django models).

## References
- https://fastapi.tiangolo.com/
- https://docs.pydantic.dev/latest/migration/
- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- https://www.uvicorn.org/deployment/
- https://github.com/zhanymkanov/fastapi-best-practices
- https://schemathesis.readthedocs.io/en/stable/
- https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
- https://taskiq-python.github.io/
