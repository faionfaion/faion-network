---
slug: uv-lockfile-floor
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Standardize every Python project on Astral's `uv` for environment management, dependency resolution, lockfile, and Python version installation.
content_id: "938aa9879612057c"
tags: [uv, python, lockfile, dependency-management, reproducible-builds]
---
# uv as the Python Lockfile Floor

## Summary

**One-sentence:** Standardize every Python project on Astral's `uv` for environment management, dependency resolution, lockfile, and Python version installation.

**One-paragraph:** Standardize every Python project on Astral's `uv` for environment management, dependency resolution, lockfile, and Python version installation. The committed `uv.lock` is the single source of truth for reproducible installs; AI coding agents must invoke commands through `uv run <cmd>` (never bare `pytest` / `python`) so the right virtualenv and the right Python version are guaranteed for every tool call.

## Applies If (ALL must hold)

- Every new Python project (Python 3.10+).
- Migrating Poetry / pip-tools / requirements.txt projects when the team can switch lockfile formats.
- Multi-Python-version repos (uv installs and pins interpreter versions per project).
- Any repo where AI agents will run `pytest`, type-checkers, or scripts.

## Skip If (ANY kills it)

- Conda / scientific stacks needing CUDA, GDAL, or other binary deps from conda-forge — `pixi` handles that subset better.
- Repos pinned to legacy Python (2.7) or to a private registry that uv's resolver does not understand.
- Single-file scripts where a venv is more ceremony than the script is worth.
- Projects that must keep `requirements.txt` for an external consumer (pull request agents, security scanners) until those consumers learn `uv.lock`.

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
