# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

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
