# Django Service Layer Pattern

## Summary

**One-sentence:** Produces a reviewed service-module diff that moves every write operation out of views and serializers into keyword-only service functions with transaction.atomic + full_clean + domain exceptions.

**One-paragraph:** All write operations (create, update, delete, side effects) belong in service functions, not in views, serializers, or model save() overrides. Services take keyword-only arguments (asterisk enforcer), wrap multi-model writes in transaction.atomic(), call full_clean() before save(), dispatch side effects through transaction.on_commit(), and raise domain exceptions instead of HTTP exceptions. This makes business logic independently testable and reusable across views, Celery tasks, admin actions, and management commands. Sister methodology to `[[django-selectors]]` (the read counterpart).

**Ефективно для:** Django/DRF backend developer refactoring a fat view or ModelViewSet into a thin view + service module before adding the next feature; CTO checkpoint when a project crosses ~10 endpoints; junior code review.

## Applies If (ALL must hold)

- Project is Django 4.2+ with at least one write endpoint (POST/PUT/PATCH/DELETE).
- Some write logic currently lives in views, serializers, or model.save() overrides.
- Business logic touches >1 model OR has side effects (email, task, audit log).
- The team has agreed to the HackSoft-style services/selectors split (or is adopting it).
- A custom exception hierarchy (ApplicationError + subclasses) either exists or can be introduced.

## Skip If (ANY kills it)

- Read-only operations — those belong in selectors, not services.
- Trivial single-model creates with no validation, no side effects, no cross-field rules — Model.objects.create() inline in the view is fine and a service adds no value.
- View-only glue (HTTP header setting, request shape munging) — that stays in the view.
- Codebase is locked to Django REST Framework generic ModelViewSet without override hooks — refactor target is invalid; use api-developer methodology first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current view file | Python | `apps/<domain>/views.py` |
| Model definitions | Python | `apps/<domain>/models.py` |
| Existing exception classes | Python | `core/exceptions.py` (or to be created) |
| Test runner config | TOML | `pyproject.toml` (pytest-django) |
| List of write entry points | Markdown | grep `request.method in ("POST", "PUT", "PATCH", "DELETE")` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[django-selectors]]` | The read-side counterpart; this methodology must coexist with it. |
| `[[django-pytest-setup]]` | The pytest runner that exercises the extracted services. |
| `[[django-imports]]` | Settles the import ordering used inside `services.py` modules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: keyword-only args, atomic, full_clean, domain exceptions, on_commit | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the service-extraction diff record + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: create-shortcut bypass, nested atomic surprise, side-effects-in-atomic, parallel-paths-after-DRF, circular-imports-via-models | ~700 |
| `content/04-procedure.xml` | medium | 6-step extraction procedure: inventory → exception scaffold → service skeleton → atomic wrap → on_commit dispatch → view slim-down | ~600 |
| `content/05-examples.xml` | recommended | Worked example: thin view + order_create service with multi-model atomic block | ~500 |
| `content/06-decision-tree.xml` | essential | Decide: extract service vs leave-inline vs build-selector based on writes/side-effects/multi-entrypoint signals | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Inventory write entry points | sonnet | Mechanical grep + classification. |
| Author exception hierarchy | sonnet | Pattern-replicable scaffold. |
| Extract service function | opus | Cross-file refactor with atomicity reasoning. |
| Wire transaction.on_commit dispatch | opus | Easy to get wrong; tasks fire before commit otherwise. |
| Trim the view | sonnet | Mechanical once the service exists. |

## Templates

| File | Purpose |
|------|---------|
| `templates/services.py` | Working skeleton for a domain `services.py` module with one create + one update service. |
| `templates/exceptions.py` | `core/exceptions.py` skeleton — `ApplicationError`, `NotFoundError`, `ValidationError`, `PermissionDeniedError`. |
| `templates/exception-handler.py` | DRF custom_exception_handler mapping domain exceptions to HTTP. |
| `templates/_smoke-test.py` | Minimum viable `order_create` service exercised by one pytest. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-service-layer.py` | Validate a service-extraction record (JSON) against the output contract: required keys, signature shape, atomic + full_clean markers. | Pre-commit on the refactor PR; gating CI step. |

## Related

- parent skill: `free/dev/python-developer/`
- `[[django-selectors]]` — the read-side sister
- `[[django-pytest-setup]]` — exercises extracted services
- `[[django-api]]` — thins the views that consume the services
- HackSoftware Django Styleguide §services — canonical external source.

## Decision tree

The decision tree at `content/06-decision-tree.xml` classifies each write endpoint: trivial single-create with no side effects → keep inline; ≥1 of {multi-model, side effects, multi-entrypoint reuse} → extract into a service; read-only path mistakenly handled here → route to `[[django-selectors]]`. The tree references rule ids from `01-core-rules.xml`.
