---
slug: python-poetry-setup
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Poetry is the standard for Python dependency management: deterministic builds via poetry.
content_id: "29e568def229e20c"
tags: [python, poetry, dependencies, lockfile, reproducible-builds]
---
# Poetry Project Setup

## Summary

**One-sentence:** Poetry is the standard for Python dependency management: deterministic builds via poetry.

**One-paragraph:** Poetry is the standard for Python dependency management: deterministic builds via poetry.lock, isolated virtual environments, and streamlined PyPI publishing. Always commit poetry.lock; always use --sync in CI; never mix pip and poetry in the same project.

## Applies If (ALL must hold)

- Starting any new Python project (service, library, CLI).
- Managing complex dependency trees requiring reproducible builds.
- Publishing packages to PyPI or private registries.
- Agent-managed repos where dependency changes must go through --dry-run + human approval.
- Bootstrapping a new Python service or library that will be agent-managed (Claude Code as primary contributor).
- Locking dependency closures so a CI agent and a local agent produce byte-identical environments.
- Wrapping a Django/FastAPI repo where you want poetry add / poetry remove to be the only mutation surface for pyproject.toml.
- Publishing a wheel to PyPI/private index with token-based auth (Poetry handles upload state without manual twine).

## Skip If (ANY kills it)

- Throwaway scripts or notebooks — uv pip install or pipx run is faster.
- Projects already standardized on pip-tools, uv, or pdm — don't migrate for novelty.
- Docker images built from requirements.txt with no solver runtime needed — export from Poetry at build time and use pip in the final stage.
- Monorepos with Pants/Bazel workspace tooling — Poetry has no first-class workspace concept.
- Containers built from requirements.txt with no need for solver runtime — keep pip; export from Poetry only at build time.
- Monorepos with native workspace tooling (Pants, Bazel) — Poetry has no first-class workspace concept (until 2.0 plugins).

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

- parent skill: `free/dev/software-developer/`
