---
slug: python-basics
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Foundational Python 3.12+ patterns: built-in generics, EAFP, dataclasses, pathlib, uv + ruff + mypy.
content_id: "16e10c3c6f88939e"
complexity: light
produces: code
est_tokens: 2700
tags: [python, data-structures, functions, error-handling, type-hints]
---
# Python Basics

## Summary

**One-sentence:** Foundational Python 3.12+ patterns: built-in generics, EAFP, dataclasses, pathlib, uv + ruff + mypy.

**One-paragraph:** Foundational Python patterns for 3.12+ projects: data structures, control flow, functions, OOP, error handling, file I/O, and tooling (uv, ruff, mypy). Use built-in generic syntax (list[int], dict[str, int], X | None); prefer uv for environment and dependency management; use ruff for both lint and format.

**Ефективно для:** розробника, який починає новий 3.12+ проєкт або проводить ревʼю фундаменту — закриває петлю між сучасним синтаксисом і інструментарієм uv/ruff/mypy.

## Applies If (ALL must hold)

- Bootstrapping a fresh Python 3.12+ project (pyproject.toml, uv, ruff, mypy, pytest).
- Code review where the issue is fundamentals: mutable defaults, EAFP misuse, legacy typing imports.
- Onboarding developers from older Python or other languages.
- Migrating 3.9/3.10 syntax to 3.12+ built-in generics and X | None.

## Skip If (ANY kills it)

- Production async services — load python-async instead.
- Framework-specific work — load python-fastapi or django-* methodologies.
- Type-system deep dives — load python-type-hints.
- Tooling/quality setup — load python-code-quality.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python 3.12+ interpreter | binary | uv install |
| Empty repo or pyproject.toml | TOML | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | Self-contained foundational methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: built-in generics, X | None union, EAFP over LBYL, no mutable defaults, pathlib over os.path, dataclasses for data containers. | ~900 |
| `content/02-output-contract.xml` | essential | Shape: 3.12+ syntax only, no typing.List/Optional/Union, no f-string {var=} debug in prod, dataclasses with frozen=True for immutable, with/context-managers for resources. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: mutable default args, LBYL on hasattr, broad except Exception, legacy typing imports, dict instead of dataclass. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: container = list of plain items? → list. Mixed types? → dataclass. Hashable lookup? → dict. Need set ops? → set. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-project` | haiku | Boilerplate from template. |
| `upgrade-syntax` | sonnet | 3.9/3.10 → 3.12+ rewrite with judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dataclass.py` | Frozen + slotted dataclass skeleton with __post_init__ validation. |
| `templates/pyproject.toml.fragment` | Minimal pyproject for 3.12+: build-system, requires-python, ruff target-version, mypy python_version. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-basics.py` | Lint a module for: typing.List/Optional/Union imports, mutable default args, bare except. | Pre-commit. |

## Related

- [[python-modern-2026]]
- [[python-type-hints]]
- [[python-code-quality]]

## Decision tree

The tree at content/06-decision-tree.xml picks the right primitive (list / dict / set / dataclass / NamedTuple) and the right error pattern (EAFP vs LBYL) for the case at hand. Walk it any time you reach for typing.* imports or hasattr.
