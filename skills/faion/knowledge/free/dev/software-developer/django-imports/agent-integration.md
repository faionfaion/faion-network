# Agent Integration — Django Import Patterns

## When to use
- New Django project setup: lock down import style before app sprawl creates name collisions (`User` from auth vs custom `User`).
- Onboarding multi-app codebases (`apps/orders`, `apps/users`, `apps/catalog`) where `Order`, `User`, `Item` collide in handlers and serializers.
- Mid-refactor of a legacy Django repo with `from app.models import *` style — apply isort + alias rule to remove ambiguity.
- Adding type hints to a Django codebase that has circular import problems between `models.py` files.
- Pre-commit hook authoring: encoding the alias convention into ruff/isort to keep agents and humans consistent.

## When NOT to use
- Single-app Django projects with <10 models — the alias overhead pays nothing.
- Non-Django Python repos (FastAPI, Flask) with flat package structure — the rule is Django-app-specific.
- Serializers / form classes where direct symbol import is idiomatic (`from rest_framework import serializers`) — the rule applies to *cross-app project* imports.
- One-shot scripts and Jupyter notebooks where readability of unaliased names trumps consistency.

## Where it fails / limitations
- **No automated enforcement out of the box.** ruff/isort sort imports but don't enforce the *alias-on-cross-app* rule; teams drift unless a custom AST checker runs in CI.
- **Alias bikeshedding.** `order_models` vs `orders_models` vs `m_orders` — without a written convention every PR re-litigates the alias.
- **Long lines.** `order_models.OrderLineItemDiscount` reads worse than `OrderLineItemDiscount`; the rule trades readability for unambiguity.
- **TYPE_CHECKING + circular imports.** The README mentions `from __future__ import annotations` but doesn't show how it interacts with serializer `Meta.model` (which needs runtime symbols). Easy to break.
- **DRF / Django generics use direct imports by convention.** Mixing the two styles in one file (alias for app models, direct for DRF) confuses readers and tools.
- **Refactor cost.** Renaming an app (`apps.orders` → `apps.commerce`) cascades into every alias usage; a `git grep` works but agents still miss usages in tests and migrations.

## Agentic workflow
Use Claude subagents in three modes against this convention. (1) **Scaffolder** — when generating a new app or models module, the agent emits the import block in the canonical order (stdlib → third-party → cross-app aliased → relative) and pre-imports the app's own `models`, `services`, `constants` siblings. (2) **Linter / fixer** — an agent reads existing files, detects `from apps.X.models import Y` violations, and rewrites them to `from apps.X import models as X_models` plus call-site changes. (3) **Reviewer** — on PRs, the agent confirms no `import *`, no unaliased cross-app, no missing `TYPE_CHECKING` for circular dependencies.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — gates Django PRs; rejects merges that violate the import rule and creates `.aidocs/.../todo/` tasks for fixes.
- A purpose-built **django-import-linter agent** (worth creating): wraps `import-linter` config + AST diff to enforce the alias rule and the order-by-tier rule.
- `password-scrubber-agent` — only relevant when sharing settings/imports externally that may reference vendor-specific app names.

### Prompt pattern
Lint-fix pass:
```
Apply Django import conventions from
free/dev/software-developer/django-imports/README.md to <files>:
- Cross-app imports MUST use `from apps.<X> import models as <X>_models`
  (never `from apps.<X>.models import Y`).
- Order: __future__, stdlib, third-party (django, rest_framework),
  apps.* aliased, relative `from . import ...`.
- Preserve runtime semantics: rewrite all call sites accordingly.
- No `import *`. Output unified diff only.
```

Review pass:
```
For each .py file in the diff, verify:
1. No bare `from apps.X.models import Y` (use alias).
2. No `import *`.
3. Type-only imports are gated by `if TYPE_CHECKING:` and the file has
   `from __future__ import annotations` at top.
4. isort sections are in canonical order.
Reply with a markdown table: file | violation | line | fix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` (`ruff check --select I --fix`) | Sort imports (replaces isort) | `pip install ruff` ; https://docs.astral.sh/ruff/ |
| `isort` | Legacy import sorter; still useful for nuanced configs | `pip install isort` ; https://pycqa.github.io/isort/ |
| `import-linter` | Declarative architecture rules ("apps.users may not import apps.orders.models directly") | `pip install import-linter` ; https://import-linter.readthedocs.io |
| `pylint` (`--enable=cyclic-import`) | Detect circular imports | `pip install pylint` |
| `pydeps` | Visual graph of module dependencies | `pip install pydeps` ; https://pydeps.readthedocs.io |
| `mypy` / `pyright` | Static check that aliased usage typechecks; needed for `TYPE_CHECKING` block | `pip install mypy` ; https://mypy.readthedocs.io |
| `grimp` | Programmatic import-graph queries (powers import-linter) | `pip install grimp` |
| `git grep -nE "from apps\\.[a-z_]+\\.models import "` | Quick violation detector | bundled with git |
| `pre-commit` | Run ruff + import-linter before commit | https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions / GitLab CI | SaaS / OSS | yes | Run import-linter on every PR; block on contract violation. |
| import-linter | OSS | yes (CLI exits non-zero) | Declarative `[importlinter]` contracts encode the alias rule and forbidden cross-app coupling. |
| Sourcery | SaaS code review | partial | Flags general Python smells; not Django-aware out of the box. |
| Sentry / Better Stack | SaaS | n/a | Unrelated to imports, but circular-import errors at boot show up here. |
| Renovate / Dependabot | SaaS | yes | Bumps Django/DRF versions that may rename modules and break imports — agents triage these. |

## Templates & scripts

The README ships canonical examples; the missing piece for agents is a deterministic linter. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# django_import_lint.py — flag cross-app imports without alias.
# Usage: python django_import_lint.py path/to/repo
import ast, pathlib, sys

BAD: list[tuple[str, int, str]] = []

def check(path: pathlib.Path) -> None:
    try:
        tree = ast.parse(path.read_text(), filename=str(path))
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            # Cross-app: from apps.<other>.{models,services,constants} import X
            if mod.startswith("apps.") and mod.count(".") >= 2:
                tail = mod.split(".", 2)[2]
                if tail in {"models", "services", "constants"}:
                    BAD.append((str(path), node.lineno,
                        f"use `from apps.{mod.split('.')[1]} import {tail} as {mod.split('.')[1]}_{tail}`"))
            for alias in node.names:
                if alias.name == "*":
                    BAD.append((str(path), node.lineno, "wildcard import banned"))

root = pathlib.Path(sys.argv[1])
for py in root.rglob("*.py"):
    if "/migrations/" in str(py) or "/.venv/" in str(py):
        continue
    check(py)

for f, ln, msg in BAD:
    print(f"{f}:{ln}: {msg}")
sys.exit(1 if BAD else 0)
```

Wire into `pre-commit` and CI; agents that scaffold new code learn the rule by failing fast.

## Best practices
- **Pin the alias convention in `pyproject.toml`** under `[tool.ruff.lint.isort]` `known-first-party = ["apps"]` and document the alias suffix (`_models`, `_services`, `_constants`).
- **Never re-export models from `__init__.py`.** It collapses the alias rule and re-creates the original collision problem.
- **Use `TYPE_CHECKING` aggressively for cross-app type hints.** Combined with `from __future__ import annotations`, it eliminates 90% of circular import problems.
- **Migrations must use string app labels** (`"users.User"`, not `from apps.users.models import User`); enforce this with a separate ruff rule on `*/migrations/*`.
- **Keep settings.py free of app imports.** Lazy resolve with `django.apps.apps.get_model("users", "User")` when needed at runtime.
- **One alias per app per module** — don't mix `user_models` and `users_models` in the same file.
- **Document forbidden direction.** `apps.users` should not import from `apps.orders`; encode in `import-linter` contracts. Domain coupling enforced at import level prevents architectural rot.
- **Refactor in two steps**: first add the new alias and run, then mechanically delete the old direct imports.

## AI-agent gotchas
- **Default LLM output is direct imports.** Models trained on tutorials produce `from apps.users.models import User`. Always pin the prompt to the alias rule and run the linter post-generation.
- **Alias name drift.** Agents pick `users_models` one file and `user_models` the next. Force a canonical pattern and reject diffs that deviate.
- **Removing an alias usage breaks call sites.** Agents that "fix" imports often forget to update `User` → `user_models.User` references downstream. Require an AST-based rewrite, not a regex one.
- **Generated `__init__.py` re-exports.** Agents creating an `__init__.py` like to populate `__all__` from submodules — that defeats the alias intent. Keep `__init__.py` empty unless explicitly justified.
- **Circular imports masked by `TYPE_CHECKING`.** Agents wrap *runtime* imports in the gate when they shouldn't; runtime breakage at module load. Verify by booting Django (`manage.py check`) after agent edits.
- **DRF serializer `Meta.model` requires runtime symbol.** Agents put it under `TYPE_CHECKING`; serializer fails at import. Guard with a runtime import or `apps.get_model()`.
- **Migrations rewriting.** Migrations generated by `makemigrations` reference models by string; an over-eager import-fixer agent may rewrite them to use the alias and break Django's migration loader. Exclude `migrations/` paths.
- **Wildcard re-imports.** Agents trained on `from .views import *` patterns reintroduce wildcards into `urls.py`. Lint blocks this.
- **isort vs ruff conflict.** Agents installing isort separately produce different sort orders than ruff; pick one tool (`ruff`) and disable the other in `pre-commit`.
- **`apps` ambiguity.** Some Django projects keep apps at the top level (`users/`, not `apps/users/`). The rule must be re-templated; an agent reusing the README verbatim emits `from apps.X` against the wrong layout.

## References
- PEP 8 — Imports. https://peps.python.org/pep-0008/#imports
- PEP 563 — Postponed Evaluation of Annotations. https://peps.python.org/pep-0563/
- isort docs. https://pycqa.github.io/isort/
- ruff isort rules (`I` group). https://docs.astral.sh/ruff/rules/#isort-i
- import-linter docs. https://import-linter.readthedocs.io
- Adam Johnson — "How to avoid circular imports in Python." https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-avoid-circular-imports/
- Django app loading reference (`django.apps.apps.get_model`). https://docs.djangoproject.com/en/stable/ref/applications/
- Sibling methodologies in this repo: `free/dev/software-developer/django-coding-standards/`, `free/dev/software-developer/django-base-model/`, `free/dev/software-developer/django-decision-tree/`.
