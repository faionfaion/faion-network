# Django Code Quality Tools

## Summary

Quality toolchain for Django projects: ruff (format + lint), mypy + django-stubs (typing), bandit (security), and pre-commit hooks orchestrating all of them. The canonical setup is `pyproject.toml`-only — no separate `.flake8`, no `setup.cfg`, no black/isort alongside ruff.

## Why

A deterministic format/lint baseline removes whitespace noise from diffs so code review focuses on logic. Pre-commit hooks enforce the baseline at commit time; CI enforces it at merge time. mypy + django-stubs catches type errors before runtime. Without this, each agent writes code in a different style and introduces subtle type errors that only surface in production.

## When To Use

- Bootstrapping a new Django project before first feature commit.
- Migrating a legacy Django repo from black+isort+flake8 to ruff.
- Onboarding agents to a Django codebase that needs a deterministic baseline.
- Adding type-checking incrementally module by module via mypy overrides.

## When NOT To Use

- Non-Django Python projects — drop `mypy_django_plugin` and DJ rules; rest still applies.
- Single-script utilities where pre-commit setup exceeds the code itself.
- Legacy migration files — gate with `--diff` first or you'll create a 5k-line format PR.

## Content

| File | What's inside |
|------|---------------|
| `content/01-toolchain-rules.xml` | Ruff config rules, mypy setup, pre-commit wiring, checklist phases. |
| `content/02-exception-handling.xml` | Rules for specific exception handling; bare-except and broad-except antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject-ruff.toml` | Modern ruff + mypy config block for Django (replaces black/isort/flake8). |
| `templates/pre-commit-config.yaml` | pre-commit hooks: ruff, ruff-format, bandit, end-of-file-fixer, trailing-whitespace. |
