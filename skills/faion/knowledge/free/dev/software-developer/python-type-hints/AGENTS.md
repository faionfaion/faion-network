---
slug: python-type-hints
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a typed-module spec (modern X|None unions, Protocol/TypedDict, mypy-strict config) and a CI gate running strict checks only on touched files.
content_id: "d0b8493323c48bba"
complexity: medium
produces: spec
est_tokens: 4400
tags: [python, typing, mypy, type-safety, static-analysis, pep-604, pep-695]
---
# Python Type Hints

## Summary

**One-sentence:** Configures modern Python typing (PEP 604 unions, PEP 695 generics, TypedDict, Protocol) plus mypy --strict CI gate that only runs on changed files.

**One-paragraph:** Old typing syntax (`Optional[X]`, `List[T]`, `Dict[K,V]`) mixed with modern `X | None` and `list[T]` in the same repo produces ruff UP007 noise and confuses readers. Running `mypy --strict` repo-wide on day 1 produces thousands of errors and freezes adoption. This methodology fixes both: it standardises on PEP 604 + PEP 695 syntax via ruff auto-fix, requires `# type: ignore[code]` with a specific error code (never bare), uses `Protocol` over ABC for cross-package contracts, picks `TypedDict` for cache/queue payloads and `Pydantic` for HTTP bodies (never both for the same shape), and gates CI with `mypy --strict $(git diff --name-only)` so historical untyped modules do not block new work. Output is a `pyproject.toml` mypy block + a `typecheck-touched.sh` CI script.

**Ефективно для:**

- Зрілий Python-репо без типів: поступова міграція по файлу за раз, без big-bang ремонту.
- Командна робота на Pydantic+FastAPI: межі типізовані строго, internals — за потреби.
- AI-loop генерації коду: чітка межа `mypy --strict` ловить регрессії, які агент може випадково внести.
- Бібліотеки (PyPI-пакети) — публічний API типізується першим, internal helpers потім.

## Applies If (ALL must hold)

- Python 3.9+ codebase (3.10+ for `X | Y` unions natively, 3.12+ for PEP 695 generics).
- Public API surface exists: route handlers, service functions, library exports — boundaries worth typing first.
- CI runs on every PR and can execute `mypy` against changed files.

## Skip If (ANY kills it)

- One-off scripts under ~100 lines — mypy setup cost exceeds value.
- Heavy dynamic metaprogramming (decorators mutating signatures, `__getattr__` proxies) — types fight the code, use `# type: ignore[attr-defined]` sparingly or skip.
- Hot import paths where `typing.get_type_hints()` resolution time matters.
- Python 3.8 — methodology assumes `list[int]` (3.9+) and `X | Y` (3.10+).
- Codebase already standardised on Pydantic models — do not maintain parallel `TypedDict` definitions for the same data shape.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `pyproject.toml` | TOML | repo root |
| CI workflow file | YAML | `.github/workflows/` |
| Public-API manifest | list of module paths | `AGENTS.md` or `pyproject.toml [tool.faion]` |
| Python version | `>=3.9` | `pyproject.toml [project] requires-python` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Foundational. May feed into `[[code-review-process]]` once the CI gate exists. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: pep604-only, annotate-boundary, no-bare-ignore, protocol-over-abc, typeddict-vs-pydantic, no-strict-on-day-1 | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for typed-module spec + mypy-config validation | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: future-annotations-pydantic-v1, bare-type-ignore, protocol-without-runtime-checkable, mixed-union-syntax | 700 |
| `content/04-procedure.xml` | essential | 5-step file-by-file adoption procedure | 800 |
| `content/05-examples.xml` | optional | One worked example: untyped service module → typed + CI green | 900 |
| `content/06-decision-tree.xml` | essential | Routing: python version → adoption mode → checker (mypy / pyright) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_python_version` | haiku | Lockfile / pyproject parse; deterministic. |
| `annotate_signatures` | sonnet | Per-file annotation needs source context but is mechanical. |
| `pick_protocol_or_abc` | opus | Cross-module design call; needs whole-codebase reasoning. |
| `write_mypy_config` | haiku | Filling a known template. |
| `extract_mypy_errors` | haiku | Parsing stderr to per-file error list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mypy.toml` | `[tool.mypy]` strict block with test + migration overrides |
| `templates/typecheck-touched.sh` | CI script: run `mypy --strict` only on `git diff` changed `.py` files |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-type-hints.py` | Validate a typed-module spec JSON against the schema | After spec generation, before PR merge |

## Related

- [[code-review-process]] — the mypy gate runs inside the review process.
- [[code-coverage]] — type coverage + line coverage together are stronger than either alone.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on Python version (3.9 / 3.10 / 3.11 / 3.12+) → checker choice (mypy / pyright) → adoption mode (greenfield strict / legacy diff-only). Greenfield gets `strict = true` globally; legacy gets `disallow_untyped_defs` per-file via `files = [...]` allowlist that grows on each PR. All leaves reference rules from `01-core-rules.xml`.
