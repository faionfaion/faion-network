---
slug: django-constants
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use Django's TextChoices (string enums) and IntegerChoices (int enums) for all status fields, type fields, and other string/integer enumerations.
content_id: "19c2e4657813654a"
tags: [django, constants, textchoices, enums]
---
# Django Constants and TextChoices

## Summary

**One-sentence:** Use Django's TextChoices (string enums) and IntegerChoices (int enums) for all status fields, type fields, and other string/integer enumerations.

**One-paragraph:** Use Django's TextChoices (string enums) and IntegerChoices (int enums) for all status fields, type fields, and other string/integer enumerations. Centralize numeric limits and thresholds in a constants.py module per app. Never use magic strings or numbers in model fields, services, or views — always reference named constants.

## Applies If (ALL must hold)

- Any CharField or IntegerField with a fixed set of allowed values (status, type, category, role).
- Business limits repeated across services and tests (max items, max length, page size).
- Configuration thresholds that may change over time (retry delays, rate limits).
- Any string literal used to filter querysets (filter(status="pending") must become filter(status=OrderStatus.PENDING)).

## Skip If (ANY kills it)

- Free-text fields where any string is valid (name, description, address) — those are not enums.
- Boolean flags with only two states — use BooleanField, not a two-value TextChoices.
- External API values that change independently — map them in a translation layer, not a Django enum.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/python-developer/`
