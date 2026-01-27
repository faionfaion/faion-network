# Django Quality Examples

Real-world implementation examples for Django code quality patterns.

## Exception Handling

### NEVER Use Bare Except

```python
# WRONG - hides all errors including bugs
try:
    do_something()
except:  # NEVER!
    pass

# WRONG - too broad, catches SystemExit, KeyboardInterrupt
try:
    do_something()
except Exception:
    logger.error("Error occurred")
```

### Correct Exception Handling

```python
import logging
from django.http import Http404
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


# Django ORM - specific model exception
def get_user_or_404(user_id: int) -> User:
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404(f"User {user_id} not found")


# Multiple specific exceptions
def validate_and_process(data: dict) -> dict:
    try:
        validated = validate_data(data)
        return process_data(validated)
    except (ValidationError, ValueError) as e:
        logger.warning("Validation failed: %s", e)
        raise ValidationError({"detail": str(e)})
    except ProcessingError as e:
        logger.error("Processing failed: %s", e, exc_info=True)
        raise


# HTTP requests with specific exceptions
import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError


def fetch_external_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from external API with proper error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Timeout:
        logger.warning("Request to %s timed out", url)
        raise ExternalServiceError("External service timeout")
    except HTTPError as e:
        logger.error("HTTP error from %s: %s", url, e.response.status_code)
        raise ExternalServiceError(f"Service returned {e.response.status_code}")
    except ConnectionError:
        logger.error("Connection failed to %s", url)
        raise ExternalServiceError("Unable to connect to external service")
```

## Query Optimization

### N+1 Query Problem and Solutions

```python
from django.db.models import Prefetch


# PROBLEM: N+1 queries (1 + N additional queries)
def get_orders_bad():
    orders = Order.objects.all()
    for order in orders:
        print(order.user.email)        # Query per order!
        print(order.shipping_address)  # Another query per order!
    return orders


# SOLUTION 1: select_related for ForeignKey/OneToOne
def get_orders_good():
    orders = Order.objects.select_related(
        "user",
        "shipping_address"
    ).all()
    for order in orders:
        print(order.user.email)        # No extra query
        print(order.shipping_address)  # No extra query
    return orders


# SOLUTION 2: prefetch_related for ManyToMany/reverse FK
def get_orders_with_items():
    orders = Order.objects.prefetch_related("items").all()
    for order in orders:
        for item in order.items.all():  # No extra query
            print(item.name)
    return orders


# SOLUTION 3: Combined select_related + prefetch_related
def get_orders_optimized():
    """Fetch orders with user, address, and items efficiently."""
    return Order.objects.select_related(
        "user",
        "shipping_address"
    ).prefetch_related(
        "items",
        "items__product"  # Nested prefetch
    )


# SOLUTION 4: Custom Prefetch for filtered/annotated related objects
def get_users_with_recent_orders():
    """Fetch users with only their recent orders."""
    recent_orders = Prefetch(
        "orders",
        queryset=Order.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).select_related("shipping_address"),
        to_attr="recent_orders"  # Access via user.recent_orders
    )
    return User.objects.prefetch_related(recent_orders)


# SOLUTION 5: only/defer for large fields
def get_articles_list():
    """Fetch articles without large content field."""
    return Article.objects.defer("content", "raw_html").all()


def get_article_detail(article_id: int):
    """Fetch single article with all fields."""
    return Article.objects.get(pk=article_id)
```

## Service Layer Pattern

### Simple Service Layer (Hacksoft Style)

```python
# services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from typing import Optional
import logging

from .models import Order, OrderItem, Product
from .tasks import send_order_confirmation

logger = logging.getLogger(__name__)


def create_order(
    *,
    user: User,
    items: list[dict],
    shipping_address_id: int,
    notes: Optional[str] = None
) -> Order:
    """
    Create a new order with items.

    Args:
        user: The user placing the order
        items: List of dicts with product_id and quantity
        shipping_address_id: ID of shipping address
        notes: Optional order notes

    Returns:
        Created Order instance

    Raises:
        ValidationError: If items are invalid or out of stock
    """
    _validate_order_items(items)

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            shipping_address_id=shipping_address_id,
            notes=notes or ""
        )

        _create_order_items(order=order, items=items)
        _update_inventory(items=items)

        logger.info(
            "Order created",
            extra={
                "order_id": order.id,
                "user_id": user.id,
                "item_count": len(items)
            }
        )

    # Async task outside transaction
    send_order_confirmation.delay(order_id=order.id)

    return order


def _validate_order_items(items: list[dict]) -> None:
    """Validate order items for availability and stock."""
    if not items:
        raise ValidationError("Order must have at least one item")

    product_ids = [item["product_id"] for item in items]
    products = Product.objects.filter(
        id__in=product_ids,
        is_active=True
    ).in_bulk()

    for item in items:
        product = products.get(item["product_id"])
        if not product:
            raise ValidationError(f"Product {item['product_id']} not found")
        if product.stock < item["quantity"]:
            raise ValidationError(f"Insufficient stock for {product.name}")


def _create_order_items(*, order: Order, items: list[dict]) -> None:
    """Bulk create order items."""
    order_items = [
        OrderItem(
            order=order,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=Product.objects.get(pk=item["product_id"]).price
        )
        for item in items
    ]
    OrderItem.objects.bulk_create(order_items)


def _update_inventory(*, items: list[dict]) -> None:
    """Decrease product inventory."""
    for item in items:
        Product.objects.filter(pk=item["product_id"]).update(
            stock=F("stock") - item["quantity"]
        )
```

### Using Services in Views

```python
# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .services import create_order
from .serializers import OrderCreateSerializer, OrderSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order_view(request):
    """Create a new order."""
    serializer = OrderCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        order = create_order(
            user=request.user,
            items=serializer.validated_data["items"],
            shipping_address_id=serializer.validated_data["shipping_address_id"],
            notes=serializer.validated_data.get("notes")
        )
    except ValidationError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        OrderSerializer(order).data,
        status=status.HTTP_201_CREATED
    )
```

## Security Examples

### Content Security Policy (Django 6.0+)

```python
# settings.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",  # New in Django 6.0
    # ... other middleware
]

# Native CSP configuration
CONTENT_SECURITY_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "'nonce-<CSP_NONCE_SENTINEL>'"],
    "style-src": ["'self'", "'nonce-<CSP_NONCE_SENTINEL>'"],
    "img-src": ["'self'", "data:", "https:"],
    "font-src": ["'self'", "https://fonts.gstatic.com"],
    "connect-src": ["'self'"],
    "frame-ancestors": ["'none'"],
    "form-action": ["'self'"],
}

# Report-only mode for testing
CONTENT_SECURITY_POLICY_REPORT_ONLY = True
```

### Using CSP Nonce in Templates

```html
<!-- template.html -->
{% load csp %}

<script nonce="{{ request.csp_nonce }}">
    // This script will be allowed by CSP
    console.log("Allowed by nonce");
</script>

<style nonce="{{ request.csp_nonce }}">
    /* This style will be allowed by CSP */
    .safe-style { color: blue; }
</style>
```

### Rate Limiting with django-ratelimit

```python
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse


@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_view(request):
    """Login with rate limiting: 5 attempts per minute per IP."""
    # ... login logic
    pass


@ratelimit(key="user", rate="100/h", method="GET")
def api_endpoint(request):
    """API endpoint with per-user rate limit."""
    if getattr(request, "limited", False):
        return JsonResponse(
            {"error": "Rate limit exceeded. Try again later."},
            status=429
        )
    # ... normal handling
```

### Input Validation

```python
from django import forms
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re


class UserRegistrationForm(forms.Form):
    """User registration with comprehensive validation."""

    username = forms.CharField(
        min_length=3,
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="Username may only contain letters, numbers, and @/./+/-/_"
            )
        ]
    )

    email = forms.EmailField()

    password = forms.CharField(
        min_length=12,
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(12)]
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username.lower()

    def clean_password(self):
        password = self.cleaned_data["password"]

        # Check password complexity
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain lowercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain a digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain special character.")

        return password
```

## Logging Examples

### Structured Logging with django-structlog

```python
# settings.py
import structlog

MIDDLEWARE = [
    # ... other middleware
    "django_structlog.middlewares.RequestMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console" if DEBUG else "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

### Using Structured Logging

```python
import structlog

logger = structlog.get_logger(__name__)


def process_payment(order_id: int, amount: Decimal) -> bool:
    """Process payment with structured logging."""
    log = logger.bind(order_id=order_id, amount=str(amount))

    log.info("payment_processing_started")

    try:
        result = payment_gateway.charge(amount)
        log.info(
            "payment_processed",
            transaction_id=result.transaction_id,
            status=result.status
        )
        return True
    except PaymentError as e:
        log.error(
            "payment_failed",
            error_code=e.code,
            error_message=str(e)
        )
        return False
```

## Custom System Checks

```python
# checks.py
from django.core.checks import Error, Warning, register, Tags


@register(Tags.security)
def check_secret_key_not_default(app_configs, **kwargs):
    """Ensure SECRET_KEY is not the default insecure value."""
    from django.conf import settings

    errors = []

    if settings.SECRET_KEY == "django-insecure-change-me":
        errors.append(
            Error(
                "SECRET_KEY is set to an insecure default value.",
                hint="Generate a new SECRET_KEY using `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`",
                id="security.E001",
            )
        )

    return errors


@register(Tags.security, deploy=True)
def check_sentry_configured(app_configs, **kwargs):
    """Ensure Sentry is configured for production."""
    from django.conf import settings

    warnings = []

    if not getattr(settings, "SENTRY_DSN", None):
        warnings.append(
            Warning(
                "SENTRY_DSN is not configured.",
                hint="Configure Sentry for production error tracking.",
                id="monitoring.W001",
            )
        )

    return warnings


@register()
def check_cache_configured(app_configs, **kwargs):
    """Warn if using local memory cache in production."""
    from django.conf import settings

    warnings = []

    if not settings.DEBUG:
        cache_backend = settings.CACHES.get("default", {}).get("BACKEND", "")
        if "LocMemCache" in cache_backend:
            warnings.append(
                Warning(
                    "Using LocMemCache in production.",
                    hint="Configure Redis or Memcached for production.",
                    id="caching.W001",
                )
            )

    return warnings
```

### Register Checks in AppConfig

```python
# apps.py
from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "myapp"

    def ready(self):
        # Import checks to register them
        from . import checks  # noqa: F401
```

## Model Best Practices

```python
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import MinValueValidator
from django.utils import timezone


class Product(models.Model):
    """Product model with proper validation and constraints."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "-created_at"]),
        ]
        constraints = [
            CheckConstraint(
                check=Q(price__gte=0),
                name="product_price_non_negative"
            ),
            CheckConstraint(
                check=Q(stock__gte=0),
                name="product_stock_non_negative"
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """Model-level validation."""
        super().clean()
        if self.price and self.price > 1000000:
            raise ValidationError({"price": "Price cannot exceed 1,000,000"})

    @property
    def is_in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.stock > 0 and self.is_active
```

## Testing Examples

```python
# tests/test_services.py
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock

from myapp.services import create_order
from myapp.models import User, Product, Order


@pytest.fixture
def user(db):
    """Create test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def product(db):
    """Create test product with stock."""
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        price=Decimal("99.99"),
        stock=10,
        is_active=True
    )


@pytest.fixture
def shipping_address(db, user):
    """Create test shipping address."""
    return Address.objects.create(
        user=user,
        street="123 Test St",
        city="Test City",
        country="US"
    )


class TestCreateOrder:
    """Tests for create_order service."""

    def test_create_order_success(self, user, product, shipping_address):
        """Test successful order creation."""
        items = [{"product_id": product.id, "quantity": 2}]

        with patch("myapp.services.send_order_confirmation") as mock_email:
            order = create_order(
                user=user,
                items=items,
                shipping_address_id=shipping_address.id
            )

        assert order.user == user
        assert order.items.count() == 1
        assert order.items.first().quantity == 2
        mock_email.delay.assert_called_once_with(order_id=order.id)

        # Verify stock was decreased
        product.refresh_from_db()
        assert product.stock == 8

    def test_create_order_empty_items_raises(self, user, shipping_address):
        """Test that empty items raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            create_order(
                user=user,
                items=[],
                shipping_address_id=shipping_address.id
            )

        assert "at least one item" in str(exc_info.value)

    def test_create_order_insufficient_stock_raises(self, user, product, shipping_address):
        """Test that insufficient stock raises ValidationError."""
        items = [{"product_id": product.id, "quantity": 100}]  # More than stock

        with pytest.raises(ValidationError) as exc_info:
            create_order(
                user=user,
                items=items,
                shipping_address_id=shipping_address.id
            )

        assert "Insufficient stock" in str(exc_info.value)

    def test_create_order_inactive_product_raises(self, user, product, shipping_address):
        """Test that inactive product raises ValidationError."""
        product.is_active = False
        product.save()

        items = [{"product_id": product.id, "quantity": 1}]

        with pytest.raises(ValidationError) as exc_info:
            create_order(
                user=user,
                items=items,
                shipping_address_id=shipping_address.id
            )

        assert "not found" in str(exc_info.value)
```
