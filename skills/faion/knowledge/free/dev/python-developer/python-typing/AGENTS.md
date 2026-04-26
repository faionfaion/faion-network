# Python Type Hints and Static Typing

## Summary

Rules for adding and maintaining type annotations in Python 3.10+ codebases using mypy (CI) and pyright (IDE). Core rules: use built-in generics (`list[int]`, `X | None`), use PEP 695 syntax (`class Foo[T]:`) on 3.12+ floors, never add bare `# type: ignore` without a rule code, never silence with `cast()` when a narrowing guard works.

## Why

Type annotations catch shape mismatches before runtime, make IDE navigation reliable, and give LLMs accurate context for code generation. Without a strict discipline (`# type: ignore[code]` with justification, no stray `Any`), the annotation coverage erodes silently — future errors are hidden rather than flagged.

## When To Use

- Adding type hints to an untyped or partially-typed module (run `mypy --strict` to find gaps).
- Migrating `from typing import List, Dict, Optional, Union` to 3.10+ built-ins.
- Migrating to PEP 695 generic syntax (`class Repo[T]:`) from legacy `TypeVar`/`Generic`.
- Designing a public API surface with Protocol-based duck typing.
- Hardening a payload boundary with `TypedDict` + `Required`/`NotRequired`.
- CI quality gate: `mypy --strict` blocking PRs that introduce `Any`.

## When NOT To Use

- Throwaway scripts and one-off notebooks — setup cost exceeds benefit.
- Codebases supporting Python &lt;3.10 — `X | Y` syntax breaks on 3.9.
- Cython/PyO3 extension modules — types live in `.pyi` stubs.
- Bridging dynamic libraries without stubs (legacy ML libs) — fighting `Untyped` errors yields no signal.

## Content

| File | What's inside |
|------|---------------|
| `content/01-annotation-rules.xml` | Built-in generics rule; PEP 695 generics; `X | None` vs Optional; TypedDict; Protocol. |
| `content/02-checker-config.xml` | mypy strict config; pyright config; Django-stubs wiring; ruff ANN/TCH/UP rules. |
| `content/03-antipatterns.xml` | `Any` overuse, bare `# type: ignore`, `cast()` misuse, `@runtime_checkable` on hot paths, mixed union styles. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mypy-config.toml` | `[tool.mypy]` strict block with Django-stubs override and test/migrations exclusions. |
| `templates/no-new-any.sh` | Pre-commit script: fail if a touched `.py` file introduces a new `Any` annotation. |
