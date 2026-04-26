# Agent Integration — Django REST Framework API

Methodology codifies a "thin views + services + drf-spectacular OpenAPI + ViewSet" stack for DRF. Goal of this file: turn it into a checklist an LLM can execute end-to-end without re-deriving conventions.

## When to use
- New DRF endpoint inside a Django 5 project that already follows `apps/<name>/{views,services,serializers,urls}.py` layout.
- Refactor of a "fat view" (business logic in `def post`) into thin view + `services.py` extraction.
- Adding OpenAPI documentation to existing endpoints via `drf-spectacular`.
- Standardizing pagination, filtering, permission classes across a ViewSet.
- Bringing legacy DRF code (no `@extend_schema`, no services layer, mixed validation in views) up to faion-net standard.

## When NOT to use
- FastAPI / Starlette / Flask projects — different idioms (Pydantic, dependency injection); see `python/README.md` FastAPI section instead.
- Internal-only endpoints used by Django admin / management commands — DRF is overhead; use plain Django views.
- Pure GraphQL APIs — `graphene-django` / `strawberry-django` have orthogonal patterns; this methodology will mislead.
- Async-first endpoints with heavy I/O concurrency — DRF's class-based views are sync; use Django Ninja or FastAPI.
- One-off webhooks where you want raw JSON in/out without serializers — overkill, write an `@csrf_exempt` view.

## Where it fails / limitations
- README skips **versioning** (`/api/v1/` vs accept-header). Agents will randomly pick one per endpoint.
- **No error-handling guidance.** Pairs poorly with the sibling `error-handling/` (RFC 7807) methodology — needs explicit reference.
- ViewSet example overrides `get_queryset` but does not address N+1 (`select_related` / `prefetch_related`); agents copy-paste and ship slow endpoints.
- `extend_schema` snippet shows minimal fields; missing `parameters=` for query strings, `examples=` for OpenAPI samples — auto-generated docs end up empty.
- No mention of **throttling** (`DEFAULT_THROTTLE_CLASSES`), **CORS**, or **CSRF for SessionAuthentication** — production blockers.
- Permission classes shown only as `IsAuthenticated`; no object-level perms or per-action perms (`get_permissions`).
- Services pattern leaks DRF concerns: `services.activate_user_item(user=request.user, ...)` — `request.user` belongs in the view, services should take a domain `User` model.

## Agentic workflow
For each endpoint task: (1) read the methodology section + project's existing app for naming style, (2) generate serializer (request + response separately), (3) generate service function with full type hints, (4) generate thin view calling service, (5) wire into `urls.py`, (6) write `@extend_schema` block, (7) add `tests/test_<view>.py` with `@pytest.mark.django_db` and `APIClient`. Commit each step atomically — the pre-commit ruff hook will catch lint issues immediately. Always run `python manage.py spectacular --validate` before merging to catch broken OpenAPI.

### Recommended subagents
- `faion-code-agent` — Default for view/service/serializer scaffolding.
- `faion-api-developer` (sibling skill) — Owns API design decisions: paths, status codes, pagination, versioning.
- `faion-test-agent` — Owns the integration test layer (`@pytest.mark.django_db` + `APIClient`).
- `faion-software-architect` — Decides ViewSet vs APIView vs function-based; rarely invoked but critical for non-CRUD endpoints (bulk ops, RPC-style).
- `faion-sdd-execution` — Drives the spec → endpoint → test cycle when the endpoint is part of a larger feature.

### Prompt pattern
Endpoint scaffold:

```
Add POST /api/v1/orders/ endpoint per django-api/README.md.
Layers: serializer (CreateOrderRequest + OrderResponse), service
(apps/orders/services.create_order), thin APIView, drf-spectacular
@extend_schema with tags=['Orders']. Permission: IsAuthenticated.
Tests: pytest fixtures user + authenticated_client, cover 201 + 400
+ 401. Use ruff format. Return diff and `pytest -x` output.
```

Refactor fat view:

```
Refactor apps/users/views.UserCreateView.post into:
1) serializer validation in view
2) services.create_user() owning DB writes
3) UserResponse serializer for output
Do not change URL or behavior. Add type hints. Run `pytest apps/users/tests/test_views.py`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `django-admin` / `manage.py` | Project ops, migrations, shell | https://docs.djangoproject.com |
| `manage.py spectacular --file schema.yml` | Export OpenAPI 3.1 schema | https://drf-spectacular.readthedocs.io |
| `manage.py spectacular --validate` | Lint OpenAPI schema | same |
| `httpie` / `curl` | Hit endpoints from CLI | `apt install httpie` |
| `pytest` + `pytest-django` | Run API integration tests | https://pytest-django.readthedocs.io |
| `ruff` | Lint + format (DJ ruleset for Django gotchas) | https://docs.astral.sh/ruff |
| `django-debug-toolbar` (dev) | Inspect query counts on each endpoint | https://django-debug-toolbar.readthedocs.io |
| `silk` | Profile per-request SQL + timings | https://github.com/jazzband/django-silk |
| `schemathesis` | Property-based testing from OpenAPI schema | https://schemathesis.readthedocs.io |
| `openapi-diff` | Detect breaking API changes between PRs | https://github.com/Tufin/oasdiff |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Swagger UI / ReDoc | OSS | Yes — served by drf-spectacular at `/api/schema/swagger-ui/` | No auth UI by default; add behind staff-only |
| Postman / Bruno | SaaS / OSS | Yes — import `schema.yml` | Bruno is git-friendly; agents can edit collections as files |
| Stoplight Studio | SaaS | Yes — design-first OAS editor | Useful when API is contract-first |
| Schemathesis Cloud | SaaS | Yes — runs property tests against deployed API | Free tier limited |
| Sentry (Django integration) | SaaS | Yes — `sentry-sdk[django]` | Capture DRF exceptions automatically |
| Datadog APM | SaaS | Yes — `ddtrace-run python manage.py runserver` | Per-endpoint latency, query traces |
| Cloudflare API Shield | SaaS | Yes — schema-validated WAF | Imports drf-spectacular OpenAPI directly |

## Templates & scripts
See README for view/serializer/service samples. Add this CI step to catch schema regressions (≤30 lines):

```bash
#!/usr/bin/env bash
# scripts/check-api-schema.sh — fail PR if OpenAPI changes without intent.
set -euo pipefail
python manage.py spectacular --file /tmp/schema.new.yml --fail-on-warn
if [ -f docs/api/schema.yml ]; then
  if command -v oasdiff >/dev/null; then
    oasdiff breaking docs/api/schema.yml /tmp/schema.new.yml \
      --fail-on ERR
  else
    diff -u docs/api/schema.yml /tmp/schema.new.yml || {
      echo "OpenAPI schema changed. Update docs/api/schema.yml or fix the regression." >&2
      exit 1
    }
  fi
fi
mv /tmp/schema.new.yml docs/api/schema.yml
```

Run inside `pre-commit` or GitHub Actions. Commits the new schema only when explicitly accepted.

## Best practices
- **Separate request and response serializers.** `CreateOrderRequest` ≠ `OrderResponse`. Mixing them via one `ModelSerializer` leaks write-only fields into responses.
- **Make services framework-agnostic.** Pass `user_id` (int) or domain `User` model, not `request.user`. Services callable from Celery tasks, mgmt commands, tests.
- **Always set `tags=`** in `@extend_schema`. Without tags, Swagger UI groups everything under "default" — useless for >10 endpoints.
- **Cap `queryset` in ViewSet at the user's scope** in `get_queryset`. Never expose `Model.objects.all()` directly — guarantees an IDOR sooner or later.
- **`select_for_update` requires `transaction.atomic` and a real DB** (not SQLite). Wrap explicitly; readers will copy-paste.
- **Use `@action(detail=True)`** for non-CRUD verbs (`/orders/{id}/cancel/`) — keeps URL conf flat.
- **Pagination**: set `DEFAULT_PAGINATION_CLASS = 'rest_framework.pagination.LimitOffsetPagination'` in settings; never paginate ad-hoc per view.
- **Permissions per action**: override `get_permissions(self)` in ViewSet, returning different classes for `create` vs `list`. README's static `permission_classes = [...]` is too coarse for real apps.
- **Tests must hit URL, not view.** Use `reverse('app:url-name')` — refactoring URL conf doesn't break tests.
- **`@pytest.mark.django_db(transaction=True)`** only when you actually need committed transactions (e.g., post_commit signals); otherwise default rollback is faster.

## AI-agent gotchas
- **`request.user` in services** breaks tests + Celery callers. Lint rule worth adding: ban `request.` inside `services/*.py`.
- **`is_valid(raise_exception=True)`** maps to HTTP 400 with DRF's default exception handler — but if you also have a custom exception middleware, double-handling can produce confusing 500s.
- **`@extend_schema(request=Serializer)`** and a `request.data` shape that doesn't match (e.g., flat field vs nested) will silently generate wrong OpenAPI without runtime errors. `manage.py spectacular --validate` catches some, not all.
- **ViewSet `get_queryset` runs per request**; calling `.all()` then `.filter()` re-issues the query. Use `self.queryset.filter(...)` only after assigning a queryset class attr.
- **Auth class order matters.** SessionAuth before TokenAuth makes browser tools convenient but breaks header-only clients with CSRF. Spell it out per project.
- **`PUT vs PATCH`**: ModelViewSet's `update` defaults to PUT (full replace). Agents who think `PUT == PATCH` will write tests sending partials and hit 400.
- **`drf-spectacular` infers nullable wrong** for `serializers.CharField(allow_null=True, required=False)` vs missing field — explicit `OpenApiTypes.STR` + `OpenApiParameter(...)` overrides may be needed.
- **CORS**: README never mentions `corsheaders`. Endpoint works in tests, fails from frontend with CORS error — common spec-vs-runtime mismatch.
- **`ModelViewSet` exposes DELETE** by default. Agents copy-paste and accidentally ship destructive endpoints. Whitelist actions: `http_method_names = ['get', 'post', 'patch']`.
- **Schema breakage** when adding a required field to a request serializer is a backward-incompatible API change. Always run `oasdiff breaking` before merging.
- **`force_authenticate(user=user)`** in tests bypasses permission classes — green tests, broken prod when permissions misconfigured. Pair with at least one un-authenticated test asserting 401/403.
- **Bulk endpoints** are out of scope here. ModelViewSet doesn't bulk-create; agents reach for `serializer(many=True, data=list)` and skip per-row validation. Use `drf-bulk` or write explicit endpoint.

## References
- README: `./README.md`
- Sibling: `../django-base-model/`, `../django-models/`, `../django-pytest/`, `../django-quality/`, `../django-imports/`, `../django-coding-standards/`
- Cross-skill: `../python/`, `../error-handling/`, `../api-testing/`
- DRF: https://www.django-rest-framework.org
- drf-spectacular: https://drf-spectacular.readthedocs.io
- OpenAPI 3.1: https://spec.openapis.org/oas/v3.1.0
- oasdiff (breaking-change detector): https://github.com/Tufin/oasdiff
- Schemathesis: https://schemathesis.readthedocs.io
- Django async views: https://docs.djangoproject.com/en/5.0/topics/async/
