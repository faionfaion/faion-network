# Modern Python 2026

## Summary

Python 3.12/3.13/3.14 feature guide and tooling stack (uv, ruff, hatchling, pyright). Covers PEP 695 generics, PEP 701 f-strings, free-threaded mode (3.13t/3.14), t-strings (3.14 only), deferred annotations, and uv-based project bootstrap. Core rule: pin one Python version per repo via `.python-version`; keep `requires-python`, ruff `target-version`, and mypy `python_version` in sync.

## Why

Syntax from 3.14 (t-strings, lazy imports) pasted into a 3.12 project causes `SyntaxError` at import time — a silent failure that only manifests in CI or production. Consistent tooling alignment (uv + ruff + hatchling) eliminates the "works on my machine" class of environment bugs and cuts install time by 10-100x.

## When To Use

- Bootstrapping a new Python project (`uv init`, `pyproject.toml`, ruff + mypy + pytest).
- Migrating 3.10/3.11 code to 3.12+: built-in generics, PEP 695 type parameters, modern f-strings.
- Switching from pip/poetry/venv to uv.
- Replacing Black + Flake8 + isort + pyupgrade with a single Ruff config.
- Setting up CI/CD with lockfile-aware caching and pinned Python versions.

## When NOT To Use

- Locked legacy environments (Python 3.8, RHEL system Python, vendored interpreters).
- Production free-threaded mode without a thread-safety audit of all C extensions (3.13 experimental, 3.14 stabilizes).
- Pure data-science notebooks where conda/mamba is entrenched.
- Existing healthy poetry/PDM project — switching costs more than the benefit.

## Content

| File | What's inside |
|------|---------------|
| `content/01-version-features.xml` | 3.12 (PEP 695, PEP 701, perf), 3.13 (free-threading, JIT, TypeIs), 3.14 (t-strings, PEP 649) with version floors. |
| `content/02-tooling-stack.xml` | uv commands, ruff config, pyright/mypy alignment, hatchling build backend. |
| `content/03-migration-path.xml` | 3.10/3.11 → 3.12+: ruff UP auto-fix, TypeVar → PEP 695, f-string upgrades. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Full pyproject.toml: uv, hatchling, ruff (E F I B UP N S C4 PT), mypy strict, pytest-asyncio auto mode. |
| `templates/bootstrap.sh` | One-shot project bootstrap: uv init, add deps, pre-commit with ruff + mypy hooks. |
