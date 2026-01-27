# Django Services Layer Examples

Real-world case studies, good/bad code comparisons, and practical implementation examples.

---

## Case Study 1: E-Commerce Order Processing

### Problem

An e-commerce app needs to handle order creation with:
- Inventory validation
- Payment processing
- Email notification
- Audit logging

### Bad: Logic Scattered Across Layers

```python
# views.py - BAD: Business logic in view
class OrderCreateView(APIView):
    def post(self, request):
        user = request.user
        items = request.data['items']

        # Check inventory - business logic in view!
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            if product.stock < item['quantity']:
                return Response({'error': 'Out of stock'}, status=400)

        # Create order
        order = Order.objects.create(user=user, status='pending')
        total = Decimal('0')

        for item in items:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price,
            )
            total += product.price * item['quantity']
            product.stock -= item['quantity']
            product.save()

        order.total = total
        order.save()

        # Process payment - external call in view!
        try:
            payment = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency='usd',
                customer=user.stripe_customer_id,
            )
            order.payment_intent_id = payment.id
            order.status = 'paid'
            order.save()
        except stripe.error.CardError:
            order.status = 'payment_failed'
            order.save()
            return Response({'error': 'Payment failed'}, status=402)

        # Send email - side effect in view!
        send_mail(
            'Order Confirmation',
            f'Your order {order.id} has been placed.',
            'orders@example.com',
            [user.email],
        )

        return Response(OrderSerializer(order).data, status=201)
```

**Problems:**
- View is 50+ lines of business logic
- No transaction safety (partial failure leaves bad state)
- Hard to test (need to mock stripe, email)
- Logic not reusable (admin order creation needs same logic)
- N+1 queries on products

### Good: Service Layer Pattern

```python
# services/order_services.py
from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from django.db import transaction

from apps.orders.exceptions import (
    InsufficientStockError,
    PaymentFailedError,
)

if TYPE_CHECKING:
    from apps.orders.models import Order
    from apps.users.models import User
    from apps.payments.gateways import PaymentGateway


@transaction.atomic
def order_create(
    *,
    user: User,
    items: list[dict],
    payment_gateway: PaymentGateway,
) -> Order:
    """
    Create and process an order.

    Business logic:
    - Validates inventory availability
    - Creates order and order items
    - Deducts inventory
    - Processes payment
    - Sends confirmation email (async)

    Args:
        user: User placing the order.
        items: List of dicts with product_id and quantity.
        payment_gateway: Payment processor instance.

    Returns:
        Created Order instance.

    Raises:
        InsufficientStockError: If product out of stock.
        PaymentFailedError: If payment processing fails.
    """
    from apps.orders.models import Order, OrderItem
    from apps.products.models import Product
    from apps.orders.tasks import send_order_confirmation_email

    # Validate inventory
    products = _validate_inventory(items=items)

    # Create order
    order = Order.objects.create(user=user, status='pending')

    # Create order items and calculate total
    total = _create_order_items(order=order, items=items, products=products)

    # Deduct inventory
    _deduct_inventory(items=items, products=products)

    # Update order total
    order.total = total
    order.save(update_fields=['total', 'updated_at'])

    # Process payment
    _process_payment(order=order, payment_gateway=payment_gateway)

    # Queue email notification (async)
    send_order_confirmation_email.delay(order_id=order.id)

    return order


def _validate_inventory(*, items: list[dict]) -> dict[int, Product]:
    """Validate all products have sufficient stock."""
    from apps.products.models import Product

    product_ids = [item['product_id'] for item in items]
    products = {
        p.id: p for p in Product.objects.filter(id__in=product_ids)
                                        .select_for_update()
    }

    for item in items:
        product = products.get(item['product_id'])
        if not product:
            raise InsufficientStockError(
                product_id=item['product_id'],
                message="Product not found",
            )
        if product.stock < item['quantity']:
            raise InsufficientStockError(
                product_id=product.id,
                available=product.stock,
                requested=item['quantity'],
            )

    return products


def _create_order_items(
    *,
    order: Order,
    items: list[dict],
    products: dict[int, Product],
) -> Decimal:
    """Create order items and return total."""
    from apps.orders.models import OrderItem

    total = Decimal('0')
    order_items = []

    for item in items:
        product = products[item['product_id']]
        order_items.append(OrderItem(
            order=order,
            product=product,
            quantity=item['quantity'],
            unit_price=product.price,
        ))
        total += product.price * item['quantity']

    OrderItem.objects.bulk_create(order_items)
    return total


def _deduct_inventory(
    *,
    items: list[dict],
    products: dict[int, Product],
) -> None:
    """Deduct ordered quantities from inventory."""
    from apps.products.models import Product
    from django.db.models import F

    for item in items:
        Product.objects.filter(id=item['product_id']).update(
            stock=F('stock') - item['quantity']
        )


def _process_payment(
    *,
    order: Order,
    payment_gateway: PaymentGateway,
) -> None:
    """Process payment for order."""
    try:
        payment_result = payment_gateway.charge(
            amount=order.total,
            customer_id=order.user.payment_customer_id,
        )
        order.payment_id = payment_result.id
        order.status = 'paid'
        order.save(update_fields=['payment_id', 'status', 'updated_at'])
    except payment_gateway.PaymentError as e:
        order.status = 'payment_failed'
        order.save(update_fields=['status', 'updated_at'])
        raise PaymentFailedError(order_id=order.id, reason=str(e))
```

```python
# views.py - GOOD: Thin view
class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = order_create(
                user=request.user,
                items=serializer.validated_data['items'],
                payment_gateway=get_payment_gateway(),
            )
            return Response(OrderSerializer(order).data, status=201)
        except InsufficientStockError as e:
            return Response({'error': str(e)}, status=400)
        except PaymentFailedError as e:
            return Response({'error': str(e)}, status=402)
```

**Benefits:**
- View is 15 lines (HTTP handling only)
- Transaction safety (all-or-nothing)
- Testable (inject mock payment gateway)
- Reusable (admin, API, CLI can call same service)
- No N+1 queries (single fetch with select_for_update)

---

## Case Study 2: User Registration with Email Verification

### Bad: Logic in Serializer

```python
# serializers.py - BAD: Business logic in serializer
class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already taken")
        return value

    def create(self, validated_data):
        # Business logic in serializer - BAD!
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
        )

        # Generate verification token
        token = signing.dumps(
            {'user_id': user.id},
            salt='email-verification',
        )

        # Create verification record
        EmailVerification.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=24),
        )

        # Send email - side effect in serializer!
        send_mail(
            'Verify your email',
            f'Click here: example.com/verify?token={token}',
            'noreply@example.com',
            [user.email],
        )

        return user
```

### Good: Service Pattern

```python
# services/auth_services.py
from __future__ import annotations
from datetime import timedelta
from typing import TYPE_CHECKING
from django.db import transaction
from django.core import signing
from django.utils import timezone

if TYPE_CHECKING:
    from apps.users.models import User


class UserAlreadyExistsError(Exception):
    pass


class InvalidVerificationTokenError(Exception):
    pass


@transaction.atomic
def user_register(
    *,
    email: str,
    password: str,
) -> User:
    """
    Register a new user with email verification.

    Business logic:
    - Validates email uniqueness
    - Creates inactive user
    - Generates verification token
    - Queues verification email

    Args:
        email: User's email address.
        password: User's password (will be hashed).

    Returns:
        Created User instance (inactive).

    Raises:
        UserAlreadyExistsError: If email is already registered.
    """
    from apps.users.models import User
    from apps.auth.models import EmailVerification
    from apps.auth.tasks import send_verification_email

    # Check uniqueness
    if User.objects.filter(email=email).exists():
        raise UserAlreadyExistsError(f"Email {email} is already registered")

    # Create user
    user = User.objects.create_user(
        email=email,
        password=password,
        is_active=False,
    )

    # Create verification token
    verification = _create_verification_token(user=user)

    # Queue email (async)
    send_verification_email.delay(
        user_id=user.id,
        token=verification.token,
    )

    return user


def _create_verification_token(*, user: User) -> EmailVerification:
    """Create email verification record."""
    from apps.auth.models import EmailVerification

    token = signing.dumps(
        {'user_id': user.id, 'email': user.email},
        salt='email-verification',
    )

    return EmailVerification.objects.create(
        user=user,
        token=token,
        expires_at=timezone.now() + timedelta(hours=24),
    )


@transaction.atomic
def user_verify_email(*, token: str) -> User:
    """
    Verify user's email address.

    Args:
        token: Verification token from email.

    Returns:
        Verified User instance.

    Raises:
        InvalidVerificationTokenError: If token invalid/expired.
    """
    from apps.users.models import User
    from apps.auth.models import EmailVerification

    # Decode token
    try:
        data = signing.loads(
            token,
            salt='email-verification',
            max_age=86400,  # 24 hours
        )
    except signing.BadSignature:
        raise InvalidVerificationTokenError("Invalid or expired token")

    # Get verification record
    try:
        verification = EmailVerification.objects.select_related('user').get(
            token=token,
            user_id=data['user_id'],
            used_at__isnull=True,
        )
    except EmailVerification.DoesNotExist:
        raise InvalidVerificationTokenError("Token already used or not found")

    # Check expiry
    if verification.expires_at < timezone.now():
        raise InvalidVerificationTokenError("Token has expired")

    # Activate user
    user = verification.user
    user.is_active = True
    user.email_verified_at = timezone.now()
    user.save(update_fields=['is_active', 'email_verified_at', 'updated_at'])

    # Mark token as used
    verification.used_at = timezone.now()
    verification.save(update_fields=['used_at'])

    return user
```

---

## Case Study 3: Selectors for Complex Queries

### Bad: Query Logic in View

```python
# views.py - BAD: Complex query in view
class DashboardView(APIView):
    def get(self, request):
        user = request.user

        # Complex query logic in view!
        orders = (
            Order.objects
            .filter(user=user)
            .filter(status__in=['pending', 'processing', 'shipped'])
            .select_related('shipping_address')
            .prefetch_related('items__product')
            .annotate(
                item_count=Count('items'),
                total_with_tax=F('total') * Decimal('1.1'),
            )
            .order_by('-created_at')[:10]
        )

        # More complex query
        recent_products = (
            Product.objects
            .filter(orderitem__order__user=user)
            .distinct()
            .annotate(
                last_ordered=Max('orderitem__order__created_at'),
                times_ordered=Count('orderitem'),
            )
            .order_by('-last_ordered')[:5]
        )

        return Response({
            'orders': OrderSerializer(orders, many=True).data,
            'recent_products': ProductSerializer(recent_products, many=True).data,
        })
```

### Good: Selector Pattern

```python
# selectors/dashboard_selectors.py
from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from django.db.models import Count, F, Max, QuerySet

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.orders.models import Order
    from apps.products.models import Product


def user_active_orders(
    *,
    user: User,
    limit: int = 10,
) -> QuerySet[Order]:
    """
    Get user's active orders for dashboard.

    Returns orders with status pending/processing/shipped,
    with related items and products prefetched.

    Query count: 3 (orders, items, products)
    """
    from apps.orders.models import Order

    return (
        Order.objects
        .filter(user=user)
        .filter(status__in=['pending', 'processing', 'shipped'])
        .select_related('shipping_address')
        .prefetch_related('items__product')
        .annotate(
            item_count=Count('items'),
            total_with_tax=F('total') * Decimal('1.1'),
        )
        .order_by('-created_at')[:limit]
    )


def user_recently_ordered_products(
    *,
    user: User,
    limit: int = 5,
) -> QuerySet[Product]:
    """
    Get products the user has recently ordered.

    Returns distinct products annotated with last order date
    and order count.

    Query count: 1
    """
    from apps.products.models import Product

    return (
        Product.objects
        .filter(orderitem__order__user=user)
        .distinct()
        .annotate(
            last_ordered=Max('orderitem__order__created_at'),
            times_ordered=Count('orderitem'),
        )
        .order_by('-last_ordered')[:limit]
    )
```

```python
# views.py - GOOD: Thin view using selectors
from apps.dashboard.selectors import (
    user_active_orders,
    user_recently_ordered_products,
)

class DashboardView(APIView):
    def get(self, request):
        return Response({
            'orders': OrderSerializer(
                user_active_orders(user=request.user),
                many=True,
            ).data,
            'recent_products': ProductSerializer(
                user_recently_ordered_products(user=request.user),
                many=True,
            ).data,
        })
```

---

## Case Study 4: Dependency Injection

### Without DI (Hard to Test)

```python
# services/notification_services.py - BAD: Hard-coded dependencies
import stripe
from sendgrid import SendGridAPIClient

def order_complete_notify(*, order: Order) -> None:
    # Hard-coded Stripe call
    stripe.api_key = settings.STRIPE_API_KEY
    stripe.PaymentIntent.capture(order.payment_intent_id)

    # Hard-coded SendGrid call
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
```

### With Dependency Injection (Testable)

```python
# services/notification_services.py - GOOD: Dependencies injected
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from apps.orders.models import Order


class PaymentGateway(Protocol):
    """Protocol for payment gateways."""
    def capture(self, payment_id: str) -> None: ...


class EmailSender(Protocol):
    """Protocol for email senders."""
    def send(self, to: str, subject: str, body: str) -> None: ...


def order_complete_notify(
    *,
    order: Order,
    payment_gateway: PaymentGateway,
    email_sender: EmailSender,
) -> None:
    """
    Complete order and notify customer.

    Args:
        order: Order to complete.
        payment_gateway: Payment processor instance.
        email_sender: Email sender instance.
    """
    # Capture payment
    payment_gateway.capture(payment_id=order.payment_intent_id)

    # Send email
    email_sender.send(
        to=order.user.email,
        subject=f"Order {order.id} Confirmed",
        body=f"Your order has been confirmed.",
    )
```

```python
# tests/test_notification_services.py - Easy to test with mocks
from unittest.mock import Mock


def test_order_complete_notify_captures_payment_and_sends_email(db, order_factory):
    order = order_factory(status='pending')
    mock_payment = Mock()
    mock_email = Mock()

    order_complete_notify(
        order=order,
        payment_gateway=mock_payment,
        email_sender=mock_email,
    )

    mock_payment.capture.assert_called_once_with(
        payment_id=order.payment_intent_id
    )
    mock_email.send.assert_called_once()
```

---

## Pattern Summary

| Pattern | Use When | Example |
|---------|----------|---------|
| **Simple Function** | Single responsibility, no state | `user_create()` |
| **Private Helpers** | Breaking down complex service | `_validate_inventory()` |
| **Injected Dependencies** | External services, testability | `PaymentGateway` protocol |
| **Selectors** | Complex read operations | `user_active_orders()` |
| **Service Class** | Shared state across methods | `OrderProcessingService` |

---

*Part of the faion-python-developer skill. Last updated: 2026-01.*
