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
| `content/01-core-rules.xml` | essential | 10 testable rules: PEP 8 order, absolute > multi-dot, mandatory aliases, string FKs, apps.get_model, TYPE_CHECKING, core/ extraction, ruff config | ~1400 |
| `content/02-output-contract.xml` | essential | JSON schema for imports spec | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: unaliased cross-app, wildcard, __future__ in serializers, PEP 810 on 3.13, multi-dot relative | ~900 |
| `content/04-procedure.xml` | medium | 5 steps: order → alias → FK refs → ruff config → CI gate | ~600 |
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
| `templates/find-circular-imports.sh` | Shell script that runs python -c "import …" against every app to surface circulars. |
| `templates/imports-spec.json` | Reference output document. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-imports.py` | Validate an imports spec JSON against the methodology contract. | After spec emission, before pyproject.toml updates. |

## Related

- [[django-project-structure]] — `apps/` layout that this spec assumes.
- [[django-models]] — string FK references referenced by rule r6.
- [[django-quality-linting]] — ruff rule set this spec extends.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree routes each cross-app dependency: model field at module level → string FK ref. Service that needs runtime model class → apps.get_model(). Type annotation only → TYPE_CHECKING block. ≥ 3 apps cyclically depending → extract to core/.
