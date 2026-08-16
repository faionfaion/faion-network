# Python Type Hints and Static Typing

## Summary

**One-sentence:** Rules for adding and maintaining type annotations in Python 3.10+ codebases using mypy (CI) and pyright (IDE).

**One-paragraph:** Produces a typed Python module plus mypy/pyright/ruff configuration that passes `--strict` on Python 3.12+. Core rules: use PEP 585 built-in generics (`list[int]`, `dict[str, X]`), use PEP 604 unions (`X | None`), use PEP 695 type parameter syntax (`class Repo[T]:`) on 3.12+ floors, never add bare `# type: ignore` without a rule code, never silence with `cast()` when a narrowing guard works, never let `Any` leak across module boundaries.

**Ефективно для:** новий або частково-типізований модуль на Python 3.10+, де треба ввімкнути `mypy --strict` у CI і прибрати приховані `Any`.

## Applies If (ALL must hold)

- Target codebase floor is Python 3.10+ (so `X | None` works); ideally 3.12+ (PEP 695 syntax).
- A type checker is already in CI or about to be added (`mypy`, `pyright`, or both).
- The module has a stable public API surface worth annotating (services, models, payload boundaries).
- The team has agreed to treat `Any` as a code smell, not a fallback.
- ruff is available in pre-commit (used for UP/ANN/TCH auto-fixes).

## Skip If (ANY kills it)

- Codebase still supports Python ≤3.9 — `X | Y` syntax fails at parse time.
- Throwaway scripts, exploratory notebooks, one-off ETL — setup cost exceeds payoff.
- Cython/PyO3 extension modules where types live in `.pyi` stubs maintained separately.
- Bridging dynamic legacy libraries (old ML stacks) with no stubs and no will to write any.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `pyproject.toml` | TOML | repo root |
| Module(s) to be annotated | `*.py` | repo source tree |
| Python version floor | declared in `pyproject.toml` / `mise.toml` | project config |
| List of third-party deps without stubs | newline-separated | `mypy --strict` first run output |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-modern-2026` | Establishes the 3.12+ baseline this methodology builds on. |
| `free/dev/software-developer/best-practices-2026` | Provides pre-commit / CI hook surface this plugs into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: PEP 585 generics, PEP 604 unions, PEP 695 syntax, strict mypy config, scoped `type: ignore`, no-`cast()`-as-silencer, django-stubs wiring | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced annotated-module report: file paths, error count before/after, `Any` count, deltas | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: Any-as-shortcut, dict-of-Any payloads, bare ignore, cast-as-silencer, mixed Optional/pipe styles, @runtime_checkable on hot paths | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step migration: baseline scan → fix UP/ANN → add stubs → strict per-module → CI gate | ~700 |
| `content/06-decision-tree.xml` | essential | Which annotation strategy for which input shape | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Initial annotation pass on existing code | sonnet | High volume mechanical work; sonnet handles ruff/mypy fix loops reliably. |
| Designing new Protocol / TypedDict shapes for public APIs | opus | Requires modeling judgment — opus picks better shape boundaries. |
| Wiring mypy + django-stubs + ruff config | sonnet | Configuration plumbing, deterministic. |
| Auditing a PR for `Any` leaks | sonnet | Mechanical diff check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mypy-config.toml` | Strict mypy config with `django-stubs` plugin and per-module overrides for `tests.*` and `migrations.*`. |
| `templates/no-new-any.sh` | CI guard: greps the diff for new `: Any`, `-> Any`, `dict[str, Any]`; exits 1 if introduced. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-typing.py` | Validates output report against the `02-output-contract.xml` schema. | After running the annotation pass, before merging the PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[python-modern-2026]] — Python 3.12+ feature baseline.
- [[django-coding-standards]] — Django-side annotation rules (django-stubs).
- [[best-practices-2026]] — overarching 2026 TypeScript / Python quality bar.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the annotation strategy from the input shape (dict-shaped payload → TypedDict; structural contract → Protocol; class hierarchy with `super()` chains → ABC; generic container → PEP 695 generic). Use it whenever the right answer is "what type construct fits this case", not "should I annotate at all".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/mypy-config.toml`

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_ignores = true
warn_return_any = true

# Django-stubs plugin
plugins = ["mypy_django_plugin.main"]

# django-stubs reads its own settings from [tool.django-stubs], not from a
# table under [tool.mypy].plugins — that key is the plugin-list array above.
[tool.django-stubs]
django_settings_module = "config.settings.development"
# Strict mode for Django models (requires django-stubs 5.0+)
strict_settings = true

# ─── Per-module overrides ────────────────────────────────────────────────────

# Tests: allow untyped fixtures and parametrize helpers
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
disallow_any_generics = false

# Migrations: generated code, skip entirely
[[tool.mypy.overrides]]
module = ["*.migrations.*", "conftest"]
ignore_errors = true

# Third-party packages without stubs
[[tool.mypy.overrides]]
module = [
    "boto3.*",
    "botocore.*",
    "celery.*",
    "redis.*",
    "factory.*",
]
ignore_missing_imports = true

# Incrementally typed modules — add strict as they are annotated:
# [[tool.mypy.overrides]]
# module = ["apps.orders.services", "apps.users.services"]
# strict = true
```

### `templates/no-new-any.sh`

```bash
set -euo pipefail

# Get list of staged .py files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

echo "==> Checking for new Any annotations in staged files..."

# Run mypy on staged files, grep for error codes that indicate Any
MYPY_OUTPUT=$(uv run mypy --no-error-summary $STAGED_FILES 2>&1 || true)

# Check for Any-related errors
ANY_ERRORS=$(echo "$MYPY_OUTPUT" | grep -E "(no-any-return|type\[Any\]|Returning Any|has type.*Any)" || true)

if [ -n "$ANY_ERRORS" ]; then
    echo "ERROR: New Any annotations detected in staged files:"
    echo "$ANY_ERRORS"
    echo ""
    echo "Fix: Replace Any with a specific type or use TypedDict/Protocol."
    echo "If unavoidable: use '# type: ignore[return-value]' with a justification comment."
    exit 1
fi

echo "==> No new Any annotations found."
exit 0

# ─── .pre-commit-config.yaml snippet ─────────────────────────────────────────
# - repo: local
#   hooks:
#     - id: no-new-any
#       name: No new Any annotations
#       entry: bash skills/faion/knowledge/free/dev/python-developer/python-typing/templates/no-new-any.sh
#       language: system
#       stages: [pre-push]
#       pass_filenames: false
```
