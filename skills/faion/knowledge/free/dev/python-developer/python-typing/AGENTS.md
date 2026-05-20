---
slug: python-typing
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rules for adding and maintaining type annotations in Python 3.
content_id: "a18fe0acb1cd3a29"
tags: [python, typing, mypy, pep-695, static-analysis]
---
# Python Type Hints and Static Typing

## Summary

**One-sentence:** Rules for adding and maintaining type annotations in Python 3.

**One-paragraph:** Rules for adding and maintaining type annotations in Python 3.10+ codebases using mypy (CI) and pyright (IDE). Core rules: use built-in generics (list[int], X | None), use PEP 695 syntax (class Foo[T]:) on 3.12+ floors, never add bare # type: ignore without a rule code, never silence with cast() when a narrowing guard works.

## Applies If (ALL must hold)

- Adding type hints to an untyped or partially-typed module (run mypy --strict to find gaps).
- Migrating from typing import List, Dict, Optional, Union to 3.10+ built-ins.
- Migrating to PEP 695 generic syntax (class Repo[T]:) from legacy TypeVar/Generic.
- Designing a public API surface with Protocol-based duck typing.
- Hardening a payload boundary with TypedDict + Required/NotRequired.
- CI quality gate: mypy --strict blocking PRs that introduce Any.

## Skip If (ANY kills it)

- Throwaway scripts and one-off notebooks — setup cost exceeds benefit.
- Codebases supporting Python less than 3.10 — X | Y syntax breaks on 3.9.
- Cython/PyO3 extension modules — types live in .pyi stubs.
- Bridging dynamic libraries without stubs (legacy ML libs) — fighting Untyped errors yields no signal.

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
