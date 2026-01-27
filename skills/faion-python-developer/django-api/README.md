# Django API Development

Comprehensive guide for building REST APIs with Django REST Framework (DRF) and Django Ninja.

## Overview

| Framework | Best For | Performance | Learning Curve |
|-----------|----------|-------------|----------------|
| **DRF 3.15+** | Complex APIs, large teams, enterprise | Good | Moderate |
| **Django Ninja 1.x** | Fast APIs, type-safety, async | Excellent | Easy |

## DRF vs Django Ninja Comparison

### Django REST Framework (DRF)

**Strengths:**
- Battle-tested since 2011, massive ecosystem
- 1000+ third-party packages
- Browsable API for debugging
- Powerful ViewSets for CRUD operations
- Built-in authentication, permissions, throttling
- Extensive documentation and community

**Weaknesses:**
- Complex class hierarchy (ViewSets, Mixins, Generics)
- No native async support (added via external module)
- Slower than Ninja for high-concurrency apps
- Serializers can be verbose

**Best for:**
- Large enterprise projects
- Teams familiar with Django patterns
- APIs requiring complex permissions
- Projects needing extensive third-party integrations

### Django Ninja

**Strengths:**
- FastAPI-inspired, modern Python (type hints)
- Native async/await support
- Pydantic validation (faster, more intuitive)
- Automatic OpenAPI documentation
- ~2-3x faster than DRF in benchmarks
- Clean, minimal code

**Weaknesses:**
- Smaller ecosystem (since 2021)
- No ViewSet equivalent (write each endpoint)
- Less built-in functionality
- Fewer third-party packages

**Best for:**
- New greenfield projects
- High-performance APIs
- Teams familiar with FastAPI/Pydantic
- Simple to medium complexity APIs

### Decision Matrix

| Criteria | Choose DRF | Choose Ninja |
|----------|-----------|--------------|
| Team experience | Django experts | FastAPI/modern Python |
| API complexity | Complex, many models | Simple to moderate |
| Performance needs | Standard | High concurrency |
| Ecosystem needs | Many integrations | Minimal dependencies |
| Async requirements | Optional | Critical |
| Code style | Class-based | Function-based |

## Core Concepts

### 1. ViewSets vs APIViews (DRF)

**ViewSets** - CRUD operations on models:
```python
# Automatic URL routing, less code
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

**APIViews** - Custom endpoints:
```python
# Full control, explicit HTTP methods
class ActivateUserView(APIView):
    def post(self, request):
        # Custom logic
        return Response({"status": "activated"})
```

**Rule of thumb:** Use ViewSets for standard CRUD, APIViews for custom actions.

### 2. Serializers (DRF) vs Schemas (Ninja)

**DRF Serializers:**
```python
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'amount', 'status']
```

**Ninja Schemas (Pydantic):**
```python
class OrderSchema(ModelSchema):
    class Meta:
        model = Order
        fields = ['id', 'amount', 'status']
```

### 3. Authentication Methods

| Method | Use Case | Package |
|--------|----------|---------|
| **JWT** | SPAs, mobile apps | `djangorestframework-simplejwt` |
| **Session** | Django templates, same-origin | Built-in |
| **OAuth2** | Third-party integrations | `django-oauth-toolkit` |
| **API Key** | Machine-to-machine | `djangorestframework-api-key` |

**JWT Best Practices:**
- Access tokens: 15-30 minutes
- Refresh tokens: 7-30 days
- Store in HttpOnly cookies (not localStorage)
- Enable token rotation and blacklisting

### 4. Permissions & Throttling

**Permission Classes:**
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**Throttling:**
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
}
```

### 5. Pagination Strategies

| Style | Use Case | Example |
|-------|----------|---------|
| **PageNumber** | Simple UIs, pages | `?page=2` |
| **LimitOffset** | Flexible clients | `?limit=20&offset=40` |
| **Cursor** | Large datasets, real-time | `?cursor=cD0yMDIx` |

**Best Practice:** Cursor pagination for feeds/timelines, PageNumber for admin panels.

### 6. API Versioning

| Strategy | URL Example | Pros |
|----------|-------------|------|
| **URL Path** | `/api/v1/users/` | Clear, cacheable |
| **Query Param** | `/api/users/?version=1` | Easy to test |
| **Header** | `Accept: application/json; version=1` | Clean URLs |

**Recommendation:** URL Path versioning is most common and explicit.

### 7. OpenAPI Documentation

**DRF:** Use `drf-spectacular` (recommended by DRF)
```python
INSTALLED_APPS = ['drf_spectacular']
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

**Ninja:** Built-in automatic OpenAPI generation

## LLM Usage Tips

### When to Use This Methodology

- Building new Django REST APIs
- Adding endpoints to existing Django projects
- Choosing between DRF and Ninja
- Implementing authentication/authorization
- Optimizing API performance

### Effective Prompts

1. **For new APIs:** "Create a DRF ViewSet for [Model] with list, create, retrieve, update, delete actions"
2. **For custom endpoints:** "Create an APIView for [action] that validates [input] and returns [output]"
3. **For Ninja:** "Create Django Ninja endpoints for [Model] CRUD with Pydantic schemas"
4. **For auth:** "Implement JWT authentication with refresh token rotation"

### Context to Provide

- Django version (5.x recommended)
- DRF version (3.15+) or Ninja version (1.x)
- Existing models and their relationships
- Authentication requirements
- Performance requirements (sync vs async)

## Quick Reference

### DRF Imports

```python
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
```

### Ninja Imports

```python
from ninja import NinjaAPI, Schema, ModelSchema
from ninja.security import HttpBearer
```

## External Resources

### Official Documentation
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Ninja](https://django-ninja.dev/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)

### Authentication
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
- [django-oauth-toolkit](https://django-oauth-toolkit.readthedocs.io/)

### Filtering & Search
- [django-filter](https://django-filter.readthedocs.io/)

### Best Practices
- [OWASP DRF Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_REST_Framework_Cheat_Sheet.html)
- [DRF vs Ninja Comparison (DigitalOcean)](https://www.digitalocean.com/community/questions/django-rest-framework-vs-django-ninja-a-comprehensive-comparison-for-api-development)
- [HackerOne DRF vs Ninja](https://www.hackerone.com/blog/django-rest-framework-vs-django-ninja-high-level-comparison)

## Related Files

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step API development checklist |
| [examples.md](examples.md) | Real implementations with good/bad patterns |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted development |

---

*Last updated: 2026-01-25*
