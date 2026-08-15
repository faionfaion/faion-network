# Python Type Hints

## Summary

**One-sentence:** Configures modern Python typing (PEP 604 unions, PEP 695 generics, TypedDict, Protocol) plus mypy --strict CI gate that only runs on changed files.

**One-paragraph:** Old typing syntax (`Optional[X]`, `List[T]`, `Dict[K,V]`) mixed with modern `X | None` and `list[T]` in the same repo produces ruff UP007 noise and confuses readers. Running `mypy --strict` repo-wide on day 1 produces thousands of errors and freezes adoption. This methodology fixes both: it standardises on PEP 604 + PEP 695 syntax via ruff auto-fix, runs the checker (mypy or pyright) strict at the boundary with named per-module relaxations only, requires `# type: ignore[code]` with a specific error code (never bare), bans `Any` in new code in favour of concrete types / `Protocol` / `object`, uses `Protocol` over ABC for cross-package contracts, picks `TypedDict` or a frozen dataclass for cache/queue payloads and `Pydantic` v2 at every IO boundary — HTTP body, queue message, external row — but never inside a hot loop and never as a second definition of a shape that already has one, and gates CI with `mypy --strict $(git diff --name-only)` so historical untyped modules do not block new work. Output is a `pyproject.toml` checker block + a `typecheck-touched.sh` CI script.

**Ефективно для:**

- Зрілий Python-репо без типів: поступова міграція по файлу за раз, без big-bang ремонту.
- Командна робота на Pydantic+FastAPI: межі типізовані строго, internals — за потреби.
- AI-loop генерації коду: чітка межа `mypy --strict` ловить регрессії, які агент може випадково внести.
- Бібліотеки (PyPI-пакети) — публічний API типізується першим, internal helpers потім.
- Типізація IO-меж (HTTP, черга, DB) через Pydantic v2 — сирі dict'и перетворюються на перевірені контракти.

## Applies If (ALL must hold)

- Python 3.9+ codebase (3.10+ for `X | Y` unions natively, 3.12+ for PEP 695 generics).
- Public API surface exists: route handlers, service functions, library exports — boundaries worth typing first.
- CI runs on every PR and can execute `mypy` against changed files.

## Skip If (ANY kills it)

- One-off scripts under ~100 lines, and exploratory notebooks — setup cost exceeds value.
- Hot loops where Pydantic validation overhead dominates — use frozen dataclasses internally instead.
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
| `content/01-core-rules.xml` | essential | 10 testable rules: pep604-only, pep695-type-params, annotate-boundary, strict-at-boundary, no-bare-ignore, protocol-over-abc, typeddict-vs-pydantic, pydantic-at-io, no-bare-any, no-strict-on-day-1 | 1700 |
| `content/02-output-contract.xml` | essential | JSON Schema for typed-module spec + checker-config validation + the four boolean gates | 1200 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: future-annotations-pydantic-v1, bare-type-ignore, protocol-without-runtime-checkable, any-everywhere, untyped-public-api, pydantic-in-hot-loop, mixed-union-syntax | 1100 |
| `content/04-procedure.xml` | essential | 7-step file-by-file adoption procedure incl. IO-boundary typing and Any elimination | 1100 |
| `content/05-examples.xml` | optional | One worked example: untyped service module → typed + CI green | 900 |
| `content/06-decision-tree.xml` | essential | Routing: python version → adoption mode → checker (mypy / pyright), plus per-data-shape branches (Pydantic / dataclass / PEP 695 / object) | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_python_version` | haiku | Lockfile / pyproject parse; deterministic. |
| `annotate_signatures` | sonnet | Per-file annotation needs source context but is mechanical. |
| `pick_protocol_or_abc` | opus | Cross-module design call; needs whole-codebase reasoning. |
| `write_mypy_config` | haiku | Filling a known template. |
| `extract_mypy_errors` | haiku | Parsing stderr to per-file error list. |
| `audit_any_leaks` | haiku | Grep `Any` usage and `# type: ignore` without a reason comment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mypy.toml` | `[tool.mypy]` strict block with test + migration overrides |
| `templates/pyright.toml` | `[tool.pyright]` strict block, the `checker = pyright` counterpart to `mypy.toml` |
| `templates/typecheck-touched.sh` | CI script: run `mypy --strict` only on `git diff` changed `.py` files |
| `templates/precommit-mypy.yaml` | Pre-commit config: ruff on commit, strict mypy on push |
| `templates/pydantic-schema.py` | Pydantic v2 BaseModel with `model_config` and validators, for the IO boundary |
| `templates/typed-service.py` | Service function fully typed with PEP 695 generics |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-type-hints.py` | Validate a typed-module spec JSON against the schema | After spec generation, before PR merge |

## Related

- [[code-review-process]] — the mypy gate runs inside the review process.
- [[code-coverage]] — type coverage + line coverage together are stronger than either alone.
- [[python-basics]] — built-in generics and `X | None` idioms.
- [[python-modern-2026]] — PEP 695 type parameters.
- [[python-code-quality]] — ruff rules that enforce these conventions.
- [[python-fastapi]] — the framework where the Pydantic IO boundary lands most often.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on Python version (3.9 / 3.10 / 3.11 / 3.12+) → checker choice (mypy / pyright) → adoption mode (greenfield strict / legacy diff-only). Greenfield gets `strict = true` globally; legacy gets `disallow_untyped_defs` per-file via `files = [...]` allowlist that grows on each PR. All leaves reference rules from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/mypy.toml`

```toml
# Paste under [tool] in pyproject.toml.
# Adjust python_version and per-module overrides as needed.

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
warn_redundant_casts = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
strict = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true
```

### `templates/typecheck-touched.sh`

```bash
#!/usr/bin/env bash
# scripts/typecheck-touched.sh
# Run mypy --strict only on Python files changed vs base branch.
# Usage: bash scripts/typecheck-touched.sh [base-ref]
# Exits 0 if no files changed or all pass.
set -euo pipefail

BASE_REF="${1:-origin/main}"

mapfile -t files < <(
  git diff --name-only --diff-filter=AM "$BASE_REF" -- '*.py' \
    | grep -v -E '^(migrations/|tests/fixtures/|conftest\.py$)'
)

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No Python files changed."
  exit 0
fi

echo "Typechecking ${#files[@]} file(s) with mypy --strict..."
mypy --strict "${files[@]}"
```

### `templates/pyright.toml`

```toml
# purpose: [tool.pyright] strict block with test + migration overrides
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

# Paste under [tool] in pyproject.toml when `checker = "pyright"`.
# The mypy equivalent is templates/mypy.toml — pick one checker per repo,
# never run both gates on the same files.
#
# Strict at the boundary; relaxation is per-module and named, never global.
# See content/01-core-rules.xml#strict-at-boundary.

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
include = ["src"]

# Legacy modules not yet migrated. Delete an entry as its files go green —
# the list is the migration backlog, so keep it short and visible in review.
exclude = ["**/migrations", "**/node_modules"]

reportMissingTypeStubs = "error"
reportUnknownParameterType = "error"
reportUnknownMemberType = "error"
reportUnnecessaryTypeIgnoreComment = "error"
reportPrivateUsage = "warning"

# `Any` is a last resort (content/01-core-rules.xml#no-bare-any):
# surface every explicit one rather than letting it spread silently.
reportAny = "warning"

# Tests may stay untyped while the source tree migrates.
[[tool.pyright.executionEnvironments]]
root = "tests"
reportUnknownParameterType = "none"
reportMissingParameterType = "none"
```

### `templates/precommit-mypy.yaml`

```yaml
# purpose: Pre-commit hook config for mypy strict
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/01-core-rules.xml
# token-budget-impact: small
# .pre-commit-config.yaml snippet — add to existing pre-commit config
# Runs strict mypy on changed files at pre-push stage (not pre-commit)
# to keep commit speed fast while still catching type regressions.

repos:
  # ─── Ruff (fast, runs on every commit) ───────────────────────────────────
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
        stages: [pre-commit]
      - id: ruff-format
        stages: [pre-commit]

  # ─── mypy (slower, runs only on push) ────────────────────────────────────
  - repo: local
    hooks:
      - id: mypy-touched
        name: mypy strict (changed files)
        entry: bash scripts/typecheck-touched.sh
        language: system
        stages: [pre-push]
        pass_filenames: false
        # Env override for base branch if not main:
        # env:
        #   BASE_BRANCH: develop
```

### `templates/pydantic-schema.py`

```python
"""
purpose: Pydantic v2 BaseModel with model_config and validators.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
```

### `templates/typed-service.py`

```python
"""
purpose: Service function fully typed with PEP 695 generics.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Item:
    id: int
    name: str


def find_by_id[T](items: list[T], pred) -> T | None:
    for item in items:
        if pred(item):
            return item
    return None


def first_with_name(items: list[Item], name: str) -> Item | None:
    return find_by_id(items, lambda i: i.name == name)
```
