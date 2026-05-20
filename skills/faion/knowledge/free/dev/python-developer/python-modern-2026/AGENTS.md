---
slug: python-modern-2026
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Python 3.
content_id: "348d315e419eae89"
tags: [python-3.12, python-3.13, uv, ruff, pyright]
---
# Modern Python 2026

## Summary

**One-sentence:** Python 3.

**One-paragraph:** Python 3.12/3.13/3.14 feature guide and tooling stack (uv, ruff, hatchling, pyright). Covers PEP 695 generics, PEP 701 f-strings, free-threaded mode (3.13t/3.14), t-strings (3.14 only), deferred annotations, and uv-based project bootstrap. Core rule: pin one Python version per repo via .python-version; keep requires-python, ruff target-version, and mypy python_version in sync.

## Applies If (ALL must hold)

- Bootstrapping a new Python project (uv init, pyproject.toml, ruff + mypy + pytest).
- Migrating 3.10/3.11 code to 3.12+: built-in generics, PEP 695 type parameters, modern f-strings.
- Switching from pip/poetry/venv to uv.
- Replacing Black + Flake8 + isort + pyupgrade with a single Ruff config.
- Setting up CI/CD with lockfile-aware caching and pinned Python versions.

## Skip If (ANY kills it)

- Locked legacy environments (Python 3.8, RHEL system Python, vendored interpreters).
- Production free-threaded mode without a thread-safety audit of all C extensions (3.13 experimental, 3.14 stabilizes).
- Pure data-science notebooks where conda/mamba is entrenched.
- Existing healthy poetry/PDM project — switching costs more than the benefit.

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

- parent skill: `free/dev/python-developer/`
