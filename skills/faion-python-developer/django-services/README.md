# Django Services Architecture

A comprehensive guide to implementing the service layer pattern in Django applications.

## Overview

The service layer pattern separates business logic from Django models, views, and serializers. This approach improves testability, maintainability, and code organization in medium-to-large Django projects.

## When to Use Services

| Scenario | Use Service | Why |
|----------|-------------|-----|
| CREATE/UPDATE/DELETE operations | Yes | Encapsulates write logic, enables transactions |
| Complex business rules | Yes | Keeps models clean, improves testability |
| Multiple model interactions | Yes | Orchestrates cross-model operations |
| External API calls (POST/PUT/DELETE) | Yes | Isolates side effects |
| Simple property calculation | No | Use model property |
| Simple queryset filter | No | Use manager/queryset method |
| Read-only data fetching | Maybe | Use selector pattern (see below) |

## Core Concepts

### Services vs Selectors (HackSoft Pattern)

```
services/     - Write operations (CREATE, UPDATE, DELETE)
selectors/    - Read operations (complex queries, permissions-aware fetching)
```

**Services:** Functions that modify state (database writes, external API calls).

**Selectors:** Functions that fetch data with complex logic (visibility, permissions, aggregations).

### Services vs Fat Models vs Managers

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Fat Models** | DRY, discoverable | Becomes god object, hard to test | Simple CRUD, properties |
| **Custom Managers** | Reusable querysets, chainable | Only for queries, not actions | Read operations |
| **Service Layer** | Testable, decoupled, explicit | More files, indirection | Complex business logic |

**Recommendation:** Use a pragmatic mix. Keep simple properties on models, complex queries in managers, business logic in services.

## File Organization

### Small App: Single File

```
myapp/
├── models.py
├── services.py      # All services in one file
├── selectors.py     # All selectors in one file
├── views.py
└── tests/
    ├── test_services.py
    └── test_selectors.py
```

### Large App: Services Folder

```
myapp/
├── models.py
├── services/
│   ├── __init__.py          # Re-export public functions
│   ├── user_services.py     # user_create, user_update, ...
│   ├── order_services.py    # order_create, order_cancel, ...
│   └── payment_services.py
├── selectors/
│   ├── __init__.py
│   ├── user_selectors.py
│   └── order_selectors.py
├── views.py
└── tests/
    ├── services/
    │   ├── test_user_services.py
    │   └── test_order_services.py
    └── selectors/
```

## Naming Conventions

### HackSoft Pattern: `<entity>_<action>`

```python
# services.py
def user_create(*, email: str, password: str) -> User: ...
def user_update(*, user: User, email: str) -> User: ...
def user_deactivate(*, user: User) -> User: ...

def order_create(*, user: User, items: list[Item]) -> Order: ...
def order_cancel(*, order: Order, reason: str) -> Order: ...
```

**Benefits:**
- Easy grep: `user_` finds all user-related services
- Natural grouping in module
- Clear action naming

### Alternative: Verb-First

```python
def create_user(*, email: str, password: str) -> User: ...
def activate_subscription(*, user: User, plan: Plan) -> Subscription: ...
```

Choose one convention and be consistent.

## Key Patterns

### 1. Keyword-Only Arguments

Use `*` to force keyword arguments for clarity:

```python
def user_create(
    *,  # Forces all args to be keyword-only
    email: str,
    password: str,
    is_active: bool = True,
) -> User:
    ...
```

### 2. Type Hints Everywhere

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.orders.models import Order
```

### 3. Transaction Management

```python
from django.db import transaction

@transaction.atomic
def order_create(*, user: User, items: list[Item]) -> Order:
    order = Order.objects.create(user=user, status='pending')
    for item in items:
        OrderItem.objects.create(order=order, item=item)
    inventory_deduct(items=items)  # Also wrapped in transaction
    return order
```

### 4. Input Validation

Validate at service entry point, not in models:

```python
from dataclasses import dataclass
from pydantic import BaseModel, EmailStr

# Option A: Pydantic
class UserCreateInput(BaseModel):
    email: EmailStr
    password: str

# Option B: Dataclass
@dataclass(frozen=True)
class UserCreateInput:
    email: str
    password: str
```

### 5. Error Handling

```python
# exceptions.py
class ServiceError(Exception):
    """Base exception for service layer."""
    pass

class ValidationError(ServiceError):
    pass

class BusinessRuleError(ServiceError):
    pass

class ExternalServiceError(ServiceError):
    pass
```

## LLM Usage Tips

### Prompt Engineering

When asking LLM to generate services:

1. **Specify the pattern:** "Use HackSoft-style services with `entity_action` naming"
2. **Request type hints:** "Include full type hints with TYPE_CHECKING pattern"
3. **Ask for tests:** "Generate pytest tests with Factory Boy factories"
4. **Mention transactions:** "Wrap mutating operations in @transaction.atomic"

### Code Review Checklist for LLM

Ask the LLM to verify:
- [ ] All write operations in services (not views/serializers)
- [ ] Keyword-only arguments for clarity
- [ ] Proper transaction boundaries
- [ ] Error handling with custom exceptions
- [ ] No N+1 queries in selectors
- [ ] Test coverage for happy path and edge cases

### Context to Provide

When working with existing codebase, provide LLM:
- Existing model definitions
- Current exception hierarchy
- Project conventions (from CLAUDE.md)
- Related service examples

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## External Resources

### Official Documentation

- [Django Database Transactions](https://docs.djangoproject.com/en/5.0/topics/db/transactions/)
- [Django Custom Managers](https://docs.djangoproject.com/en/5.0/topics/db/managers/)
- [Django QuerySet API](https://docs.djangoproject.com/en/5.0/ref/models/querysets/)

### Community Resources

- [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide) - Comprehensive service/selector pattern
- [HackSoft Example Project](https://github.com/HackSoftware/Django-Styleguide-Example) - Reference implementation
- [Django Service Layer Pattern (DabApps)](https://www.dabapps.com/insights/django-models-and-encapsulation/) - Service layer architecture
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) - General Django best practices

### Testing Resources

- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [HackSoft: Fakes and Factories](https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories)

### Dependency Injection

- [python-dependency-injector](https://python-dependency-injector.ets-labs.org/) - DI framework with Django support
- [django-injector](https://github.com/blubber/django_injector) - Django-specific DI
- [Wireup](https://forum.djangoproject.com/t/show-wireup-modern-dependency-injection-for-django/31535) - Modern DI for Django

## Related Methodologies

- [django-models/](../django-models/) - Model design patterns
- [django-pytest.md](../django-pytest.md) - Testing Django with pytest
- [django-api.md](../django-api.md) - API design patterns
- [python-type-hints.md](../python-type-hints.md) - Type annotations

---

*Part of the faion-python-developer skill. Last updated: 2026-01.*
