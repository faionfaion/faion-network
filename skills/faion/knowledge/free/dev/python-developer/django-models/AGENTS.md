# Django Models

## Summary

Django models are thin data containers: fields, indexes, constraints, and `__str__`. Business logic belongs in services (HackSoft style). Every domain model inherits from `BaseModel` (uid + timestamps). Status fields use `TextChoices`/`IntegerChoices`. ForeignKey `on_delete` is chosen deliberately — `PROTECT` for user/account refs, `CASCADE` only for child rows with no meaning without parent. Every generated migration file is reviewed by a human before `migrate`.

## Why

Thin models and a service layer keep business rules testable, migrations predictable, and ORM queries composable via custom QuerySets. Omitting `full_clean()` before `save()` in services silently drops model-level validation. Omitting `related_name` generates confusing `<model>_set` reverse names that break when models are renamed. Every `db_index=True` added without justification bloats write amplification.

## When To Use

- Adding a new model to a Django app
- Refactoring a model bloated with business logic into thin model + service functions
- Audit: scanning for missing `db_index`, wrong `on_delete`, missing `Meta.constraints`
- Designing status/state fields — converting raw string choices to `TextChoices`
- Migrating Django 4.x → 5.x to use `db_default` and `GeneratedField`

## When NOT To Use

- ORM-less projects (FastAPI + SQLAlchemy, Flask + SQLAlchemy) — route to SQLAlchemy methodology
- Migrating to a different ORM (peewee, Tortoise, SQLModel) — conventions don't translate
- Quick throwaway prototypes where Django Admin + auto-generated tables are sufficient
- Reporting/read-only projects backed by views or external warehouses

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-design.xml` | BaseModel, SoftDeleteModel, TextChoices, DB constraints, ForeignKey on_delete rules |
| `content/02-managers-and-querysets.xml` | Custom QuerySet, Manager.from_queryset(), chainable methods, factory methods |
| `content/03-performance-and-validation.xml` | Indexing strategy, N+1 prevention, model validators, Django 5 features |
| `content/04-antipatterns.xml` | Missing full_clean, id leak in serializers, GeneratedField on SQLite, LLM gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/base_model.py` | BaseModel + SoftDeleteModel scaffold |
| `templates/django-model-lint.sh` | AST-based lint: flags FK without related_name and raw choices tuples |
