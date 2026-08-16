# Django Constants and TextChoices

## Summary

**One-sentence:** Produces a per-app `constants.py` spec — every status/type/role enum as TextChoices or IntegerChoices, every business limit as UPPER_SNAKE_CASE — so models, services, and tests never reference magic strings or numbers.

**Ефективно для:** Django apps where status comparisons are written as `order.status == "pending"`, business limits are scattered (`if user.orders.count() >= 50`), and rename refactors silently miss a string somewhere.

**One-paragraph:** Codifies the recurring "where do enum values and limits live?" decision. Output names each enum class (TextChoices for human-readable strings, IntegerChoices only when storage size matters at very large scale), declares its members, and lists named limits as constants. Forbids raw string filters, magic numbers in services, and switching enum types after data is in production.

## Applies If (ALL must hold)

- Django ≥ 4.2 (TextChoices is 3.0+).
- App has at least one CharField/IntegerField with a fixed set of allowed values.
- App has at least one business limit referenced in more than one file.
- The team commits to compare enum-to-enum, never enum-to-string.
- Output drives the codegen of constants.py + the lint pass that flags magic literals.

## Skip If (ANY kills it)

- Free-text fields (name, description, address) — not enums.
- Boolean two-state flags — use BooleanField, not TextChoices.
- External API values that change independently — map in a translation layer.
- One-off scripts where centralised constants are pure overhead.
- App already uses django-model-utils Choices class consistently — don't add a parallel system.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| List of enum candidate fields | bullets | grep for `choices=` in models |
| List of business limits referenced ≥ twice | bullets | grep for numeric literals in services |
| App name | string | repo apps/ folder |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[django-models]]` | Field definitions consuming the choices=. |
| `[[django-imports]]` | Import order for constants in models.py / services.py. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: TextChoices everywhere, constants.py per app, UPPER_SNAKE limits, enum-to-enum compare, .label not dict-lookup | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the constants spec | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: magic strings, dict-of-tuples for label, integer-after-text swap, scattered limits | ~700 |
| `content/06-decision-tree.xml` | essential | Per-field: enum-y? → TextChoices vs IntegerChoices. Per-limit: cross-file? → constants.py | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_enum_candidates` | haiku | Mechanical: grep models + services. |
| `emit_constants_spec` | sonnet | Bounded transformation: assign members + limits. |

## Templates

| File | Purpose |
|---|---|
| `templates/constants.py` | Reference per-app constants.py with one TextChoices + one IntegerChoices + named limits. |
| `templates/constants-spec.json` | Reference output document. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-constants.py` | Validate a constants spec JSON. | After spec emission, before codegen. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-models]] — fields that consume the enum classes.
- [[django-quality-linting]] — lint rules that flag magic strings/numbers.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per field: is the set small + fixed + human-readable? → TextChoices. Storage-cost-critical at very large scale? → IntegerChoices. Per limit: referenced in ≥ 2 files? → constants.py UPPER_SNAKE_CASE; otherwise inline.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/constants.py`

```python
"""

from __future__ import annotations

from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending Payment"
    PAID = "paid", "Paid"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class UserRole(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Administrator"
    MEMBER = "member", "Member"
    VIEWER = "viewer", "Viewer"


# Business limits — referenced by services, models, and tests.
# Reviewed quarterly per ops/limits-policy.md.
MAX_ORDERS_PER_USER: int = 100
DEFAULT_PAGE_SIZE: int = 25
MAX_PAGE_SIZE: int = 100
ORDER_CANCEL_WINDOW_HOURS: int = 24
RETRY_BACKOFF_SECONDS: tuple[int, ...] = (1, 5, 30, 120)
```

### `templates/constants-spec.json`

```json
{
  "_purpose": "Reference per-app constants spec output.",
  "_consumes": "Enum field list + cross-file limit list.",
  "_produces": "JSON for constants.py codegen.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~150 tokens.",
  "artefact_id": "orders-constants",
  "owner": "ruslan@faion.net",
  "app": "orders",
  "django_version": "5.2.1",
  "enums": [
    {
      "name": "OrderStatus",
      "kind": "TextChoices",
      "members": [
        {
          "name": "PENDING",
          "value": "pending",
          "label": "Pending Payment"
        },
        {
          "name": "PAID",
          "value": "paid",
          "label": "Paid"
        },
        {
          "name": "SHIPPED",
          "value": "shipped",
          "label": "Shipped"
        },
        {
          "name": "DELIVERED",
          "value": "delivered",
          "label": "Delivered"
        },
        {
          "name": "CANCELLED",
          "value": "cancelled",
          "label": "Cancelled"
        }
      ]
    }
  ],
  "limits": [
    {
      "name": "MAX_ORDERS_PER_USER",
      "value": 100,
      "rationale": "Compliance + abuse cap; reviewed quarterly."
    },
    {
      "name": "DEFAULT_PAGE_SIZE",
      "value": 25,
      "rationale": "Matches mobile UI list size."
    },
    {
      "name": "MAX_PAGE_SIZE",
      "value": 100,
      "rationale": "Hard cap to prevent table scans."
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
