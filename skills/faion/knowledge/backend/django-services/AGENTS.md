# Django Services Layer

## Summary

**One-sentence:** Separates Django write logic into entity_action services with keyword-only args, full type hints, explicit @transaction.atomic, and on_commit-deferred side effects.

**One-paragraph:** Separates Django write logic into entity_action services with keyword-only args, full type hints, explicit @transaction.atomic, and on_commit-deferred side effects. Services own writes; selectors own reads; serializers validate input; views delegate. Service functions take primitives, dataclasses or pydantic models — never a request or queryset — and return primitives, never an HttpResponse, so views, admins, management commands and Celery tasks all share one tested core. Modules are organised one per aggregate, never one per caller type, and carry no HTTP imports. Multi-write services are @transaction.atomic; side effects use transaction.on_commit. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Django/DRF project with views that contain business logic across multiple models.
- Brownfield codebases where fat views or fat models hurt testability.
- Tests are slow or coupled to request/response cycles instead of pure functions.
- Multiple entry points (API, admin, CLI, Celery) need to invoke the same business action.
- Onboarding agents and engineers to a consistent layering convention.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Django/DRF project with views that contain business logic across multiple models.
- Tests are slow or coupled to request/response cycles instead of pure functions.
- Multiple entry points (API, admin, CLI, Celery) need to invoke the same business action.

## Skip If (ANY kills it)

- Trivial single-model CRUD where a direct ORM call is clearer, or a ModelViewSet is the whole logic.
- Read-only operations — use selectors, not services.
- Pure property/derived value — use a @property on the model.
- Codebase already uses CQRS / hexagonal with explicit handlers — a different methodology applies.
- Logic is a one-off script with no reuse — no payoff from extraction.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing view code | Django/DRF view modules | apps/<app>/views.py |
| Domain model map | model list per app | django app registry |
| List of business operations + their callers (view, admin, task, cmd) | table | tech-lead |
| Pydantic or dataclass policy for service inputs/outputs | ADR | tech-lead |
| Test framework + factory library (pytest + factory_boy) | config | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[decomposition-django]] | App boundaries this services live inside. |
| [[django-celery]] | Side effects deferred via on_commit when async. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 testable rules (incl. run-the-checklist + skip-this-methodology) with rationale + source | 1600 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden patterns + allowed transformations | 1300 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom + root-cause + fix | 1300 |
| `content/04-procedure.xml` | essential | 8-step end-to-end procedure with input/action/output per step | 1300 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip and run leaves always reachable | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `operation-inventory` | sonnet | Walk the codebase, find logic in views/admin/tasks and list its callers. |
| `extract-service` | opus | Refactor must preserve behaviour while decoupling HTTP. |
| `decide-atomic-boundary` | opus | Cross-cutting judgement: which writes must commit together. |
| `write-selector` | sonnet | Mechanical extraction of read queries. |
| `test-authoring` | sonnet | Mechanical pytest cases against pure service functions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service.py` | Python scaffold realising the artefact in code. |
| `templates/selector.py` | Python scaffold realising the artefact in code. |
| `templates/exceptions.py` | Python scaffold realising the artefact in code. |
| `templates/service-module.py` | Service module skeleton with function signatures + docstrings |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-services.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[decomposition-django]]
- [[django-celery]]
- [[django-service-layer]]
- [[logging-patterns]]
- [[database-design]]

Runtime notes for agents — where the layer fails, CLI tools, services and AI-agent gotchas — live in
`agent-integration.md` beside this file.

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does the change perform writes across ≥2 models, trigger side effects, or carry logic reused by more than one caller?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly, and the run-the-checklist branch is the all-gates-green approval leaf. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/service.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Python scaffold realising the artefact in code.","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#entity-action-naming","token_budget_impact":"~150 tokens when loaded"}}
"""Django Services Layer scaffold. See AGENTS.md for context and content/02-output-contract.xml for the contract."""
from __future__ import annotations

# Minimal scaffold for the django-services methodology.
# Replace this stub with real implementation; keep the header intact.

def main() -> int:
    """Entrypoint; returns exit code."""
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### `templates/selector.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Python scaffold realising the artefact in code.","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#entity-action-naming","token_budget_impact":"~150 tokens when loaded"}}
"""Django Services Layer scaffold. See AGENTS.md for context and content/02-output-contract.xml for the contract."""
from __future__ import annotations

# Minimal scaffold for the django-services methodology.
# Replace this stub with real implementation; keep the header intact.

def main() -> int:
    """Entrypoint; returns exit code."""
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### `templates/exceptions.py`

```python
"""Django Services Layer scaffold. See AGENTS.md for context and content/02-output-contract.xml for the contract."""
from __future__ import annotations

# Minimal scaffold for the django-services methodology.
# Replace this stub with real implementation; keep the header intact.

def main() -> int:
    """Entrypoint; returns exit code."""
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### `templates/service-module.py`

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import transaction

if TYPE_CHECKING:
    from apps.<app>.models import <Model>
    from apps.users.models import User


class <Feature>Error(Exception):
    """Domain errors raised by <feature> service."""


@transaction.atomic
def <verb>_<noun>(
    user: "User",
    *,
    param: str,
) -> "<Model>":
    """One-line summary.

    Business logic:
    - bullet describing each rule

    Args:
        user: User performing the action.
        param: Description.

    Returns:
        The created/updated <Model> instance.

    Raises:
        <Feature>Error: When a business rule is violated.
    """
    from apps.<app>.models import <Model>

    try:
        obj = <Model>.objects.select_for_update().get(field=param)
    except <Model>.DoesNotExist:
        raise <Feature>Error(f"<Model> {param!r} not found")

    # mutate
    obj.field = ...
    obj.save(update_fields=["field", "updated_at"])
    return obj
```
