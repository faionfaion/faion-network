# Agent Integration — Python Typing

## When to use
- Adding type hints to an untyped or partially-typed module — agent runs `mypy --strict` to find gaps and fills them.
- Refactoring `from typing import List, Dict, Optional, Union` to 3.10+ built-ins (`list`, `dict`, `X | None`, `X | Y`).
- Migrating to PEP 695 generic syntax (`class Repo[T]:`) from legacy `TypeVar`/`Generic`.
- Designing a public API surface where Protocol-based duck typing would simplify dependencies.
- Hardening a payload boundary with `TypedDict` + `Required`/`NotRequired` (e.g. webhook handlers, JSON RPC).
- CI quality gate: `mypy --strict` or `pyright --strict` blocking PRs that introduce `Any`.

## When NOT to use
- Throwaway scripts and one-off notebooks.
- Codebases supporting Python <3.10 — agents will sprinkle `X | Y` and break on 3.9.
- Cython/PyO3 extension modules — types live in `.pyi` stubs, not in source; different methodology.
- Bridging dynamic libraries that don't ship stubs (legacy ML libs) — agents will spend hours fighting `Untyped` errors.

## When to defer to a different file
- Pydantic-specific validation behavior — `python-fastapi/` has more.
- SQLAlchemy 2 typed mappings — covered in framework methodologies.
- TypedDict for Django Rest Framework serializer-replacement — see `django-api/`.

## Where it fails / limitations
- README claims "Pyright is 3-5x faster than mypy" — true on cold cache, less so on incremental. Agents quote it as a reason to drop mypy.
- "Both mypy + Pyright" recommendation for "maximum strictness" doubles CI time and produces conflicting messages on edge cases (Pyright's structural inference vs mypy's nominal-by-default). Pick one for CI.
- `ty` (Astral) is described as a real option — in 2025-2026 it's still pre-1.0 and missing features (plugin equivalents, some PEP coverage). Agents will adopt it prematurely.
- README's PEP 695 examples (`class Foo[T]:`) require Python 3.12+; agents apply them in 3.10/3.11 codebases and break syntax.
- TypedDict examples mix Python 3.11 (`NotRequired`/`Required`) and 3.13 (`ReadOnly`) without flagging the version floor. Agents emit `ReadOnly` in 3.12 and the import fails.
- Protocol section enables `@runtime_checkable` everywhere; runtime checks are slow (`isinstance` walks methods) and break on protocols with default values.
- mypy `[tool.mypy]` config in README is `strict = true` plus a list of redundant options (`warn_return_any`, etc., are already implied by strict). Agents copy as-is and the config becomes noise.
- "django-stubs" requires `django_settings_module` set; if the module path is wrong, `mypy` runs but emits subtly wrong results. Agents miss this.
- ParamSpec example assumes 3.12 generic syntax (`def logged[**P, T]`); on 3.10/3.11 you must `P = ParamSpec("P")` separately. Agents will mix.
- No mention of `cast()` overuse — agents reach for `cast` to silence errors instead of fixing the underlying type narrowing.
- No mention of `# type: ignore[<rule>]` discipline — agents add bare `# type: ignore` which hides future regressions.

## Agentic workflow
Two passes per module: (1) **type inference** — a sonnet/opus subagent reads the module + runs `mypy --strict` (or `pyright --strict`) to surface gaps, then proposes a typing diff (annotations only, no behavior change); (2) **verification** — a haiku/sonnet subagent runs the type-checker on the patched module and the test suite (behavior must be unchanged). For breaking moves (`X | None` migration on a public API), require a deprecation cycle. Never let an agent silence errors with `cast` or bare `# type: ignore`; require the rule code (`# type: ignore[arg-type]`) and a comment explaining why.

### Recommended subagents
- `type-annotator` (sonnet) — reads code + mypy report, emits annotations-only diff.
- `type-verifier` (haiku) — runs `mypy --strict` and `pytest`, fails on any new error.
- `faion-feature-executor` — sequential gate; type-check is one of the gates.
- `password-scrubber-agent` — sweep before commit (no behavior change should leak secrets, but be safe).

### Prompt pattern
```
Target Python version: 3.12. Type checker: mypy --strict.
Module: <path>.
Add type annotations only. No behavior changes.
Constraints:
- Use built-in generics (list[int], dict[str, int]).
- Use X | None for optionals, X | Y for unions (PEP 604).
- Use PEP 695 generics (class Foo[T]:) where 3.12+ is the floor.
- No `Any` unless justified in a comment.
- No `cast()` unless paired with a proof comment.
- No bare `# type: ignore`; always with rule code.
After: run `mypy --strict <path>`. Stop on any new error.
```

```
Audit pass on `<dir>`:
1) Find all `from typing import List|Dict|Optional|Union` imports.
2) Replace with built-in equivalents in 3.10+ files (check `requires-python`).
3) Find all `cast()` and `# type: ignore` without rule code; flag each.
Output a unified diff. Do NOT change runtime behavior.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mypy` (+ `django-stubs`, `djangorestframework-stubs`, `sqlalchemy[mypy]`) | Reference type checker | https://mypy.readthedocs.io/ |
| `pyright` / `pylance` | Microsoft's checker; fast | https://github.com/microsoft/pyright |
| `ty` | Astral's Rust-based checker (preview) | https://astral.sh/blog/ty |
| `ruff` (`UP`, `ANN` rule sets) | Lint type-related issues, autofix `typing.X` -> `X` | https://docs.astral.sh/ruff/ |
| `pytype` | Google's checker; rare | https://github.com/google/pytype |
| `monkeytype` | Generate annotations from runtime traces | https://github.com/Instagram/MonkeyType |
| `pyre` | Meta's checker; rare outside Meta | https://github.com/facebook/pyre-check |
| `typeguard` | Runtime type-check decorator | https://github.com/agronholm/typeguard |
| `stubgen` | Generate `.pyi` stubs | https://mypy.readthedocs.io/en/stable/stubgen.html |
| `mypy_primer` | Run mypy against many open-source projects (regression guard) | https://github.com/hauntsaninja/mypy_primer |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| typeshed | OSS | Yes | Stub repo; vendored by mypy/pyright. Submit PRs upstream when stubs are wrong. |
| Pylance (VS Code) | SaaS (free tier) | Yes | Best IDE typing UX; powered by Pyright. |
| typeddjango/django-stubs | OSS | Yes | Plugin-based Django typing. |
| typeddjango/djangorestframework-stubs | OSS | Yes | DRF stubs; pair with django-stubs. |
| Pydantic Logfire | SaaS | Yes | Captures runtime validation events that complement static checks. |
| GitHub Actions cache | SaaS | Yes | mypy incremental cache (`.mypy_cache`) caches well; speeds CI. |

## Templates & scripts
Strict mypy + ruff config (drop into `pyproject.toml`):

```toml
[tool.mypy]
python_version = "3.12"
strict = true
plugins = []  # add "mypy_django_plugin.main" for Django

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "ANN", "TCH"]
ignore = ["ANN101", "ANN102"]  # deprecated; self/cls

[tool.ruff.lint.flake8-annotations]
mypy-init-return = true
suppress-dummy-args = true
```

Pre-commit hook to enforce no-`Any` regression on touched files:

```bash
#!/usr/bin/env bash
# scripts/no-new-any.sh — fail if a touched .py adds an `Any` import or annotation
set -euo pipefail
files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)
[[ -z "$files" ]] && exit 0
if git diff --cached -U0 -- $files | grep -E '^\+.*\b(Any\b|: Any\b|-> Any\b)' >/dev/null; then
  echo "Refusing to add new uses of Any."
  exit 1
fi
```

## Best practices
- Pin one type checker for CI (mypy is the safest default in 2025-2026; pyright in IDE).
- Drop `from typing import List|Dict|Optional|Union` in 3.10+ code. Use `list`, `dict`, `X | None`, `X | Y`.
- Use `Protocol` for "duck-typed" callables/dependencies; reserve abstract base classes for inheritance hierarchies.
- Use `TypedDict` for JSON payload boundaries; `dataclass` for in-memory containers; `Pydantic` for validated input.
- Mark all stubs (`.pyi`) explicitly when shipping a typed library; `py.typed` marker file required.
- For decorators preserving signatures, use `ParamSpec` / PEP 695 `[**P, T]`. `Callable[..., Any]` defeats the purpose.
- Be explicit about `# type: ignore[<rule>]` codes; CI should fail on bare `# type: ignore`.
- Never silence by `cast()` if a proper narrowing (`if isinstance`, `assert`) works.
- For Django, set `DJANGO_SETTINGS_MODULE` correctly in `pyproject.toml`'s `[tool.mypy.plugins.django-stubs]` block.

## AI-agent gotchas
- Agents emit PEP 695 generics on Python 3.10/3.11 — `SyntaxError` at import.
- Agents use `ReadOnly[T]` in TypedDict on Python <3.13 — `ImportError`.
- Agents replace narrow exceptions with `cast()` to silence type errors. Forbid in prompt; require narrowing.
- Agents add `Any` everywhere `mypy` complains; CI passes but typing value is gone. Use `--disallow-any-explicit` to block.
- Agents mix `from typing import Optional` with `X | None` in the same file. Force one style.
- Agents forget `py.typed` marker when publishing a typed package; consumers don't pick up types.
- Agents sprinkle `@runtime_checkable` on every Protocol — slow `isinstance` checks at hot paths.
- Agents enable both mypy and pyright in CI without coordinating; conflicting messages waste reviews.
- Agents use `cast(SomeModel, queryset.first())` to suppress `Optional` — should be `if obj := queryset.first():` narrowing.
- Agents copy mypy plugin configs from one project to another without updating `django_settings_module`; static analysis silently goes wrong.
- Human-in-loop checkpoint: any new `Any`, any new `cast()`, any new `# type: ignore`.

## References
- https://docs.python.org/3/library/typing.html
- https://typing.python.org/en/latest/
- https://peps.python.org/pep-0484/ (Type Hints)
- https://peps.python.org/pep-0544/ (Protocols)
- https://peps.python.org/pep-0604/ (Union syntax)
- https://peps.python.org/pep-0612/ (ParamSpec)
- https://peps.python.org/pep-0655/ (Required/NotRequired)
- https://peps.python.org/pep-0695/ (Type Parameter Syntax)
- https://mypy.readthedocs.io/
- https://github.com/microsoft/pyright
- https://github.com/typeddjango/django-stubs
