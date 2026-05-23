# `pyproject.toml` as the Single Source of Configuration

## Summary

**One-sentence:** Concentrate every Python tool's configuration in `pyproject.toml` ([project], [tool.uv], [tool.ruff], [tool.pytest.ini_options], [tool.coverage.*], [tool.ty]/[tool.mypy], [tool.bandit], [tool.mutmut]); forbid setup.cfg / tox.ini / .flake8 / requirements*.txt on new code.

**One-paragraph:** Python projects historically scatter config across `setup.py`, `setup.cfg`, `tox.ini`, `.flake8`, `pytest.ini`, `requirements*.txt`. Each file is a separate parser, a separate format, and a separate place an AI agent must read, parse, and mutate. PEP 621 plus `[tool.*]` tables let every modern tool read from a single TOML file. This methodology produces a `pyproject.toml` artefact carrying everything plus a CI check that fails the build when legacy config files reappear.

**Ефективно для:**

- Новий Python проект, library, service, або CLI.
- Migration repo, де `setup.cfg` / `tox.ini` / `.flake8` живуть поруч з pyproject.
- Tooling-heavy repo з ruff + pytest + coverage + bandit + mutmut.
- Repo з coding agent — менше файлів = менше drift.

## Applies If (ALL must hold)

- Python project (library, service, CLI, app).
- Tools used (ruff, pytest, coverage, ty/mypy, bandit, mutmut) all support `[tool.*]` in pyproject.
- Build backend supports PEP 621 (hatchling, setuptools&gt;=64, poetry-core, pdm-backend).
- Team agrees to add a CI check that fails on legacy files.

## Skip If (ANY kills it)

- Project uses an exotic build system with imperative `setup.py` steps TOML cannot express.
- Vendored read-only mirror of upstream — you cannot change the layout.
- `tox` user who deliberately keeps `tox.ini` for parallelism config the `[tool.tox]` table does not yet support.
- Repo pins on Python &lt; 3.10 with tools that haven't migrated to `[tool.*]` tables.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| pyproject.toml | TOML | lead |
| Build backend choice | hatchling / setuptools / poetry-core / pdm-backend | lead |
| CI workflow | GitHub Actions / GitLab CI | platform |
| Legacy config inventory | list of files to remove | maintainer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-ruff-and-biome-as-default]] | Ruff config blocks live in this same pyproject.toml. |
| [[lint-precommit-floor]] | Pre-commit hook can run check-no-legacy.sh. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pyproject_draft` | sonnet | Tool-config layout needs judgement (ruff selects, pytest addopts). |
| `legacy_migrate` | haiku | Mechanical move from setup.cfg → pyproject. |
| `ci_check` | haiku | Boilerplate bash check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Full pyproject skeleton with [project] + [tool.*] tables. |
| `templates/check-no-legacy.sh` | CI script that fails on legacy Python config files. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pyproject-single-source.py` | Validate pyproject artefact has required tables + no legacy file companions. | Pre-merge of pyproject.toml |

## Related

- [[lint-ruff-and-biome-as-default]]
- [[lint-precommit-floor]]
- [[pnpm-catalogs]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (Python project? tool support? exotic build?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to consolidate config — the tree terminates either on the active rule or on `skip-this-methodology`.
