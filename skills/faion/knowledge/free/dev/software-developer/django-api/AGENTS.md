# Django REST Framework API

## Summary

Thin views + service layer + `drf-spectacular` OpenAPI + `ViewSet` pattern for Django REST Framework.
Views validate input and call services; services own all business logic and accept domain types (not
`request.user`). Every endpoint gets `@extend_schema` with `summary`, `request`, `responses`,
and `tags`.

## Why

Fat views (business logic in `def post`) are untestable from Celery or management commands and
resist refactoring. Separating concerns into serializer → thin view → service → repository lets each
layer be tested independently and reused across callers. `drf-spectacular` generates accurate OpenAPI
from code; `manage.py spectacular --validate` catches schema regressions before deployment.

## When To Use

- New DRF endpoint inside a Django 5 project following `apps/<name>/{views,services,serializers,urls}.py`
- Refactoring a fat view (business logic in `def post`) into thin view + `services.py` extraction
- Adding OpenAPI docs to existing endpoints via `drf-spectacular`
- Standardizing pagination, permissions, filtering across a `ViewSet`

## When NOT To Use

- FastAPI / Starlette / Flask — different idioms; see `python-fastapi/` instead
- Internal-only endpoints used by Django admin or management commands — plain Django views suffice
- Pure GraphQL APIs — `graphene-django` / `strawberry-django` have orthogonal patterns
- Async-first endpoints with heavy I/O concurrency — use Django Ninja or FastAPI
- One-off webhooks needing raw JSON in/out — DRF serializer overhead not justified

## Content

| File | What's inside |
|------|---------------|
| `content/01-thin-views.xml` | `APIView` pattern: validate → call service → return; `@extend_schema` required fields |
| `content/02-viewsets.xml` | `ModelViewSet`, `get_queryset` scoping, `@action`, `get_permissions` per action |
| `content/03-serializers.xml` | Separate request vs response serializers, `validate_*` methods, `ModelSerializer` |
| `content/04-antipatterns.xml` | `request.user` in services, N+1 in ViewSet, `PUT vs PATCH` confusion, DELETE exposure |

## Templates

| File | Purpose |
|------|---------|
| `templates/check-api-schema.sh` | CI: export + diff OpenAPI schema, fail on breaking changes |
| `templates/prompt-endpoint-scaffold.txt` | Prompt to scaffold serializer + service + view + tests atomically |
