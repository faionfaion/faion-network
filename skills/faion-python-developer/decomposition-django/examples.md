# Django Decomposition Examples

Real-world examples of Django project decomposition.

---

## Example 1: E-commerce User App

### Before: Monolithic Structure

```python
# users/models.py (800+ lines)
class User(AbstractUser):
    phone = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/')
    is_verified = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=100, blank=True)

    # 30+ methods mixed: business logic, queries, notifications
    def send_verification_email(self):
        # Email logic here
        pass

    def get_active_orders(self):
        # Query logic here
        pass

    def create_stripe_customer(self):
        # Payment logic here
        pass

# users/views.py (1000+ lines)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        # 50 lines of validation
        # 30 lines of user creation
        # 20 lines of email sending
        # 10 lines of Stripe setup
        pass

    @action(detail=True, methods=['post'])
    def verify_email(self, request, pk=None):
        # All logic inline
        pass
```

### After: Decomposed Structure

```
users/
├── __init__.py
├── models/
│   ├── __init__.py           # from .user import User
│   ├── user.py               # User model (80 lines)
│   └── profile.py            # UserProfile model (60 lines)
├── services/
│   ├── __init__.py
│   ├── user_service.py       # CRUD operations (100 lines)
│   ├── auth_service.py       # Auth logic (80 lines)
│   ├── verification_service.py  # Email verification (60 lines)
│   └── stripe_service.py     # Stripe operations (80 lines)
├── selectors/
│   ├── __init__.py
│   └── user_selectors.py     # Query methods (60 lines)
├── serializers/
│   ├── __init__.py
│   ├── user_read.py          # UserListSerializer, UserDetailSerializer
│   ├── user_write.py         # UserCreateSerializer, UserUpdateSerializer
│   └── auth.py               # LoginSerializer, RegisterSerializer
├── views/
│   ├── __init__.py
│   ├── user_views.py         # User CRUD (60 lines)
│   ├── auth_views.py         # Login/Register (50 lines)
│   └── verification_views.py # Email verification (40 lines)
├── permissions.py            # Permission classes (40 lines)
├── signals.py                # Signal handlers (30 lines)
├── admin.py                  # Admin config (50 lines)
├── urls.py                   # URL routing (30 lines)
└── tests/
    ├── __init__.py
    ├── conftest.py           # Fixtures
    ├── factories.py          # User factories
    ├── test_models.py
    ├── test_services.py
    └── test_views.py
```

### Key Files After Decomposition

**models/user.py** (80 lines)
```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model with extended fields."""

    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_verified = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def full_name(self) -> str:
        """Return full name or username."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def has_stripe(self) -> bool:
        """Check if user has Stripe customer ID."""
        return bool(self.stripe_customer_id)
```

**services/user_service.py** (100 lines)
```python
from dataclasses import dataclass
from typing import Optional

from django.db import transaction

from users.models import User
from users.selectors import user_selectors
from users.services.stripe_service import StripeService
from users.services.verification_service import VerificationService


@dataclass
class UserCreateInput:
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""


@dataclass
class UserUpdateInput:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserService:
    """User write operations."""

    @staticmethod
    @transaction.atomic
    def create(data: UserCreateInput) -> User:
        """Create new user with verification email."""
        if user_selectors.email_exists(data.email):
            raise ValueError("Email already registered")

        user = User.objects.create_user(
            username=data.email,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
        )

        # Side effects
        VerificationService.send_verification_email(user)
        StripeService.create_customer(user)

        return user

    @staticmethod
    @transaction.atomic
    def update(user: User, data: UserUpdateInput) -> User:
        """Update user fields."""
        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.phone is not None:
            user.phone = data.phone
        user.save()
        return user

    @staticmethod
    def deactivate(user: User) -> None:
        """Soft delete user."""
        user.is_active = False
        user.save()
```

**selectors/user_selectors.py** (60 lines)
```python
from django.db.models import Q, QuerySet

from users.models import User


def get_all() -> QuerySet[User]:
    """Get all users."""
    return User.objects.all()


def get_active() -> QuerySet[User]:
    """Get active users."""
    return User.objects.filter(is_active=True)


def get_by_id(user_id: int) -> User | None:
    """Get user by ID."""
    return User.objects.filter(id=user_id).first()


def get_by_email(email: str) -> User | None:
    """Get user by email."""
    return User.objects.filter(email__iexact=email).first()


def email_exists(email: str) -> bool:
    """Check if email is taken."""
    return User.objects.filter(email__iexact=email).exists()


def search(query: str) -> QuerySet[User]:
    """Search users by name or email."""
    return User.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query),
        is_active=True,
    )


def get_unverified() -> QuerySet[User]:
    """Get users pending verification."""
    return User.objects.filter(is_verified=False, is_active=True)
```

**views/user_views.py** (60 lines)
```python
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.selectors import user_selectors
from users.serializers import UserDetailSerializer, UserUpdateSerializer
from users.services.user_service import UserService, UserUpdateInput


class UserMeView(APIView):
    """Current user profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.update(
            user=request.user,
            data=UserUpdateInput(**serializer.validated_data)
        )
        return Response(UserDetailSerializer(user).data)


class UserDetailView(APIView):
    """Get user by ID."""

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = user_selectors.get_by_id(user_id)
        if not user:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(UserDetailSerializer(user).data)
```

---

## Example 2: Blog App with DRF

### Before: Fat ViewSet

```python
# posts/views.py (500+ lines)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_queryset(self):
        # 30 lines of filtering logic
        # 20 lines of permission checks
        # 10 lines of prefetching
        pass

    def perform_create(self, serializer):
        # 40 lines of post creation
        # Notification logic
        # Analytics tracking
        # SEO updates
        pass
```

### After: Clean ViewSet

```python
# posts/views/post_views.py (80 lines)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from posts.selectors import post_selectors
from posts.serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostListSerializer,
)
from posts.services.post_service import PostService, PostCreateInput


class PostViewSet(ViewSet):
    """Blog post endpoints."""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """List published posts."""
        posts = post_selectors.get_published()

        # Optional filtering
        category = request.query_params.get('category')
        if category:
            posts = post_selectors.filter_by_category(posts, category)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Get post detail."""
        post = post_selectors.get_by_slug(pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Track view
        PostService.record_view(post, request.user)

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        """Create new post."""
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = PostService.create(
            author=request.user,
            data=PostCreateInput(**serializer.validated_data)
        )

        return Response(
            PostDetailSerializer(post).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish draft post."""
        post = post_selectors.get_by_id(pk)
        if not post or post.author != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        PostService.publish(post)
        return Response(PostDetailSerializer(post).data)
```

---

## Example 3: Order Processing (Complex Domain)

### Domain-Driven Structure

```
orders/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── entities.py           # Order, OrderItem (no Django)
│   ├── value_objects.py      # Money, Address
│   ├── events.py             # OrderCreated, OrderShipped
│   └── exceptions.py         # InsufficientStock, InvalidOrder
├── application/
│   ├── __init__.py
│   ├── create_order.py       # CreateOrderUseCase
│   ├── process_payment.py    # ProcessPaymentUseCase
│   └── ship_order.py         # ShipOrderUseCase
├── infrastructure/
│   ├── __init__.py
│   ├── models.py             # Django ORM models
│   ├── repositories.py       # OrderRepository implementation
│   └── payment_gateway.py    # Stripe integration
├── interface/
│   ├── __init__.py
│   ├── views.py              # API views
│   ├── serializers.py        # DRF serializers
│   └── urls.py               # URL routing
└── tests/
    ├── test_domain.py        # Unit tests (no DB)
    ├── test_application.py   # Use case tests
    └── test_interface.py     # API tests
```

### Use Case Example

```python
# orders/application/create_order.py (80 lines)
from dataclasses import dataclass
from decimal import Decimal
from typing import List

from django.db import transaction

from orders.domain.entities import Order, OrderItem
from orders.domain.events import OrderCreated
from orders.domain.exceptions import InsufficientStock
from orders.infrastructure.repositories import OrderRepository
from products.selectors import product_selectors


@dataclass
class OrderItemInput:
    product_id: int
    quantity: int


@dataclass
class CreateOrderInput:
    user_id: int
    items: List[OrderItemInput]
    shipping_address_id: int


class CreateOrderUseCase:
    """Create new order use case."""

    def __init__(
        self,
        order_repository: OrderRepository,
        event_bus: EventBus,
    ):
        self.order_repository = order_repository
        self.event_bus = event_bus

    @transaction.atomic
    def execute(self, data: CreateOrderInput) -> Order:
        """Create order with stock validation."""

        # Validate stock
        items = []
        for item_data in data.items:
            product = product_selectors.get_by_id(item_data.product_id)
            if not product:
                raise ValueError(f"Product {item_data.product_id} not found")

            if product.stock < item_data.quantity:
                raise InsufficientStock(product.name, product.stock)

            items.append(OrderItem(
                product=product,
                quantity=item_data.quantity,
                unit_price=product.price,
            ))

        # Create order
        order = Order(
            user_id=data.user_id,
            items=items,
            shipping_address_id=data.shipping_address_id,
        )

        # Persist
        order = self.order_repository.save(order)

        # Emit event
        self.event_bus.publish(OrderCreated(order_id=order.id))

        return order
```

---

## Example 4: Multi-App Project Structure

### Large Project Layout

```
project/
├── config/                   # Django settings
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                     # All Django apps
│   ├── __init__.py
│   ├── core/                 # Shared utilities
│   │   ├── models.py         # BaseModel, TimeStampedModel
│   │   ├── permissions.py    # Shared permissions
│   │   ├── pagination.py     # Custom pagination
│   │   └── exceptions.py     # Base exceptions
│   ├── users/                # User management
│   │   └── ...
│   ├── products/             # Product catalog
│   │   └── ...
│   ├── orders/               # Order processing
│   │   └── ...
│   └── payments/             # Payment handling
│       └── ...
├── api/                      # API versioning
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── views/
│   │       ├── users.py
│   │       ├── products.py
│   │       └── orders.py
│   └── v2/
│       └── ...
└── tests/
    ├── conftest.py           # Shared fixtures
    ├── factories/            # All factories
    │   ├── users.py
    │   ├── products.py
    │   └── orders.py
    └── integration/          # Cross-app tests
```

---

## Anti-Patterns to Avoid

### 1. Circular Imports

```python
# BAD: users/services.py imports orders/services.py
# AND orders/services.py imports users/services.py

# GOOD: Use events or dependency injection
# orders/services.py
class OrderService:
    def __init__(self, user_notifier):
        self.user_notifier = user_notifier

    def create_order(self, user, items):
        order = Order.objects.create(...)
        self.user_notifier.notify_order_created(user, order)
```

### 2. Business Logic in Serializers

```python
# BAD
class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # 50 lines of business logic
        user = User.objects.create(**validated_data)
        send_welcome_email(user)  # Side effect
        create_stripe_customer(user)  # Side effect
        return user

# GOOD
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

# View calls service
user = UserService.create(UserCreateInput(**serializer.validated_data))
```

### 3. Queries in Views

```python
# BAD
class UserListView(APIView):
    def get(self, request):
        users = User.objects.filter(
            is_active=True,
            date_joined__gte=timezone.now() - timedelta(days=30)
        ).select_related('profile').prefetch_related('orders')
        return Response(...)

# GOOD
class UserListView(APIView):
    def get(self, request):
        users = user_selectors.get_recent_active(days=30)
        return Response(...)
```

---

## Related

- [README.md](README.md) - Overview and patterns
- [checklist.md](checklist.md) - Step-by-step checklist
- [templates.md](templates.md) - Code templates
- [llm-prompts.md](llm-prompts.md) - LLM prompts for decomposition
