# Agent Integration — Python Type Hints

Methodology codifies modern Python typing (3.9+ generics, PEP 604 unions, TypedDict, Protocol) plus mypy strict configuration. Use this file as a runbook for an LLM agent introducing or maintaining type safety.

## When to use
- Adding type hints to an untyped Python codebase, file-by-file (mypy strict on touched files only).
- Public API surfaces — function signatures of services, route handlers, library exports.
- Complex data shapes flowing across boundaries (request/response, queue payloads, cache values) — TypedDict / Pydantic / dataclass.
- Defining structural interfaces between modules without inheritance — `Protocol`.
- CI gate to prevent type regressions on PRs that touch typed modules.

## When NOT to use
- One-off scripts (<100 lines) where mypy setup costs more than it saves.
- Migrating dynamic metaprogramming (decorators that mutate signatures, `__getattr__` proxies) — types fight you; use `# type: ignore[attr-defined]` sparingly or skip.
- Hot paths where `typing.get_type_hints` resolution at import time matters (rare; only relevant to code-gen / deserializers).
- Code that must run on Python 3.8 — README assumes 3.9+ syntax (`list[int]`) and PEP 604 (`X | Y`, 3.10+).
- Codebases standardized on Pydantic models — adding parallel TypedDict definitions creates two sources of truth.

## Where it fails / limitations
- README does not pick a side between `Optional[X]` and `X | None` — agents will mix both.
- No coverage of `TypeVarTuple`, `ParamSpec`, `Self`, `Concatenate`, or `Unpack` — common in real generics.
- `mypy --strict` flags every test fixture lacking a return type — README's mypy override `tests.* disallow_untyped_defs = false` fixes that, but agents miss it and start typing every test.
- `Protocol` example uses `def send(self, message: str) -> bool: ...` — without `@runtime_checkable`, `isinstance(x, Sendable)` fails. Real-world reads expect runtime check support.
- `Callable[[int, str], bool]` shown but no mention of `Callable[..., T]` for variadic args — agents reach for it.
- Generic `Repository[T]` uses `T` without `bound=`; at runtime no constraint, no protection from `Repository[int]`.
- mypy section omits `--enable-incomplete-feature=NewGenericSyntax` (PEP 695) and the new `type` statement (3.12+).
- No mention of `pyright` (often faster, default in VSCode) — agents default to mypy because that's what the README shows.

## Agentic workflow
File-by-file mode: (1) pick one module, (2) add types to every public signature + module-level vars, (3) run `mypy --strict <file>` and fix one error class at a time (start with `no-untyped-def`, then `var-annotated`, then `assignment`, then `arg-type`), (4) add to mypy `files=[...]` once green, (5) commit. Never run `--strict` repo-wide on day 1; you'll get 1000+ errors and freeze. CI gate: `mypy --strict $(git diff --name-only --diff-filter=AM origin/main -- '*.py')`.

### Recommended subagents
- `faion-code-agent` — Default for adding annotations.
- `faion-test-agent` — Owns test fixture types; uses mypy override for tests.
- `faion-software-architect` — Decides Protocol vs ABC vs Pydantic for cross-module contracts.
- `faion-devtools-developer` — Owns mypy / pyright config, pre-commit integration.
- `faion-sdd-execution` — Runs the gradual-typing rollout as a feature with milestones.

### Prompt pattern
Type one file:

```
Add types to apps/<module>/<file>.py per
free/dev/software-developer/python-type-hints/README.md.
Rules:
  - Use X | None, never Optional[X].
  - list[T] / dict[K,V] / tuple[T,...]; never typing.List/Dict.
  - Public functions: full annotations including return.
  - Internal helpers: annotate args + return; locals only if mypy complains.
Run: mypy --strict apps/<module>/<file>.py — paste full output.
Iterate until 0 errors. Do NOT add `# type: ignore` without a comment justifying it.
```

Introduce Protocol:

```
Replace abstract Sendable ABC in apps/notifications/base.py with
typing.Protocol (runtime_checkable). Update concrete classes
(EmailClient, SMSClient) — they must NOT inherit from Sendable.
Update factory typing to return Sendable. Run mypy + pytest.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mypy` | Reference type checker | https://mypy.readthedocs.io |
| `pyright` | Microsoft type checker, ~10x faster, basic + strict modes | https://microsoft.github.io/pyright |
| `pytype` | Google type checker, infers types | https://github.com/google/pytype |
| `pyre` | Meta's type checker | https://pyre-check.org |
| `ruff` (rule UP) | pyupgrade — converts old syntax (`Optional[X]` → `X | None`) | https://docs.astral.sh/ruff |
| `ruff` (rule ANN) | Flag missing annotations on public funcs | same |
| `monkeytype` | Record types from runtime traces, emit stubs | https://monkeytype.readthedocs.io |
| `pyannotate` | Similar runtime-trace stub generator | https://github.com/dropbox/pyannotate |
| `stubgen` (mypy bundled) | Generate `.pyi` for an untyped third-party lib | bundled |
| `mypy --html-report` | HTML coverage of typed % per module | bundled |
| `mypy_django_plugin` | mypy plugin for Django ORM type narrowing | https://github.com/typeddjango/django-stubs |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| typeshed | OSS stubs registry | Yes — auto-loaded by mypy | Contribute stubs for missing libs |
| typing-extensions | OSS lib | Yes | Backport newer typing features to older Python |
| GitHub Actions | CI | Yes — `mypy . --strict` | Cache `.mypy_cache` keyed on lockfile |
| Pre-commit | OSS | Yes — `pre-commit-mirrors-mypy` | Run on staged files |
| Codecov "type coverage" | Beta SaaS | Partial — niche | Track typed-function % over time |

## Templates & scripts
README covers config snippets. Add this incremental adoption helper (≤45 lines):

```bash
#!/usr/bin/env bash
# scripts/typecheck-touched.sh — strict mypy on changed files only.
set -euo pipefail
BASE_REF="${1:-origin/main}"
mapfile -t files < <(git diff --name-only --diff-filter=AM "$BASE_REF" -- '*.py' \
  | grep -v -E '^(migrations/|tests/fixtures/|conftest\.py$)')
if [[ ${#files[@]} -eq 0 ]]; then
  echo "No Python files changed."; exit 0
fi
echo "Typechecking ${#files[@]} files with mypy --strict..."
mypy --strict "${files[@]}"
```

Hook into `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: mypy-touched
      name: mypy touched files (strict)
      entry: scripts/typecheck-touched.sh
      language: system
      pass_filenames: false
      stages: [pre-push]
```

## Best practices
- **One union syntax per project.** Pick `X | None` (modern) and ban `Optional` via ruff `UP007`.
- **Type the boundary, then the seams.** Annotate I/O (HTTP handlers, queue consumers, DB models), then services, then internals.
- **Avoid `Any` in production code.** Use `object` (no operations allowed) when you really mean "anything"; reach for `Any` only at FFI / dynamic boundaries with a `# type: ignore` reason.
- **`TypedDict` for cache / queue payloads, Pydantic for HTTP.** Don't run both in the same path.
- **`Protocol` over ABC** when you don't control all implementers (third-party libs). Add `@runtime_checkable` only if you actually call `isinstance`.
- **`TypeVar` with `bound=`** to constrain generics to a useful upper bound: `T = TypeVar("T", bound=Model)`.
- **Use `Self` (3.11+)** for fluent / builder return types instead of `TForward = TypeVar("TForward", bound="Foo")` gymnastics.
- **Sealed unions via `Literal`** for finite states: `Status = Literal["pending", "active", "deleted"]`. mypy exhaustiveness via `assert_never`.
- **Per-module mypy override**: relax `disallow_untyped_defs` for tests, ignore migrations, strict everything else. README's snippet is correct; don't dilute it.
- **Run mypy AND ruff `ANN`** — mypy catches type errors, ruff ANN catches missing annotations entirely. Different signal.
- **Cache `.mypy_cache`** in CI keyed on Python version + lockfile hash.

## AI-agent gotchas
- **`Optional[X]` vs `X | None` mixing** in one PR confuses readers and ruff. Auto-fix with `ruff --select UP007 --fix`.
- **Forward references**: `def f() -> "Foo":` strings are still required when `Foo` is defined below. Or use `from __future__ import annotations` (then everything is a string at runtime, breaks Pydantic v1 / FastAPI body parsing!).
- **`from __future__ import annotations` + Pydantic v1** → "field type is undefined" runtime errors. Pydantic v2 handles it. FastAPI was sensitive — check your version.
- **`Generic[T]` at runtime** doesn't enforce anything. `Repository[int]()` and `Repository[str]()` are the same class object.
- **`Protocol` without `@runtime_checkable`** + `isinstance(x, Proto)` raises `TypeError` at runtime. Quiet at type-check time.
- **`TypedDict` `total=False`** vs `NotRequired[X]` per-field: different versions of typing handle them differently. Stick with `NotRequired` (3.11+ via typing_extensions).
- **`Callable[..., T]`** types accept any args — silently allows misuse. Be specific where possible.
- **`mypy_django_plugin`** type-narrows `Manager.get()` etc. but requires settings module config: `[tool.django-stubs] django_settings_module = "config.settings.test"`. Without it, errors are spurious.
- **`# type: ignore` without code**: `# type: ignore[attr-defined]` is required by ruff and best practice; bare `# type: ignore` masks future bugs.
- **Type narrowing through `assert`** works in mypy but not at runtime if `python -O`. Don't rely on `assert isinstance(x, Foo)` for branching.
- **`reveal_type(x)`** is mypy-only; leaving it in code raises `NameError` at runtime. Strip via pre-commit.
- **`from typing import Optional`** unused after migration — ruff F401 catches; otherwise stale imports linger.
- **Generators**: `Generator[YieldT, SendT, ReturnT]` vs `Iterator[YieldT]` vs `Iterable[YieldT]` — agents pick the wrong one half the time. Prefer `Iterator` for read-only sequences.
- **Async**: `Coroutine[Any, Any, T]` vs `Awaitable[T]` — return annotate `T` directly on `async def f() -> T`; mypy unwraps automatically.

## References
- README: `./README.md`
- Sibling: `../python/` (umbrella), `../typescript-strict-mode/` (TS analog)
- mypy strict: https://mypy.readthedocs.io/en/stable/getting_started.html#strict-mode
- pyright: https://microsoft.github.io/pyright/
- typeshed: https://github.com/python/typeshed
- typing-extensions: https://pypi.org/project/typing-extensions/
- PEP 604 (X | Y): https://peps.python.org/pep-0604/
- PEP 695 (type statement, 3.12): https://peps.python.org/pep-0695/
- PEP 692 (Unpack TypedDict): https://peps.python.org/pep-0692/
- django-stubs: https://github.com/typeddjango/django-stubs
- ruff annotations rules: https://docs.astral.sh/ruff/rules/#flake8-annotations-ann
