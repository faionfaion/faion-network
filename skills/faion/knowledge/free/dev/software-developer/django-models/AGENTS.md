# Django Models

## Summary

Django model design following the `BaseModel` abstract pattern (integer PK + UUID field + timestamps), with explicit `on_delete` on every ForeignKey, `TextChoices` enums in per-app `constants.py`, and composite `Meta.indexes` for query-driven indexing. Django 5 `db_default` is supported for database-computed defaults.

## Why

A consistent `BaseModel` base eliminates timestamp/UUID boilerplate and gives every record a stable external identifier (`uid`) separate from the internal integer PK. Explicit `on_delete` prevents accidental data loss. `TextChoices` centralizes enum values so admin, forms, and serializers share one source. Declaring indexes in `Meta.indexes` keeps them reviewable in migrations.

## When To Use

- Creating a new Django app's `models/` package.
- Refactoring ad-hoc models to the canonical `BaseModel` + `Meta.indexes` shape.
- Adding ForeignKey relations and choosing `on_delete` policy.
- Introducing per-app `constants.py` with `TextChoices` enums.
- Adding Django 5 `db_default` / computed fields.

## When NOT To Use

- Async ORM workflows (`.asave()`, `.aget()`) — async manager patterns are not covered here.
- Multi-database routing, sharding, or replicas — out of scope.
- Heavy `JSONField` / `ArrayField` document-style data — methodology assumes relational schema.
- Tenant isolation (`django-tenants`, schema-per-tenant) — needs additional methodology.

## Content

| File | What's inside |
|------|---------------|
| `content/01-base-model.xml` | `BaseModel` abstract pattern, ForeignKey `on_delete` policies, `Meta.indexes`, `__str__`, Django 5 `db_default`. |
| `content/02-constants.xml` | `TextChoices` enum pattern, per-app `constants.py` structure, usage in model field definitions. |
| `content/03-project-structure.xml` | Django project layout: `config/`, `apps/`, `core/`, per-app folder structure with `models/`, `services/`, `tests/`. |
| `content/04-checklist.xml` | Planning, model definition, relationships, constraints, indexing, migrations, and documentation checklist. |

## Templates

| File | Purpose |
|------|---------|
| `templates/base-model.py` | Abstract `BaseModel` with UUID + timestamps. |
| `templates/constants.py` | Per-app `constants.py` with `TextChoices` enum example. |
| `templates/check-migrations.sh` | Pre-commit script: refuse commit if model changed without staged migration. |
