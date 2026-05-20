---
slug: python-type-hints
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Python type hints and static type checking with mypy, pyright, and pydantic: catch bugs at development time, enable IDE autocomplete, and improve code readability.
content_id: "d0b8493323c48bba"
tags: [type-hints, mypy, static-typing, python, pydantic]
---
# Python Type Hints

## Summary

**One-sentence:** Python type hints and static type checking with mypy, pyright, and pydantic: catch bugs at development time, enable IDE autocomplete, and improve code readability.

**One-paragraph:** Python type hints and static type checking with mypy, pyright, and pydantic: catch bugs at development time, enable IDE autocomplete, and improve code readability.

## Applies If (ALL must hold)

- Python 3.5+ projects where IDE autocomplete and static analysis improve productivity.
- Teams or codebases where runtime type errors cause production bugs.
- APIs exposed to multiple callers (libraries, microservices) where contract clarity matters.
- Projects using Pydantic for request/response validation in APIs.
- Refactoring legacy Python code to improve maintainability.

## Skip If (ANY kills it)

- Throwaway scripts or prototypes where typing overhead exceeds value.
- Python 3.4 or older codebases (upgrade Python version first).
- Teams not yet familiar with static typing; learning curve can slow initial development.
- Simple scripts where runtime duck typing is sufficient and failure modes are obvious.

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
