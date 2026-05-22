---
slug: python-type-hints
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern Python typing (3.
content_id: "d0b8493323c48bba"
tags: [python, typing, mypy, type-safety, static-analysis]
---
# Python Type Hints

## Summary

**One-sentence:** Modern Python typing (3.

**One-paragraph:** Modern Python typing (3.9+ generics, PEP 604 unions, TypedDict, Protocol) plus mypy strict configuration. Type public interfaces first.

## Applies If (ALL must hold)

- Adding types to an untyped file — annotate public signatures first, then service-layer seams.
- Public API surfaces: route handlers, service functions, library exports.
- Complex data shapes crossing boundaries: request/response bodies, queue payloads, cache values.
- Defining structural contracts between modules without inheritance (Protocol).
- CI gate to prevent type regressions on PRs touching typed modules.
- Adding type hints to an untyped Python codebase, file-by-file (mypy strict on touched files only).

## Skip If (ANY kills it)

- One-off scripts under ~100 lines where mypy setup costs more than it saves.
- Dynamic metaprogramming (decorators that mutate signatures, __getattr__ proxies) — types fight you.
- Hot import paths where typing.get_type_hints() resolution at import time matters.
- Code that must run on Python 3.8 — methodology assumes 3.9+ (list[int]) and 3.10+ (X | Y).
- Codebases standardized on Pydantic models — avoid parallel TypedDict definitions.
- Migrating dynamic metaprogramming (decorators that mutate signatures, __getattr__ proxies) — types fight you; use # type: ignore[attr-defined] sparingly or skip.

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
