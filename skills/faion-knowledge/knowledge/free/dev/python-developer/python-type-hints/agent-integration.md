# Agent Integration — Python Type Hints

Methodology codifies modern Python typing for 3.12+ (PEP 695 type parameter syntax, PEP 604 unions, PEP 742 `TypeIs`, PEP 705 `ReadOnly`, TypeVar defaults, Protocol structural subtyping). This file is the runbook for an LLM agent introducing or maintaining type safety in a Python (often Django/FastAPI) codebase.

## When to use
- Adding type hints to an untyped Python codebase, file-by-file with strict mode on touched files only.
- Public API surfaces — service signatures, route handlers, queue consumers, library exports.
- Cross-boundary data shapes — request/response, cache values, queue payloads — modelled with `TypedDict` (cheap) or Pydantic (validating).
- Defining structural inter-module contracts without forcing inheritance — `Protocol` (+ `@runtime_checkable` if `isinstance` is needed).
- CI gate: type-check files changed in a PR; block regressions on already-typed modules.
- Migrating old `typing.List` / `typing.Optional` to PEP 585 / PEP 604 syntax via `ruff --select UP --fix`.

## When NOT to use
- One-off scripts < ~100 lines — mypy/pyright setup costs more than it returns.
- Heavy metaprogramming surfaces (decorators that mutate signatures, `__getattr__` proxies, dynamic ORM-like APIs) — annotations fight the runtime; isolate behind `Any` or `cast`.
- Codebases pinned to Python 3.8 — README assumes 3.9+ (`list[int]`) and PEP 604 (3.10+); use `typing_extensions` only if you must.
- Pure Pydantic-only domains — adding parallel `TypedDict` definitions creates two sources of truth for the same shape.
- Generated migrations (`apps/*/migrations/`) — exclude in mypy config; cluttering them yields no signal.

## Where it fails / limitations
- README oscillates between `Optional[X]` and `X | None` in examples — agents will mix both unless ruff `UP007` is enabled.
- No coverage of `TypeVarTuple`, `Unpack`, `Concatenate`, `Self` (3.11+), or PEP 695 `type` statement edge cases (`type Vec[T] = list[T]`).
- `mypy --strict` flags every test fixture and conftest helper — README does not show the `[mypy-tests.*]` override that fixes this.
- `Protocol` example omits `@runtime_checkable` — `isinstance(x, Sendable)` raises `TypeError` at runtime if missing, but type-checks fine.
- No mention of `Generic[T]` having zero runtime enforcement: `Repository[int]` and `Repository[str]` are the same class.
- `from __future__ import annotations` interacts badly with Pydantic v1 / older FastAPI body-parsing — README does not warn.
- `TypeIs` example is correct but agents conflate it with `TypeGuard`; pick one and document narrowing direction.
- mypy/pyright comparison table is high-level — does not call out `reportMissingTypeStubs` (pyright) vs `--ignore-missing-imports` (mypy) divergence that bites in CI.

## Agentic workflow
File-by-file rollout: (1) pick one module, (2) annotate every public signature plus module-level vars, (3) run `mypy --strict <file>` (or `pyright --strict <file>`), (4) fix one error class at a time — start with `no-untyped-def`, then `var-annotated`, then `assignment`, then `arg-type`, (5) add file to `mypy.files=[...]` allowlist when green, (6) commit. Never run repo-wide `--strict` on day 1; the 1000+ errors will freeze the work. CI gate: strict-check only files in the diff (`git diff --name-only --diff-filter=AM origin/main -- '*.py'`).

### Recommended subagents
- `faion-code-agent` — Default for adding annotations and fixing type errors.
- `faion-test-agent` — Owns test fixture / factory types under the relaxed `tests.*` mypy override.
- `faion-software-architect` — Decides Protocol vs ABC vs Pydantic for cross-module contracts.
- `faion-devtools-developer` — Owns mypy / pyright / ruff config and pre-commit integration.
- `faion-sdd-execution` — Runs the gradual-typing rollout as a feature with milestones (per-app allowlist).

### Prompt pattern

Type one file:

```
Add type hints to apps/<module>/<file>.py per
free/dev/python-developer/python-type-hints/README.md.
Rules:
  - Python 3.12+ syntax: list[T], dict[K,V], X | None (NEVER Optional/List/Dict).
  - PEP 695 generics for new classes/functions: class Box[T]:, def first[T](...).
  - Public functions: full annotations including return type.
  - Internal helpers: annotate args + return; locals only if mypy complains.
  - Use TypedDict for cache/queue payloads; Pydantic for HTTP I/O.
  - Use Protocol (with @runtime_checkable IFF isinstance is called) for duck-typed interfaces.
Run: mypy --strict apps/<module>/<file>.py
Iterate to 0 errors. Each `# type: ignore[code]` MUST include a justification comment.
```

Introduce Protocol over ABC:

```
Replace abstract Sendable ABC in apps/notifications/base.py with
typing.Protocol. Add @runtime_checkable iff isinstance is called.
Concrete classes (EmailClient, SMSClient) must NOT inherit from Sendable.
Update factory return type to Sendable. Run mypy + pytest.
```

Migrate `TypeVar` to PEP 695:

```
In apps/<module>/<file>.py, convert all `T = TypeVar("T", bound=X)` blocks
to PEP 695 `class C[T: X]:` / `def f[T: X](...)`. Drop the TypeVar import
if unused. Verify with `ruff check` and `mypy --strict`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mypy` | Reference type checker; plugin support (django-stubs) | https://mypy.readthedocs.io |
| `pyright` | Microsoft type checker, ~10x faster than mypy, default in VSCode/Pylance | https://microsoft.github.io/pyright |
| `pytype` | Google type checker, infers types | https://github.com/google/pytype |
| `pyre` | Meta's type checker, used at scale | https://pyre-check.org |
| `ruff` rule `UP` | pyupgrade — converts `Optional[X]` → `X \| None`, `List` → `list`, etc. | https://docs.astral.sh/ruff |
| `ruff` rule `ANN` | flake8-annotations — flag missing annotations on public funcs | same |
| `ruff` rule `TCH` | flake8-type-checking — move type-only imports under `if TYPE_CHECKING` | same |
| `monkeytype` | Record types from runtime traces, emit stubs / inline annotations | https://monkeytype.readthedocs.io |
| `pyannotate` | Dropbox runtime-trace annotator | https://github.com/dropbox/pyannotate |
| `stubgen` (mypy) | Generate `.pyi` stubs for an untyped third-party lib | bundled with mypy |
| `mypy --html-report` | HTML coverage of typed % per module | bundled |
| `mypy_django_plugin` | Plugin for Django ORM type narrowing | https://github.com/typeddjango/django-stubs |
| `pyright --outputjson` | Machine-readable diagnostics for CI annotators | bundled |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| typeshed | OSS stub registry | Yes — auto-loaded by mypy/pyright | Contribute stubs when missing |
| typing-extensions | OSS lib | Yes | Backport newer typing features (TypeIs, Self, etc.) |
| GitHub Actions | CI | Yes — `mypy --strict $changed` | Cache `.mypy_cache` keyed on lockfile + Python version |
| pre-commit.com | OSS | Yes — `pre-commit-mirrors-mypy` | Run on staged files only |
| Codecov "type coverage" | SaaS (beta) | Partial — niche | Track typed-function % over time |
| pyright LSP / Pylance | IDE | Yes — VSCode extension | Inline diagnostics during agentic edits |

## Templates & scripts

See `templates.md` and `examples.md` for code patterns. Add this incremental adoption helper for CI / pre-push (≤45 lines):

```bash
#!/usr/bin/env bash
# scripts/typecheck-touched.sh — strict mypy on changed files only.
set -euo pipefail
BASE_REF="${1:-origin/main}"
mapfile -t files < <(git diff --name-only --diff-filter=AM "$BASE_REF" -- '*.py' \
  | grep -v -E '^(.*/migrations/|tests/fixtures/|conftest\.py$)')
if [[ ${#files[@]} -eq 0 ]]; then
  echo "No Python files changed."; exit 0
fi
echo "Typechecking ${#files[@]} files with mypy --strict..."
mypy --strict "${files[@]}"
```

`.pre-commit-config.yaml` hook:

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
- **One union syntax per project.** Pick `X | None`, ban `Optional` via ruff `UP007` auto-fix.
- **Type the boundary, then the seams.** Annotate I/O (HTTP, queue, DB) first; then services; then internals.
- **`Any` is a smell.** Use `object` (no operations allowed) when you mean "anything"; reserve `Any` for FFI / dynamic metaprogramming with a `# type: ignore[code]` reason.
- **`TypedDict` for cache/queue payloads, Pydantic for HTTP.** Don't run both in the same path — pick one source of truth.
- **`Protocol` over ABC** when implementers are out of your control (third-party libs); add `@runtime_checkable` only if you actually `isinstance` it.
- **Constrain `TypeVar` with `bound=`** or PEP 695 syntax (`class C[T: Model]:`); unconstrained generics rarely add safety.
- **`Self` (3.11+)** for fluent builder return types, not `TForward = TypeVar(..., bound="Foo")` gymnastics.
- **Sealed unions via `Literal`** for finite states + `assert_never()` for exhaustiveness checks.
- **Per-module mypy override**: relax `disallow_untyped_defs` for tests, ignore migrations, strict everywhere else.
- **Run mypy AND ruff `ANN`** — mypy catches type mismatches; ruff `ANN` catches *missing* annotations entirely (different signal).
- **Cache `.mypy_cache` / `.pyright_cache`** in CI keyed on Python + lockfile hash.
- **`pyright` for IDE, `mypy` for CI** — pyright is faster for inline feedback; mypy has the plugin ecosystem (Django, attrs, etc.).

## AI-agent gotchas
- **`Optional[X]` vs `X | None` mixing** in one PR confuses readers and ruff. Auto-fix with `ruff check --select UP007 --fix`.
- **Forward refs**: `def f() -> "Foo":` strings still required when `Foo` is defined below. `from __future__ import annotations` makes everything a string at runtime — breaks Pydantic v1, FastAPI body parsing on some versions.
- **`from __future__ import annotations` + Pydantic v1** → "field type is undefined" runtime errors. Pydantic v2 handles it.
- **`Generic[T]` runtime is a no-op.** `Repository[int]()` and `Repository[str]()` are the same class object. Don't rely on it for safety at runtime.
- **`Protocol` without `@runtime_checkable`** + `isinstance(x, Proto)` raises `TypeError` at runtime; type-checks fine.
- **`TypedDict` `total=False`** vs `NotRequired[X]` per-field: different typing versions handle them differently. Prefer `NotRequired` (3.11+ via `typing_extensions`).
- **`TypeIs[T]` (3.13)** vs `TypeGuard[T]` (3.10) — `TypeIs` narrows in BOTH branches, `TypeGuard` only narrows in the `True` branch. Pick deliberately.
- **`Callable[..., T]`** allows any args — silently allows misuse. Be specific where possible.
- **`mypy_django_plugin`** narrows `Manager.get()` etc. but requires `[tool.django-stubs] django_settings_module = "config.settings.test"`. Without it, errors are spurious; agents revert annotations instead of fixing config.
- **Bare `# type: ignore`** masks future bugs; ruff `PGH003` blocks it. Always `# type: ignore[code]` with a comment.
- **Type narrowing through `assert`** works in mypy but not at runtime under `python -O`. Don't branch on it.
- **`reveal_type(x)`** is mypy-only; leaving it in code raises `NameError` at runtime. Strip via pre-commit.
- **Generators**: `Generator[YieldT, SendT, ReturnT]` vs `Iterator[YieldT]` vs `Iterable[YieldT]` — agents pick wrong half the time. Default to `Iterator` for read-only sequences.
- **Async**: `Coroutine[Any, Any, T]` vs `Awaitable[T]` — return-annotate `T` directly on `async def f() -> T`; type-checker unwraps automatically.
- **PEP 695 `type` statement** is lazy-evaluated — `type Vec[T] = list[T]` resolves at first use, not at module load. Subtle in circular-import scenarios.
- **PEP 649 lazy annotations (3.14)** changes `__annotations__` access — code that introspects annotations may need `inspect.get_annotations(...)` instead of `cls.__annotations__`.

## References
- README: `./README.md`
- Sibling: `../python-modern-2026/`, `../python-typing/`, `../django-coding-standards/`
- mypy strict: https://mypy.readthedocs.io/en/stable/getting_started.html#strict-mode
- pyright: https://microsoft.github.io/pyright/
- typeshed: https://github.com/python/typeshed
- typing_extensions: https://pypi.org/project/typing-extensions/
- PEP 604 (X | Y): https://peps.python.org/pep-0604/
- PEP 695 (type parameter syntax, 3.12): https://peps.python.org/pep-0695/
- PEP 705 (ReadOnly): https://peps.python.org/pep-0705/
- PEP 742 (TypeIs, 3.13): https://peps.python.org/pep-0742/
- PEP 649 (lazy annotations, 3.14): https://peps.python.org/pep-0649/
- django-stubs: https://github.com/typeddjango/django-stubs
- ruff annotations rules: https://docs.astral.sh/ruff/rules/#flake8-annotations-ann
