# Poetry Project Setup

## Summary

**One-sentence:** Poetry 2.x project setup with PEP 621, lockfile-first reproducibility, plugin ecosystem.

**One-paragraph:** Modern Python dependency management with Poetry 2.x: PEP 621-aligned pyproject.toml, deterministic lockfiles, virtual environment management, and reproducible builds. Use this only when uv is not an option; new projects default to uv (see python-modern-2026).

**Ефективно для:** розробника, який зобовʼязаний використовувати Poetry (legacy-репо, корпоративні політики) — закриває петлю між PEP 621 і поведінкою Poetry 2.x.

## Applies If (ALL must hold)

- Project mandated to use Poetry (corporate standard, legacy infra).
- Migrating Poetry 1.x to Poetry 2.x with PEP 621 layout.
- Authoring a library to publish to PyPI via poetry publish.
- Authoring a monorepo with Poetry workspaces.

## Skip If (ANY kills it)

- Greenfield project with no constraint — use uv instead (python-modern-2026).
- Pure script / single-file utility — pip install is enough.
- Conda-managed data-science env.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Poetry 2.0+ installed | binary | pipx install 'poetry>=2.0' |
| pyproject.toml (PEP 621) | TOML | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-code-quality` | Ruff/mypy/pre-commit settings the lockfile pins. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 rules: PEP 621 layout, lockfile committed, dep groups (main/dev/test/docs), no caret on libs, in-project .venv, `--sync` in CI, no bare `poetry update`, tight Python constraint, `check --lock` before add, Docker builder export, CI `.venv` cache. | ~1600 |
| `content/02-output-contract.xml` | essential | Gate schema (pyproject + CI + Dockerfile invariants) + valid / invalid project shapes. | ~1400 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: caret in libraries, missing lockfile, parallel pip + poetry, no dev group, bare `poetry update`, Poetry in the final Docker stage, broad Python constraint. | ~1200 |
| `content/04-procedure.xml` | medium | Steps: poetry init → PEP 621 → dev group → test/docs groups → lock → CI wiring → multi-stage Docker → hooks → publish. | ~1200 |
| `content/06-decision-tree.xml` | essential | Tree: Poetry mandated (vs uv)? → CI able to carry it? → PEP 621 + lockfile present? Routes to full / partial / skip. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-poetry` | haiku | Template fill. |
| `migrate-pep621` | sonnet | Per-section rewrite from [tool.poetry] to [project] with judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | PEP 621 + [tool.poetry] config: dependencies, dev-group, build-system. |
| `templates/Dockerfile` | Multi-stage build — builder runs `poetry export`, final stage runs `pip install`; no Poetry in production. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-poetry-setup.py` | Check pyproject has [project] (PEP 621), lockfile committed, dev group separate, virtualenvs.in-project=true, tight Python pin, `--sync` in CI, no `poetry install` in the final Dockerfile stage. | Pre-commit and on lockfile change. |

## Related

- [[python-modern-2026]]
- [[python-code-quality]]

## Decision tree

The tree at content/06-decision-tree.xml decides Poetry vs uv migration, library vs app constraint resolution, and dev-group composition. Walk it before any pyproject edit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pyproject.toml`

```toml
[project]
name = "demo"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[tool.poetry]
package-mode = false

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
ruff = "^0.7"
mypy = "^1.11"

[tool.poetry]
virtualenvs = { in-project = true }

[build-system]
requires = ["poetry-core>=2.0"]
build-backend = "poetry.core.masonry.api"
```
