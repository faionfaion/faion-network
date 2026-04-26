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
