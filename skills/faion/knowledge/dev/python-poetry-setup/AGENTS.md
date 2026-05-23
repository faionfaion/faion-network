# Python Poetry Setup

## Summary

**One-sentence:** Produces a reproducible Poetry setup — poetry.lock committed, --sync install in CI, dep groups (main/dev/test/docs), tight Python constraint, builder-stage Docker, snok install action + .venv cache.

**One-paragraph:** Poetry is the standard for Python dependency management: deterministic builds via poetry.lock, isolated virtual environments, streamlined PyPI publishing. Always commit `poetry.lock`. Use `poetry install --sync --no-interaction` in CI (the `--sync` removes packages that left the lockfile, preventing zombies). Never run bare `poetry update` in a shared repo — bump per-package only. Split deps into groups: main, dev, test, docs (docs `optional = true`). Tight Python constraints (`python = "^3.11"`, not `>=3.8`). Docker: builder stage runs `poetry export`, final stage runs `pip install -r requirements.txt` so Poetry doesn't ship into production. CI uses `snok/install-poetry@v1` + cache `.venv` by `poetry.lock` hash.

**Ефективно для:** new Python projects, services migrating from requirements.txt + pip-tools, Docker images bloated with Poetry runtime, CI suites with slow install times.

## Applies If (ALL must hold)

- Python project on 3.11+.
- Team accepts Poetry as dep manager (or willing to adopt).
- CI can install Poetry and cache .venv.
- Docker builds (if any) can use multi-stage.

## Skip If (ANY kills it)

- Project on uv / hatch / Rye — different tool family.
- requirements.txt-only legacy with no migration mandate.
- Pure pip-installable library where Poetry overhead exceeds value.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python version | semver | tech stack |
| Dep list (current) | requirements.txt or Pipfile | repo |
| CI provider | string | infra ADR |
| Docker target | image base | infra ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[python]]` | Broader Python conventions; this file is the dep-manager focus. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: commit lockfile, --sync in CI, no bare update, dep groups, tight Python, poetry check --lock, Docker multi-stage, snok+cache, env var for PyPI token | ~800 |
| `content/02-output-contract.xml` | essential | Required pyproject + CI + Dockerfile invariants | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: missing lockfile, bare update, Poetry in final Docker stage, broad Python constraint | ~600 |
| `content/06-decision-tree.xml` | essential | Root: "Python project where Poetry is acceptable?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Migration from requirements.txt | sonnet | Dep parsing + pyproject generation. |
| Docker multi-stage rewrite | sonnet | Template. |
| CI cache config | haiku | YAML boilerplate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Poetry pyproject with groups + ruff + mypy config. |
| `templates/Dockerfile` | Multi-stage Dockerfile (builder + final). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-poetry-setup.py` | Verifies poetry.lock presence, --sync in CI, Python tight pin, no `poetry install` in final Dockerfile stage. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[python]]` — broader Python rules

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: Python project, Poetry acceptable, CI can cache .venv.
