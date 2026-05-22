---
slug: django-models
tier: free
group: dev
domain: python-developer
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django models spec (BaseModel inheritance, TextChoices, on_delete choice with rationale, indexes, constraints, full_clean policy) for a Django 5.x app.
content_id: "0700366d46fa49cb"
complexity: deep
produces: spec
est_tokens: 4500
tags: [django, models, querysets, indexes, constraints]
---

# Django Models

## Summary

**One-sentence:** Produces a per-app models spec — every model's BaseModel inheritance, choices class, on_delete + rationale, db_index + composite indexes, Meta.constraints, and the service-layer full_clean policy.

**Ефективно для:** Django apps where models drift toward 200-line classes carrying business logic, where ad-hoc `CASCADE` on user FKs has caused data loss, and where missing indexes turn list endpoints into table scans.

**One-paragraph:** Turns "what does a thin Django model look like?" into one auditable spec the reviewer can apply identically to every new model. The output names every field, the choices class, every FK with on_delete + reason, every constraint, every index with a justification, and the service-layer rule that full_clean() runs before save(). Forbids: business logic in models, raw string choices, default CASCADE on user references, db_index without justification, GeneratedField on non-PostgreSQL.

## Applies If (ALL must hold)

- Django ≥ 5.0 + chosen DB engine documented (PostgreSQL preferred).
- App has ≥ 1 domain model with state, validation, or relationships.
- Team commits to thin models + service layer.
- Output drives codegen of models.py + migrations review.
- Audit pass on existing models.py is in scope.

## Skip If (ANY kills it)

- ORM-less project (SQLAlchemy / Tortoise / SQLModel) — methodology doesn't translate.
- Read-only analytical / reporting model backed by external warehouse views.
- Quick prototype using Django Admin defaults only.
- Codebase already moved to a different ORM.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| ERD or model list | bullets / diagram | product doc |
| BaseModel decisions | spec or code | [[django-base-model]] output |
| DB engine + version | text | settings |
| Soft-delete + PII scope list | YAML | compliance |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-base-model]]` | Abstract bases this models spec extends. |
| `[[django-constants]]` | TextChoices/IntegerChoices classes consumed here. |
| `[[django-imports]]` | String FK refs and import style assumed here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 13 testable rules: BaseModel, thin models, TextChoices, on_delete deliberate, Meta constraints, full_clean, QuerySet methods, indexes with justification, partial indexes pg-only, select_related defaults, clean(), db_default, no soft-delete for PII | ~1500 |
| `content/02-output-contract.xml` | essential | JSON schema for the models spec | ~1000 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: direct models.Model, missing full_clean, exposing id, GeneratedField on SQLite, auto-squash migrations, blanket db_index, field reorder | ~900 |
| `content/04-procedure.xml` | deep | 6 steps: extend BaseModel → declare fields → constraints → indexes → on_delete audit → full_clean wiring | ~700 |
| `content/05-examples.xml` | deep | One worked example: Invoice with constraints, indexes, partial-unique | ~600 |
| `content/06-decision-tree.xml` | essential | on_delete choice tree + index choice tree | ~250 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_fields` | haiku | Mechanical extraction from ERD. |
| `emit_models_spec` | sonnet | Bounded transformation: fields + constraints + indexes. |
| `review_for_perf_security` | opus | Index + on_delete + PII audit. |

## Templates

| File | Purpose |
|---|---|
| `templates/base_model.py` | Reference BaseModel implementation (mirrors django-base-model). |
| `templates/django-model-lint.sh` | grep-based audit script for common antipatterns. |
| `templates/models-spec.json` | Reference output document. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-models.py` | Validate models spec against contract. | After spec emission. |

## Related

- [[django-base-model]] — abstract bases inherited by every model here.
- [[django-constants]] — enum classes consumed by choices=.
- [[django-pytest-fixtures]] — fixtures built on top of the model spec.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per FK: parent is user/account → PROTECT or SET_NULL; child-without-parent has no meaning → CASCADE (only). Per field used in filter()/order_by() on production traffic → add db_index OR composite Index with justification. Per cross-field invariant → CheckConstraint (pg) or clean() (cross-engine).
