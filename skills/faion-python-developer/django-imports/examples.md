# Django Import Examples

Real-world examples and anti-patterns for Django import organization.

## Good Examples

### Complete Django View File

```python
"""Views for the orders app."""
from __future__ import annotations

import logging
from datetime import timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.catalog import models as catalog_models
from apps.catalog import services as catalog_services
from apps.users import models as user_models

from .forms import OrderForm
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .services import OrderService

if TYPE_CHECKING:
    from apps.payments.models import Payment
    from apps.shipping.models import Shipment


logger = logging.getLogger(__name__)


class OrderCreateView(View):
    """Create new order."""

    def post(self, request: HttpRequest) -> HttpResponse:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = OrderService.create_order(
                user=request.user,
                items=form.cleaned_data["items"],
            )
            return redirect("orders:detail", pk=order.pk)
        return render(request, "orders/create.html", {"form": form})
```

### Django Model with Cross-App References

```python
"""Order models."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel

if TYPE_CHECKING:
    from apps.payments.models import Payment


class Order(TimeStampedModel):
    """Customer order."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    # String reference - no import needed
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    # String reference for cross-app relation
    shipping_address = models.ForeignKey(
        "addresses.Address",
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def get_payment(self) -> Payment | None:
        """Get associated payment (lazy import)."""
        from apps.payments.models import Payment

        return Payment.objects.filter(order=self).first()

    def get_items_count(self) -> int:
        """Get count of order items."""
        return self.items.count()


class OrderItem(TimeStampedModel):
    """Single item in an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    # String reference to catalog app
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self) -> Decimal:
        """Calculate item total."""
        return self.unit_price * self.quantity
```

### Service Layer with apps.get_model()

```python
"""Order services."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.apps import apps
from django.db import transaction

from .models import Order, OrderItem

if TYPE_CHECKING:
    from apps.catalog.models import Product
    from apps.users.models import User


class OrderService:
    """Order business logic."""

    @classmethod
    @transaction.atomic
    def create_order(
        cls,
        user: User,
        items: list[dict],
    ) -> Order:
        """Create order with items."""
        # Use apps.get_model for runtime model access
        Product = apps.get_model("catalog", "Product")

        order = Order.objects.create(
            user=user,
            total=Decimal("0"),
        )

        total = Decimal("0")
        for item_data in items:
            product = Product.objects.get(pk=item_data["product_id"])
            quantity = item_data["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
            )
            total += product.price * quantity

        order.total = total
        order.save(update_fields=["total"])

        return order

    @classmethod
    def get_user_orders(cls, user_id: int) -> list[Order]:
        """Get all orders for user."""
        return list(
            Order.objects.filter(user_id=user_id)
            .select_related("shipping_address")
            .prefetch_related("items__product")
        )
```

### Serializers with TYPE_CHECKING

```python
"""Order serializers."""
from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import serializers

from apps.catalog import serializers as catalog_serializers

from .models import Order, OrderItem

if TYPE_CHECKING:
    from apps.users.models import User


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items."""

    product = catalog_serializers.ProductSerializer(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders."""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "status", "total", "items", "created_at"]
        read_only_fields = ["user", "total", "created_at"]
```

### Celery Tasks with Lazy Imports

```python
"""Order-related Celery tasks."""
from __future__ import annotations

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_order_confirmation(order_id: int) -> None:
    """Send order confirmation email."""
    # Lazy import to avoid circular imports and improve task startup
    from apps.orders.models import Order
    from apps.notifications.services import EmailService

    order = Order.objects.select_related("user").get(pk=order_id)

    EmailService.send_order_confirmation(
        email=order.user.email,
        order=order,
    )

    logger.info("Sent confirmation for order %s", order_id)


@shared_task
def process_order_payment(order_id: int) -> None:
    """Process payment for order."""
    from django.apps import apps

    Order = apps.get_model("orders", "Order")
    PaymentService = apps.get_model("payments", "PaymentService")

    order = Order.objects.get(pk=order_id)
    PaymentService.process(order)
```

## Anti-Patterns (Avoid These)

### Wildcard Imports

```python
# BAD - namespace pollution, unclear dependencies
from apps.orders.models import *
from apps.users.models import *

# Order and User could conflict with local names
```

### Direct Class Imports from Other Apps

```python
# BAD - prone to naming conflicts
from apps.orders.models import Order, OrderItem
from apps.users.models import User, Profile
from apps.catalog.models import Product, Category

# What if orders also has a Product model?
```

### Import Cycles at File Level

```python
# apps/orders/models.py
from apps.payments.models import Payment  # BAD - may cause circular import

class Order(models.Model):
    def get_payment(self):
        return Payment.objects.filter(order=self).first()
```

```python
# apps/payments/models.py
from apps.orders.models import Order  # CIRCULAR IMPORT!

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
```

### Multi-Dot Relative Imports

```python
# BAD - hard to understand, fragile
from ...users.models import User
from ..catalog.services import CatalogService

# GOOD - use absolute imports for cross-app
from apps.users import models as user_models
from apps.catalog import services as catalog_services
```

### Imports Inside __init__.py for "Convenience"

```python
# apps/orders/__init__.py
# BAD - causes unnecessary imports on any module access
from .models import Order, OrderItem
from .services import OrderService
from .serializers import OrderSerializer
```

### TYPE_CHECKING with Runtime Usage

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.models import User

def create_user() -> User:
    # BAD - User is not available at runtime!
    return User.objects.create(username="test")
```

### Importing Models in apps.py

```python
# apps/orders/apps.py
# BAD - models aren't ready when apps.py loads
from .models import Order

class OrdersConfig(AppConfig):
    name = "apps.orders"

    def ready(self):
        # Models are ready here
        from .models import Order  # OK in ready()
        from . import signals  # OK - register signals
```

## Refactoring Examples

### Before: Circular Import Issue

```python
# apps/orders/services.py (BEFORE)
from apps.payments.services import PaymentService  # Circular!

class OrderService:
    def complete(self, order):
        PaymentService.charge(order)
```

```python
# apps/payments/services.py (BEFORE)
from apps.orders.services import OrderService  # Circular!

class PaymentService:
    def refund(self, payment):
        OrderService.cancel(payment.order)
```

### After: Fixed with Lazy Import

```python
# apps/orders/services.py (AFTER)
class OrderService:
    def complete(self, order):
        from apps.payments.services import PaymentService  # Lazy
        PaymentService.charge(order)
```

```python
# apps/payments/services.py (AFTER)
class PaymentService:
    def refund(self, payment):
        from apps.orders.services import OrderService  # Lazy
        OrderService.cancel(payment.order)
```

### After: Fixed with Dependency Injection

```python
# apps/orders/services.py (AFTER - better architecture)
class OrderService:
    def complete(self, order, payment_processor=None):
        if payment_processor is None:
            from apps.payments.services import PaymentService
            payment_processor = PaymentService
        payment_processor.charge(order)
```

### After: Fixed with Signals (Best for Cross-App Events)

```python
# apps/orders/signals.py
from django.dispatch import Signal

order_completed = Signal()  # sender, order

# apps/orders/services.py
from .signals import order_completed

class OrderService:
    def complete(self, order):
        order.status = "completed"
        order.save()
        order_completed.send(sender=self.__class__, order=order)

# apps/payments/receivers.py
from apps.orders.signals import order_completed

@receiver(order_completed)
def charge_order_payment(sender, order, **kwargs):
    from .services import PaymentService
    PaymentService.charge(order)
```

## Python Version-Specific Examples

### Python 3.9 (with __future__)

```python
from __future__ import annotations
from typing import Optional, List

def get_users() -> List[User]:
    pass

def get_order(id: int) -> Optional[Order]:
    pass
```

### Python 3.10+ (Native Union Syntax)

```python
def get_order(id: int) -> Order | None:
    pass

def get_users() -> list[User]:
    pass
```

### Python 3.14+ (Explicit Lazy Imports)

```python
# Future: PEP 810 explicit lazy imports
lazy from heavy_analytics import ReportGenerator

def generate_report():
    # ReportGenerator module loaded only here
    return ReportGenerator().run()
```
