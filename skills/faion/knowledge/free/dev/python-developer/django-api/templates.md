# Django API Templates

Copy-paste templates for common API patterns. Customize placeholders marked with `{...}`.

## Table of Contents

1. [DRF Settings](#1-drf-settings)
2. [Serializers](#2-serializers)
3. [Views](#3-views)
4. [ViewSets](#4-viewsets)
5. [Permissions](#5-permissions)
6. [Filters](#6-filters)
7. [Pagination](#7-pagination)
8. [Authentication](#8-authentication)
9. [URL Configuration](#9-url-configuration)
10. [Django Ninja](#10-django-ninja)
11. [Testing](#11-testing)

---

## 1. DRF Settings

### Complete REST_FRAMEWORK Configuration

```python
# settings.py

REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # Permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Versioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],

    # Schema
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Renderers
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    # Exception handler
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',

    # Datetime format
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# drf-spectacular Settings
SPECTACULAR_SETTINGS = {
    'TITLE': '{Project Name} API',
    'DESCRIPTION': '{Project description}',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]+',
}
```

---

## 2. Serializers

### Model Serializer (Output)

```python
# serializers.py
from rest_framework import serializers
from apps.{app}.models import {Model}


class {Model}Serializer(serializers.ModelSerializer):
    """
    {Model} representation for API responses.
    """
    class Meta:
        model = {Model}
        fields = [
            'id',
            'uid',
            # Add fields here
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'uid', 'created_at', 'updated_at']
```

### List Serializer (Minimal Output)

```python
class {Model}ListSerializer(serializers.ModelSerializer):
    """
    Minimal {Model} data for list views.
    """
    class Meta:
        model = {Model}
        fields = ['id', 'uid', 'name']  # Minimal fields
        read_only_fields = fields
```

### Detail Serializer (Full Output)

```python
class {Model}DetailSerializer(serializers.ModelSerializer):
    """
    Full {Model} data for detail views.
    """
    # Nested relations
    {related} = {Related}Serializer(read_only=True)

    class Meta:
        model = {Model}
        fields = [
            'id',
            'uid',
            # All fields
            '{related}',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields
```

### Create Serializer (Input)

```python
class Create{Model}Serializer(serializers.Serializer):
    """
    Validate {Model} creation input.
    """
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    {field} = serializers.{FieldType}()

    def validate_name(self, value):
        """Custom field validation."""
        if {Model}.objects.filter(name=value).exists():
            raise serializers.ValidationError("Name already exists")
        return value

    def validate(self, attrs):
        """Cross-field validation."""
        # Add cross-field validation logic
        return attrs
```

### Update Serializer (Input)

```python
class Update{Model}Serializer(serializers.Serializer):
    """
    Validate {Model} update input.
    """
    name = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    {field} = serializers.{FieldType}(required=False)
```

### Nested Create Serializer

```python
class Create{Model}ItemSerializer(serializers.Serializer):
    """Nested item for {Model} creation."""
    {item_field}_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class Create{Model}Serializer(serializers.Serializer):
    """
    Create {Model} with nested items.
    """
    items = Create{Model}ItemSerializer(many=True, min_length=1)
    {field} = serializers.{FieldType}()

    def validate_items(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Maximum 100 items")
        return value
```

---

## 3. Views

### APIView Template

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.{app} import services as {app}_services
from . import serializers


class {Action}{Model}View(APIView):
    """
    {Description of the endpoint}.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="{Short summary}",
        description="{Detailed description}",
        request=serializers.{Request}Serializer,
        responses={
            200: serializers.{Response}Serializer,
            400: OpenApiTypes.OBJECT,
        },
        tags=['{Tag}'],
    )
    def post(self, request):
        # 1. Validate input
        serializer = serializers.{Request}Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Call service
        try:
            result = {app}_services.{action}(
                user=request.user,
                **serializer.validated_data,
            )
        except {app}_services.{Exception} as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Return response
        response = serializers.{Response}Serializer(result)
        return Response(response.data, status=status.HTTP_200_OK)
```

### GET Endpoint with Query Parameters

```python
class {Model}SearchView(APIView):
    """
    Search {models} with filters.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Search {models}",
        description="Search and filter {models}",
        parameters=[
            OpenApiParameter(
                name='q',
                type=str,
                required=False,
                description='Search query'
            ),
            OpenApiParameter(
                name='status',
                type=str,
                required=False,
                enum=['active', 'inactive'],
                description='Filter by status'
            ),
            OpenApiParameter(
                name='page',
                type=int,
                required=False,
                description='Page number'
            ),
        ],
        responses={200: serializers.{Model}ListSerializer(many=True)},
        tags=['{Tag}'],
    )
    def get(self, request):
        query = request.query_params.get('q', '')
        status_filter = request.query_params.get('status')

        results = {app}_services.search_{models}(
            user=request.user,
            query=query,
            status=status_filter,
        )

        # Paginate
        paginator = StandardPagination()
        page = paginator.paginate_queryset(results, request)
        serializer = serializers.{Model}ListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
```

---

## 4. ViewSets

### ModelViewSet Template

```python
# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.{app}.models import {Model}
from apps.{app} import services as {app}_services
from . import serializers, filters


@extend_schema_view(
    list=extend_schema(
        summary="List {models}",
        description="Get paginated list of {models}",
        tags=['{Tag}'],
    ),
    create=extend_schema(
        summary="Create {model}",
        description="Create a new {model}",
        tags=['{Tag}'],
    ),
    retrieve=extend_schema(
        summary="Get {model}",
        description="Get {model} details",
        tags=['{Tag}'],
    ),
    update=extend_schema(
        summary="Update {model}",
        description="Full update of {model}",
        tags=['{Tag}'],
    ),
    partial_update=extend_schema(
        summary="Partial update {model}",
        description="Partial update of {model}",
        tags=['{Tag}'],
    ),
    destroy=extend_schema(
        summary="Delete {model}",
        description="Delete {model}",
        tags=['{Tag}'],
    ),
)
class {Model}ViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for {Model}.
    """
    queryset = {Model}.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = filters.{Model}Filter
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by user's organization."""
        return self.queryset.filter(
            organization=self.request.user.organization
        ).select_related('{related}').prefetch_related('{many_related}')

    def get_serializer_class(self):
        """Return appropriate serializer for action."""
        if self.action == 'create':
            return serializers.Create{Model}Serializer
        if self.action in ['update', 'partial_update']:
            return serializers.Update{Model}Serializer
        if self.action == 'list':
            return serializers.{Model}ListSerializer
        return serializers.{Model}DetailSerializer

    def perform_create(self, serializer):
        """Set organization on create."""
        serializer.save(organization=self.request.user.organization)

    @extend_schema(
        summary="{Custom action}",
        description="{Description}",
        request=serializers.{Action}RequestSerializer,
        responses={200: serializers.{Action}ResponseSerializer},
        tags=['{Tag}'],
    )
    @action(detail=True, methods=['post'])
    def {custom_action}(self, request, pk=None):
        """Custom action on {model}."""
        instance = self.get_object()

        serializer = serializers.{Action}RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = {app}_services.{action}(
            instance=instance,
            **serializer.validated_data,
        )

        response = serializers.{Action}ResponseSerializer(result)
        return Response(response.data)
```

### ReadOnlyModelViewSet Template

```python
class {Model}ViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only operations for {Model}.
    """
    queryset = {Model}.objects.all()
    serializer_class = serializers.{Model}Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(is_active=True)
```

---

## 5. Permissions

### Custom Permission Class

```python
# permissions.py
from rest_framework import permissions


class Is{Role}(permissions.BasePermission):
    """
    Allow access only to users with {role} role.
    """
    message = "You must be a {role} to perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == '{role}'
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object owner can modify, others can only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOrganizationMember(permissions.BasePermission):
    """
    User must belong to object's organization.
    """
    message = "You don't have access to this resource"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'organization'):
            return obj.organization == request.user.organization
        return False
```

---

## 6. Filters

### FilterSet Template

```python
# filters.py
import django_filters
from apps.{app}.models import {Model}


class {Model}Filter(django_filters.FilterSet):
    """
    Filter {Model} queryset.
    """
    # Exact match
    status = django_filters.ChoiceFilter(choices={Model}.STATUS_CHOICES)
    category = django_filters.CharFilter(field_name='category__slug')

    # Range filters
    min_{field} = django_filters.NumberFilter(
        field_name='{field}',
        lookup_expr='gte'
    )
    max_{field} = django_filters.NumberFilter(
        field_name='{field}',
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
    is_active = django_filters.BooleanFilter()

    # Custom method
    has_{relation} = django_filters.BooleanFilter(method='filter_has_{relation}')

    class Meta:
        model = {Model}
        fields = ['status', 'category', 'is_active']

    def filter_has_{relation}(self, queryset, name, value):
        if value:
            return queryset.filter({relation}__isnull=False)
        return queryset.filter({relation}__isnull=True)
```

---

## 7. Pagination

### Custom Pagination Class

```python
# pagination.py
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """Standard pagination with metadata."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class TimelinePagination(CursorPagination):
    """Cursor pagination for feeds/timelines."""
    page_size = 50
    ordering = '-created_at'
    cursor_query_param = 'cursor'
```

---

## 8. Authentication

### Custom Token View

```python
# auth/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

---

## 9. URL Configuration

### ViewSet URLs with Router

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('{models}', views.{Model}ViewSet, basename='{model}')

urlpatterns = [
    path('', include(router.urls)),
]
```

### APIView URLs

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('{models}/', views.{Model}ListView.as_view(), name='{model}-list'),
    path('{models}/<int:pk>/', views.{Model}DetailView.as_view(), name='{model}-detail'),
    path('{models}/<int:pk>/{action}/', views.{Model}{Action}View.as_view(), name='{model}-{action}'),
]
```

### Versioned API URLs

```python
# project/urls.py
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # API v1
    path('api/v1/', include([
        path('', include('apps.{app}.urls')),
        path('auth/', include('apps.auth.urls')),
    ])),

    # OpenAPI Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

---

## 10. Django Ninja

### API Setup

```python
# api.py
from ninja import NinjaAPI
from ninja.security import HttpBearer
import jwt
from django.conf import settings

api = NinjaAPI(
    title="{Project} API",
    version="1.0.0",
    description="{Description}",
)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            from apps.users.models import User
            user = User.objects.get(id=payload['user_id'])
            return user
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return None
```

### Ninja Schemas

```python
# schemas.py
from ninja import Schema, ModelSchema
from pydantic import Field, field_validator
from decimal import Decimal
from datetime import datetime

from apps.{app}.models import {Model}


class Create{Model}Schema(Schema):
    """Input schema for creating {Model}."""
    name: str = Field(..., min_length=1, max_length=200)
    {field}: {Type}

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        return v.strip()


class Update{Model}Schema(Schema):
    """Input schema for updating {Model}."""
    name: str | None = Field(None, min_length=1, max_length=200)
    {field}: {Type} | None = None


class {Model}Schema(ModelSchema):
    """Output schema for {Model}."""
    class Meta:
        model = {Model}
        fields = ['id', 'uid', 'name', 'created_at']
```

### Ninja Routes

```python
# api.py
from ninja import Router
from django.shortcuts import get_object_or_404

from apps.{app}.models import {Model}
from . import schemas

router = Router(tags=["{Models}"])


@router.get("/", response=list[schemas.{Model}Schema])
def list_{models}(request, status: str = None):
    """List all {models}."""
    qs = {Model}.objects.all()
    if status:
        qs = qs.filter(status=status)
    return qs


@router.get("/{id}", response=schemas.{Model}Schema)
def get_{model}(request, id: int):
    """Get {model} by ID."""
    return get_object_or_404({Model}, id=id)


@router.post("/", response={201: schemas.{Model}Schema}, auth=AuthBearer())
def create_{model}(request, payload: schemas.Create{Model}Schema):
    """Create new {model}."""
    {model} = {Model}.objects.create(
        **payload.dict(),
        user=request.auth,
    )
    return 201, {model}


@router.patch("/{id}", response=schemas.{Model}Schema, auth=AuthBearer())
def update_{model}(request, id: int, payload: schemas.Update{Model}Schema):
    """Update {model}."""
    {model} = get_object_or_404({Model}, id=id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr({model}, attr, value)
    {model}.save()
    return {model}


@router.delete("/{id}", response={204: None}, auth=AuthBearer())
def delete_{model}(request, id: int):
    """Delete {model}."""
    {model} = get_object_or_404({Model}, id=id)
    {model}.delete()
    return 204, None


# Main API registration
api.add_router("/{models}/", router)
```

---

## 11. Testing

### APITestCase Template

```python
# tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.users.models import User
from apps.{app}.models import {Model}


class {Model}APITestCase(APITestCase):
    """Test suite for {Model} API."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        cls.{model} = {Model}.objects.create(
            name='Test {Model}',
            user=cls.user,
        )

    def setUp(self):
        """Authenticate before each test."""
        self.client.force_authenticate(user=self.user)

    # List
    def test_list_{models}(self):
        """GET /{models}/ returns 200."""
        url = reverse('{model}-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_list_{models}_unauthenticated(self):
        """GET /{models}/ returns 401 without auth."""
        self.client.force_authenticate(user=None)
        url = reverse('{model}-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Create
    def test_create_{model}_valid(self):
        """POST /{models}/ creates {model}."""
        url = reverse('{model}-list')
        data = {'name': 'New {Model}'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual({Model}.objects.count(), 2)

    def test_create_{model}_invalid(self):
        """POST /{models}/ with invalid data returns 400."""
        url = reverse('{model}-list')
        data = {'name': ''}  # Invalid
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Retrieve
    def test_retrieve_{model}(self):
        """GET /{models}/{id}/ returns {model}."""
        url = reverse('{model}-detail', args=[self.{model}.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.{model}.id)

    def test_retrieve_{model}_not_found(self):
        """GET /{models}/{id}/ returns 404 for invalid ID."""
        url = reverse('{model}-detail', args=[99999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update
    def test_update_{model}(self):
        """PATCH /{models}/{id}/ updates {model}."""
        url = reverse('{model}-detail', args=[self.{model}.id])
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')

    # Delete
    def test_delete_{model}(self):
        """DELETE /{models}/{id}/ removes {model}."""
        url = reverse('{model}-detail', args=[self.{model}.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual({Model}.objects.count(), 0)
```

---

## Placeholder Reference

| Placeholder | Replace With |
|-------------|--------------|
| `{Model}` | Model class name (e.g., `Product`) |
| `{model}` | Model instance name (e.g., `product`) |
| `{models}` | Plural form (e.g., `products`) |
| `{app}` | Django app name (e.g., `products`) |
| `{field}` | Field name |
| `{Type}` | Python type hint |
| `{FieldType}` | Serializer field type |
| `{Tag}` | OpenAPI tag name |
| `{Action}` | Action name (e.g., `Activate`) |
| `{action}` | Action function name (e.g., `activate`) |
| `{related}` | Related model field |
| `{Role}` | User role name |
| `{role}` | Role value |

---

*Last updated: 2026-01-25*
