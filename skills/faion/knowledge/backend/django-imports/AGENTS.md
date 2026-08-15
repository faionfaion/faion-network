# Django Import Patterns

## Summary

**One-sentence:** Produces an imports spec naming the PEP 8 section order, the cross-app alias convention (mandatory), the TYPE_CHECKING block usage, the string FK reference rule, and the ruff configuration that enforces it all.

**Ефективно для:** Multi-app Django repos where two apps will eventually have a `User` model, where DRF serializers crash from `from __future__ import annotations`, and where circular ImportError surfaces in CI but not in dev.

**One-paragraph:** Codifies "where do imports live and how are they aliased?" into one spec. Output names the imports.section_order, the alias_convention (apps.users → user_models), the type_checking_policy, the FK reference style (string vs class), the apps.get_model() boundary, and the ruff config that automates enforcement. Forbids: unaliased cross-app imports, multi-dot relative imports, wildcard imports, `from __future__ import annotations` in DRF serializer files, PEP 810 lazy imports on Python &lt; 3.14.

## Applies If (ALL must hold)

- Django ≥ 5.0 project with at least 2 apps that import each other.
- Python ≥ 3.11.
- A tool exists (ruff or isort) to enforce import order automatically.
- Repo has CI on PRs (pre-commit / GitHub Actions) where the rules can run.
- Output drives the ruff config + the per-PR import-discipline review.

## Skip If (ANY kills it)

- Single-app project — alias rules add noise without benefit.
- Codebase already uses a `core.imports` central re-export shim — direct imports defeat the shim.
- One-off management commands where readability beats convention.
- Pure data pipelines (Airflow, Prefect) — Django ORM rarely involved.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| List of apps with cross-app dependencies | bullets | `apps/` folder + grep |
| Python version + Django version | semver | pyproject.toml |
| Existing ruff / isort config | TOML | pyproject.toml |
| List of circular import incidents (last 90d) | bullets | CI history |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-project-structure]]` | apps/ layout assumed here. |
| `[[django-quality-linting]]` | ruff rule set this spec extends. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 11 testable rules: PEP 8 section order, absolute cross-app + relative in-app, no multi-dot relative, mandatory aliases, circular-strategy ladder, string FKs, apps.get_model, TYPE_CHECKING, core/ extraction, ruff first-party, no star imports | ~1800 |
| `content/02-output-contract.xml` | essential | JSON schema for imports spec | ~900 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: unaliased cross-app, wildcard, __future__ in serializers, PEP 810 on 3.13, multi-dot relative, misconfigured first-party, type-only import at runtime | ~1150 |
| `content/04-procedure.xml` | medium | 6 steps: enumerate apps → policies → ruff config → FK strategy → wire the lint → validate | ~750 |
| `content/06-decision-tree.xml` | essential | Per cross-app dependency: model field vs runtime service vs type-only | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_cross_app_deps` | haiku | Mechanical: grep imports. |
| `emit_imports_spec` | sonnet | Bounded transformation. |
| `audit_for_circular` | opus | Cross-checks runtime + type-only + load order. |

## Templates

| File | Purpose |
|---|---|
| `templates/ruff-isort-config.toml` | Ruff config snippet that enforces sections + aliases. |
| `templates/find-circular-imports.sh` | Grep audit for unaliased cross-app imports, multi-dot relatives and wildcards in an existing tree. |
| `templates/django_import_lint.py` | AST pre-commit hook failing the build on a bare cross-app symbol import, a multi-dot relative or a wildcard. |
| `templates/imports-spec.json` | Reference output document. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-imports.py` | Validate an imports spec JSON against the methodology contract. | After spec emission, before pyproject.toml updates. |

## Related

- [[django-project-structure]] — `apps/` layout that this spec assumes.
- [[django-models]] — string FK references referenced by rule r6.
- [[django-quality-linting]] — ruff rule set this spec extends.
- [[django-coding-standards]] — the apps/core/config layout `known-first-party` names.
- [[python-typing]] — the type-checker whose annotations rule r8 keeps out of the runtime.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree routes each cross-app dependency: model field at module level → string FK ref. Service that needs runtime model class → apps.get_model(). Type annotation only → TYPE_CHECKING block. ≥ 3 apps cyclically depending → extract to core/.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ruff-isort-config.toml`

```toml
# ruff isort config for Django multi-app projects
# Add to pyproject.toml — adjust known-first-party to match your project structure

[tool.ruff.lint]
select = [
    "I",   # isort
    "E",   # pycodestyle
    "F",   # pyflakes
    "UP",  # pyupgrade
    "B",   # bugbear
    "T20", # no print()
    "DJ",  # flake8-django
]

[tool.ruff.lint.isort]
# Your Django apps namespace — ruff treats these as first-party
known-first-party = ["apps", "config", "core"]

# Import section order: stdlib → third-party → first-party → local
section-order = [
    "future",
    "standard-library",
    "third-party",
    "first-party",
    "local-folder",
]

# Force each import section onto its own line group
force-sort-within-sections = false

# Django-specific: keep related imports grouped
combine-as-imports = false

# Explicit section for Django itself (optional — helps large projects)
known-third-party = [
    "django",
    "rest_framework",
    "celery",
    "redis",
    "boto3",
]

# Lines between sections
lines-between-types = 0
lines-after-imports = 2

# ─── Usage ───────────────────────────────────────────────────────────────────
# Run: ruff check --select I --fix .
# Pre-commit hook:
# - repo: https://github.com/astral-sh/ruff-pre-commit
#   rev: v0.8.0
#   hooks:
#     - id: ruff
#       args: [--select, I, --fix]
```

### `templates/find-circular-imports.sh`

```bash
#!/usr/bin/env bash
# find-circular-imports.sh — Grep for unaliased cross-app model imports likely to cause circular deps.
# Run from project root. Adjust APP_PREFIX to your project's apps namespace.

set -euo pipefail

APP_PREFIX=${1:-apps}
SRC_DIR=${2:-.}

echo "==> Scanning for unaliased cross-app imports in $SRC_DIR (prefix: $APP_PREFIX)..."
echo ""

# Pattern 1: Direct model import from another app (unaliased)
# e.g. "from apps.users.models import User" — should be aliased
echo "── Unaliased cross-app model imports ──────────────────────────────────"
grep -rn \
    --include="*.py" \
    --exclude-dir=".git" \
    --exclude-dir="migrations" \
    -E "from ${APP_PREFIX}\.[a-z_]+\.(models|services|selectors) import [A-Z]" \
    "$SRC_DIR" || echo "  (none found)"

echo ""

# Pattern 2: Multi-dot relative imports (should be absolute)
echo "── Multi-dot relative imports (fragile) ───────────────────────────────"
grep -rn \
    --include="*.py" \
    --exclude-dir=".git" \
    --exclude-dir="migrations" \
    -E "^from \.\.(\.*)?" \
    "$SRC_DIR" || echo "  (none found)"

echo ""

# Pattern 3: Star imports
echo "── Wildcard imports (never allowed) ───────────────────────────────────"
grep -rn \
    --include="*.py" \
    --exclude-dir=".git" \
    -E "^from .+ import \*" \
    "$SRC_DIR" || echo "  (none found)"

echo ""
echo "==> Scan complete."
echo ""
echo "Fix: Replace unaliased imports with:"
echo "  from ${APP_PREFIX}.users import models as user_models"
echo "  # then use: user_models.User"
```

### `templates/imports-spec.json`

```json
{
  "_purpose": "Reference Django imports spec output.",
  "_consumes": "apps list + Python/Django versions + existing ruff config.",
  "_produces": "JSON for pyproject.toml update + PR review.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~140 tokens.",
  "artefact_id": "faion-net-be-imports",
  "owner": "ruslan@faion.net",
  "django_version": "5.2.1",
  "python_version": "3.12",
  "apps": [
    "accounts",
    "billing",
    "content",
    "core"
  ],
  "policies": {
    "section_order": [
      "future",
      "stdlib",
      "third-party",
      "first-party",
      "local"
    ],
    "alias_convention": "from apps.<app> import models as <app>_models",
    "fk_reference_style": "string-for-cross-app",
    "type_checking_policy": "mandatory-for-cross-app-types",
    "wildcard_allowed": false,
    "multi_dot_relative_allowed": false
  },
  "ruff_config": {
    "known_first_party": [
      "apps",
      "config",
      "core"
    ],
    "section_order": [
      "future",
      "standard-library",
      "third-party",
      "first-party",
      "local-folder"
    ]
  },
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/django_import_lint.py`

```python
import ast
import pathlib
import sys

BAD: list[tuple[str, int, str]] = []


def check(path: pathlib.Path) -> None:
    try:
        tree = ast.parse(path.read_text(), filename=str(path))
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        mod = node.module or ""
        # Cross-app: from apps.<other>.<module> import X (direct symbol import)
        if mod.startswith("apps.") and mod.count(".") >= 2:
            tail = mod.split(".", 2)[2]
            if tail in {"models", "services", "selectors", "constants", "serializers"}:
                app = mod.split(".")[1]
                BAD.append((
                    str(path),
                    node.lineno,
                    f"use `from apps.{app} import {tail} as {app}_{tail}` "
                    f"instead of `from {mod} import ...`",
                ))
        # Multi-dot relative imports
        if node.level and node.level > 1:
            BAD.append((str(path), node.lineno,
                        "multi-dot relative import banned; use the absolute apps.<app> path"))
        # Wildcard imports
        for alias in node.names:
            if alias.name == "*":
                BAD.append((str(path), node.lineno, "wildcard import banned"))


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print(__doc__ or "usage: django_import_lint.py <repo-root>")
        return 0 if argv[1:2] in ([], ["-h"], ["--help"]) else 2
    root = pathlib.Path(argv[1])
    for py in root.rglob("*.py"):
        s = str(py)
        if "/migrations/" in s or "/.venv/" in s or "/node_modules/" in s:
            continue
        check(py)
    for f, ln, msg in BAD:
        print(f"{f}:{ln}: {msg}")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```
