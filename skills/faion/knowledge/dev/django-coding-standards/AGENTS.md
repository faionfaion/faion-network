# Django Coding Standards

## Summary

**One-sentence:** Produces a Django code-layout standard: apps/ + core/ + config/ tree, aliased cross-app imports, service-layer logic, keyword-only args, TextChoices, update_fields on saves.

**One-paragraph:** Produces a Django code-layout standard: apps/ + core/ + config/ tree, aliased cross-app imports, service-layer logic, keyword-only args, TextChoices, update_fields on saves. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Project uses Django 5.x (or 4.2 LTS) with Python 3.12+.
- Code in question lives under `apps/<app>/` or `core/` per the django-coding-standards layout.
- A test runner is configured (`pytest + pytest-django`).
- The team has agreed to enforce service-layer logic separation.

## Skip If (ANY kills it)

- Project is not on Django (FastAPI, Flask, or other) — load the framework-specific methodology instead.
- Tiny throwaway tool with no growth horizon — overhead exceeds payoff.
- Codebase has not adopted the apps/core/config layout and refactoring it is out of scope right now.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `pyproject.toml` | TOML | repo root |
| `apps/<app>/` layout | directory tree | repo source |
| Target Django version | string | `pyproject.toml` |
| Existing test runner config | TOML | `pyproject.toml` `[tool.pytest.ini_options]` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-typing` | Type-checker baseline for Django code. |
| `free/dev/software-developer/django-coding-standards` | Layout standard that gates placement of files produced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to django-coding-standards | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold model/serializer/view/test from spec | sonnet | Mechanical code generation. |
| Design service-layer boundaries | opus | Needs domain judgement. |
| Audit existing code for layering violations | sonnet | Pattern matching with deterministic output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ruff-django.toml` | ruff config tuned for Django (DJ + B + E + F + I + UP). |
| `templates/service-stub.py` | Service-layer module skeleton with @transaction.atomic. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-coding-standards.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-models]] — see methodology AGENTS.md for context.
- [[django-pytest]] — see methodology AGENTS.md for context.
- [[django-api]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ruff-django.toml`

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "DJ", "T20", "RUF", "PT"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["apps", "core", "config"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.lint.per-file-ignores]
"**/migrations/*.py" = ["E", "F", "UP"]
"**/tests/*.py" = ["S101"]
```

### `templates/service-stub.py`

```python
"""Service stub template for Django service-layer functions."""
from django.db import transaction


def do_something(
    entity: Entity,
    param: str,
    *,
    optional_flag: bool = True,
) -> Entity:
    """
    One-line description of what this service does.

    Args:
        entity: The primary domain object being acted on
        param: Description of the parameter
        optional_flag: Description of the optional flag

    Returns:
        The modified Entity instance

    Raises:
        Entity.DoesNotExist: If entity is not found
        ValidationError: If precondition is violated
    """
    # 1. Load and lock if mutating
    obj = Entity.objects.select_for_update().get(pk=entity.pk)

    # 2. Guard preconditions
    # if obj.already_done:
    #     raise ValidationError("Already processed")

    # 3. Apply changes — always list all modified fields
    obj.some_field = param
    obj.save(update_fields=["some_field", "updated_at"])

    # 4. Enqueue side effects after commit
    if optional_flag:
        transaction.on_commit(lambda: side_effect_task.delay(obj.pk))

    return obj
```
