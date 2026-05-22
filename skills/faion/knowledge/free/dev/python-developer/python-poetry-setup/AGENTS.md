---
slug: python-poetry-setup
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern Python dependency management with Poetry 2.
content_id: "29e568def229e20c"
tags: [poetry, dependencies, packaging, python, pep-621]
---
# Poetry Project Setup

## Summary

**One-sentence:** Modern Python dependency management with Poetry 2.

**One-paragraph:** Modern Python dependency management with Poetry 2.x: deterministic lock files, virtual environment management, PEP 621 metadata, and reproducible builds.

## Applies If (ALL must hold)

- New Python project expected to live for years and be published or vendored.
- Migrating Poetry 1.x to Poetry 2.x with PEP 621 layout.
- Adding/removing dependencies on established repo with CI/CD validation.
- Splitting deps into groups (dev, test, docs).
- Producing deterministic build artifacts (wheel/sdist) for PyPI or internal indexes.
- Complex dependency trees requiring deterministic resolution.
- Reproducible builds across dev, CI, and production.

## Skip If (ANY kills it)

- One-shot scripts or throwaway experiments.
- CI hot paths where install speed is critical (use uv instead).
- Memory-constrained environments (<512 MB).
- Repos already using uv/pdm/hatch.
- Cross-language monorepos with Bazel/Pants build graphs.

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
