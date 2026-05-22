---
slug: python-poetry-setup
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Poetry 2.x project setup with PEP 621, lockfile-first reproducibility, plugin ecosystem.
content_id: "29e568def229e20c"
complexity: medium
produces: config
est_tokens: 3500
tags: [poetry, dependencies, packaging, python, pep-621]
---
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
| `content/01-core-rules.xml` | essential | 5 rules: PEP 621 layout, lockfile committed, separate dev group, no caret on libs, poetry env via virtualenvs.in-project. | ~900 |
| `content/02-output-contract.xml` | essential | Shape: pyproject.toml [project] + [tool.poetry] + poetry.lock + .venv/. Forbidden: requirements.txt + poetry.lock both, untracked lockfile. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: caret in libraries, missing lockfile, parallel pip + poetry, no dev group. | ~700 |
| `content/04-procedure.xml` | medium | Steps: poetry init → migrate to PEP 621 → add dev group → lock → install hooks → publish. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: library? → no caret. App? → caret. Need uv speed? → migrate. Else: stay Poetry. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-poetry` | haiku | Template fill. |
| `migrate-pep621` | sonnet | Per-section rewrite from [tool.poetry] to [project] with judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | PEP 621 + [tool.poetry] config: dependencies, dev-group, build-system. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-poetry-setup.py` | Check pyproject has [project] (PEP 621), lockfile committed, dev group separate, virtualenvs.in-project=true. | Pre-commit and on lockfile change. |

## Related

- [[python-modern-2026]]
- [[python-code-quality]]

## Decision tree

The tree at content/06-decision-tree.xml decides Poetry vs uv migration, library vs app constraint resolution, and dev-group composition. Walk it before any pyproject edit.
