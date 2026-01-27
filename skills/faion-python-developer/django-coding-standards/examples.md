# Django Code Examples

> Good vs bad patterns for common Django scenarios.

---

## Table of Contents

1. [Service Layer](#service-layer)
2. [Selectors](#selectors)
3. [Views/APIs](#viewsapis)
4. [Models](#models)
5. [Serializers](#serializers)
6. [Imports](#imports)
7. [Error Handling](#error-handling)
8. [Testing](#testing)
9. [Constants](#constants)
10. [Queries](#queries)

---

## Service Layer

### Creating Objects

```python
# BAD - Logic in view, no validation
class UserCreateView(APIView):
    def post(self, request):
        user = User.objects.create(
            email=request.data['email'],
            name=request.data['name'],
        )
        send_welcome_email(user)  # Side effect in view
        return Response({'id': user.id})
```

```python
# GOOD - Service handles all logic
# services.py
def user_create(
    *,
    email: str,
    name: str,
    send_welcome: bool = True,
) -> User:
    """
    Create a new user with validation.

    Args:
        email: User's email address
        name: User's display name
        send_welcome: Whether to send welcome email

    Returns:
        Created User instance

    Raises:
        ValidationError: If email already exists
    """
    user = User(email=email, name=name)
    user.full_clean()  # Triggers model validation
    user.save()

    if send_welcome:
        send_welcome_email.enqueue(user_id=user.id)

    return user


# views.py
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_create(**serializer.validated_data)

        return Response(
            UserResponse(user).data,
            status=status.HTTP_201_CREATED,
        )
```

### Updating Objects

```python
# BAD - Partial update without update_fields
def user_update(user: User, data: dict) -> User:
    for key, value in data.items():
        setattr(user, key, value)
    user.save()  # Updates ALL fields
    return user
```

```python
# GOOD - Explicit update_fields
def user_update(
    *,
    user: User,
    name: str | None = None,
    bio: str | None = None,
) -> User:
    """Update user profile fields."""
    fields_to_update = []

    if name is not None:
        user.name = name
        fields_to_update.append("name")

    if bio is not None:
        user.bio = bio
        fields_to_update.append("bio")

    if fields_to_update:
        user.full_clean()
        user.save(update_fields=[*fields_to_update, "updated_at"])

    return user
```

### Multi-Model Operations

```python
# BAD - No transaction, partial failure possible
def order_create(user: User, items: list) -> Order:
    order = Order.objects.create(user=user)
    for item in items:
        OrderItem.objects.create(order=order, **item)
    order.total = sum(i.price for i in order.items.all())
    order.save()
    return order
```

```python
# GOOD - Atomic transaction
from django.db import transaction

def order_create(
    *,
    user: User,
    items: list[dict],
    shipping_address: str,
) -> Order:
    """
    Create order with items atomically.

    Args:
        user: The user placing the order
        items: List of {"product_id": int, "quantity": int}
        shipping_address: Delivery address

    Returns:
        Created Order with items

    Raises:
        ValidationError: If products unavailable
    """
    with transaction.atomic():
        order = Order(
            user=user,
            shipping_address=shipping_address,
            status=OrderStatus.PENDING,
        )
        order.full_clean()
        order.save()

        total = Decimal("0")
        for item_data in items:
            product = Product.objects.get(id=item_data["product_id"])
            item = OrderItem(
                order=order,
                product=product,
                quantity=item_data["quantity"],
                unit_price=product.price,
            )
            item.full_clean()
            item.save()
            total += item.unit_price * item.quantity

        order.total = total
        order.save(update_fields=["total", "updated_at"])

    return order
```

---

## Selectors

### Basic Query

```python
# BAD - Query in view, no optimization
class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)
```

```python
# GOOD - Selector with optimization
# selectors.py
def order_list_for_user(
    *,
    user: User,
    status: str | None = None,
    limit: int | None = None,
) -> QuerySet[Order]:
    """
    Get orders for user with related data.

    Args:
        user: The user to query orders for
        status: Optional status filter
        limit: Optional result limit

    Returns:
        Optimized QuerySet of orders
    """
    queryset = (
        Order.objects
        .filter(user=user)
        .select_related("shipping_method")
        .prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by("-created_at")
    )

    if status:
        queryset = queryset.filter(status=status)

    if limit:
        queryset = queryset[:limit]

    return queryset


# views.py
class OrderListView(APIView):
    def get(self, request):
        orders = order_list_for_user(
            user=request.user,
            status=request.query_params.get("status"),
        )
        return Response(OrderListResponse(orders, many=True).data)
```

### Single Object Fetch

```python
# BAD - Raw get without handling
def get_order(order_id: int):
    return Order.objects.get(id=order_id)
```

```python
# GOOD - With optional ownership check
def order_get_by_id(
    *,
    order_id: int,
    user: User | None = None,
) -> Order:
    """
    Fetch single order by ID.

    Args:
        order_id: The order primary key
        user: Optional user for ownership verification

    Returns:
        Order instance

    Raises:
        Order.DoesNotExist: If not found or not owned by user
    """
    queryset = Order.objects.select_related(
        "user",
        "shipping_method",
    ).prefetch_related("items__product")

    if user:
        queryset = queryset.filter(user=user)

    return queryset.get(id=order_id)
```

---

## Views/APIs

### View Structure

```python
# BAD - Fat view with mixed concerns
class CreateOrderView(APIView):
    def post(self, request):
        # Validation mixed with logic
        items = request.data.get('items', [])
        if not items:
            return Response({'error': 'No items'}, status=400)

        # Business logic in view
        user = request.user
        total = 0
        order = Order.objects.create(user=user)

        for item in items:
            product = Product.objects.get(id=item['product_id'])
            if product.stock < item['quantity']:
                order.delete()
                return Response({'error': 'Out of stock'}, status=400)
            total += product.price * item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )

        order.total = total
        order.save()

        # Send email directly
        send_mail(
            'Order Confirmation',
            f'Your order {order.id} is confirmed',
            'noreply@example.com',
            [user.email]
        )

        return Response({'id': order.id, 'total': total})
```

```python
# GOOD - Thin view delegating to service
class OrderCreateView(APIView):
    """Create a new order for authenticated user."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Validate input
        serializer = OrderCreateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Call service
        order = order_create(
            user=request.user,
            items=serializer.validated_data["items"],
            shipping_address=serializer.validated_data["shipping_address"],
        )

        # 3. Return response
        return Response(
            OrderResponse(order).data,
            status=status.HTTP_201_CREATED,
        )
```

### Error Responses

```python
# BAD - Inconsistent error format
class UserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User not found", status=404)
        except Exception as e:
            return Response(str(e), status=500)
```

```python
# GOOD - Consistent error handling via exceptions
class UserView(APIView):
    def get(self, request, user_id: int):
        user = user_get_by_id(user_id=user_id)  # Raises DoesNotExist
        return Response(UserResponse(user).data)


# Exception handler converts to consistent format
# {"error": "User not found", "code": "not_found"}
```

---

## Models

### Base Model

```python
# BAD - Repeated fields in every model
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ... fields


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ... fields
```

```python
# GOOD - Abstract base model
# core/models.py
class BaseModel(models.Model):
    """Base model with timestamps."""

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# apps/orders/models.py
class Order(BaseModel):
    """Customer order."""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self) -> str:
        return f"Order #{self.id}"
```

### Model Validation

```python
# BAD - Validation in save()
class Event(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if self.end_date < self.start_date:
            raise ValueError("End date must be after start date")
        super().save(*args, **kwargs)
```

```python
# GOOD - Validation in clean() + DB constraint
class Event(BaseModel):
    """Scheduled event."""

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="event_end_after_start",
            ),
        ]

    def clean(self) -> None:
        """Validate event dates."""
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({
                "end_date": "End date must be after start date",
            })
```

---

## Serializers

### Input vs Output

```python
# BAD - Same serializer for input and output
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'is_staff', 'created_at']
```

```python
# GOOD - Separate input and output serializers
class UserCreateRequest(serializers.Serializer):
    """Input serializer for user creation."""

    email = serializers.EmailField()
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=8, write_only=True)


class UserResponse(serializers.Serializer):
    """Output serializer for user data."""

    id = serializers.IntegerField()
    email = serializers.EmailField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    # Note: password and is_staff NOT exposed


class UserDetailResponse(UserResponse):
    """Extended user response with additional fields."""

    orders_count = serializers.SerializerMethodField()

    def get_orders_count(self, obj: User) -> int:
        return obj.orders.count()
```

### Nested Serializers

```python
# BAD - No related data optimization
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # N+1 query

    class Meta:
        model = Order
        fields = ['id', 'items', 'total']
```

```python
# GOOD - Selector provides optimized queryset
# selectors.py returns prefetched data
# Serializer just formats it

class OrderItemResponse(serializers.Serializer):
    """Order item with product details."""

    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    product_name = serializers.CharField(source="product.name")


class OrderResponse(serializers.Serializer):
    """Complete order response."""

    id = serializers.IntegerField()
    status = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = OrderItemResponse(many=True)
    created_at = serializers.DateTimeField()
```

---

## Imports

```python
# BAD - Messy imports, circular import risk
from apps.orders.models import Order, OrderItem
from datetime import datetime
from apps.users.models import User
from django.db import models
import uuid
from typing import Optional
from .services import *
```

```python
# GOOD - Organized imports with aliases
from __future__ import annotations

# Standard library
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

# Third-party
from django.db import models, transaction
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.views import APIView

# Cross-app (with aliases)
from apps.orders import models as order_models
from apps.orders import selectors as order_selectors
from apps.products import services as product_services

# Local (relative)
from .constants import UserStatus, MAX_ORDERS_PER_DAY
from .models import User
from .serializers import UserCreateRequest, UserResponse

# Type checking only
if TYPE_CHECKING:
    from django.db.models import QuerySet
```

---

## Error Handling

```python
# BAD - Bare except, generic errors
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        return None
```

```python
# GOOD - Specific exceptions, proper handling
from core.exceptions import NotFoundError, ValidationError


def user_get_by_id(*, user_id: int) -> User:
    """
    Fetch user by ID.

    Raises:
        NotFoundError: If user doesn't exist
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFoundError(f"User {user_id} not found")


def user_create(*, email: str, name: str) -> User:
    """
    Create user with validation.

    Raises:
        ValidationError: If email already exists
    """
    if User.objects.filter(email=email).exists():
        raise ValidationError(
            "Email already registered",
            extra={"email": email},
        )

    user = User(email=email, name=name)
    user.full_clean()
    user.save()
    return user
```

---

## Testing

```python
# BAD - Tests without factories, unclear names
class TestUser(TestCase):
    def test_1(self):
        u = User.objects.create(email='test@test.com', name='Test')
        self.assertEqual(u.email, 'test@test.com')
```

```python
# GOOD - Factories, descriptive names, isolated tests
import pytest
from tests.factories import UserFactory, OrderFactory


class TestUserCreate:
    """Tests for user_create service."""

    def test_creates_user_with_valid_data(self, db):
        """User is created when valid data provided."""
        user = user_create(
            email="john@example.com",
            name="John Doe",
        )

        assert user.id is not None
        assert user.email == "john@example.com"
        assert user.name == "John Doe"

    def test_raises_error_for_duplicate_email(self, db):
        """ValidationError raised when email exists."""
        UserFactory(email="existing@example.com")

        with pytest.raises(ValidationError) as exc_info:
            user_create(
                email="existing@example.com",
                name="New User",
            )

        assert "already registered" in str(exc_info.value)


class TestOrderListForUser:
    """Tests for order_list_for_user selector."""

    def test_returns_only_user_orders(self, db):
        """Only orders belonging to user are returned."""
        user = UserFactory()
        other_user = UserFactory()

        user_order = OrderFactory(user=user)
        OrderFactory(user=other_user)  # Should not be returned

        orders = order_list_for_user(user=user)

        assert list(orders) == [user_order]

    def test_no_n_plus_one_queries(self, db, django_assert_num_queries):
        """Selector uses optimal number of queries."""
        user = UserFactory()
        OrderFactory.create_batch(5, user=user)

        with django_assert_num_queries(2):  # 1 for orders, 1 for items
            orders = list(order_list_for_user(user=user))
            # Access related data to trigger queries
            for order in orders:
                list(order.items.all())
```

---

## Constants

```python
# BAD - Magic strings and numbers
class Order(models.Model):
    status = models.CharField(max_length=20, default='pending')

def check_limit(user):
    if user.orders.count() > 50:
        raise ValueError("Too many orders")
```

```python
# GOOD - TextChoices and named constants
# constants.py
from django.db import models


class OrderStatus(models.TextChoices):
    """Order lifecycle states."""

    PENDING = "pending", "Pending Payment"
    PROCESSING = "processing", "Processing"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class PaymentMethod(models.TextChoices):
    """Supported payment methods."""

    CARD = "card", "Credit Card"
    PAYPAL = "paypal", "PayPal"
    BANK = "bank", "Bank Transfer"


# Limits and thresholds
MAX_ORDERS_PER_USER = 50
MAX_ITEMS_PER_ORDER = 100
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# models.py
class Order(BaseModel):
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )


# services.py
from .constants import MAX_ORDERS_PER_USER

def order_create(*, user: User, items: list) -> Order:
    if user.orders.count() >= MAX_ORDERS_PER_USER:
        raise ValidationError(
            f"Maximum {MAX_ORDERS_PER_USER} orders allowed"
        )
```

---

## Queries

### N+1 Prevention

```python
# BAD - N+1 query problem
def get_orders_summary(user):
    orders = Order.objects.filter(user=user)
    for order in orders:
        print(order.items.count())  # Query per order!
        for item in order.items.all():  # Another query per order!
            print(item.product.name)  # Another query per item!
```

```python
# GOOD - Optimized with prefetch
from django.db.models import Count, Prefetch

def order_list_with_summary(*, user: User) -> QuerySet[Order]:
    """Get orders with item counts and product details."""
    return (
        Order.objects
        .filter(user=user)
        .annotate(items_count=Count("items"))
        .prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
    )
```

### Bulk Operations

```python
# BAD - Individual saves in loop
def update_prices(products, increase_pct):
    for product in products:
        product.price = product.price * (1 + increase_pct)
        product.save()
```

```python
# GOOD - Bulk update
from django.db.models import F

def product_increase_prices(*, increase_pct: Decimal) -> int:
    """Increase all product prices by percentage."""
    return Product.objects.update(
        price=F("price") * (1 + increase_pct),
        updated_at=timezone.now(),
    )


# Or for more complex logic:
def product_bulk_update_prices(
    *,
    product_prices: dict[int, Decimal],
) -> int:
    """Update multiple products with specific prices."""
    products = Product.objects.filter(id__in=product_prices.keys())

    for product in products:
        product.price = product_prices[product.id]

    Product.objects.bulk_update(products, ["price", "updated_at"])
    return len(products)
```

### Existence Checks

```python
# BAD - Fetches all data just to check existence
if Order.objects.filter(user=user, status='pending').count() > 0:
    pass

if len(Order.objects.filter(user=user)) > 0:
    pass
```

```python
# GOOD - Efficient existence check
if Order.objects.filter(user=user, status=OrderStatus.PENDING).exists():
    pass
```
