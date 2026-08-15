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
| `content/01-core-rules.xml` | essential | 11 testable rules: framework lock, thin views, serializer pair, no __all__, JWT cfg, IsAuthenticated default, object-level perms, scoped throttle + cursor pagination, service takes domain types, generated OpenAPI, RFC 7807 errors | ~1800 |
| `content/02-output-contract.xml` | essential | JSON schema for the API spec | ~1250 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns: fat view, serializer business logic, __all__, BrowsableAPIRenderer in prod, async in DRF without adrf, service takes request, hand-maintained OpenAPI, mixed error shapes, unpaginated list | ~1200 |
| `content/04-procedure.xml` | deep | 9 steps: layer audit → framework → endpoints → serializers → service signatures → auth → throttle → schema + error shape → validate | ~950 |
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
| `templates/check-api-schema.sh` | CI step: regenerate the OpenAPI schema, fail on a breaking diff. |
| `templates/prompt-endpoint-scaffold.txt` | Subagent prompt scaffolding one endpoint across all five layers. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-api.py` | Validate an API spec JSON against the contract. | After the spec is emitted, before endpoint codegen runs. |

## Related

- [[django-base-model]] — uid pattern surfaced through serializers.
- [[django-models]] — model field types consumed by ModelSerializer / ModelSchema.
- [[django-pytest-integration]] — integration test patterns for these endpoints.
- [[django-coding-standards]] — apps/core/config layout that gates where services and views land.
- [[python-typing]] — type-checker baseline the service-signature rule (r9) depends on.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree first picks framework once at project bootstrap (DRF for ecosystem / Ninja for async-first). Per endpoint: maps single-resource CRUD → ModelViewSet; action verbs / multi-resource → APIView. Per list endpoint: timeline-style → cursor; counted page list → page-number.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/apiview.py`

```python
"""
Thin APIView: validate → service → return pattern.
Use for action verbs (activate, archive, retry) or multi-model aggregates.
"""

from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders import services as order_services
from apps.orders.serializers import OrderDetailSerializer


class ArchiveOrderView(APIView):
    """
    POST /api/v1/orders/{pk}/archive/
    Archive an order. Archived orders are hidden from default list views.
    """

    permission_classes = [IsAuthenticated]
    throttle_scope = "burst"

    def post(self, request: Request, pk: int) -> Response:
        # 1. Validate input (empty body in this case, but pattern is same)
        serializer = ArchiveOrderInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Delegate to service
        try:
            result = order_services.archive_order(
                order_id=pk,
                user=request.user,
                reason=serializer.validated_data.get("reason"),
            )
        except order_services.OrderNotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except order_services.OrderAlreadyArchived as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except order_services.PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        # 3. Return typed response
        return Response(OrderDetailSerializer(result).data, status=status.HTTP_200_OK)


class ArchiveOrderInputSerializer(serializers.Serializer):
    """Optional reason for archiving — validates input shape."""

    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)
```

### `templates/viewset.py`

```python
"""
ModelViewSet with action-specific serializers, get_queryset, and @action.
Pattern: thin viewset — validate in serializer, delegate logic to service.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.orders import services as order_services
from apps.orders.models import Order
from apps.orders.serializers import (
    CreateOrderSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    UpdateOrderSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for orders.
    URL: /api/v1/orders/ (router-registered)
    """

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_scope = "burst"  # Applies to write actions

    def get_queryset(self):
        """Scope queryset to current user's organization."""
        return (
            Order.objects.filter(
                organization=self.request.user.organization,
            )
            .select_related("user", "organization")
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        """Return action-specific serializer."""
        if self.action == "create":
            return CreateOrderSerializer
        if self.action in ("update", "partial_update"):
            return UpdateOrderSerializer
        if self.action == "list":
            return OrderListSerializer
        return OrderDetailSerializer  # retrieve, custom actions

    def perform_create(self, serializer: CreateOrderSerializer) -> None:
        """Delegate creation to service layer."""
        order_services.create_order(
            validated_data=serializer.validated_data,
            user=self.request.user,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="confirm",
        throttle_classes=[],  # Override throttle for this action if needed
    )
    def confirm(self, request: Request, pk: int | None = None) -> Response:
        """POST /api/v1/orders/{id}/confirm/ — confirm a pending order."""
        order = self.get_object()  # Calls has_object_permission
        try:
            result = order_services.confirm_order(order=order, user=request.user)
        except order_services.OrderAlreadyConfirmed as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        return Response(OrderDetailSerializer(result).data)
```

### `templates/ninja-routes.py`

```python
"""
Django Ninja router with ModelSchema, AuthBearer, and CRUD endpoints.
Pattern: Ninja router per app, mounted in api.py.
"""

from decimal import Decimal

from ninja import ModelSchema, Router, Schema
from ninja.security import HttpBearer
from pydantic import Field, field_validator

from apps.orders.models import Order
from apps.orders import services as order_services


# ─── Auth ────────────────────────────────────────────────────────────────────

class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str):
        from rest_framework_simplejwt.tokens import AccessToken
        try:
            validated_token = AccessToken(token)
            from django.contrib.auth import get_user_model
            User = get_user_model()
            return User.objects.get(id=validated_token["user_id"])
        except Exception:
            return None


# ─── Schemas ─────────────────────────────────────────────────────────────────

class CreateOrderSchema(Schema):
    """Input: validated at route entry."""
    amount: Decimal = Field(..., ge=0, decimal_places=2)
    product_id: int
    notes: str | None = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return v


class OrderSchema(ModelSchema):
    """Output: read-only fields from the model."""
    class Meta:
        model = Order
        fields = ["id", "uid", "amount", "status", "created_at", "updated_at"]


# ─── Router ──────────────────────────────────────────────────────────────────

router = Router(auth=AuthBearer(), tags=["orders"])


@router.get("/", response=list[OrderSchema])
def list_orders(request):
    return Order.objects.filter(
        organization=request.auth.organization,
    ).order_by("-created_at")


@router.get("/{order_id}", response=OrderSchema)
def get_order(request, order_id: int):
    from ninja.errors import HttpError
    try:
        return Order.objects.get(id=order_id, organization=request.auth.organization)
    except Order.DoesNotExist:
        raise HttpError(404, "Order not found")


@router.post("/", response={201: OrderSchema})
def create_order(request, payload: CreateOrderSchema):
    order = order_services.create_order(
        validated_data=payload.model_dump(),
        user=request.auth,
    )
    return 201, order


# Mount in api.py:
# from ninja import NinjaAPI
# from apps.orders.routes import router as orders_router
# api = NinjaAPI()
# api.add_router("/orders/", orders_router)
```

### `templates/drf-settings.py`

```python
"""
Complete REST_FRAMEWORK + SIMPLE_JWT + SPECTACULAR_SETTINGS config block.
Copy into settings.py (or settings/base.py).
"""

from datetime import timedelta

REST_FRAMEWORK = {
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Permissions — locked down by default, opt-in to AllowAny per view
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Renderer — JSON only in production; BrowsableAPI only in development
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Throttling — scoped per endpoint type
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
        "burst": "30/min",      # Write endpoints (POST/PUT/PATCH/DELETE)
        "login": "5/min",       # Auth endpoints — brute-force protection
    },
    # Pagination — always paginate list endpoints
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    # Filtering
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Schema generation
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Versioning
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    # Exception handler
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}

# JWT Configuration — simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),   # Short-lived: 15 min
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),       # 7-day refresh
    "ROTATE_REFRESH_TOKENS": True,                     # New refresh on use
    "BLACKLIST_AFTER_ROTATION": True,                  # Blacklist old refresh
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# drf-spectacular OpenAPI schema settings
SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "REST API documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Postprocessing hooks
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
    # Component naming
    "COMPONENT_SPLIT_REQUEST": True,   # Separate request/response schemas
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]+",
}
```

### `templates/permissions.py`

```python
"""
Custom DRF permission classes: IsOrganizationMember, IsOwnerOrReadOnly, IsOwnerOrAdmin.
"""

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOrganizationMember(permissions.BasePermission):
    """
    Object-level: user must belong to the object's organization.
    Supports objects with .organization or .user FK.
    """

    message = "You don't have access to this resource."

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if hasattr(obj, "organization"):
            return obj.organization == request.user.organization
        if hasattr(obj, "user"):
            return obj.user.organization == request.user.organization
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level: write access only for owner; read access for authenticated users.
    Requires obj.user or obj.owner FK.
    """

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level: owner or staff/superuser can access.
    Unauthenticated users are always denied.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.user.is_staff or request.user.is_superuser:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user
```

### `templates/pagination.py`

```python
"""
StandardPagination (page-number) and TimelinePagination (cursor).
Reference these in REST_FRAMEWORK DEFAULT_PAGINATION_CLASS.
"""

from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Page-number pagination for general list endpoints.
    Supports ?page=N and ?page_size=N query params.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema: dict) -> dict:
        return {
            "type": "object",
            "properties": {
                "count": {"type": "integer"},
                "next": {"type": "string", "nullable": True},
                "previous": {"type": "string", "nullable": True},
                "results": schema,
            },
        }


class TimelinePagination(CursorPagination):
    """
    Cursor pagination for timeline/feed endpoints.
    Ordered by -created_at with -id tie-breaker.
    REQUIRES: ordering fields must be indexed in the DB.
    """

    page_size = 20
    ordering = ("-created_at", "-id")  # -id ensures stable ordering
    cursor_query_param = "cursor"
    page_size_query_param = "page_size"
    max_page_size = 50
```

### `templates/api-spec.json`

```json
{
  "_purpose": "Reference Django REST API spec output.",
  "_consumes": "Endpoint list + auth model + SLO.",
  "_produces": "JSON for endpoint codegen / review.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~200 tokens.",
  "artefact_id": "billing-api-spec",
  "owner": "ruslan@faion.net",
  "framework": "drf",
  "django_version": "5.2.1",
  "endpoints": [
    {
      "resource": "Invoice",
      "kind": "model-viewset",
      "methods": [
        "GET",
        "POST",
        "PATCH",
        "DELETE"
      ],
      "input_serializer": "CreateInvoiceSerializer",
      "output_serializer": "InvoiceDetailSerializer",
      "permission_classes": [
        "IsAuthenticated",
        "IsOrganizationMember"
      ],
      "throttle_scope": "user",
      "pagination": "cursor"
    }
  ],
  "auth": {
    "mode": "jwt-simplejwt",
    "access_ttl_minutes": 15,
    "refresh_ttl_days": 7,
    "rotate_refresh": true,
    "blacklist_after_rotation": true,
    "transport": "httponly-cookie"
  },
  "throttle": {
    "scopes": [
      "anon",
      "user",
      "burst",
      "login"
    ]
  },
  "openapi": {
    "generator": "drf-spectacular",
    "ci_drift_check": true,
    "schema_path": "docs/api/schema.yml"
  },
  "error_shape": "rfc-7807",
  "service_signature_style": "domain-types",
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/check-api-schema.sh`

```bash
# Export the OpenAPI schema and fail if breaking changes appear vs docs/api/schema.yml.
# Run in CI or as a pre-commit hook.
set -euo pipefail

SCHEMA_FILE="docs/api/schema.yml"

python manage.py spectacular --file /tmp/schema.new.yml --fail-on-warn

if [ -f "$SCHEMA_FILE" ]; then
  if command -v oasdiff >/dev/null 2>&1; then
    oasdiff breaking "$SCHEMA_FILE" /tmp/schema.new.yml --fail-on ERR
  else
    diff -u "$SCHEMA_FILE" /tmp/schema.new.yml || {
      echo "OpenAPI schema changed. Update ${SCHEMA_FILE} or fix the regression." >&2
      exit 1
    }
  fi
fi

mkdir -p "$(dirname "$SCHEMA_FILE")"
mv /tmp/schema.new.yml "$SCHEMA_FILE"
echo "Schema updated: ${SCHEMA_FILE}"
```

### `templates/prompt-endpoint-scaffold.txt`

```text
Add POST /api/v1/<resource>/ endpoint per the django-api methodology.

Layers to create (each as a separate commit):
  1. Serializers: Create<Resource>Request + <Resource>Response in apps/<app>/serializers.py
  2. Service: apps/<app>/services.<function_name>(user_id: int, ...) with full type hints
  3. View: thin APIView or ModelViewSet action calling the service, @extend_schema with summary/request/responses/tags
  4. URL: wire into apps/<app>/urls.py and config/urls.py
  5. Tests: pytest @pytest.mark.django_db covering 201 success + 400 bad input + 401 unauthenticated

Rules:
  - Service must NOT receive request or request.user — pass user_id: int instead (r9)
  - Input and output serializers must be different classes (r3)
  - Meta.fields = "__all__" is forbidden; list fields explicitly (r4)
  - @extend_schema is required on every view with non-empty tags=["<Tag>"] (r10)
  - Errors are raised as exceptions and rendered RFC 7807 by the global handler (r11)
  - Run: python manage.py spectacular --validate after implementation
  - Run: pytest apps/<app>/tests/ -x after each step
```
