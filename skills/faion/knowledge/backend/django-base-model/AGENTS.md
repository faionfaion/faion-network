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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/base_model.py`

```python
"""

from __future__ import annotations

import uuid

from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone


class TimestampMixin(models.Model):
    """Adds created_at and updated_at to any model."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UidMixin(models.Model):
    """Adds a public-facing UUID `uid` while keeping integer `id` as the PK."""

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """Overrides delete() at the QuerySet level — without this, bulk deletes hard-delete."""

    def delete(self):  # type: ignore[override]
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Default manager: only live rows. Pair with `all_objects = models.Manager()` on the model."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # required: gives admin / loaddata access to every row

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):  # type: ignore[override]
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self) -> None:
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])


class BaseModel(TimestampMixin, UidMixin):
    class Meta:
        abstract = True


class SoftDeletableModel(TimestampMixin, UidMixin, SoftDeleteMixin):
    class Meta:
        abstract = True


# Example concrete model showing the partial-unique pattern required by r3.
# class Customer(SoftDeletableModel):
#     email = models.EmailField()
#
#     class Meta:
#         constraints = [
#             UniqueConstraint(
#                 fields=["email"],
#                 condition=Q(deleted_at__isnull=True),
#                 name="unique_active_customer_email",
#             ),
#         ]
```

### `templates/base-model-spec.json`

```json
{
  "_purpose": "Reference base-model spec output.",
  "_consumes": "ERD + soft-delete scope + tenant scope.",
  "_produces": "JSON for codegen.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~150 tokens.",
  "artefact_id": "billing-base-model-spec",
  "owner": "ruslan@faion.net",
  "django_version": "5.2.1",
  "db_engine": "postgresql",
  "bases": [
    {
      "name": "BaseModel",
      "abstract": true,
      "mixins": [
        "TimestampMixin",
        "UidMixin"
      ]
    },
    {
      "name": "SoftDeletableModel",
      "abstract": true,
      "mixins": [
        "TimestampMixin",
        "UidMixin",
        "SoftDeleteMixin"
      ]
    }
  ],
  "models": [
    {
      "name": "Customer",
      "extends": "SoftDeletableModel",
      "soft_delete": true,
      "exposes_uid": true,
      "tenant_scoped": false,
      "unique_fields": [
        "email"
      ],
      "foreign_keys": []
    },
    {
      "name": "Order",
      "extends": "SoftDeletableModel",
      "soft_delete": true,
      "exposes_uid": true,
      "tenant_scoped": false,
      "unique_fields": [],
      "foreign_keys": [
        {
          "field": "customer",
          "on_delete": "PROTECT",
          "reason": "Retain order history even when Customer is soft-deleted; compliance requires 7y retention."
        }
      ]
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
