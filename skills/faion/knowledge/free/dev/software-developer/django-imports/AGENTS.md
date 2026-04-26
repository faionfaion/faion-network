# Django Import Patterns

## Summary

A convention for Django multi-app projects: always import cross-app modules via alias (`from apps.orders import models as order_models`), never via direct symbol import (`from apps.orders.models import Order`). Import order: `__future__`, stdlib, third-party (Django/DRF), cross-app aliased, relative. Type-only cross-app imports go under `if TYPE_CHECKING:` with `from __future__ import annotations` at the file top.

## Why

In Django projects with many apps, model names collide: `User`, `Order`, `Item` appear in multiple apps. Direct imports create ambiguity in call sites and make grep-based refactoring unreliable. The alias convention (`order_models.Order`) makes the source app explicit at every usage, eliminates name collisions, and enables reliable tooling (import-linter, AST fixers) to enforce cross-app coupling constraints.

## When To Use

- New Django project: lock down import style before apps proliferate.
- Onboarding multi-app codebases where `Order`, `User`, `Item` collide in serializers.
- Refactoring legacy code with `from app.models import *` patterns.
- Adding type hints to a Django codebase with circular import problems.
- Authoring pre-commit hooks to enforce the alias rule.

## When NOT To Use

- Single-app Django projects with fewer than 10 models — alias overhead pays nothing.
- Non-Django Python repos with flat package structure — rule is Django-app-specific.
- DRF serializers and form classes where direct symbol import is idiomatic (`from rest_framework import serializers`).
- One-shot scripts and Jupyter notebooks where unaliased names are more readable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Cross-app alias rule, import order tiers, TYPE_CHECKING pattern, migration exclusion rule |
| `content/02-examples.xml` | Correct alias imports, bad direct imports, type-hint with __future__, Python 3.10+ syntax |
| `content/03-antipatterns.xml` | Antipatterns: bare cross-app import, wildcard, re-export via __init__.py, runtime under TYPE_CHECKING |

## Templates

| File | Purpose |
|------|---------|
| `templates/django_import_lint.py` | AST linter: flags cross-app imports without alias and wildcard imports |
