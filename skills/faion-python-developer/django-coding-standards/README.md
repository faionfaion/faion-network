# Django Coding Standards

> LLM-optimized patterns for Django 6.x (2026) based on HackSoft Styleguide and Two Scoops.

## Overview

Django coding standards ensure consistent, maintainable code. These patterns cover project structure, service layer architecture, selectors, and view patterns that separate concerns and improve testability.

**Key sources:**
- [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide)
- [Two Scoops of Django 3.x](https://www.feldroy.com/two-scoops-of-django)
- [Django 6.0 Documentation](https://docs.djangoproject.com/en/6.0/)

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Services for writes** | Business logic in services, views handle HTTP only |
| **Selectors for reads** | Complex queries in selectors, not views or serializers |
| **Explicit imports** | Use aliases for cross-app imports to prevent circular deps |
| **Type hints everywhere** | All parameters and returns are typed |
| **Constants over magic** | Use `TextChoices` and `constants.py` |
| **Validation in models** | Use `clean()` for multi-field validations |

---

## Project Structure

```
project/
├── config/                    # Django configuration
│   ├── settings/
│   │   ├── base.py           # Common settings
│   │   ├── development.py    # Dev overrides (DEBUG=True)
│   │   └── production.py     # Prod overrides (security)
│   ├── urls.py               # Root URL configuration
│   ├── celery.py             # Celery app (if used)
│   └── tasks.py              # Django 6.0 native tasks
│
├── apps/                      # Domain applications
│   └── {app_name}/
│       ├── __init__.py
│       ├── apps.py           # App configuration
│       ├── constants.py      # TextChoices, limits, thresholds
│       ├── models.py         # Models with validation
│       ├── services.py       # Write operations (or services/)
│       ├── selectors.py      # Read operations (or selectors/)
│       ├── apis.py           # API views (or apis/)
│       ├── serializers.py    # DRF serializers
│       ├── urls.py           # App URL patterns
│       ├── admin.py          # Admin configuration
│       └── tests/
│           ├── __init__.py
│           ├── test_models.py
│           ├── test_services.py
│           ├── test_selectors.py
│           └── test_apis.py
│
├── core/                      # Shared code
│   ├── __init__.py
│   ├── models.py             # BaseModel
│   ├── exceptions.py         # Custom exceptions
│   ├── pagination.py         # Custom pagination
│   └── permissions.py        # Custom permissions
│
├── tests/
│   ├── conftest.py           # pytest fixtures
│   └── factories/            # Factory Boy factories
│
├── manage.py
├── pyproject.toml            # Dependencies + tools config
└── requirements/
    ├── base.txt
    ├── development.txt
    └── production.txt
```

---

## Naming Conventions

### Files and Modules

| Type | Convention | Example |
|------|------------|---------|
| Apps | `snake_case`, plural nouns | `users`, `orders`, `user_profiles` |
| Models | `PascalCase`, singular | `User`, `Order`, `UserProfile` |
| Services | `<entity>_<action>` | `user_create`, `order_process` |
| Selectors | `<entity>_<query>` | `user_list`, `order_get_by_id` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_ITEMS`, `DEFAULT_PAGE_SIZE` |
| TextChoices | `PascalCase` class, `UPPER` values | `OrderStatus.PENDING` |

### Services Naming Pattern

```python
# Pattern: <entity>_<action>

# Create operations
user_create(*, email: str, name: str) -> User
order_create(*, user: User, items: list[Item]) -> Order

# Update operations
user_update(*, user: User, data: dict) -> User
order_mark_paid(*, order: Order, transaction_id: str) -> Order

# Delete operations
user_deactivate(*, user: User) -> User
order_cancel(*, order: Order, reason: str) -> Order

# Complex actions
user_send_verification_email(*, user: User) -> None
order_process_payment(*, order: Order, payment_method: str) -> PaymentResult
```

### Selectors Naming Pattern

```python
# Pattern: <entity>_<query>

# Get single object
user_get_by_id(*, user_id: int) -> User
user_get_by_email(*, email: str) -> User | None

# Get lists
user_list(*, is_active: bool = True) -> QuerySet[User]
order_list_for_user(*, user: User) -> QuerySet[Order]

# Filtered queries
user_list_with_recent_orders(*, days: int = 30) -> QuerySet[User]
order_list_pending_payment() -> QuerySet[Order]
```

---

## Import Organization

Use `isort` with Django profile. Order:

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import uuid
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

# 3. Third-party
from django.db import models, transaction
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.views import APIView

# 4. Cross-app imports (ALWAYS use alias)
from apps.orders import models as order_models
from apps.orders import services as order_services
from apps.users import selectors as user_selectors

# 5. Local imports (relative)
from .constants import OrderStatus, MAX_ITEMS
from .models import Order
from .serializers import OrderCreateRequest, OrderResponse

# 6. TYPE_CHECKING imports (avoid circular imports)
if TYPE_CHECKING:
    from apps.users.models import User
```

### isort Configuration

```toml
# pyproject.toml
[tool.isort]
profile = "django"
line_length = 88
known_first_party = ["apps", "core", "config"]
sections = [
    "FUTURE",
    "STDLIB",
    "THIRDPARTY",
    "DJANGO",
    "FIRSTPARTY",
    "LOCALFOLDER"
]
known_django = ["django", "rest_framework"]
```

---

## Architecture Patterns

### Service Layer Pattern

**Where business logic lives:**

| Layer | Responsibility |
|-------|----------------|
| **Services** | Write operations, business rules, transactions |
| **Selectors** | Read operations, complex queries, filtering |
| **Models** | Data structure, simple validation, properties |
| **APIs/Views** | HTTP handling, auth, serialization |

**Where business logic does NOT belong:**

- Views/APIs (keep thin)
- Serializers (validation only)
- Model `save()` method
- Signals (hidden side effects)

### Service Structure

```python
# apps/orders/services.py
from django.db import transaction

from apps.orders.models import Order, OrderItem
from apps.products import selectors as product_selectors


def order_create(
    *,
    user: "User",
    items: list[dict],
    shipping_address: str,
) -> Order:
    """
    Create a new order with items.

    Args:
        user: The user placing the order
        items: List of {"product_id": int, "quantity": int}
        shipping_address: Delivery address

    Returns:
        Created Order instance

    Raises:
        ValidationError: If any product is unavailable
    """
    # Validate products exist and have stock
    product_ids = [item["product_id"] for item in items]
    products = product_selectors.product_list_by_ids(product_ids=product_ids)

    if len(products) != len(product_ids):
        raise ValidationError("Some products not found")

    with transaction.atomic():
        order = Order(
            user=user,
            shipping_address=shipping_address,
            status=OrderStatus.PENDING,
        )
        order.full_clean()
        order.save()

        for item in items:
            product = next(p for p in products if p.id == item["product_id"])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                unit_price=product.price,
            )

        order.calculate_total()

    return order
```

### Selector Structure

```python
# apps/orders/selectors.py
from django.db.models import QuerySet, Prefetch

from apps.orders.models import Order, OrderItem


def order_list_for_user(
    *,
    user: "User",
    status: str | None = None,
) -> QuerySet[Order]:
    """
    Get orders for a user with optimized queries.

    Args:
        user: The user to get orders for
        status: Optional status filter

    Returns:
        QuerySet of orders with prefetched items
    """
    queryset = Order.objects.filter(user=user).prefetch_related(
        Prefetch(
            "items",
            queryset=OrderItem.objects.select_related("product"),
        )
    )

    if status:
        queryset = queryset.filter(status=status)

    return queryset.order_by("-created_at")


def order_get_by_id(*, order_id: int, user: "User" = None) -> Order:
    """
    Get single order by ID.

    Args:
        order_id: The order ID
        user: Optional user for ownership check

    Returns:
        Order instance

    Raises:
        Order.DoesNotExist: If order not found
    """
    queryset = Order.objects.prefetch_related("items__product")

    if user:
        queryset = queryset.filter(user=user)

    return queryset.get(id=order_id)
```

---

## Django 6.0 Features

### Native Background Tasks

```python
# config/tasks.py
from django.tasks import task

@task
def send_order_confirmation(order_id: int) -> None:
    """Send order confirmation email asynchronously."""
    from apps.orders import selectors as order_selectors
    from apps.notifications import services as notification_services

    order = order_selectors.order_get_by_id(order_id=order_id)
    notification_services.send_email(
        to=order.user.email,
        template="order_confirmation",
        context={"order": order},
    )


# Usage in service
from config.tasks import send_order_confirmation

def order_complete(*, order: Order) -> Order:
    order.status = OrderStatus.COMPLETED
    order.save(update_fields=["status", "updated_at"])

    # Queue background task
    send_order_confirmation.enqueue(order_id=order.id)

    return order
```

### Template Partials

```html
<!-- templates/orders/order_list.html -->
{% partialdef order_card %}
<div class="order-card">
    <h3>Order #{{ order.id }}</h3>
    <p>{{ order.status }}</p>
    <p>{{ order.total|currency }}</p>
</div>
{% endpartialdef %}

{% for order in orders %}
    {% partial order_card %}
{% endfor %}
```

### Content Security Policy

```python
# config/settings/production.py
from django.conf.global_settings import CONTENT_SECURITY_POLICY

CONTENT_SECURITY_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "cdn.example.com"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", "data:", "*.cloudinary.com"],
}
```

---

## Error Handling

### Custom Exceptions

```python
# core/exceptions.py
from rest_framework.exceptions import APIException
from rest_framework import status


class ApplicationError(Exception):
    """Base exception for business logic errors."""

    def __init__(self, message: str, extra: dict = None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class NotFoundError(ApplicationError):
    """Resource not found."""
    pass


class ValidationError(ApplicationError):
    """Business validation failed."""
    pass


class PermissionDeniedError(ApplicationError):
    """User lacks permission for this action."""
    pass
```

### Exception Handler

```python
# core/exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from core.exceptions import ApplicationError, NotFoundError, ValidationError


def custom_exception_handler(exc, context):
    """Handle both DRF and custom exceptions."""
    response = exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, NotFoundError):
        return Response(
            {"error": exc.message, "extra": exc.extra},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, ValidationError):
        return Response(
            {"error": exc.message, "extra": exc.extra},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, ApplicationError):
        return Response(
            {"error": exc.message, "extra": exc.extra},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return None
```

---

## Testing Strategy

### Test Organization

| Test Type | Location | What to Test |
|-----------|----------|--------------|
| Models | `test_models.py` | Validation, properties, clean() |
| Services | `test_services.py` | Business logic, transactions |
| Selectors | `test_selectors.py` | Queries, filtering, N+1 |
| APIs | `test_apis.py` | HTTP codes, auth, serialization |

### Factory Pattern

```python
# tests/factories/orders.py
import factory
from factory.django import DjangoModelFactory

from apps.orders.models import Order, OrderItem
from apps.orders.constants import OrderStatus


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory("tests.factories.users.UserFactory")
    status = OrderStatus.PENDING
    shipping_address = factory.Faker("address")
    total = factory.Faker("pydecimal", left_digits=4, right_digits=2)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory("tests.factories.products.ProductFactory")
    quantity = factory.Faker("random_int", min=1, max=10)
    unit_price = factory.LazyAttribute(lambda obj: obj.product.price)
```

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Code review checklist |
| [examples.md](examples.md) | Good/bad code examples |
| [templates.md](templates.md) | Code templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for code generation |

---

## References

- [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide) - Service/selector architecture
- [HackSoft Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example) - Reference implementation
- [Two Scoops of Django 3.x](https://www.feldroy.com/two-scoops-of-django) - Django patterns book
- [Django 6.0 Release Notes](https://docs.djangoproject.com/en/6.0/releases/6.0/) - Native tasks, CSP, partials
- [Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) - Official style guide
