# purpose: Thin DRF ViewSet using select_related + service call
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for practices-django-coding
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Order
from .services import create_and_charge
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related('customer').all()

    def perform_create(self, serializer):
        order = create_and_charge(
            customer=serializer.validated_data['customer'],
            amount=serializer.validated_data['amount'],
            payment_token=self.request.data['payment_token'],
        )
        serializer.instance = order
