# Django API Development

## Summary

**One-sentence:** Produces a Django REST API spec naming the framework (DRF 3.15+ or Ninja 1.x), per-endpoint ViewSet-vs-APIView choice, input/output serializer pair, JWT configuration, throttle scopes, and pagination strategy.

**Ефективно для:** New REST endpoints on a Django 5.x service where the team needs to commit, once and explicitly, to DRF or Ninja, to thin views over fat ones, and to scoped throttling instead of one global anon/user limit.

**One-paragraph:** Codifies the recurring "DRF or Ninja? ViewSet or APIView? one serializer or two? where does the JWT live?" decisions into one auditable spec. The output forbids `Meta.fields = '__all__'`, fat views with business logic, async-in-DRF without adrf, BrowsableAPIRenderer in production, and AllowAny defaults. Each endpoint maps to {router, action, input_serializer, output_serializer, permission_classes, throttle_scope, pagination}.

## Applies If (ALL must hold)

- Django ≥ 5.0 with a chosen API framework (DRF 3.15+ or Django Ninja 1.x).
- The service exposes JSON REST endpoints to first-party clients or third-party consumers.
- The team commits to thin views + service layer separation.
- JWT or session auth is required (or "public read + authenticated write" is the contract).
- Output drives endpoint codegen and security review.

## Skip If (ANY kills it)

- Non-Django Python API — use `python-fastapi` instead.
- Greenfield project with no Django code and no admin requirement — FastAPI is usually a better fit.
- Pure GraphQL APIs — use graphene-django / strawberry-django.
- Internal RPC services — gRPC + protobuf, not REST.
- Mixing DRF + Ninja in one app — pick one; never both.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Endpoint list (path, method, resource) | YAML | API spec / OpenAPI draft |
| Auth model + token lifetime | text | architecture decision |
| Existing serializer / view conventions | code refs | repo |
| SLO targets (latency p95, throttle limits) | numbers | NFR doc |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-models]]` | Field types + Meta consumed by serializers. |
| `[[django-base-model]]` | `uid` exposure: API returns uid, never id. |
| `[[django-imports]]` | Conventional import order in viewsets/serializers. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules: framework lock, ViewSet vs APIView, serializer pair, no __all__, JWT cfg, IsAuthenticated default, object-level perms, scoped throttle, cursor pagination | ~1400 |
| `content/02-output-contract.xml` | essential | JSON schema for the API spec | ~1100 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: fat view, serializer business logic, __all__, BrowsableAPIRenderer in prod, async in DRF without adrf | ~800 |
| `content/04-procedure.xml` | deep | 6 steps: pick framework → enumerate endpoints → declare serializers → wire auth → set throttle → paginate | ~700 |
| `content/05-examples.xml` | deep | One worked example: Invoice resource with ModelViewSet + CreateInvoiceSerializer + InvoiceDetailSerializer | ~700 |
| `content/06-decision-tree.xml` | essential | Per-endpoint: ViewSet vs APIView; per-resource: cursor vs page pagination | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_endpoints` | haiku | Mechanical extraction from API spec. |
| `emit_api_spec` | sonnet | Bounded mapping of endpoints to serializers/perms. |
| `audit_security` | opus | Cross-checks auth + throttle + perms across all endpoints. |

## Templates

| File | Purpose |
|---|---|
| `templates/apiview.py` | Thin APIView: validate → service → return pattern. |
| `templates/viewset.py` | ModelViewSet with action-specific serializers. |
| `templates/ninja-routes.py` | Ninja router with ModelSchema + AuthBearer. |
| `templates/drf-settings.py` | REST_FRAMEWORK + SIMPLE_JWT + SPECTACULAR config. |
| `templates/permissions.py` | IsOrganizationMember / IsOwnerOrReadOnly. |
| `templates/pagination.py` | StandardPagination + TimelinePagination (cursor). |
| `templates/api-spec.json` | Reference API spec output. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-api.py` | Validate an API spec JSON against the contract. | After the spec is emitted, before endpoint codegen runs. |

## Related

- [[django-base-model]] — uid pattern surfaced through serializers.
- [[django-models]] — model field types consumed by ModelSerializer / ModelSchema.
- [[django-pytest-integration]] — integration test patterns for these endpoints.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree first picks framework once at project bootstrap (DRF for ecosystem / Ninja for async-first). Per endpoint: maps single-resource CRUD → ModelViewSet; action verbs / multi-resource → APIView. Per list endpoint: timeline-style → cursor; counted page list → page-number.
