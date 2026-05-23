# purpose: Service function wrapping multi-write flow in transaction.atomic
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for practices-django-coding
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

from django.db import transaction
from .models import Order, PaymentAttempt


@transaction.atomic
def create_and_charge(customer, amount, payment_token):
    order = Order.objects.create(customer=customer, amount=amount, status='pending')
    attempt = PaymentAttempt.objects.create(order=order, token=payment_token)
    attempt.charge()
    order.status = 'charged'
    order.save(update_fields=['status'])
    return order
