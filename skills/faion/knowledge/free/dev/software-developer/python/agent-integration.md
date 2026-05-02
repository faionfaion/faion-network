# Agent Integration — Python Ecosystem

The methodology bundles 8 sub-topics (Poetry setup, Django, FastAPI, pytest, type hints + mypy, Black/isort/flake8, venv management, asyncio). Treat it as a routing menu: an LLM agent picks ONE sub-topic per task, not all eight at once.

## When to use
- Bootstrapping a new Python service (Django 5 / FastAPI / standalone) where layout, deps and lint config must match faion-net house style.
- Adding a feature to an existing project that already follows this skill's structure (`apps/<name>/{models,views,services,serializers,admin}.py`).
- Migrating a legacy project from `setup.py` / `requirements.txt` to Poetry + lockfile.
- Introducing static typing (mypy strict) on a previously untyped codebase, file-by-file.
- Wiring pre-commit so contributing agents cannot land unformatted code.

## When NOT to use
- Pure data / notebook work — Poetry is overkill, use `uv`/`pip` + `pyproject.toml` minimal.
- Edge / serverless functions where cold-start matters — skip async ORM, skip mypy at runtime, lean stdlib only.
- Codebases standardized on `ruff` (faion-net itself does — see project AGENTS.md) — do NOT introduce Black/isort/flake8; they conflict with `ruff format`.
- Python ≤3.9 — most snippets assume 3.11+ (`asyncio.TaskGroup`, PEP 604 `X | Y`).
- Greenfield API where FastAPI is on the table — don't auto-default to Django because the methodology lists it first.

## Where it fails / limitations
- Black/isort/flake8 trio is **deprecated in faion-net** (ruff replaces all three). README has not been updated; agents must skip that section here.
- `poetry shell` was removed in Poetry 2.0 (Sept 2024) — replace with `poetry env activate` or `eval $(poetry env activate)`.
- Django services pattern shows `transaction.atomic` decorator on a function that does not actually require it; encourages over-locking.
- Async section assumes `aiohttp` but never imports it in the snippets.
- `Optional[X]` and `X | None` shown side-by-side without picking a winner — agents will mix both in the same file.
- No coverage of `pyproject.toml` build backends besides `poetry-core` (no setuptools, no hatchling).
- pytest section conflates Django integration tests with pure unit tests; running everything as `pytest` ignores the slow-tier separation.

## Agentic workflow
Drive Python work as: classify task → pick sub-topic → load only the relevant section into context (don't paste the full 1700-line README). Execute in a Bash sandbox with `python:*, poetry:*, pytest:*, ruff:*, mypy:*` allow-list. After every code edit, run the project's actual lint command (faion-net = `ruff check --fix && ruff format`), not Black. Commit only after `pytest -x` is green. Never run `poetry update` without explicit user approval — it rewrites the lockfile.

### Recommended subagents
- `faion-code-agent` — Default executor for implementation snippets (Django models/services, FastAPI routes, async handlers).
- `faion-test-agent` — Owns pytest fixtures, mocking, parametrize, coverage runs.
- `faion-devtools-developer` (sibling skill) — Owns pre-commit, lint config, Poetry/uv migration.
- `faion-software-architect` (sibling) — Owns Django-vs-FastAPI choice and async/sync boundary decisions.
- `/faion` (knowledge/solo/sdd/sdd/) — Wraps the whole loop in spec → impl → test → review when the task is non-trivial.

### Prompt pattern
Sub-topic dispatch:

```
Task: <short>. Stack: Django 5 + DRF on Python 3.11.
Apply ONLY the "Django Patterns" section of free/dev/software-developer/python/README.md.
Constraints: thin views, services for business logic, ruff (not black) for format,
type hints required, pytest with @pytest.mark.django_db.
Return diff + test run output.
```

mypy onboarding (one file at a time):

```
Add types to apps/<module>/services.py. Use `X | None` not Optional. Update mypy
overrides only if a third-party stub is missing. Do NOT touch other files.
Run: mypy apps/<module>/services.py — paste full output.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `poetry` | Dep + venv mgmt; lockfile | https://python-poetry.org/docs |
| `uv` | 10-100x faster Poetry alt; `pip`-compat | https://docs.astral.sh/uv |
| `ruff` | Lint + format (replaces black/isort/flake8) | https://docs.astral.sh/ruff |
| `mypy` | Static type checking | https://mypy.readthedocs.io |
| `pyright` | Faster mypy alt; default in VSCode Pylance | https://microsoft.github.io/pyright |
| `pytest` + `pytest-django` + `pytest-cov` | Test runner | https://docs.pytest.org |
| `pre-commit` | Git hook orchestrator | https://pre-commit.com |
| `pyenv` | Multiple Python versions | https://github.com/pyenv/pyenv |
| `pipx` | Install Python CLIs in isolated venvs | https://pipx.pypa.io |
| `python -m venv` | stdlib venv (no extra dep) | https://docs.python.org/3/library/venv.html |
| `safety` / `pip-audit` | CVE scan against installed deps | https://pyup.io/safety / https://pypi.org/project/pip-audit |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| PyPI | OSS registry | Yes — `pip search` removed; use `pip index` or web | Resolve version pins via `poetry add pkg@^1` |
| ReadTheDocs | OSS docs | Yes — sphinx-build CLI | Trigger via webhook from GitHub |
| Codecov / Coveralls | SaaS | Yes — REST + GH App | Upload `coverage.xml` after `pytest --cov` |
| Sentry | SaaS APM | Yes — `sentry-sdk` + `@sentry_sdk.init()` | Add to FastAPI/Django via middleware |
| Render / Fly.io / Railway | SaaS PaaS | Yes — CLI + buildpacks | Detect `pyproject.toml` automatically |
| Anthropic Claude Code skills | Internal | Yes | This methodology is a skill itself |

## Templates & scripts
See README sub-sections (Project Setup, Django Patterns, FastAPI Patterns, pytest, etc.) for full templates. Minimal modern alternative to the README's pyproject.toml (replaces black+isort+flake8 with ruff, matches faion-net standard):

```toml
[project]
name = "service-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["django>=5.0", "djangorestframework>=3.14"]

[dependency-groups]
dev = ["pytest>=8", "pytest-django>=4.8", "pytest-cov>=4.1", "ruff>=0.5", "mypy>=1.8", "django-stubs"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "SIM", "DJ", "T20"]

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["mypy_django_plugin.main"]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
addopts = "-x --tb=short --strict-markers"
```

## Best practices
- **Use ruff, not the Black/isort/flake8 trio.** faion-net AGENTS.md mandates this; the README is stale on that point.
- **Pin Python in `.python-version`** so CI, Docker, and local dev share a version. Match minor across `pyproject.toml requires-python`, `tool.mypy python_version`, and Dockerfile `FROM python:X.Y`.
- **Services own writes; views own HTTP.** Never call `Model.objects.create()` from a view. Never raise `HTTPException` from a service.
- **Type the public boundary first.** `services/*.py` and route handlers, then internal helpers. Tests can be untyped via mypy override.
- **Async is contagious.** Don't sprinkle `async` into Django code unless the whole stack (ASGI server, ORM calls via `sync_to_async`, middleware) is ready.
- **Use `select_for_update()` only inside `transaction.atomic()`** — and only when there's an actual race. The README's `transfer_ownership` is the rare legitimate case.
- **`uv` for new projects, Poetry only when existing lockfile**. uv is dramatically faster and `pip`-compatible; less agent waiting.
- **Lock `pyproject.toml` and lockfile together** in one commit. Splitting them breaks reproducible builds.
- **`pytest -x --lf`** during iterative dev (stop on first fail, then run last-failed). Cuts feedback loop ~10x on big suites.

## AI-agent gotchas
- **README contradicts faion-net repo standard** on the linter (Black vs ruff). Trust repo `AGENTS.md` over knowledge base when they disagree.
- **`poetry shell` removal** — agents trained pre-Poetry 2.0 will run it and silently get a non-shell. Use `poetry env activate` or `poetry run <cmd>`.
- **Mixing `Optional[X]` and `X | None`** in one file makes mypy noisy and hurts diffs. Pick one per project (modern: `X | None`).
- **Django `transaction.atomic` as decorator vs context manager** — only the context-manager form respects custom `using=` databases. Default to context manager.
- **Async DB calls in Django** require `sync_to_async`; calling `User.objects.get()` directly inside `async def` raises `SynchronousOnlyOperation`. Easy to miss in code review.
- **`@pytest.mark.django_db`** without `transaction=True` rolls back fixtures between tests — but mixing it with `select_for_update` deadlocks under SQLite. Use Postgres for those.
- **`asyncio.gather` swallows exceptions** unless `return_exceptions=False` (default) is paired with a try/except around the await. `TaskGroup` is safer; prefer it on 3.11+.
- **`BackgroundTasks` in FastAPI runs in the request lifecycle** — long jobs block the worker. Use Celery / arq / dramatiq for >1s work.
- **Test discovery + Django settings**: `pytest-django` needs `DJANGO_SETTINGS_MODULE` set in `pyproject.toml` OR env. Forgetting this causes "Apps aren't loaded yet" with zero useful traceback.
- **Black/isort run order**: README says `isort && black && flake8`. With ruff, all three are one call: `ruff check --fix && ruff format`. Don't run both stacks; they fight on import groups.
- **Print statements (T20)**: `ruff` blocks `print()` in faion-net code. Use `logging`. Tests are exempt via per-file overrides.
- **Cross-app imports**: README rule "always alias" is real — without it, circular imports silently break Django app loading.

## References
- README: `./README.md`
- Sibling methodologies in `software-developer/`: `python-type-hints/`, `python-fastapi/`, `python-poetry-setup/`, `django-api/`, `django-pytest/`, `django-base-model/`
- ruff docs: https://docs.astral.sh/ruff/configuration/
- uv: https://docs.astral.sh/uv/
- Poetry 2.0 changelog: https://python-poetry.org/blog/announcing-poetry-2.0.0/
- pytest-django: https://pytest-django.readthedocs.io
- mypy strict mode: https://mypy.readthedocs.io/en/stable/getting_started.html#strict-mode
- FastAPI async docs: https://fastapi.tiangolo.com/async/
- Django async views: https://docs.djangoproject.com/en/5.0/topics/async/
