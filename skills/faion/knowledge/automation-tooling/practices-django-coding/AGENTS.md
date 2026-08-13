# Django Coding Practices

## Summary

**One-sentence:** Produces Django app code that uses fat-model thin-view discipline, custom QuerySet managers, select_related/prefetch_related to kill N+1, atomic transactions on writes, and class-based views/DRF for HTTP boundaries.

**One-paragraph:** Django coding practices distilled into testable rules. Models hold business logic and validation (clean() + custom QuerySet); views stay thin; querysets resolve relations eagerly via select_related (FK) and prefetch_related (M2M); all writes are wrapped in transaction.atomic; signals are limited to cross-app concerns; settings are split env-aware. The artefact is the metadata describing the generated app, validated by the per-rule schema.

**Ефективно для:**

- New Django app/module under an existing project.
- Refactor passes removing N+1 queries surfaced by django-silk.
- Code-review gates checking transaction.atomic on write paths.
- Migrating fat-view code into fat-model + service-layer shape.

## Applies If (ALL must hold)

- Django 4.x or 5.x project using the ORM.
- Code path includes write operations that need atomicity.
- Views touch related models (FK / M2M / reverse relations).
- Project has a tests/ directory wired to pytest-django or unittest.

## Skip If (ANY kills it)

- Non-Django projects (use practices-python-ecosystem).
- Read-only async serverless endpoints with no ORM use.
- Legacy projects that explicitly mandate fat-view style and refuse refactor.
- Pure data-pipeline code without HTTP boundary.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Django project root | directory | filesystem |
| App / module name | string | task brief |
| Domain model spec | model fields + relations | design doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[practices-python-ecosystem]] | shared Python tooling: ruff, mypy, pyproject.toml |
| [[testing-django-pytest]] | tests use pytest-django fixtures and factories |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `emit-models` | sonnet | model fields + QuerySet methods + clean() |
| `emit-views` | sonnet | class-based views or DRF viewsets respecting thin-view rule |
| `scan-n-plus-one` | haiku | static check for FK access in template loops + missing select_related |

## Templates

| File | Purpose |
|------|---------|
| `templates/models.py` | Model with custom QuerySet + clean() validation |
| `templates/services.py` | Service function wrapping multi-write flow in transaction.atomic |
| `templates/views.py` | Thin DRF ViewSet using select_related + service call |
| `templates/settings-base.py` | Base settings imported by dev/prod variants |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-practices-django-coding.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

- [[testing-django-pytest]]
- [[practices-python-ecosystem]]
- [[practices-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/models.py`

```python
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
```

### `templates/services.py`

```python
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
```

### `templates/views.py`

```python
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
```

### `templates/settings-base.py`

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
INSTALLED_APPS = ['django.contrib.admin']
```

### `templates/artefact.json`

```json
{
  "module_name": "orders",
  "fat_model_ok": true,
  "select_prefetch_ok": true,
  "atomic_writes_ok": true,
  "custom_queryset_ok": true,
  "settings_split_ok": true,
  "max_view_lines": 22
}
```
