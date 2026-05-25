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

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-constants.py` | Validate a constants spec JSON. | After spec emission, before codegen. |

## Related

- [[django-models]] — fields that consume the enum classes.
- [[django-quality-linting]] — lint rules that flag magic strings/numbers.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per field: is the set small + fixed + human-readable? → TextChoices. Storage-cost-critical at very large scale? → IntegerChoices. Per limit: referenced in ≥ 2 files? → constants.py UPPER_SNAKE_CASE; otherwise inline.
