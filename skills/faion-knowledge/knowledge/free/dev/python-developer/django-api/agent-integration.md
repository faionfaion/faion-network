# Agent Integration — Django API (DRF / Django Ninja)

## When to use
- Building a REST API on top of an existing Django project.
- Choosing between DRF and Django Ninja at project bootstrap; this README's decision matrix is the routing layer.
- Adding endpoints to a DRF ViewSet/APIView codebase (CRUD + custom actions).
- Migrating piece-by-piece from DRF to Ninja for hot endpoints (greenfield-style speedup) while keeping DRF for the rest.
- Generating OpenAPI for client SDKs from `drf-spectacular` or Ninja's built-in spec.
- Layering JWT/OAuth2/API-key auth, throttling, and pagination onto an existing API.

## When NOT to use
- Non-Django Python APIs — route to `python-fastapi/` instead.
- Greenfield project with no Django code at all and no admin requirement — FastAPI is usually a better fit.
- Pure GraphQL APIs — use `graphene-django` / `strawberry-django`; this methodology covers REST only.
- Internal RPC services — gRPC + protobuf; REST is overhead.

## Where it fails / limitations
- README presents DRF and Ninja as roughly interchangeable — they are not. DRF has 14 years of permissions/throttling/filters/serializers; Ninja is a thinner layer. Migrations across them are not 1:1 and agents will assume parity.
- "Ninja is ~2-3x faster than DRF in benchmarks" is unsourced; agents quote it. The real gap is async I/O, not request overhead.
- "JWT Best Practices: store in HttpOnly cookies (not localStorage)" — correct, but the README doesn't show how to wire that with `simplejwt` (default is body/JSON). Agents miss the cookie middleware step.
- "Use cursor pagination for feeds/timelines" — DRF's `CursorPagination` requires a stable, indexed `ordering` field. Agents apply it to `created_at` without an index and queries collapse.
- DRF Serializers vs Ninja Schemas section is misleading: ModelSerializer auto-generates fields by default; ModelSchema in Ninja requires explicit `Meta.fields = [...]` (no `__all__` shortcut in earlier versions). Agents copy DRF idioms.
- No discussion of nested writes (DRF's notorious gap), `to_representation`/`to_internal_value`, or partial updates (`PATCH`).
- Throttling example uses anon/user only; no scoped throttling, burst control, or Redis-backed throttle.
- Permission classes section is one snippet; nothing about object-level permissions (`has_object_permission`) which is where most security bugs live.
- No mention of API versioning bug: DRF's `URLPathVersioning` requires `version` in URL routes; agents add `URLPathVersioning` setting but forget to actually include `<version>` in the URL pattern.
- No async section for DRF (it has limited async support via `adrf`); agents will write async DRF views that don't actually run async.

## Agentic workflow
Two-phase loop. Phase 1: an opus/sonnet subagent reads the project brief and picks DRF vs Ninja using the decision matrix; output goes into `constitution.md`. Phase 2: a feature executor scaffolds endpoints in vertical slices (model → serializer/schema → view/router → URL/route → permission → throttle → test). Always require the test to call the real URL via the test client, not the view function directly — that's the only path that exercises auth/permission/throttle middleware. Lock the choice once made; mixing DRF and Ninja in the same app multiplies failure surface.

### Recommended subagents
- `framework-router` (sonnet) — picks DRF vs Ninja from project brief.
- `faion-sdd-executor-agent` — endpoint-per-task SDD execution.
- `faion-feature-executor` — sequential gate; runs `ruff`, `mypy` (with `django-stubs` and `djangorestframework-stubs`), `pytest-django`.
- General-purpose subagent restricted to `apps/<domain>/api/`, `apps/<domain>/serializers/`, `apps/<domain>/permissions/`, and tests for that domain.
- `password-scrubber-agent` — sweep settings + `.env*` for `SECRET_KEY`, JWT secrets, API keys.

### Prompt pattern
```
Stack: Django 5.x + DRF 3.15 + drf-spectacular + simplejwt + django-filter.
For new endpoint <METHOD> <path>:
1) Add/extend ModelSerializer (no `fields = "__all__"`, list fields explicitly).
2) Add/extend ViewSet (ModelViewSet) or APIView (custom action).
3) Permissions class (default IsAuthenticated; document any override).
4) Throttle scope.
5) URL route via DefaultRouter or path().
6) pytest-django test calling self.client.get/post() with auth fixture.
After: run `python manage.py spectacular --validate --fail-on-warn`.
```

```
Stack: Django Ninja 1.x + Pydantic v2 + simplejwt.
For new endpoint:
1) Pydantic schemas for request + response (ModelSchema OK, list fields).
2) Router function with type hints; sync or async (state which).
3) Auth via HttpBearer or custom security class.
4) Test with Django test client against the URL (not the function).
Generate OpenAPI: `api.openapi()` and snapshot to openapi.json.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `manage.py runserver` / `migrate` / `spectacular` | Django lifecycle + DRF schema | https://docs.djangoproject.com/en/5.2/ref/django-admin/ , https://drf-spectacular.readthedocs.io/ |
| `pytest-django` | Test runner integration | https://pytest-django.readthedocs.io/ |
| `factory_boy` / `model_bakery` | Test data | https://factoryboy.readthedocs.io/ |
| `django-stubs` + `djangorestframework-stubs` | mypy plugins | https://github.com/typeddjango/django-stubs , https://github.com/typeddjango/djangorestframework-stubs |
| `drf-spectacular` | OpenAPI 3 schema for DRF | https://drf-spectacular.readthedocs.io/ |
| `djangorestframework-simplejwt` | JWT auth | https://django-rest-framework-simplejwt.readthedocs.io/ |
| `django-oauth-toolkit` | OAuth2 server | https://django-oauth-toolkit.readthedocs.io/ |
| `django-filter` | Filter backend for DRF | https://django-filter.readthedocs.io/ |
| `django-cors-headers` | CORS | https://github.com/adamchainz/django-cors-headers |
| `django-ninja` 1.x | Async API framework | https://django-ninja.dev/ |
| `adrf` | Async DRF | https://github.com/em1208/adrf |
| `ruff` (`DJ` ruleset) | Django-specific lint | https://docs.astral.sh/ruff/rules/#flake8-django-dj |
| `schemathesis` | Spec-driven fuzz tests | https://schemathesis.readthedocs.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostgreSQL | OSS | Yes | Required for advanced filters, `JSONField`, full-text search. |
| Redis | OSS | Yes | Cache + DRF throttle backend (`django-redis` for cache backend; throttle uses default cache). |
| Celery / Django-Q | OSS | Yes | Background jobs invoked from ViewSet actions. |
| Sentry | SaaS | Yes | DRF + Django integration captures handler exceptions. |
| OpenTelemetry | OSS | Yes | `opentelemetry-instrumentation-django` traces ORM + middleware. |
| Auth0 / Keycloak / Authentik | SaaS / OSS | Yes | OIDC; pair with `mozilla-django-oidc` or DRF token override. |
| Stripe / SendGrid / Twilio | SaaS | Yes | Wrap in service layer, mock with `responses`/`respx` in tests. |
| GraphQL alternatives (`strawberry-django`) | OSS | Limited | Out of scope but worth knowing if requirements drift to GQL. |

## Templates & scripts
Pre-merge gate: validate the DRF schema and run a contract snapshot.

```bash
#!/usr/bin/env bash
# scripts/drf-spec-gate.sh
set -euo pipefail
python manage.py spectacular --validate --fail-on-warn --file openapi.new.yml
if [[ -f openapi.yml ]]; then
  diff -u openapi.yml openapi.new.yml || {
    echo "OpenAPI changed. Review and commit openapi.yml if intentional."
    mv openapi.new.yml openapi.yml
    exit 1
  }
  rm openapi.new.yml
else
  mv openapi.new.yml openapi.yml
fi
```

ViewSet/APIView vs Ninja decision (one-liner):

```python
# choose viewset when: standard CRUD on a single model, default router URLs OK
# choose APIView when: action verb (activate, archive, retry), no router routing
# choose Ninja when: async required, Pydantic-v2 schemas, FastAPI-like style desired
```

## Best practices
- Pin `fields = [...]` explicitly in serializers/schemas. Never `fields = "__all__"` on user-facing endpoints — leaks new columns automatically.
- Object-level permissions go in `has_object_permission`; `permission_classes` only handles route-level checks.
- Use `drf-spectacular`'s `@extend_schema` decorators to keep operation IDs stable across PRs (clients depend on them).
- Throttle by scope, not just anon/user. Add a `burst` scope for write endpoints.
- Always paginate list endpoints — set `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE`.
- Cursor pagination only on indexed `ordering` fields (typically `(-created_at, -id)` to break ties).
- Run `python manage.py check --deploy` in CI; catches DEBUG=True, missing security middleware, etc.
- Snapshot `openapi.yml`/`openapi.json` per PR and review the diff — that diff is the contract.
- For async needs, prefer Django Ninja over DRF + adrf; Ninja's async path is first-class.

## AI-agent gotchas
- Agents emit `fields = "__all__"` in `ModelSerializer.Meta`. Forbid in prompt.
- Agents put business logic in serializer `validate_*` methods. Move to a service function; serializers should validate shape only.
- Agents skip `URLPathVersioning` URL config — versioning silently no-ops. Test that `request.version` is populated.
- Agents mix DRF and Ninja in the same Django app and get URL conflicts.
- Agents call `Serializer(data=request.data, partial=True)` for PATCH but forget to enforce that required fields can't be cleared — set `extra_kwargs` or use a separate `*UpdateSerializer`.
- Agents use `request.user` in DRF without checking `request.user.is_authenticated` — produces `AnonymousUser` and confusing errors.
- Agents add `simplejwt` and store tokens in `localStorage` (the default examples) despite the README warning. Force HttpOnly cookies via `dj-rest-auth`/custom middleware.
- Agents write async ViewSet methods in plain DRF without `adrf` — methods run sync and look async.
- Agents enable `BrowsableAPIRenderer` in production; turns CSRF and content negotiation into surprise vectors.
- Human-in-loop checkpoint: every new permission class, every new throttle scope, every new auth backend.

## References
- https://www.django-rest-framework.org/
- https://django-ninja.dev/
- https://drf-spectacular.readthedocs.io/
- https://django-rest-framework-simplejwt.readthedocs.io/
- https://django-filter.readthedocs.io/
- https://cheatsheetseries.owasp.org/cheatsheets/Django_REST_Framework_Cheat_Sheet.html
- https://docs.djangoproject.com/en/5.2/topics/security/
- https://github.com/em1208/adrf
