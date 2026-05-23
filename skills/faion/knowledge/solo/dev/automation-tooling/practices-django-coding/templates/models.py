# purpose: Model with custom QuerySet + clean() validation
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for practices-django-coding
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

from django.db import models
from django.core.exceptions import ValidationError


class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=['pending', 'shipped'])

    def for_customer(self, customer_id):
        return self.filter(customer_id=customer_id).select_related('customer')


class Order(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    objects = OrderQuerySet.as_manager()

    class Meta:
        ordering = ['-id']

    def clean(self):
        if self.amount <= 0:
            raise ValidationError('amount must be positive')
