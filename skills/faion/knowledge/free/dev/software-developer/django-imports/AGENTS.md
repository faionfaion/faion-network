---
slug: django-imports
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A convention for Django multi-app projects: always import cross-app modules via alias (from apps.
content_id: "9b3df72f9d943b7e"
tags: [django, imports, conventions, refactoring, lint]
---
# Django Import Patterns

## Summary

**One-sentence:** A convention for Django multi-app projects: always import cross-app modules via alias (from apps.

**One-paragraph:** A convention for Django multi-app projects: always import cross-app modules via alias (from apps.orders import models as order_models), never via direct symbol import (from apps.orders.models import Order). Import order: __future__, stdlib, third-party (Django/DRF), cross-app aliased, relative. Type-only cross-app imports go under if TYPE_CHECKING: with from __future__ import annotations at the file top.

## Applies If (ALL must hold)

- New Django project: lock down import style before apps proliferate.
- Onboarding multi-app codebases where Order, User, Item collide in serializers.
- Refactoring legacy code with from app.models import * patterns.
- Adding type hints to a Django codebase with circular import problems.
- Authoring pre-commit hooks to enforce the alias rule.

## Skip If (ANY kills it)

- Single-app Django projects with fewer than 10 models — alias overhead pays nothing.
- Non-Django Python repos with flat package structure — rule is Django-app-specific.
- DRF serializers and form classes where direct symbol import is idiomatic (from rest_framework import serializers) — the rule applies to cross-app project imports only.
- One-shot scripts and Jupyter notebooks where unaliased names are more readable.

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

- parent skill: `free/dev/software-developer/`
