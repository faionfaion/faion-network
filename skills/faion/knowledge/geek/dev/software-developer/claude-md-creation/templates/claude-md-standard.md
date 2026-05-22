<!--
purpose: Standard CLAUDE.md skeleton for a typical product repo.
consumes: Repo facts: commands, conventions, dependencies, owners.
produces: A project CLAUDE.md committed at the repo root.
depends-on: templates/extract-commands.sh for the commands section.
token-budget-impact: ~500 tokens when fully filled.
-->
# [Project Name]

One paragraph: what this project does, its purpose, tech stack at a glance.

## Commands

```bash
# Development
make dev              # Start development server (port 8000)
uvicorn src.main:app --reload

# Testing
pytest --cov=src -x           # Run tests, stop at first failure
pytest -m "not slow"          # Fast tests only

# Code Quality
ruff check . --fix            # Lint + auto-fix (rules: E/F/I/B/T20/DJ)
ruff format .                 # Format
mypy src                      # Type check

# Database
alembic upgrade head          # Apply migrations
alembic revision --autogenerate -m "description"  # New migration
```

## Structure

```
src/
  api/        FastAPI routes (v1/ subdirectory per API version)
  core/       Business logic, config, security helpers
  models/     SQLAlchemy models
  schemas/    Pydantic schemas
  services/   External integrations (email, payment, etc.)
tests/
  conftest.py     Shared fixtures
  unit/           Unit tests mirror src/ structure
  integration/    Integration tests for API endpoints
```

## Conventions

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`
- Imports: stdlib → third-party → local (ruff I rule enforces this)
- No print() in production code (ruff T20 rule blocks commits)
- Type hints required on all public functions

## Key Files

| File | Purpose |
|------|---------|
| `src/core/config.py` | Settings (reads from env, never hardcode) |
| `src/api/deps.py` | FastAPI dependencies (auth, db session) |
| `tests/conftest.py` | Shared fixtures (db, client, test user) |
| `.env.example` | Required env vars — copy to .env before running |

## Gotchas

- `DATABASE_URL=<required>` — must be set; no default
- Run migrations before first start: `alembic upgrade head`
- Test isolation: each test rolls back transaction (see conftest.py fixture)
