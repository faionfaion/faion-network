# Python Type Hints (Modern 3.12+)

## Summary

Comprehensive type annotation guide for Python 3.12+ covering PEP 695 type parameter syntax, PEP 604 union syntax, TypedDict, Protocol, TypeIs vs TypeGuard, and gradual rollout strategy. Core rules: one union style per project (`X | None`, ban `Optional` via ruff `UP007`); annotate the boundary first (HTTP I/O, queue payloads, DB results), then services, then internals; never silence with bare `# type: ignore`.

## Why

Type annotations at API boundaries catch shape mismatches before runtime and give LLMs accurate generation context. A file-by-file strict rollout (add module to mypy allowlist when green) is more effective than a repo-wide attempt — the latter produces 1000+ errors and freezes progress.

## When To Use

- Adding type hints file-by-file with strict mode on touched files only.
- Annotating public API surfaces: service signatures, route handlers, queue consumers.
- Modelling cross-boundary data shapes with `TypedDict` (cheap) or Pydantic (validating).
- Defining structural inter-module contracts without forcing inheritance via `Protocol`.
- CI gate: type-check files changed in a PR; block regressions on already-typed modules.
- Migrating `typing.List`/`typing.Optional` to PEP 585/PEP 604 via `ruff --select UP --fix`.

## When NOT To Use

- One-off scripts under ~100 lines — mypy/pyright setup costs more than it returns.
- Heavy metaprogramming (decorators that mutate signatures, `__getattr__` proxies) — isolate behind `Any` or `cast`.
- Codebases pinned to Python 3.8 — use `typing_extensions` only as a last resort.
- Pure Pydantic-only domains — adding parallel `TypedDict` creates two sources of truth.
- Generated migrations — exclude in mypy config; no signal.

## Content

| File | What's inside |
|------|---------------|
| `content/01-syntax-by-version.xml` | Feature/version matrix; PEP 695 generics (3.12+); `type` alias statement; TypedDict evolution. |
| `content/02-protocols-typeddict.xml` | Protocol vs ABC; `@runtime_checkable` when to use; TypedDict `NotRequired`/`ReadOnly`; `Literal` + `assert_never`. |
| `content/03-rollout-strategy.xml` | File-by-file mypy adoption; incremental CI gate; error-class priority order. |
| `content/04-antipatterns.xml` | `Optional` mixing, `from __future__ import annotations` + Pydantic v1, `Generic[T]` no-op, bare `# type: ignore`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/typecheck-touched.sh` | Strict mypy on changed files only — CI/pre-push script. |
| `templates/precommit-mypy.yaml` | `.pre-commit-config.yaml` hook running `typecheck-touched.sh` on pre-push. |
