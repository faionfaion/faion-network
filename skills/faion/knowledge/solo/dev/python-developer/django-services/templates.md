# Django Services Templates

Copy-paste templates for service classes, functions, selectors, and tests.

---

## Service Function Templates

### Basic Service Function

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.your_app.models import YourModel


def entity_action(
    *,
    required_param: str,
    optional_param: str | None = None,
) -> YourModel:
    """
    One-line description of what this service does.

    Business logic:
    - First business rule
    - Second business rule

    Args:
        required_param: Description of this parameter.
        optional_param: Description of optional parameter.

    Returns:
        Description of return value.

    Raises:
        ValidationError: When validation fails.
    """
    from apps.your_app.models import YourModel

    # Implementation
    instance = YourModel.objects.create(
        field=required_param,
    )

    return instance
```

### Service with Transaction

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import transaction

if TYPE_CHECKING:
    from apps.orders.models import Order
    from apps.users.models import User


@transaction.atomic
def order_create(
    *,
    user: User,
    items: list[dict],
    notes: str | None = None,
) -> Order:
    """
    Create an order with items.

    Business logic:
    - Validates item availability
    - Creates order and order items
    - Updates inventory

    Args:
        user: User placing the order.
        items: List of item dicts with product_id and quantity.
        notes: Optional order notes.

    Returns:
        Created Order instance.

    Raises:
        ValidationError: If items are invalid.
        InsufficientStockError: If item out of stock.
    """
    from apps.orders.models import Order, OrderItem
    from apps.products.models import Product

    # Validate items
    _validate_items(items=items)

    # Create order
    order = Order.objects.create(
        user=user,
        notes=notes or '',
        status='pending',
    )

    # Create order items
    _create_order_items(order=order, items=items)

    return order


def _validate_items(*, items: list[dict]) -> None:
    """Validate all items exist and have stock."""
    # Implementation
    pass


def _create_order_items(*, order: Order, items: list[dict]) -> None:
    """Create order items in bulk."""
    # Implementation
    pass
```

### Service with Input Validation (Pydantic)

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel, EmailStr, field_validator
from django.db import transaction

if TYPE_CHECKING:
    from apps.users.models import User


class UserCreateInput(BaseModel):
    """Input validation for user creation."""
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


@transaction.atomic
def user_create(*, input_data: UserCreateInput) -> User:
    """
    Create a new user.

    Args:
        input_data: Validated user creation input.

    Returns:
        Created User instance.

    Raises:
        UserAlreadyExistsError: If email already registered.
    """
    from apps.users.models import User
    from apps.users.exceptions import UserAlreadyExistsError

    if User.objects.filter(email=input_data.email).exists():
        raise UserAlreadyExistsError(email=input_data.email)

    return User.objects.create_user(
        email=input_data.email,
        password=input_data.password,
        first_name=input_data.first_name or '',
        last_name=input_data.last_name or '',
    )
```

### Service with Dependency Injection

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from apps.orders.models import Order


class PaymentGateway(Protocol):
    """Protocol for payment gateway implementations."""

    def charge(self, amount: int, customer_id: str) -> str:
        """Charge customer and return transaction ID."""
        ...

    def refund(self, transaction_id: str) -> bool:
        """Refund a transaction."""
        ...


class EmailService(Protocol):
    """Protocol for email service implementations."""

    def send(self, to: str, subject: str, body: str) -> None:
        """Send an email."""
        ...


def order_process_payment(
    *,
    order: Order,
    payment_gateway: PaymentGateway,
    email_service: EmailService,
) -> Order:
    """
    Process payment for an order.

    Args:
        order: Order to process payment for.
        payment_gateway: Payment gateway implementation.
        email_service: Email service implementation.

    Returns:
        Updated Order instance.

    Raises:
        PaymentFailedError: If payment fails.
    """
    from apps.orders.exceptions import PaymentFailedError

    try:
        transaction_id = payment_gateway.charge(
            amount=int(order.total * 100),
            customer_id=order.user.payment_customer_id,
        )
    except Exception as e:
        raise PaymentFailedError(order_id=order.id, reason=str(e))

    order.payment_transaction_id = transaction_id
    order.status = 'paid'
    order.save(update_fields=['payment_transaction_id', 'status', 'updated_at'])

    email_service.send(
        to=order.user.email,
        subject=f'Order {order.id} Confirmed',
        body=f'Your payment has been processed.',
    )

    return order
```

---

## Selector Templates

### Basic Selector

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from django.db.models import QuerySet

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.orders.models import Order


def user_orders(
    *,
    user: User,
    status: str | None = None,
) -> QuerySet[Order]:
    """
    Get orders for a user.

    Query count: 1

    Args:
        user: User to get orders for.
        status: Optional status filter.

    Returns:
        QuerySet of Order instances.
    """
    from apps.orders.models import Order

    qs = Order.objects.filter(user=user)

    if status:
        qs = qs.filter(status=status)

    return qs.order_by('-created_at')
```

### Selector with Prefetching

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from django.db.models import QuerySet, Count, Prefetch

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.orders.models import Order


def user_orders_with_items(
    *,
    user: User,
    limit: int = 10,
) -> QuerySet[Order]:
    """
    Get user's orders with items prefetched.

    Optimized for serialization - avoids N+1 queries.

    Query count: 3 (orders, items, products)

    Args:
        user: User to get orders for.
        limit: Maximum number of orders to return.

    Returns:
        QuerySet of Order instances with items prefetched.
    """
    from apps.orders.models import Order, OrderItem

    return (
        Order.objects
        .filter(user=user)
        .select_related('shipping_address', 'billing_address')
        .prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product'),
            )
        )
        .annotate(item_count=Count('items'))
        .order_by('-created_at')[:limit]
    )
```

### Selector with Aggregations

```python
from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING
from django.db.models import Sum, Avg, Count, QuerySet
from django.db.models.functions import TruncMonth

if TYPE_CHECKING:
    from apps.analytics.types import MonthlySalesData


def sales_monthly_summary(
    *,
    start_date: date,
    end_date: date,
) -> QuerySet:
    """
    Get monthly sales summary.

    Query count: 1

    Args:
        start_date: Start of date range.
        end_date: End of date range.

    Returns:
        QuerySet with month, total_sales, order_count, avg_order_value.
    """
    from apps.orders.models import Order

    return (
        Order.objects
        .filter(
            status='completed',
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
        )
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total_sales=Sum('total'),
            order_count=Count('id'),
            avg_order_value=Avg('total'),
        )
        .order_by('month')
    )
```

---

## Exception Templates

### Exception Hierarchy

```python
# exceptions.py

class ServiceError(Exception):
    """Base exception for all service errors."""
    pass


class ValidationError(ServiceError):
    """Raised when input validation fails."""
    pass


class NotFoundError(ServiceError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, identifier: str | int):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id {identifier} not found")


class PermissionDeniedError(ServiceError):
    """Raised when user lacks permission."""

    def __init__(self, action: str, resource: str):
        self.action = action
        self.resource = resource
        super().__init__(f"Permission denied: cannot {action} {resource}")


class BusinessRuleError(ServiceError):
    """Raised when a business rule is violated."""
    pass


class ExternalServiceError(ServiceError):
    """Raised when an external service fails."""

    def __init__(self, service: str, reason: str):
        self.service = service
        self.reason = reason
        super().__init__(f"External service error ({service}): {reason}")
```

### Domain-Specific Exceptions

```python
# apps/orders/exceptions.py
from apps.core.exceptions import BusinessRuleError, ExternalServiceError


class InsufficientStockError(BusinessRuleError):
    """Raised when product is out of stock."""

    def __init__(
        self,
        product_id: int,
        available: int = 0,
        requested: int = 0,
    ):
        self.product_id = product_id
        self.available = available
        self.requested = requested
        super().__init__(
            f"Product {product_id}: available {available}, requested {requested}"
        )


class OrderAlreadyCancelledError(BusinessRuleError):
    """Raised when trying to cancel an already cancelled order."""

    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order {order_id} is already cancelled")


class PaymentFailedError(ExternalServiceError):
    """Raised when payment processing fails."""

    def __init__(self, order_id: int, reason: str):
        self.order_id = order_id
        super().__init__(service='payment', reason=f"Order {order_id}: {reason}")
```

---

## Test Templates

### Basic Service Test

```python
# tests/services/test_user_services.py
import pytest
from apps.users.services import user_create
from apps.users.exceptions import UserAlreadyExistsError


class TestUserCreate:
    """Tests for user_create service."""

    def test_creates_user_with_valid_data(self, db):
        """Test successful user creation."""
        user = user_create(
            email='test@example.com',
            password='securepass123',
        )

        assert user.id is not None
        assert user.email == 'test@example.com'
        assert user.check_password('securepass123')

    def test_raises_error_for_duplicate_email(self, db, user_factory):
        """Test error when email already exists."""
        user_factory(email='taken@example.com')

        with pytest.raises(UserAlreadyExistsError) as exc:
            user_create(
                email='taken@example.com',
                password='securepass123',
            )

        assert 'taken@example.com' in str(exc.value)

    def test_creates_inactive_user_when_specified(self, db):
        """Test creating inactive user."""
        user = user_create(
            email='test@example.com',
            password='securepass123',
            is_active=False,
        )

        assert user.is_active is False
```

### Service Test with Mocking

```python
# tests/services/test_order_services.py
import pytest
from unittest.mock import Mock, patch
from apps.orders.services import order_process_payment
from apps.orders.exceptions import PaymentFailedError


class TestOrderProcessPayment:
    """Tests for order_process_payment service."""

    def test_processes_payment_successfully(self, db, order_factory):
        """Test successful payment processing."""
        order = order_factory(status='pending', total=100.00)
        mock_gateway = Mock()
        mock_gateway.charge.return_value = 'txn_123'
        mock_email = Mock()

        result = order_process_payment(
            order=order,
            payment_gateway=mock_gateway,
            email_service=mock_email,
        )

        assert result.status == 'paid'
        assert result.payment_transaction_id == 'txn_123'
        mock_gateway.charge.assert_called_once_with(
            amount=10000,
            customer_id=order.user.payment_customer_id,
        )
        mock_email.send.assert_called_once()

    def test_raises_error_when_payment_fails(self, db, order_factory):
        """Test payment failure handling."""
        order = order_factory(status='pending')
        mock_gateway = Mock()
        mock_gateway.charge.side_effect = Exception('Card declined')
        mock_email = Mock()

        with pytest.raises(PaymentFailedError) as exc:
            order_process_payment(
                order=order,
                payment_gateway=mock_gateway,
                email_service=mock_email,
            )

        assert 'Card declined' in str(exc.value)
        mock_email.send.assert_not_called()
```

### Factory Boy Factories

```python
# tests/factories.py
import factory
from factory.django import DjangoModelFactory
from apps.users.models import User
from apps.orders.models import Order, OrderItem
from apps.products.models import Product


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True

    @factory.lazy_attribute
    def password(self):
        from django.contrib.auth.hashers import make_password
        return make_password('testpass123')


class ProductFactory(DjangoModelFactory):
    """Factory for Product model."""

    class Meta:
        model = Product

    name = factory.Faker('product_name')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=0, max=100)


class OrderFactory(DjangoModelFactory):
    """Factory for Order model."""

    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    status = 'pending'
    total = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)


class OrderItemFactory(DjangoModelFactory):
    """Factory for OrderItem model."""

    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=5)
    unit_price = factory.LazyAttribute(lambda obj: obj.product.price)
```

### Conftest Setup

```python
# tests/conftest.py
import pytest
from tests.factories import (
    UserFactory,
    ProductFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.fixture
def user_factory():
    """Return UserFactory for creating users."""
    return UserFactory


@pytest.fixture
def product_factory():
    """Return ProductFactory for creating products."""
    return ProductFactory


@pytest.fixture
def order_factory():
    """Return OrderFactory for creating orders."""
    return OrderFactory


@pytest.fixture
def order_item_factory():
    """Return OrderItemFactory for creating order items."""
    return OrderItemFactory


@pytest.fixture
def user(db):
    """Create a test user."""
    return UserFactory()


@pytest.fixture
def admin_user(db):
    """Create a test admin user."""
    return UserFactory(is_staff=True, is_superuser=True)
```

---

## File Structure Template

### services/__init__.py

```python
# services/__init__.py
"""
Services module - business logic for the app.

Services handle write operations (CREATE, UPDATE, DELETE)
and business logic that spans multiple models.
"""

from apps.your_app.services.user_services import (
    user_create,
    user_update,
    user_deactivate,
)
from apps.your_app.services.order_services import (
    order_create,
    order_cancel,
    order_process_payment,
)

__all__ = [
    # User services
    'user_create',
    'user_update',
    'user_deactivate',
    # Order services
    'order_create',
    'order_cancel',
    'order_process_payment',
]
```

### selectors/__init__.py

```python
# selectors/__init__.py
"""
Selectors module - read operations for the app.

Selectors handle complex queries, permission-based filtering,
and optimized data fetching.
"""

from apps.your_app.selectors.user_selectors import (
    user_get_by_id,
    user_list_active,
)
from apps.your_app.selectors.order_selectors import (
    order_get_for_user,
    order_list_with_items,
)

__all__ = [
    # User selectors
    'user_get_by_id',
    'user_list_active',
    # Order selectors
    'order_get_for_user',
    'order_list_with_items',
]
```

---

*Part of the faion-python-developer skill. Last updated: 2026-01.*
