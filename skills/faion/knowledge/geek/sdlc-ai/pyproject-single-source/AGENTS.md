---
slug: pyproject-single-source
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Concentrate every Python tool's configuration in `pyproject.
content_id: "f3c79893b83d9f32"
tags: [pyproject, python, configuration, tooling, ruff]
---
# `pyproject.toml` as the Single Source of Configuration

## Summary

**One-sentence:** Concentrate every Python tool's configuration in `pyproject.

**One-paragraph:** Concentrate every Python tool's configuration in `pyproject.toml` — `[build-system]`, `[project]` (PEP 621), `[tool.uv]`, `[tool.ruff]`, type-checker (`[tool.ty]` or `[tool.mypy]`), `[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.bandit]`, `[tool.mutmut]`. Forbid `setup.py`, `setup.cfg`, `tox.ini`, `.flake8`, `requirements*.txt` for Python tooling on new code. One file = one place AI agents have to read, parse, and mutate.

## Applies If (ALL must hold)

- Every new Python project, library, service, or CLI.
- Migrating any project where `setup.cfg`, `tox.ini`, or `.flake8` still exists alongside `pyproject.toml`.
- Tooling-heavy repos with ruff + pytest + coverage + bandit + mutmut all configured.
- Any repo touched by a coding agent — fewer files to discover means less drift.

## Skip If (ANY kills it)

- Build systems with truly exotic native-extension logic where `setup.py` carries imperative build steps that TOML cannot express — keep `setup.py` minimal and put metadata in `[project]`.
- Vendored read-only mirrors of upstream projects whose layout you cannot change.
- `tox` users who deliberately keep `tox.ini` for parallelism config that pyproject's `[tool.tox]` does not yet support — the trade-off is local; document it.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
