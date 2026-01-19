# references/django/

Django-specific patterns and conventions. Provides coding standards for models, services, API endpoints, testing, and background tasks.

## Overview

This folder contains Django development patterns used by the code and test agents. Follows clean architecture principles with service layer for business logic and thin views for HTTP handling.

## Files

| File | Content | Lines |
|------|---------|-------|
| `models.md` | BaseModel pattern (UUID, timestamps), ForeignKey patterns, Django 5.0 features, TextChoices, project structure | ~140 |
| `services.md` | Service layer architecture, function vs class services, parameter formatting, Google-style docstrings | ~115 |
| `api.md` | DRF patterns: thin views, ViewSets, serializers, drf-spectacular documentation, custom exceptions | ~110 |
| `testing.md` | pytest with model_bakery/factory_boy, fixtures, parametrized tests, API testing | ~125 |
| `celery.md` | Task definition, routing, retry patterns, idempotency, calling tasks | ~100 |
| `imports.md` | Cross-app import conventions (alias pattern), import order, type hints for Python 3.9+ and 3.10+ | ~90 |
| `quality.md` | Code quality tools (Black, isort, flake8, mypy), pre-commit config, exception handling patterns | ~110 |

## Key Patterns

### Project Structure

```
project/
├── config/           # Settings, URLs, Celery
├── apps/             # Domain applications
│   ├── users/
│   ├── orders/
│   └── catalog/
├── core/             # Shared code
└── tests/
```

### Cross-App Imports

```python
# Always use aliases for cross-app imports
from apps.orders import models as order_models
from apps.users import services as user_services
```

### Service Layer

```python
# services/ for DB changes and external API calls
# utils/ for pure functions and data transformation
def create_order(user: User, amount: Decimal) -> Order:
    """Business logic here, not in views."""
    ...
```

### Thin Views

```python
class OrderView(APIView):
    def post(self, request):
        # 1. Validate input
        # 2. Call service (business logic)
        # 3. Return response
```

## Integration

These patterns work together:
- `models.md` defines data structures
- `services.md` handles business logic
- `api.md` exposes HTTP endpoints
- `testing.md` verifies behavior
- `celery.md` handles async tasks
- `imports.md` and `quality.md` ensure consistency
