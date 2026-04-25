# Agent Integration — Python Web Frameworks (Django / FastAPI / Flask)

## When to use
- Greenfield Python web project where the framework choice is still open — feed the decision matrix to a sonnet/opus subagent and ask for a recommendation grounded in concrete project requirements.
- Migration planning: agent compares an existing Flask/Django app against FastAPI to surface what would need to change (sync→async, ORM, admin, auth).
- "Hybrid" review — when an org runs FastAPI for public APIs + Django for admin, agents cross-check that they share a DB schema correctly.
- Onboarding: route a new dev's "where do I add X?" question to the right framework's conventions.
- Tech-debt audit: identify when a Flask app has outgrown its minimalism and should be split into FastAPI services or absorbed into Django.

## When NOT to use
- Single-framework codebase where the team has already committed — load only that framework's specific methodology (`python-fastapi`, `django-models`, etc.) and skip the comparison overhead.
- Deciding between Litestar/Sanic/Quart/Starlette — README only covers the big three; agents will hallucinate parity if you ask outside that scope.
- Non-web Python work (ML batch jobs, scripts, CLIs) — wrong abstraction layer.
- Performance-critical pure async scenarios where you've already picked FastAPI — comparison content distracts the agent.

## Where it fails / limitations
- Performance numbers are unsourced (`~1,500 RPS`, `~3,000+ RPS`); agents will quote them as fact. Strip or qualify them in prompts.
- README claims FastAPI has "built-in" background tasks "and Celery" — true, but the built-in `BackgroundTasks` runs in-process and is unsuitable for long jobs. Easy to misread.
- "Flask 2.0+ supports async views but remains WSGI-focused" — agents miss that running async views under WSGI is a footgun (each request blocks a worker for the duration of the coroutine). Restate explicitly.
- The Django ASGI deployment line (`gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -w 4`) drops `--lifespan off` which Django requires until Channels lifespan is configured; agents will copy-paste and break startup.
- ORM comparison says FastAPI has "None (use SQLAlchemy)" — agents take "None" literally and skip ORM choice entirely. Add SQLModel/Tortoise/Beanie as alternatives.
- No mention of Pydantic v1 vs v2 in framework context — agents mix them.
- "Django Async (2025) — Django 5.2 provides mature async support" overstates: ORM still has sync-only operations (signals, complex F-expressions), and middleware ordering is a frequent bug.
- Decision matrix is binary (Django | FastAPI | Flask) and ignores Litestar, Starlette, BlackSheep, Sanic, AIOHTTP — for some workloads those are better fits.

## Agentic workflow
Use this methodology as a routing layer, not as build instructions. Step 1: a sonnet/opus subagent reads the project brief and outputs a single framework choice + a 5-bullet justification mapped to the README's decision matrix. Step 2: route to the framework-specific methodology subagent (`python-fastapi`, `django-api`, or a Flask agent). Step 3: a verifier subagent reads the generated stub project and confirms it matches that framework's idioms (no Flask-style `@app.route` in FastAPI, no DRF imports in Ninja code, no sync `requests` calls in async views).

### Recommended subagents
- General-purpose `framework-router` (sonnet) — reads brief, returns one of `django|fastapi|flask|litestar` with rationale.
- `faion-sdd-executor-agent` — picks up the framework-specific tasks once choice is locked.
- `faion-feature-executor` — sequential gate; runs `ruff` + `mypy` + framework-native test runner per slice.
- `password-scrubber-agent` — sweep `settings.py`/`config.py`/`.env*` before any commit.

### Prompt pattern
```
Project brief: <one paragraph describing the product, scale, team>.
Using ONLY the README decision matrix in skills/.../python-web-frameworks/README.md,
output JSON: {"framework": "...", "version": "...", "why": ["..."], "deal_breakers": ["..."]}.
Do not invent frameworks not in the matrix. Cite the matrix row(s) in `why`.
```

```
You picked <framework>. Now scaffold the project layout per that framework's
methodology file (django-api/, python-fastapi/, etc). Do NOT mix idioms.
After scaffolding, run the test suite. If it fails, stop and report.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `django-admin startproject` / `startapp` | Django scaffolding | https://docs.djangoproject.com/en/5.2/ref/django-admin/ |
| `fastapi` CLI | Run/dev FastAPI apps, OpenAPI export | https://fastapi.tiangolo.com/fastapi-cli/ |
| `flask` CLI | Run Flask, manage shell | https://flask.palletsprojects.com/en/latest/cli/ |
| `uvicorn` / `gunicorn` (with `UvicornWorker`) | ASGI / WSGI server | https://www.uvicorn.org/ , https://docs.gunicorn.org/ |
| `daphne` | ASGI server (Django Channels) | https://github.com/django/daphne |
| `alembic` | Migrations for SQLAlchemy (FastAPI/Flask) | https://alembic.sqlalchemy.org/ |
| `manage.py makemigrations` / `migrate` | Django migrations | https://docs.djangoproject.com/en/5.2/topics/migrations/ |
| `pytest-django` / `pytest-flask` | Framework-aware testing | https://pytest-django.readthedocs.io/ , https://pytest-flask.readthedocs.io/ |
| `httpx` (`AsyncClient`) | API testing for any ASGI app | https://www.python-httpx.org/ |
| `ruff`, `mypy` / `pyright`, `bandit` | Lint / typecheck / security scan | https://docs.astral.sh/ruff/ |
| `cookiecutter-django` / `full-stack-fastapi-template` | Project templates | https://cookiecutter-django.readthedocs.io/ , https://github.com/fastapi/full-stack-fastapi-template |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Render / Fly.io / Railway | SaaS | Yes | All three deploy Django, FastAPI, Flask from `Dockerfile` or buildpacks. |
| Heroku | SaaS | Yes | Mature buildpacks for all three; expensive at scale. |
| Vercel / Netlify | SaaS | Limited | Serverless functions OK for Flask/FastAPI; Django needs custom config. |
| AWS Lambda + Mangum | SaaS | Yes | Wrap ASGI app for Lambda; FastAPI is the easiest fit. |
| Modal / Beam | SaaS | Yes | Serverless Python; native FastAPI exposure. |
| Sentry | SaaS | Yes | Native SDKs for all three; auto-instruments routes. |
| OpenTelemetry | OSS | Yes | `opentelemetry-instrumentation-django|fastapi|flask` packages. |
| Pydantic Logfire | SaaS | Yes | Best fit for FastAPI/Pydantic stacks. |
| Authentik / Keycloak / Auth0 | OSS / SaaS | Yes | OIDC providers usable across all three. |
| Celery / RQ / Arq / Taskiq | OSS | Yes | Background jobs; pick async-native (Arq/Taskiq) for FastAPI. |

## Templates & scripts
Decision helper: dump a JSON answer the orchestrator can branch on.

```bash
#!/usr/bin/env bash
# scripts/pick-framework.sh — pipe a brief, get a framework choice
set -euo pipefail
BRIEF=${1:-/dev/stdin}
python - <<'PY' < "$BRIEF"
import json, sys
brief = sys.stdin.read().lower()
score = {"django": 0, "fastapi": 0, "flask": 0}
if any(k in brief for k in ["admin panel", "cms", "full-stack", "html template"]): score["django"] += 3
if any(k in brief for k in ["ml model", "high concurrency", "async", "websocket", "openapi"]): score["fastapi"] += 3
if any(k in brief for k in ["prototype", "internal tool", "minimal", "small"]): score["flask"] += 2
if "microservice" in brief: score["fastapi"] += 2
if "rapid development" in brief: score["django"] += 1
choice = max(score, key=score.get)
print(json.dumps({"framework": choice, "scores": score}))
PY
```

For framework-specific scaffolds, route to `python-fastapi/templates.md` or `django-api/templates.md` rather than embedding here.

## Best practices
- Lock the framework choice in `constitution.md` of the SDD; the agent must not switch frameworks mid-feature.
- For "FastAPI + Django hybrid" deployments, share the database schema via Django migrations (Django owns DDL); FastAPI uses SQLAlchemy in read-mostly mode against the same tables.
- Pin one ASGI server per app and one WSGI server per app — agents will switch to whatever they saw in the last training example otherwise.
- Always include a `pytest` smoke test that boots the app via `TestClient`/`Client`/`test_client` — catches import-time errors that lint passes miss.
- Keep `requirements.txt`/`pyproject.toml` framework-pure — don't let `Flask-*` extensions leak into a Django project even "for the utility".
- For Django async views, document which views are async and which are sync — mixed apps confuse middleware and DB connections.
- Never let an agent "upgrade" a framework version (Django 4 → 5, FastAPI 0.100 → 0.110) inside a feature task — that's its own audit.

## AI-agent gotchas
- Agents quote the unsourced RPS numbers as authoritative; benchmark numbers from the README must be qualified or removed.
- Mixing imports across frameworks: `from flask import jsonify` ends up in a FastAPI route. Lint with import-graph rules.
- Agents add `Flask-Login` to FastAPI projects because they pattern-match "login extension". Force them to use FastAPI's `Depends(get_current_user)` instead.
- Django ORM in FastAPI: agents copy `User.objects.filter(...)` into a FastAPI route — works only if `django.setup()` is called at startup, which is non-standard.
- `@app.on_event("startup")` is deprecated in FastAPI; the README does not warn — agents emit deprecated lifespan code.
- Async Django views without `sync_to_async` around ORM calls — agents skip the wrapper because the README shows `await User.objects.filter(active=True).aall()` (correct) but doesn't warn that not every ORM op has an `a*` alias.
- Agents pick Flask because "minimalism" then bolt on Flask-RESTX, Flask-Migrate, Flask-Login, Flask-WTF until it's a Django clone — review the dep list before merging.
- Human-in-loop checkpoint: any change to `settings.py`/`main.py`/`app.py` (middleware order, security headers, CORS) — small edits have global effect.

## References
- https://docs.djangoproject.com/en/5.2/
- https://fastapi.tiangolo.com/
- https://flask.palletsprojects.com/
- https://blog.jetbrains.com/pycharm/2025/02/django-flask-fastapi/
- https://www.propelauth.com/post/fastapi-vs-flask-vs-django-in-2025
- https://github.com/zhanymkanov/fastapi-best-practices
- https://github.com/HackSoftware/Django-Styleguide
- https://litestar.dev/ (alternative not in README)
