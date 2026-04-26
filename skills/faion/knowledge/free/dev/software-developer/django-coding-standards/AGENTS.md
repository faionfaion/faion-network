# Django Coding Standards

## Summary

Structural and code conventions for Django projects: `apps/` + `core/` + `config/settings/` layout, aliased cross-app imports, service-layer architecture (business logic in `services/`, HTTP-only views), keyword-only service arguments, `TextChoices` for constants, and mandatory `update_fields` on `.save()`. These rules apply to new code and refactoring targets equally.

## Why

Without explicit conventions agents put business logic in views, use bare `from apps.x.models import Y` (circular import risk), omit type hints, and forget `update_fields` on save (causing full-row writes). Consistent aliasing and service isolation make the codebase testable by default and prevent the most common review findings in Django PRs.

## When To Use

- Bootstrapping a new Django app: wiring `apps/`, `core/`, `config/settings/{base,development,production}.py`.
- Refactoring a Django repo where business logic is in views or model `save()`.
- Code-review pass enforcing "fat services, thin views" on every PR.
- Onboarding a multi-app project where circular imports are a risk.
- Generating service scaffolds + unit tests from a feature spec.

## When NOT To Use

- Single-file Django scripts or management commands under ~10 lines.
- Async-first stacks (FastAPI, Litestar) — service pattern needs async adaptation.
- Greenfield prototypes where speed over structure is acceptable for day one.
- Heavy DDD / hexagonal architecture — a richer pattern set is needed beyond this baseline.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure-and-imports.xml` | Project directory layout, import aliasing rules, settings split conventions. |
| `content/02-service-layer.xml` | Service function signature rules, `transaction.atomic`, `update_fields`, docstring requirements. |
| `content/03-views-and-constants.xml` | Thin view pattern, `TextChoices`, constants.py, common antipatterns (bare except, logic in views). |

## Templates

| File | Purpose |
|------|---------|
| `templates/ruff-django.toml` | ruff config with DJ ruleset, isort first-party apps, migration ignores. |
| `templates/service-stub.py` | Service function skeleton with type hints, keyword-only args, docstring, update_fields. |
