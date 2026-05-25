# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

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
