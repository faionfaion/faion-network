# Django Base Model Pattern

## Summary

Every Django domain model must inherit from `BaseModel` — an abstract model providing `uid: UUIDField` (external identifier), `created_at`, and `updated_at`. The integer primary key is kept for join performance; `uid` is the public identifier exposed in APIs. Never expose auto-increment `id` in serializers or URLs.

## Why

Auto-increment IDs leak table size, enable enumeration attacks, and create coupling between internal DB layout and public API contracts. A UUID secondary identifier (`uid`) decouples these concerns at negligible cost. Abstract inheritance guarantees all domain models carry audit timestamps with zero per-model boilerplate.

## When To Use

- Starting any new Django project — define `BaseModel` before first domain model
- Creating any model that represents a domain entity
- Building REST/GraphQL APIs that must expose a stable, non-enumerable identifier
- Systems requiring audit trails (`created_at`/`updated_at`)
- Refactoring legacy models to add UUID + timestamp fields

## When NOT To Use

- Internal-only models never exposed externally (M2M through-tables, analytics rollups) — extra UUID column and index are dead weight
- Models inheriting from third-party abstract bases (`django-mptt`, `django-polymorphic`) that define their own PK/timestamp scheme — MRO conflicts
- High-write tables in the millions of rows without a migration plan — UUIDv4 has poor B-tree index locality (use UUIDv7 instead)
- Read-replica DBs where every extra index slows replication

## Content

| File | What's inside |
|------|---------------|
| `content/01-base-model.xml` | BaseModel implementation, ForeignKey patterns, soft delete extension, Django 5 features |
| `content/02-antipatterns.xml` | Exposing auto-increment IDs, missing indexes, CASCADE misuse, LLM gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/base_model.py` | BaseModel + SoftDeleteModel scaffold with UUIDv7 upgrade path |
