---
slug: python-basics
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Foundational Python patterns for 3.
content_id: "16e10c3c6f88939e"
tags: [python, data-structures, functions, error-handling, type-hints]
---
# Python Basics

## Summary

**One-sentence:** Foundational Python patterns for 3.

**One-paragraph:** Foundational Python patterns for 3.12+ projects: data structures, control flow, functions, OOP, error handling, file I/O, and tooling (uv, ruff, mypy). Core rule: use built-in generic syntax (list[int], dict[str, int], X | None), prefer uv for all environment and dependency management, and use ruff for both lint and format.

## Applies If (ALL must hold)

- Bootstrapping a fresh Python 3.12+ project (pyproject.toml, uv, ruff, mypy, pytest).
- Code review where the issue is fundamentals: mutable defaults, EAFP misuse, legacy typing imports.
- Refactoring legacy 3.7/3.8 code to 3.12+ idioms.
- Generating idiomatic examples or onboarding content.
- Style/idiom gate in CI (ruff UP, B, E, F rule sets).

## Skip If (ANY kills it)

- Inside a domain-specific feature (Django model, FastAPI route) — load the domain methodology; this overview is too generic.
- Performance optimization — route to python-modern-2026/ or specialized profiling tooling.
- Type-system depth (generics, ParamSpec, Protocol) — route to python-typing/.
- Async patterns — route to python-async/.
- Testing strategies — route to a pytest methodology.

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
