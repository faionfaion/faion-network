---
slug: django-base-model
tier: free
group: dev
domain: python-developer
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django abstract base-model spec (BaseModel + TimestampMixin + SoftDeleteMixin + UUID uid + managers) for a Django 5.2 LTS project.
content_id: "92b341f8e2fd8c45"
complexity: deep
produces: spec
est_tokens: 4500
tags: [django, models, abstract-base, uuid, soft-delete, timestamps]
---

# Django Base Model Pattern

## Summary

**One-sentence:** Produces a Django abstract base-model spec — BaseModel with separate `uid` UUID field, TimestampMixin with auto_now / auto_now_add, SoftDeleteMixin with manager + queryset overrides, partial-unique-constraints — for a Django 5.x project.

**Ефективно для:** Bootstrapping a new Django project or refactoring a legacy app where every model duplicates created_at/updated_at, ad-hoc soft-delete flags, and auto-increment IDs leak through public APIs.

**One-paragraph:** Codifies the recurring "what does our model base look like?" decision into a spec the codegen agent can apply identically to every concrete model. The output names the abstract bases (BaseModel, TimestampMixin, SoftDeleteMixin, TenantAwareModel where applicable), the UUID strategy (separate `uid` field — NEVER swap primary keys retroactively), the manager + queryset overrides for soft-delete, and the partial unique constraints required when soft-delete is enabled. Forbids: PK swap to UUID, unique=True on soft-deletable fields without a partial index, default manager shadowing without `all_objects`, CASCADE through soft-delete.

## Applies If (ALL must hold)

- Django ≥ 5.0 (5.2 LTS preferred); Python ≥ 3.11.
- Project has ≥ 2 concrete models that benefit from shared timestamps / soft delete / external IDs.
- Soft-delete or audit-trail is a real domain requirement (orders, accounts, posts) or external API exposes opaque IDs (uid).
- Team commits to abstract-base inheritance rather than mixin-soup.
- Output drives codegen of concrete models and migration review.

## Skip If (ANY kills it)

- One-off scripts / admin commands that don't define new models.
- Tables managed outside Django (`Meta.managed = False`) — abstract bases don't combine cleanly.
- Performance-critical analytical tables where 16-byte UUID + indexes per row are wasteful.
- Repo already standardised on django-model-utils TimeStampedModel — don't add a parallel set.
- Ephemeral data (cache, signed tokens) where timestamps + soft-delete are pure noise.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| List of concrete domain models | bullets | feature brief / ERD |
| Django + DB engine versions | semver + name | `requirements.txt` + settings |
| Soft-delete scope (which models) | YAML | product / compliance decision |
| External API ID-exposure list | YAML | API spec |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-models]]` | Concrete model conventions (Meta options, indexes, constraints) consumed downstream. |
| `[[django-project-structure]]` | Apps + base/ module placement. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: separate uid field, abstract bases, partial unique under soft-delete, manager + queryset override, all_objects preserved, CASCADE audit, tenant context | ~1300 |
| `content/02-output-contract.xml` | essential | JSON schema for the base-model spec | ~1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: PK swap, missing partial unique, manager shadowing, CASCADE through soft-delete | ~800 |
| `content/04-procedure.xml` | deep | 6 steps: bases → uid → timestamps → soft-delete scope → tenant → emit | ~700 |
| `content/05-examples.xml` | deep | One worked example: Order + Customer with full base hierarchy | ~600 |
| `content/06-decision-tree.xml` | essential | Per-model: needs soft-delete? needs tenant? needs uid? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_models` | haiku | Mechanical extraction from the ERD. |
| `emit_base_spec` | sonnet | Bounded transformation: bases + manager + constraints. |
| `audit_constraints` | opus | Cross-checks unique constraints + soft-delete + cascade edges. |

## Templates

| File | Purpose |
|---|---|
| `templates/base_model.py` | BaseModel + TimestampMixin + SoftDeleteMixin + managers reference. |
| `templates/base-model-spec.json` | Reference output document. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-base-model.py` | Validate a base-model spec JSON. | After the spec is emitted, before codegen runs. |

## Related

- [[django-models]] — concrete model patterns built on top.
- [[django-pytest-fixtures]] — fixtures that respect soft-delete + tenant context.
- [[django-api]] — DRF/Ninja serializers expose `uid`, not `id`.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree branches per concrete model: needs soft-delete? → SoftDeleteMixin + partial unique. exposes public API? → `uid` UUID field. tenant-scoped? → TenantAwareModel + tenant_context wrapper.
