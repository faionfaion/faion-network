# Django API Development Checklist

Step-by-step checklist for building production-ready Django REST APIs.

## Pre-Development

### Project Setup

- [ ] Django 5.x installed
- [ ] Choose framework: DRF 3.15+ or Django Ninja 1.x
- [ ] Install dependencies:
  ```bash
  # DRF
  pip install djangorestframework drf-spectacular django-filter

  # Ninja
  pip install django-ninja
  ```
- [ ] Add to `INSTALLED_APPS`
- [ ] Configure `REST_FRAMEWORK` settings (DRF)

### Planning

- [ ] Define API resources (nouns, not verbs)
- [ ] Plan URL structure (`/api/v1/resources/`)
- [ ] Document authentication requirements
- [ ] Define rate limiting strategy
- [ ] Plan pagination approach
- [ ] Create OpenAPI specification draft

---

## API Design

### URL Design

- [ ] Use plural nouns: `/users/`, `/orders/`
- [ ] Use hyphens for multi-word: `/order-items/`
- [ ] Nest logically: `/users/{id}/orders/`
- [ ] Version in URL: `/api/v1/`
- [ ] Keep URLs under 3 levels deep

### HTTP Methods

| Action | Method | URL | Response |
|--------|--------|-----|----------|
| List | GET | `/resources/` | 200 + array |
| Create | POST | `/resources/` | 201 + object |
| Retrieve | GET | `/resources/{id}/` | 200 + object |
| Update | PUT/PATCH | `/resources/{id}/` | 200 + object |
| Delete | DELETE | `/resources/{id}/` | 204 |
| Custom | POST | `/resources/{id}/action/` | varies |

### Response Codes

- [ ] 200 OK - successful GET, PUT, PATCH
- [ ] 201 Created - successful POST
- [ ] 204 No Content - successful DELETE
- [ ] 400 Bad Request - validation error
- [ ] 401 Unauthorized - missing/invalid auth
- [ ] 403 Forbidden - insufficient permissions
- [ ] 404 Not Found - resource doesn't exist
- [ ] 429 Too Many Requests - rate limited
- [ ] 500 Internal Server Error - server bug

---

## Implementation (DRF)

### Models

- [ ] Add `created_at`, `updated_at` timestamps
- [ ] Add `uuid` field for public identifiers
- [ ] Define `__str__` method
- [ ] Add appropriate indexes
- [ ] Set up related_name for ForeignKeys

### Serializers

- [ ] Create input serializers (validation)
- [ ] Create output serializers (response)
- [ ] Use `read_only_fields` for computed fields
- [ ] Implement custom validation methods
- [ ] Avoid `Meta.fields = "__all__"` (security risk)
- [ ] Use explicit field lists (allowlist approach)

```python
# Checklist item: Separate input/output serializers
class CreateOrderSerializer(serializers.Serializer):
    """Input validation"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class OrderSerializer(serializers.ModelSerializer):
    """Output representation"""
    class Meta:
        model = Order
        fields = ['id', 'uid', 'amount', 'status', 'created_at']
        read_only_fields = ['id', 'uid', 'created_at']
```

### Views

- [ ] Choose ViewSet (CRUD) or APIView (custom)
- [ ] Override `get_queryset()` for filtering
- [ ] Override `get_serializer_class()` for action-specific serializers
- [ ] Use `@action` decorator for custom endpoints
- [ ] Keep views thin (delegate to services)

### Permissions

- [ ] Set default permission class (NOT AllowAny)
- [ ] Create custom permissions if needed
- [ ] Combine permissions with `&` and `|`
- [ ] Test permission edge cases

```python
# Checklist: Permission configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Authentication

- [ ] Choose auth method (JWT recommended for SPAs)
- [ ] Configure token lifetimes
- [ ] Enable token refresh
- [ ] Set up token blacklisting
- [ ] Use HTTPS in production

```python
# JWT configuration checklist
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### Throttling

- [ ] Set anonymous rate limits
- [ ] Set authenticated rate limits
- [ ] Configure scoped throttling for sensitive endpoints
- [ ] Use Redis for distributed throttling (production)

```python
# Throttling configuration
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'login': '5/minute',  # Scoped throttle
    },
}
```

### Pagination

- [ ] Set default pagination class
- [ ] Configure page size
- [ ] Set max page size limit
- [ ] Use cursor pagination for large datasets

```python
# Pagination configuration
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### Filtering & Search

- [ ] Install django-filter
- [ ] Configure filter backends
- [ ] Define filterable fields
- [ ] Set up search fields
- [ ] Enable ordering

```python
# Filtering configuration
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

---

## Implementation (Django Ninja)

### Schemas

- [ ] Create Pydantic schemas for input/output
- [ ] Use `ModelSchema` for Django models
- [ ] Add field validators
- [ ] Configure schema aliases if needed

```python
# Checklist: Ninja schemas
from ninja import Schema, ModelSchema

class CreateOrderSchema(Schema):
    amount: Decimal
    item_id: int

class OrderSchema(ModelSchema):
    class Meta:
        model = Order
        fields = ['id', 'uid', 'amount', 'status']
```

### API Routes

- [ ] Create NinjaAPI instance
- [ ] Organize routes with routers
- [ ] Add authentication classes
- [ ] Document with `summary` and `description`

### Async Views

- [ ] Use `async def` for I/O-bound operations
- [ ] Use `sync_to_async` for ORM queries
- [ ] Consider connection pooling

---

## Documentation

### OpenAPI/Swagger

- [ ] Install drf-spectacular (DRF)
- [ ] Configure SPECTACULAR_SETTINGS
- [ ] Add `@extend_schema` decorators
- [ ] Document all parameters
- [ ] Provide example values
- [ ] Group endpoints with tags

```python
# DRF documentation checklist
@extend_schema(
    summary="Create order",                    # Required
    description="Creates a new order...",      # Required
    request=CreateOrderSerializer,             # Required for POST
    responses={201: OrderSerializer},          # Required
    tags=['Orders'],                           # Required
    examples=[                                 # Recommended
        OpenApiExample(
            'Valid order',
            value={'amount': '99.99', 'item_id': 1}
        )
    ]
)
def post(self, request):
    ...
```

### API Versioning

- [ ] Choose versioning strategy
- [ ] Configure version settings
- [ ] Document deprecation policy
- [ ] Set default version

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

---

## Testing

### Unit Tests

- [ ] Test serializer validation
- [ ] Test permission classes
- [ ] Test custom filters

### Integration Tests

- [ ] Test each endpoint (happy path)
- [ ] Test authentication flows
- [ ] Test error responses
- [ ] Test pagination
- [ ] Test filtering and search

### Security Tests

- [ ] Test unauthorized access
- [ ] Test CSRF protection
- [ ] Test rate limiting
- [ ] Test input validation (SQL injection, XSS)

```python
# Test checklist example
class OrderAPITestCase(APITestCase):
    def test_create_order_authenticated(self):
        """201 for valid authenticated request"""
        ...

    def test_create_order_unauthenticated(self):
        """401 for unauthenticated request"""
        ...

    def test_create_order_invalid_data(self):
        """400 for validation errors"""
        ...
```

---

## Security

### OWASP Recommendations

- [ ] Never use `AllowAny` as default permission
- [ ] Never use `Meta.fields = "__all__"`
- [ ] Always validate and sanitize input
- [ ] Use HTTPS in production
- [ ] Implement CORS properly
- [ ] Rate limit authentication endpoints
- [ ] Log authentication failures
- [ ] Use parameterized queries (Django ORM)

### Sensitive Data

- [ ] Never expose passwords or tokens in responses
- [ ] Mask sensitive fields in logs
- [ ] Use environment variables for secrets
- [ ] Implement field-level permissions if needed

---

## Deployment

### Pre-Production

- [ ] Run `python manage.py check --deploy`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS
- [ ] Configure CORS
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging

### Performance

- [ ] Use database connection pooling
- [ ] Configure caching (Redis)
- [ ] Optimize database queries (select_related, prefetch_related)
- [ ] Use async views for I/O operations (Ninja)
- [ ] Set up CDN for static files

### Monitoring

- [ ] Set up API metrics
- [ ] Monitor response times
- [ ] Track error rates
- [ ] Alert on anomalies
- [ ] Log request/response for debugging

---

## Post-Launch

### Documentation

- [ ] Publish OpenAPI spec
- [ ] Create SDK/client libraries
- [ ] Write integration guides
- [ ] Document rate limits
- [ ] Create changelog

### Versioning

- [ ] Plan deprecation timeline
- [ ] Communicate breaking changes
- [ ] Support old versions during transition
- [ ] Monitor version usage

---

## Quick Reference

### Common Issues Checklist

| Issue | Check |
|-------|-------|
| 401 Unauthorized | Token expired? Auth header format? |
| 403 Forbidden | Permission class? Object permissions? |
| 404 Not Found | URL pattern? Queryset filter? |
| 500 Error | Check logs, DEBUG=True locally |
| Slow response | N+1 queries? Missing indexes? |

---

*Last updated: 2026-01-25*
