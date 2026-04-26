# Python Type Hints

## Summary

Modern Python typing (3.9+ generics, PEP 604 `X | None` unions, `TypedDict`, `Protocol`, `TypeVar`
with `bound=`) plus strict `mypy` configuration. Type public interfaces first; use `Protocol` for
structural contracts, `TypedDict` for dict-shaped payloads, and `TypeGuard` for narrowing.

## Why

Type hints enable static analysis, IDE completions, and self-documenting APIs without runtime cost.
`mypy --strict` on changed files (not the whole repo) catches regressions early. Using the wrong
union syntax or mixing `Optional[X]` with `X | None` in one codebase degrades readability and
triggers ruff `UP007` failures. Protocol avoids ABC inheritance coupling across package boundaries.

## When To Use

- Adding types to an untyped file — annotate public signatures first, then service-layer seams
- Public API surfaces: route handlers, service functions, library exports
- Complex data shapes crossing boundaries: request/response bodies, queue payloads, cache values
- Defining structural contracts between modules without inheritance (`Protocol`)
- CI gate to prevent type regressions on PRs touching typed modules

## When NOT To Use

- One-off scripts under ~100 lines where `mypy` setup costs more than it saves
- Dynamic metaprogramming (decorators that mutate signatures, `__getattr__` proxies) — types fight you
- Hot import paths where `typing.get_type_hints()` resolution at import time matters
- Code that must run on Python 3.8 — methodology assumes 3.9+ (`list[int]`) and 3.10+ (`X | Y`)
- Codebases standardized on Pydantic models — avoid parallel `TypedDict` definitions

## Content

| File | What's inside |
|------|---------------|
| `content/01-basic-types.xml` | Variable annotations, function signatures, `X | None`, collections syntax |
| `content/02-advanced-types.xml` | `Generic[T]`, `Protocol`, `TypedDict`, `TypeGuard`, `TypeAlias`, `Callable` |
| `content/03-mypy-config.xml` | `[tool.mypy]` strict setup, per-module overrides, incremental adoption workflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/mypy.toml` | `[tool.mypy]` strict block with test + migration overrides |
| `templates/typecheck-touched.sh` | Run `mypy --strict` on git-diff changed files only (CI incremental gate) |
