# `pyproject.toml` as the Single Source of Configuration

## Summary

Concentrate every Python tool's configuration in `pyproject.toml` — `[build-system]`, `[project]` (PEP 621), `[tool.uv]`, `[tool.ruff]`, type-checker (`[tool.ty]` or `[tool.mypy]`), `[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.bandit]`, `[tool.mutmut]`. Forbid `setup.py`, `setup.cfg`, `tox.ini`, `.flake8`, `requirements*.txt` for Python tooling on new code. One file = one place AI agents have to read, parse, and mutate.

## Summary rule (testable)

The repo MUST contain exactly one `pyproject.toml` per package and zero of: `setup.py`, `setup.cfg`, `.flake8`, `requirements*.txt` (for first-party deps), `pytest.ini`, `tox.ini` (use `nox` or pyproject-configured `tox`), `mypy.ini`. CI verifies with a one-line check.

## Why

PEP 621 standardizes project metadata in pyproject.toml; Hatchling, setuptools, flit, and uv all consume that table directly. Splitting config into `setup.cfg` + `tox.ini` + `.flake8` + `requirements.txt` is a 2017-era pattern that produces silent inconsistencies — the agent edits one file, forgets the other, and the repo enters a half-migrated state. A single TOML file is parseable, diffable, and machine-mutable; agents reason about it more reliably than about a swarm of legacy config files.

## When To Use

- Every new Python project, library, service, or CLI.
- Migrating any project where `setup.cfg`, `tox.ini`, or `.flake8` still exists alongside `pyproject.toml`.
- Tooling-heavy repos with ruff + pytest + coverage + bandit + mutmut all configured.
- Any repo touched by a coding agent — fewer files to discover means less drift.

## When NOT To Use

- Build systems with truly exotic native-extension logic where `setup.py` carries imperative build steps that TOML cannot express — keep `setup.py` minimal and put metadata in `[project]`.
- Vendored read-only mirrors of upstream projects whose layout you cannot change.
- `tox` users who deliberately keep `tox.ini` for parallelism config that pyproject's `[tool.tox]` does not yet support — the trade-off is local; document it.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The single-file rule, the forbidden-files list, and the one-line CI check. |
| `content/02-sections.xml` | Canonical TOML sections: build-system, project, tool.uv, tool.ruff, tool.pytest, tool.coverage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Reference pyproject.toml with all common tool sections wired up. |
| `templates/check-no-legacy.sh` | One-line CI check that fails if forbidden config files exist. |
