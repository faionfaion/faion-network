# Django Decomposition Templates

Copy-paste templates for Django project decomposition.

---

## Model Templates

### Base Model

```python
# core/models/base.py
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Abstract base model with soft delete."""

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class BaseModel(TimeStampedModel, SoftDeleteModel):
    """Base model with timestamps and soft delete."""

    class Meta:
        abstract = True
```

### Model with Manager

```python
# users/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(models.Manager):
    """Custom manager for User model."""

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User."""
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
```

### Model Package Init

```python
# users/models/__init__.py
from .user import User
from .profile import Profile

__all__ = ['User', 'Profile']
```

---

## Service Templates

### Basic Service

```python
# users/services/user_service.py
from dataclasses import dataclass
from typing import Optional

from django.db import transaction

from users.models import User
from users.selectors import user_selectors


@dataclass
class UserCreateInput:
    """Input for user creation."""
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""


@dataclass
class UserUpdateInput:
    """Input for user update."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserService:
    """User write operations."""

    @staticmethod
    @transaction.atomic
    def create(data: UserCreateInput) -> User:
        """
        Create new user.

        Args:
            data: User creation input

        Returns:
            Created user instance

        Raises:
            ValueError: If email already exists
        """
        if user_selectors.email_exists(data.email):
            raise ValueError("Email already registered")

        user = User.objects.create_user(
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        return user

    @staticmethod
    @transaction.atomic
    def update(user: User, data: UserUpdateInput) -> User:
        """Update user fields."""
        fields_to_update = []

        if data.first_name is not None:
            user.first_name = data.first_name
            fields_to_update.append('first_name')

        if data.last_name is not None:
            user.last_name = data.last_name
            fields_to_update.append('last_name')

        if data.phone is not None:
            user.phone = data.phone
            fields_to_update.append('phone')

        if fields_to_update:
            user.save(update_fields=fields_to_update + ['updated_at'])

        return user

    @staticmethod
    def deactivate(user: User) -> None:
        """Soft delete user."""
        user.is_active = False
        user.save(update_fields=['is_active', 'updated_at'])
```

### Service with Dependencies

```python
# orders/services/order_service.py
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Protocol

from django.db import transaction

from orders.models import Order, OrderItem


class PaymentGateway(Protocol):
    """Payment gateway interface."""
    def charge(self, amount: Decimal, token: str) -> str: ...


class EmailSender(Protocol):
    """Email sender interface."""
    def send_order_confirmation(self, order: Order) -> None: ...


@dataclass
class OrderItemInput:
    product_id: int
    quantity: int


@dataclass
class CreateOrderInput:
    user_id: int
    items: List[OrderItemInput]
    payment_token: str


class OrderService:
    """Order write operations."""

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        email_sender: EmailSender,
    ):
        self.payment_gateway = payment_gateway
        self.email_sender = email_sender

    @transaction.atomic
    def create(self, data: CreateOrderInput) -> Order:
        """Create order with payment processing."""
        # Calculate total
        total = self._calculate_total(data.items)

        # Process payment
        payment_id = self.payment_gateway.charge(
            amount=total,
            token=data.payment_token,
        )

        # Create order
        order = Order.objects.create(
            user_id=data.user_id,
            total=total,
            payment_id=payment_id,
        )

        # Create order items
        for item in data.items:
            OrderItem.objects.create(
                order=order,
                product_id=item.product_id,
                quantity=item.quantity,
            )

        # Send confirmation
        self.email_sender.send_order_confirmation(order)

        return order

    def _calculate_total(self, items: List[OrderItemInput]) -> Decimal:
        """Calculate order total."""
        from products.selectors import product_selectors

        total = Decimal('0')
        for item in items:
            product = product_selectors.get_by_id(item.product_id)
            if product:
                total += product.price * item.quantity
        return total
```

---

## Selector Templates

### Basic Selectors

```python
# users/selectors/user_selectors.py
from django.db.models import Q, QuerySet
from django.utils import timezone
from datetime import timedelta

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
    """Get user by email (case-insensitive)."""
    return User.objects.filter(email__iexact=email).first()


def email_exists(email: str) -> bool:
    """Check if email is already registered."""
    return User.objects.filter(email__iexact=email).exists()


def search(query: str) -> QuerySet[User]:
    """Search users by name or email."""
    return User.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query),
        is_active=True,
    )


def get_recent(days: int = 30) -> QuerySet[User]:
    """Get users registered in last N days."""
    since = timezone.now() - timedelta(days=days)
    return User.objects.filter(date_joined__gte=since)


def get_with_orders() -> QuerySet[User]:
    """Get users with their orders (prefetched)."""
    return User.objects.prefetch_related('orders').filter(is_active=True)
```

### Selector with Pagination

```python
# products/selectors/product_selectors.py
from django.db.models import QuerySet
from django.core.paginator import Paginator

from products.models import Product


def get_published() -> QuerySet[Product]:
    """Get published products."""
    return Product.objects.filter(
        is_published=True
    ).select_related(
        'category'
    ).prefetch_related(
        'tags', 'images'
    )


def get_by_category(category_slug: str) -> QuerySet[Product]:
    """Get products by category."""
    return get_published().filter(category__slug=category_slug)


def paginate(
    queryset: QuerySet[Product],
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Product], dict]:
    """
    Paginate queryset.

    Returns:
        Tuple of (items, pagination_info)
    """
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)

    return list(page_obj), {
        'page': page_obj.number,
        'per_page': per_page,
        'total_pages': paginator.num_pages,
        'total_items': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    }
```

---

## View Templates

### Basic APIView

```python
# users/views/user_views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.selectors import user_selectors
from users.serializers import UserDetailSerializer, UserUpdateSerializer
from users.services.user_service import UserService, UserUpdateInput


class UserMeView(APIView):
    """Current user profile endpoint."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user profile."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Update current user profile."""
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.update(
            user=request.user,
            data=UserUpdateInput(**serializer.validated_data)
        )
        return Response(UserDetailSerializer(user).data)

    def delete(self, request):
        """Deactivate current user."""
        UserService.deactivate(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### ViewSet Template

```python
# products/views/product_views.py
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from products.selectors import product_selectors
from products.serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)
from products.services.product_service import ProductService, ProductCreateInput


class ProductViewSet(ViewSet):
    """Product CRUD endpoints."""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """List published products."""
        products = product_selectors.get_published()

        # Filtering
        category = request.query_params.get('category')
        if category:
            products = products.filter(category__slug=category)

        # Pagination
        page = int(request.query_params.get('page', 1))
        items, pagination = product_selectors.paginate(products, page)

        serializer = ProductListSerializer(items, many=True)
        return Response({
            'results': serializer.data,
            'pagination': pagination,
        })

    def retrieve(self, request, pk=None):
        """Get product detail."""
        product = product_selectors.get_by_slug(pk)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        """Create new product (admin only)."""
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = ProductService.create(
            ProductCreateInput(**serializer.validated_data)
        )
        return Response(
            ProductDetailSerializer(product).data,
            status=status.HTTP_201_CREATED
        )
```

---

## Serializer Templates

### Read Serializers

```python
# users/serializers/user_read.py
from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for user list."""

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user detail."""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'avatar',
            'date_joined',
        ]
```

### Write Serializers

```python
# users/serializers/user_write.py
from rest_framework import serializers


class UserCreateSerializer(serializers.Serializer):
    """Serializer for user creation."""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)


class UserUpdateSerializer(serializers.Serializer):
    """Serializer for user update."""

    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    phone = serializers.CharField(max_length=20, required=False)
```

### Nested Serializers

```python
# orders/serializers/order_read.py
from rest_framework import serializers

from orders.models import Order, OrderItem
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order item."""

    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'subtotal']


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for order list."""

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for order detail."""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'total',
            'items',
            'shipping_address',
            'created_at',
            'updated_at',
        ]
```

---

## Permission Templates

```python
# core/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """Object-level permission: only owner can access."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrAdmin(BasePermission):
    """Object-level permission: owner or admin."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    """Admin can write, others can only read."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsVerified(BasePermission):
    """Only verified users can access."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified
```

---

## Test Templates

### Service Tests

```python
# users/tests/test_services.py
import pytest
from django.core.exceptions import ValidationError

from users.services.user_service import UserService, UserCreateInput, UserUpdateInput
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserService:
    """Tests for UserService."""

    def test_create_user_success(self):
        """Test successful user creation."""
        data = UserCreateInput(
            email='test@example.com',
            password='securepassword123',
            first_name='John',
            last_name='Doe',
        )

        user = UserService.create(data)

        assert user.email == 'test@example.com'
        assert user.first_name == 'John'
        assert user.check_password('securepassword123')

    def test_create_user_duplicate_email(self):
        """Test error on duplicate email."""
        UserFactory(email='existing@example.com')

        data = UserCreateInput(
            email='existing@example.com',
            password='password123',
        )

        with pytest.raises(ValueError, match='already registered'):
            UserService.create(data)

    def test_update_user_partial(self):
        """Test partial user update."""
        user = UserFactory(first_name='Old', last_name='Name')

        data = UserUpdateInput(first_name='New')
        updated = UserService.update(user, data)

        assert updated.first_name == 'New'
        assert updated.last_name == 'Name'  # Unchanged

    def test_deactivate_user(self):
        """Test user deactivation."""
        user = UserFactory(is_active=True)

        UserService.deactivate(user)

        user.refresh_from_db()
        assert user.is_active is False
```

### Selector Tests

```python
# users/tests/test_selectors.py
import pytest
from django.utils import timezone
from datetime import timedelta

from users.selectors import user_selectors
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserSelectors:
    """Tests for user selectors."""

    def test_get_by_email_case_insensitive(self):
        """Test email lookup is case-insensitive."""
        UserFactory(email='Test@Example.com')

        user = user_selectors.get_by_email('test@example.com')

        assert user is not None
        assert user.email == 'Test@Example.com'

    def test_email_exists(self):
        """Test email existence check."""
        UserFactory(email='exists@example.com')

        assert user_selectors.email_exists('exists@example.com') is True
        assert user_selectors.email_exists('notexists@example.com') is False

    def test_search(self):
        """Test user search."""
        UserFactory(first_name='John', email='john@example.com')
        UserFactory(first_name='Jane', email='jane@example.com')

        results = list(user_selectors.search('John'))

        assert len(results) == 1
        assert results[0].first_name == 'John'

    def test_get_recent(self):
        """Test getting recent users."""
        recent = UserFactory()
        old = UserFactory(
            date_joined=timezone.now() - timedelta(days=60)
        )

        results = list(user_selectors.get_recent(days=30))

        assert recent in results
        assert old not in results
```

### Factory Template

```python
# users/tests/factories.py
import factory
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.LazyAttribute(lambda obj: obj.email)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_verified = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or 'defaultpassword123'
        self.set_password(password)
        if create:
            self.save()

    @classmethod
    def create_verified(cls, **kwargs):
        """Create a verified user."""
        return cls.create(is_verified=True, **kwargs)

    @classmethod
    def create_admin(cls, **kwargs):
        """Create an admin user."""
        return cls.create(is_staff=True, is_superuser=True, **kwargs)
```

---

## URL Templates

```python
# users/urls.py
from django.urls import path

from users.views.user_views import UserMeView, UserDetailView
from users.views.auth_views import LoginView, RegisterView, LogoutView

app_name = 'users'

urlpatterns = [
    # Auth
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # Profile
    path('me/', UserMeView.as_view(), name='me'),
    path('<int:user_id>/', UserDetailView.as_view(), name='detail'),
]
```

---

## Related

- [README.md](README.md) - Overview and patterns
- [checklist.md](checklist.md) - Step-by-step checklist
- [examples.md](examples.md) - Real-world examples
- [llm-prompts.md](llm-prompts.md) - LLM prompts for decomposition
