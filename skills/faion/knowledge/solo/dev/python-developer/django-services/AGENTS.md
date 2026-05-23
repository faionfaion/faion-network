---
slug: django-services
tier: solo
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Separates Django write logic into entity_action services with keyword-only args, full type hints, explicit @transaction.atomic, and on_commit-deferred side effects.
content_id: "67f1bcbec14acb19"
complexity: medium
produces: code
est_tokens: 5000
tags: [django, service-layer, transactions, drf, architecture]
---
# Django Services Layer

## Summary

**One-sentence:** Separates Django write logic into entity_action services with keyword-only args, full type hints, explicit @transaction.atomic, and on_commit-deferred side effects.

**One-paragraph:** Separates Django write logic into entity_action services with keyword-only args, full type hints, explicit @transaction.atomic, and on_commit-deferred side effects. Services own writes; selectors own reads; serializers validate input; views delegate. Multi-write services are @transaction.atomic; side effects use transaction.on_commit. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Django/DRF project with views that contain business logic across multiple models.
- Tests are slow or coupled to request/response cycles instead of pure functions.
- Multiple entry points (API, admin, CLI, Celery) need to invoke the same business action.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Django/DRF project with views that contain business logic across multiple models.
- Tests are slow or coupled to request/response cycles instead of pure functions.
- Multiple entry points (API, admin, CLI, Celery) need to invoke the same business action.

## Skip If (ANY kills it)

- Trivial single-model CRUD where a direct ORM call is clearer.
- Read-only operations — use selectors, not services.
- Pure property/derived value — use a @property on the model.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing view code | Django/DRF view modules | apps/<app>/views.py |
| Domain model map | model list per app | django app registry |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[decomposition-django]] | App boundaries this services live inside. |
| [[django-celery]] | Side effects deferred via on_commit when async. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-service` | sonnet | Mechanical move of view logic into a service function. |
| `decide-atomic-boundary` | opus | Cross-cutting judgement: which writes must commit together. |
| `write-selector` | sonnet | Mechanical extraction of read queries. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service.py` | Python scaffold realising the artefact in code. |
| `templates/selector.py` | Python scaffold realising the artefact in code. |
| `templates/exceptions.py` | Python scaffold realising the artefact in code. |
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-services.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[decomposition-django]]
- [[django-celery]]
- [[drf-views]]
- [[service-layer-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does the change perform writes across ≥2 models or trigger side effects?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
