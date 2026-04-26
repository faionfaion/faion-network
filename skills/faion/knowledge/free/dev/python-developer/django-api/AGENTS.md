# Django API Development

## Summary

Patterns for building REST APIs with Django REST Framework (DRF 3.15+) or Django Ninja 1.x. Covers ViewSet vs APIView selection, serializer/schema design, JWT auth, throttling, pagination, filtering, and OpenAPI documentation. Core rule: keep views thin — validate input with serializers, delegate business logic to a service layer, return typed responses.

## Why

Fat views that mix validation, business logic, and side effects are the single biggest source of Django API bugs and test failures. Separating concerns (serializer → service → view) makes each layer independently testable and reduces the surface area for security mistakes like `fields = "__all__"` leaking new columns.

## When To Use

- Building new REST endpoints on an existing Django 5.x project.
- Choosing between DRF and Ninja at project bootstrap.
- Adding CRUD ViewSets or custom APIView actions to an existing DRF codebase.
- Implementing or hardening JWT/OAuth2/API-key auth, throttling, or cursor pagination.
- Generating OpenAPI specs for client SDKs via `drf-spectacular` or Ninja's built-in spec.

## When NOT To Use

- Non-Django Python APIs — use `python-fastapi/` instead.
- Greenfield project with no Django code and no admin requirement — FastAPI is usually a better fit.
- Pure GraphQL APIs — use `graphene-django` / `strawberry-django`; this covers REST only.
- Internal RPC services — gRPC + protobuf; REST overhead is not justified.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework-selection.xml` | DRF vs Django Ninja decision matrix; when to use ViewSet vs APIView vs Ninja router. |
| `content/02-serializers-schemas.xml` | Separate input/output serializers rule; ModelSerializer field allowlisting; Ninja ModelSchema. |
| `content/03-auth-permissions-throttle.xml` | JWT configuration (simplejwt); custom permission classes; throttle by scope; cursor pagination. |
| `content/04-antipatterns.xml` | Fat views, `fields="__all__"`, single-serializer-for-all, sync DRF async misuse, browser renderer in prod. |

## Templates

| File | Purpose |
|------|---------|
| `templates/drf-settings.py` | Complete `REST_FRAMEWORK` + `SIMPLE_JWT` + `SPECTACULAR_SETTINGS` config block. |
| `templates/viewset.py` | `ModelViewSet` with action-specific serializers, `get_queryset`, `@action`. |
| `templates/apiview.py` | Thin `APIView`: validate → service → return pattern. |
| `templates/ninja-routes.py` | Ninja router with `ModelSchema`, `AuthBearer`, CRUD endpoints. |
| `templates/permissions.py` | `IsOrganizationMember`, `IsOwnerOrReadOnly`, `IsOwnerOrAdmin`. |
| `templates/pagination.py` | `StandardPagination` (page-number) and `TimelinePagination` (cursor). |
