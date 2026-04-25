# Agent Integration — Django Import Patterns

Methodology codifies PEP 8 + Django/HackSoft import ordering, cross-app aliasing, `TYPE_CHECKING` guards, lazy `apps.get_model()`, string FK references, and PEP 810 lazy imports (3.14+). Use this file when an agent organizes imports in a Django project, resolves circular import errors, or wires ruff/isort.

## When to use
- Setting up a new Django project — pyproject.toml ruff/isort with Django known-third-party + known-first-party.
- Adding a new app to an existing project — establish the cross-app alias convention before duplicate `User` collisions appear.
- Resolving `ImportError: cannot import name '...'` from circular cross-app deps.
- Adding type hints to legacy Django code — `if TYPE_CHECKING:` blocks for type-only imports.
- CI gate: ruff `I` (isort) auto-sort on staged files.
- Performance work on slow Django startup — moving heavy imports to lazy patterns (function-scoped or PEP 810 in 3.14+).

## When NOT to use
- Single-app projects — alias rules add noise without benefit.
- Codebases that have a `core.imports` shim or similar central re-export — duplicating direct imports defeats it.
- One-off management commands or scripts where readability beats convention.
- Pure data pipelines (Airflow DAGs, Prefect flows) — Django ORM rarely involved; rules don't apply.
- Codebase already migrated to Django 5.x with full `from __future__ import annotations` everywhere — no need to re-tune.

## Where it fails / limitations
- README's "always use aliases for cross-app imports" rule conflicts with auto-import in some IDEs (PyCharm, VSCode without config) — agents revert to direct imports.
- `apps.get_model('orders', 'Order')` returns `Any` to type checkers — kills mypy/pyright narrowing for the rest of the function.
- `from __future__ import annotations` interaction with Pydantic v1 / DRF serializers (`fields = '__all__'` introspection) is not warned.
- PEP 810 lazy imports (3.14+) shown as future syntax — agents will paste it into 3.12 code; SyntaxError.
- Circular import mitigations (`TYPE_CHECKING`, `apps.get_model`, string refs) cover the common cases but not metaclass-driven ones (e.g., django-modeltranslation).
- ruff config example missing `[tool.ruff.lint.isort] known-first-party = ["apps", "core"]` — agents leave first-party in third-party section.
- README's "single-dot relative imports" rule mixes badly with `src/` layout (uncommon in Django but rising) — paths shift one level.
- Multi-dot relative ban (`from ...foo import bar`) is good practice but rarely enforced by linters.

## Agentic workflow
New project: (1) configure ruff `[tool.ruff.lint.isort]` with `known-first-party = ["apps","core","config"]`, `section-order = [..., "django", "first-party", "local-folder"]` plus `[tool.ruff.lint.isort.sections] django = ["django","rest_framework","celery"]`, (2) run `ruff check --select I --fix .` to auto-sort, (3) commit. Adding an app: (1) add to `INSTALLED_APPS`, (2) write models with string FK refs (`'users.User'`) instead of imports, (3) when services need cross-app types, alias: `from apps.users import models as user_models`. Circular import fix flow: (a) try string FK, (b) try `apps.get_model`, (c) move import inside the function, (d) extract to neutral `core/` module — in that order.

### Recommended subagents
- `faion-code-agent` — Default for refactoring imports and adding aliases.
- `faion-devtools-developer` — Owns ruff/isort config and pre-commit hook for `I` rule.
- `faion-software-architect` — Decides when circular imports indicate a real layering issue (extract to core/).
- `faion-test-agent` — Verifies tests still pass after import reorganization (some tests depend on import-time side effects).

### Prompt pattern

Sort imports across an app:

```
Reorganize imports in apps/<app>/**/*.py per
free/dev/python-developer/django-imports/README.md.
Rules:
  - Section order: __future__, stdlib, third-party (incl. django, drf, celery),
    first-party (apps., core., config.), local (.).
  - Cross-app imports MUST use aliases: `from apps.users import models as user_models`.
  - Type-only imports go under `if TYPE_CHECKING:` after `from __future__ import annotations`.
  - Multi-dot relatives (`from ... import x`) banned — use absolute.
Run `ruff check --select I --fix` and `ruff format`. Show diff per file.
Do NOT introduce wildcard imports.
```

Resolve a circular import:

```
Fix the circular import between apps/orders/services.py and apps/users/services.py per
free/dev/python-developer/django-imports/README.md.
Strategy ladder (use first that works):
  1. String FK references in models (`'users.User'`).
  2. apps.get_model('users','User') inside the function body.
  3. `if TYPE_CHECKING:` import for type hints only.
  4. Move shared logic to core/ (last resort, requires architect approval).
Run app tests after the fix; no behavior change expected.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff check --select I --fix` | Sort imports (replaces isort, faster) | https://docs.astral.sh/ruff/rules/#isort-i |
| `ruff format` | Format remaining whitespace | same |
| `isort` (legacy) | Original sorter; useful for very large legacy diffs | https://pycqa.github.io/isort/ |
| `pyupgrade` (or ruff `UP`) | Drops unused `from typing import ...` | https://github.com/asottile/pyupgrade |
| `flake8-tidy-imports` (or ruff `TID`) | Ban relative-from-parent, ban specific imports | https://github.com/adamchainz/flake8-tidy-imports |
| `flake8-type-checking` (or ruff `TCH`) | Move type-only imports under `TYPE_CHECKING` | https://docs.astral.sh/ruff/rules/#flake8-type-checking-tch |
| `removestar` | Eliminate `import *` | https://github.com/asmeurer/removestar |
| `importtime` (Python `-X importtime`) | Find slow imports for migration to lazy | builtin |
| `tach` | Enforce module boundaries (e.g., apps cannot import each other directly) | https://github.com/gauge-sh/tach |
| `import-linter` | Architecture rules: layered, independent, forbidden contracts | https://import-linter.readthedocs.io |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions | CI | Yes — `ruff check .` job | Block PRs with import drift |
| pre-commit.com | OSS | Yes — `ruff-pre-commit` | Run `--select I --fix` on staged files |
| import-linter (OSS) | Architecture lint | Yes — declarative TOML contracts | Enforce app independence |
| tach (OSS) | Module boundary lint | Yes | Lighter alt to import-linter |
| pyright LSP | IDE | Yes — auto-imports respect config | Inline diagnostics |

## Templates & scripts

See `templates.md` for ruff/isort configs and `examples.md` for canonical patterns. Add this circular-import scout (≤45 lines):

```bash
#!/usr/bin/env bash
# scripts/find-circular-imports.sh — list cross-app direct imports likely to circularize.
set -euo pipefail
APPS_DIR="${1:-apps}"
echo "Cross-app direct imports (no alias) under $APPS_DIR:"
grep -rn --include='*.py' -E '^from apps\.[a-z_]+ import [A-Z][a-zA-Z]*$' "$APPS_DIR" \
  || echo "  none — clean."
echo
echo "Top-level imports of cross-app models (suspect for circular deps):"
grep -rn --include='*.py' -E '^from apps\.[a-z_]+\.models import' "$APPS_DIR" \
  | grep -v '__init__.py'
```

## Best practices
- **One ruff config, project-wide** — `pyproject.toml [tool.ruff.lint.isort]`. No per-app overrides.
- **`known-first-party`** declared explicitly: `["apps", "core", "config"]`. ruff auto-sorts them as first-party.
- **Aliases mandatory for cross-app imports** — even if there's no current naming collision, future apps will collide.
- **String FK refs > model imports** in `models.py`. Django resolves at app-loading time; circular imports become impossible.
- **`apps.get_model()` for runtime model access in non-model code** (signals, managers, migrations).
- **`TYPE_CHECKING` for type-only imports** + `from __future__ import annotations` so the strings work without quotes.
- **No wildcard imports** — even in `__init__.py`. Be explicit; it helps both ruff and humans.
- **Function-scoped imports** are a valid escape hatch for circular deps; not a code smell when justified by a comment.
- **`importtime` profiling** before optimizing — heavy imports are usually 2-3 modules, not "everything".
- **`tach` or `import-linter`** to encode "users app is leaf, doesn't import orders" rules — catches drift in CI.
- **Don't mix `from .models import *` and explicit imports** — pick one per `__init__.py`.

## AI-agent gotchas
- **`from __future__ import annotations` + DRF `Meta.fields = '__all__'`** — DRF introspects model fields at import time; `__future__` annotations stringify FK type hints, breaking introspection in some versions.
- **`apps.get_model(...)`** returns `type[Model]` typed as `Any` — type checkers can't narrow. Pair with `cast()` if you need real typing.
- **String FK reference + `from __future__ import annotations`** is double indirection but safe.
- **Ruff sorts third-party `django` correctly only with the section config** — without it, `django` may end up in stdlib or unsorted.
- **`TYPE_CHECKING` block + signals** — Django signals run at runtime; can't reference TYPE_CHECKING-only types without crashing.
- **Migrations import models** — agents adding aliases break old migrations that imported `from apps.users.models import User` directly. Don't refactor migration files.
- **Renaming an app** (e.g., `users` → `accounts`) breaks string FK refs (`'users.User'`) and `apps.get_model('users','User')` calls — global find/replace required.
- **`tests/` imports** sometimes need direct cross-app imports for fixture composition; relax alias rule with `[tool.ruff.lint.per-file-ignores] "tests/**" = ["..."]`.
- **`from . import x as y`** — single-dot relative aliases are fine; agents over-rotate to absolute and create churn.
- **PEP 810 `lazy from ...`** is 3.14+; agents pasting it into 3.12 hit `SyntaxError`. Use function-scoped imports for older Python.
- **`removestar` may break dynamic frameworks** that rely on `from package import *` populating namespace — verify before committing.
- **Pre-commit `ruff` writes files** — agents running it without `--fix` see "would reformat" without changes; with `--fix`, files mutate and need re-stage.
- **Cyclic imports across `tests/`** — pytest collection imports test modules in directory order; agents adding `from tests.shared import ...` can break collection on case-sensitive filesystems.

## References
- README: `./README.md`
- Sibling: `../django-coding-standards/`, `../python-type-hints/`, `../python-code-quality/`
- PEP 8 imports: https://peps.python.org/pep-0008/#imports
- PEP 328 (relative): https://peps.python.org/pep-0328/
- PEP 563 (postponed annotations): https://peps.python.org/pep-0563/
- PEP 810 (lazy imports, 3.14+): https://peps.python.org/pep-0810/
- ruff isort: https://docs.astral.sh/ruff/rules/#isort-i
- ruff TCH: https://docs.astral.sh/ruff/rules/#flake8-type-checking-tch
- import-linter: https://import-linter.readthedocs.io
- tach: https://github.com/gauge-sh/tach
- HackSoft Django Styleguide: https://github.com/HackSoftware/Django-Styleguide
