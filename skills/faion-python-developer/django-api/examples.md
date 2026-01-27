# Django API Examples

Real-world API implementations showing good and bad patterns.

## Table of Contents

1. [Thin Views Pattern](#1-thin-views-pattern)
2. [ViewSets vs APIViews](#2-viewsets-vs-apiviews)
3. [Serializer Patterns](#3-serializer-patterns)
4. [Authentication](#4-authentication)
5. [Permissions](#5-permissions)
6. [Error Handling](#6-error-handling)
7. [Pagination](#7-pagination)
8. [Filtering and Search](#8-filtering-and-search)
9. [Django Ninja Examples](#9-django-ninja-examples)
10. [Testing Examples](#10-testing-examples)

---

## 1. Thin Views Pattern

### Bad: Fat View with Business Logic

```python
# views.py - AVOID THIS
class OrderCreateView(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Business logic in view (BAD)
        user = request.user
        item = Item.objects.get(id=serializer.validated_data['item_id'])

        if user.balance < item.price:
            return Response(
                {'error': 'Insufficient balance'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.balance -= item.price
        user.save()

        order = Order.objects.create(
            user=user,
            item=item,
            amount=item.price,
            status='pending'
        )

        # Send email in view (BAD)
        send_mail(
            'Order Confirmation',
            f'Your order #{order.id} has been created.',
            'noreply@example.com',
            [user.email]
        )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
```

### Good: Thin View with Service Layer

```python
# services/order_services.py
from django.db import transaction
from apps.orders.models import Order
from apps.notifications import email_service


class InsufficientBalanceError(Exception):
    pass


@transaction.atomic
def create_order(user, item_id: int) -> Order:
    """
    Create order for user.

    Raises:
        InsufficientBalanceError: If user balance is too low
        Item.DoesNotExist: If item not found
    """
    item = Item.objects.select_for_update().get(id=item_id)

    if user.balance < item.price:
        raise InsufficientBalanceError(f"Need {item.price}, have {user.balance}")

    user.balance -= item.price
    user.save(update_fields=['balance'])

    order = Order.objects.create(
        user=user,
        item=item,
        amount=item.price,
        status='pending'
    )

    # Async task for email
    email_service.send_order_confirmation.delay(order.id)

    return order


# views.py - GOOD: Thin view
class OrderCreateView(APIView):
    @extend_schema(
        summary="Create order",
        description="Creates a new order for the authenticated user",
        request=CreateOrderSerializer,
        responses={
            201: OrderSerializer,
            400: OpenApiTypes.OBJECT,
        },
        tags=['Orders'],
    )
    def post(self, request):
        # 1. Validate input
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Call service
        try:
            order = order_services.create_order(
                user=request.user,
                item_id=serializer.validated_data['item_id'],
            )
        except order_services.InsufficientBalanceError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Return response
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
```

---

## 2. ViewSets vs APIViews

### Good: ViewSet for Standard CRUD

```python
# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.products.models import Product
from apps.products import services as product_services
from . import serializers


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for products.

    list: Get all products (paginated)
    create: Create new product
    retrieve: Get single product
    update: Full update of product
    partial_update: Partial update
    destroy: Delete product
    """
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter by user's organization."""
        return self.queryset.filter(
            organization=self.request.user.organization
        ).select_related('category').prefetch_related('tags')

    def get_serializer_class(self):
        """Different serializers for different actions."""
        if self.action == 'create':
            return serializers.CreateProductSerializer
        if self.action in ['update', 'partial_update']:
            return serializers.UpdateProductSerializer
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Custom action: publish product."""
        product = self.get_object()
        product_services.publish_product(product)
        return Response({'status': 'published'})

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Custom action: archive product."""
        product = self.get_object()
        product_services.archive_product(product)
        return Response({'status': 'archived'})


# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
urlpatterns = router.urls
```

### Good: APIView for Custom Logic

```python
# views.py
class ProductSearchView(APIView):
    """
    Complex search with external service.
    Not a standard CRUD operation -> use APIView.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Search products",
        description="Full-text search with Elasticsearch",
        parameters=[
            OpenApiParameter(
                name='q',
                type=str,
                required=True,
                description='Search query'
            ),
            OpenApiParameter(
                name='category',
                type=str,
                required=False,
                description='Filter by category slug'
            ),
        ],
        responses={200: serializers.ProductListSerializer(many=True)},
        tags=['Products'],
    )
    def get(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category')

        if len(query) < 2:
            return Response(
                {'error': 'Query must be at least 2 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = search_services.search_products(
            query=query,
            category=category,
            organization=request.user.organization,
        )

        serializer = serializers.ProductListSerializer(results, many=True)
        return Response(serializer.data)


class AnalyticsDashboardView(APIView):
    """
    Aggregate analytics - not tied to single model.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        summary="Get dashboard analytics",
        responses={200: serializers.DashboardAnalyticsSerializer},
        tags=['Analytics'],
    )
    def get(self, request):
        analytics = analytics_services.get_dashboard_data(
            organization=request.user.organization,
            date_from=request.query_params.get('date_from'),
            date_to=request.query_params.get('date_to'),
        )
        serializer = serializers.DashboardAnalyticsSerializer(analytics)
        return Response(serializer.data)
```

---

## 3. Serializer Patterns

### Bad: Single Serializer for Everything

```python
# AVOID: One serializer doing too much
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Security risk!
```

### Good: Separate Input/Output Serializers

```python
# serializers.py

# Input: For creating users
class CreateUserSerializer(serializers.Serializer):
    """Validate user registration input."""
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already registered")
        return value.lower()

    def validate_password(self, value):
        # Custom password validation
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter"
            )
        return value


# Output: For listing users (minimal data)
class UserListSerializer(serializers.ModelSerializer):
    """Minimal user data for lists."""
    class Meta:
        model = User
        fields = ['id', 'uid', 'email', 'first_name', 'last_name']
        read_only_fields = fields


# Output: For user detail (more data)
class UserDetailSerializer(serializers.ModelSerializer):
    """Full user data for detail view."""
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'uid', 'email', 'first_name', 'last_name',
            'organization', 'role', 'created_at', 'last_login'
        ]
        read_only_fields = fields


# Input: For updating users
class UpdateUserSerializer(serializers.Serializer):
    """Validate user update input."""
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    avatar_url = serializers.URLField(required=False, allow_null=True)
```

### Good: Nested Serializers

```python
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = UserListSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'uid', 'customer', 'items',
            'total', 'status', 'created_at'
        ]


# Creating order with nested items
class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True, min_length=1)
    shipping_address_id = serializers.IntegerField()

    def validate_items(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Maximum 100 items per order")
        return value
```

---

## 4. Authentication

### Good: JWT Configuration

```python
# settings.py
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### Good: Custom Token Claims

```python
# auth/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['organization_id'] = user.organization_id

        return token


# auth/views.py
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# urls.py
urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

## 5. Permissions

### Good: Custom Permission Classes

```python
# permissions.py
from rest_framework import permissions


class IsOrganizationMember(permissions.BasePermission):
    """
    Object-level permission: user must belong to object's organization.
    """
    message = "You don't have access to this resource"

    def has_object_permission(self, request, view, obj):
        # Read permissions for organization members
        if hasattr(obj, 'organization'):
            return obj.organization == request.user.organization
        if hasattr(obj, 'user'):
            return obj.user.organization == request.user.organization
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin users can modify, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object owner or admin can access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user


# views.py - Using permissions
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_permissions(self):
        """Different permissions for different actions."""
        if self.action == 'destroy':
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return super().get_permissions()
```

---

## 6. Error Handling

### Good: Custom Exception Handler

```python
# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


class OrderLimitExceeded(APIException):
    status_code = 400
    default_detail = 'Daily order limit exceeded'
    default_code = 'order_limit_exceeded'


class InsufficientBalance(APIException):
    status_code = 400
    default_detail = 'Insufficient account balance'
    default_code = 'insufficient_balance'


def custom_exception_handler(exc, context):
    """
    Custom exception handler with consistent error format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize error format
        error_data = {
            'error': {
                'code': getattr(exc, 'default_code', 'error'),
                'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
                'status': response.status_code,
            }
        }

        # Add field errors for validation
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            error_data['error']['fields'] = exc.detail

        response.data = error_data

    return response


# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}
```

### Good: Validation Error Examples

```python
# serializers.py
class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    item_id = serializers.IntegerField()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        if value > 10000:
            raise serializers.ValidationError("Amount exceeds maximum limit")
        return value

    def validate(self, attrs):
        """Cross-field validation."""
        item = Item.objects.filter(id=attrs['item_id']).first()
        if not item:
            raise serializers.ValidationError({
                'item_id': 'Item not found'
            })
        if not item.is_available:
            raise serializers.ValidationError({
                'item_id': 'Item is not available'
            })
        attrs['item'] = item
        return attrs
```

---

## 7. Pagination

### Good: Custom Pagination

```python
# pagination.py
from rest_framework.pagination import PageNumberPagination, CursorPagination


class StandardPagination(PageNumberPagination):
    """Standard pagination for most endpoints."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class TimelinePagination(CursorPagination):
    """Cursor pagination for feeds/timelines."""
    page_size = 50
    ordering = '-created_at'
    cursor_query_param = 'cursor'


# views.py
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = TimelinePagination
    # ...


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    # ...
```

---

## 8. Filtering and Search

### Good: Comprehensive Filtering

```python
# filters.py
import django_filters
from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):
    """Filter products by multiple criteria."""

    # Exact match
    category = django_filters.CharFilter(field_name='category__slug')
    status = django_filters.ChoiceFilter(choices=Product.STATUS_CHOICES)

    # Range filters
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )

    # Date range
    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    # Boolean
    is_featured = django_filters.BooleanFilter()
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    # Multiple values
    tags = django_filters.CharFilter(method='filter_tags')

    class Meta:
        model = Product
        fields = ['category', 'status', 'is_featured']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset.filter(stock_quantity=0)

    def filter_tags(self, queryset, name, value):
        tags = value.split(',')
        return queryset.filter(tags__slug__in=tags).distinct()


# views.py
class ProductViewSet(viewsets.ModelViewSet):
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
```

---

## 9. Django Ninja Examples

### Good: Ninja API Setup

```python
# api.py
from ninja import NinjaAPI
from ninja.security import HttpBearer

api = NinjaAPI(
    title="My API",
    version="1.0.0",
    description="API documentation",
)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return user
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return None


# schemas.py
from ninja import Schema, ModelSchema
from pydantic import Field, field_validator


class CreateProductSchema(Schema):
    name: str = Field(..., min_length=1, max_length=200)
    price: Decimal = Field(..., ge=0, le=99999)
    category_id: int

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        fields = ['id', 'uid', 'name', 'price', 'status', 'created_at']


# api.py - Routes
@api.get("/products", response=list[ProductSchema], tags=["Products"])
def list_products(request, category: str = None, min_price: Decimal = None):
    """List all products with optional filtering."""
    qs = Product.objects.all()
    if category:
        qs = qs.filter(category__slug=category)
    if min_price:
        qs = qs.filter(price__gte=min_price)
    return qs


@api.post("/products", response={201: ProductSchema}, auth=AuthBearer(), tags=["Products"])
def create_product(request, payload: CreateProductSchema):
    """Create a new product."""
    product = Product.objects.create(**payload.dict())
    return 201, product


@api.get("/products/{product_id}", response=ProductSchema, tags=["Products"])
def get_product(request, product_id: int):
    """Get product by ID."""
    return get_object_or_404(Product, id=product_id)


@api.delete("/products/{product_id}", response={204: None}, auth=AuthBearer(), tags=["Products"])
def delete_product(request, product_id: int):
    """Delete a product."""
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return 204, None
```

### Good: Ninja Async Views

```python
# api.py
from asgiref.sync import sync_to_async


@api.get("/products/search", response=list[ProductSchema], tags=["Products"])
async def search_products(request, q: str):
    """Async search with external service."""
    # Async external API call
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://search-api.example.com/products?q={q}")
        external_results = response.json()

    # Wrap ORM query in sync_to_async
    @sync_to_async
    def get_products(ids):
        return list(Product.objects.filter(id__in=ids))

    product_ids = [r['id'] for r in external_results]
    products = await get_products(product_ids)

    return products
```

---

## 10. Testing Examples

### Good: Comprehensive API Tests

```python
# tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.users.models import User
from apps.products.models import Product


class ProductAPITestCase(APITestCase):
    """Test suite for Product API."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        cls.product = Product.objects.create(
            name='Test Product',
            price='99.99',
            organization=cls.user.organization
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    # List tests
    def test_list_products_authenticated(self):
        """GET /products/ returns 200 and product list."""
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_products_unauthenticated(self):
        """GET /products/ returns 401 without auth."""
        self.client.force_authenticate(user=None)
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Create tests
    def test_create_product_valid(self):
        """POST /products/ creates product."""
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'price': '149.99',
            'category_id': self.category.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_invalid(self):
        """POST /products/ with invalid data returns 400."""
        url = reverse('product-list')
        data = {
            'name': '',  # Invalid: empty name
            'price': '-10',  # Invalid: negative price
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('price', response.data)

    # Retrieve tests
    def test_retrieve_product(self):
        """GET /products/{id}/ returns product detail."""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)

    def test_retrieve_product_not_found(self):
        """GET /products/{id}/ returns 404 for invalid ID."""
        url = reverse('product-detail', args=[99999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update tests
    def test_update_product(self):
        """PATCH /products/{id}/ updates product."""
        url = reverse('product-detail', args=[self.product.id])
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')

    # Delete tests
    def test_delete_product(self):
        """DELETE /products/{id}/ removes product."""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    # Permission tests
    def test_cannot_access_other_org_product(self):
        """User cannot access products from other organizations."""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        other_product = Product.objects.create(
            name='Other Product',
            price='50.00',
            organization=other_user.organization
        )

        url = reverse('product-detail', args=[other_product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Filtering tests
    def test_filter_by_category(self):
        """GET /products/?category=electronics filters correctly."""
        url = reverse('product-list')
        response = self.client.get(url, {'category': 'electronics'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert filtered results

    # Search tests
    def test_search_products(self):
        """GET /products/?search=test returns matching products."""
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Test'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # Pagination tests
    def test_pagination(self):
        """GET /products/ returns paginated results."""
        # Create 25 products
        for i in range(24):
            Product.objects.create(
                name=f'Product {i}',
                price='10.00',
                organization=self.user.organization
            )

        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)  # Default page size
        self.assertIsNotNone(response.data['next'])
```

---

## Anti-Patterns Summary

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Fat views | Hard to test, violates SRP | Use service layer |
| `fields = "__all__"` | Exposes sensitive data | Explicit field list |
| Single serializer | Mixed concerns | Separate input/output |
| No pagination | Memory issues | Always paginate |
| AllowAny default | Security risk | IsAuthenticated default |
| Business logic in serializers | Testing difficulty | Move to services |
| N+1 queries | Performance | select_related/prefetch_related |

---

*Last updated: 2026-01-25*
