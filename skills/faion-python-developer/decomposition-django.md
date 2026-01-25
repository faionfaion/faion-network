# Django Decomposition Patterns

LLM-friendly code organization for Django projects.

---

## Anti-Pattern: Fat Models & Views

```python
# BAD: models.py (800+ lines)
class User(models.Model):
    # 50 fields
    # 30 methods
    # Business logic mixed with ORM
    # Validation mixed with data
    # Notifications inside model
    pass

# BAD: views.py (1000+ lines)
class UserViewSet(viewsets.ModelViewSet):
    # All CRUD + custom actions
    # Permission checks inline
    # Serialization logic
    # Email sending
    # PDF generation
    pass
```

---

## LLM-Friendly Structure

```
users/
├── __init__.py
├── models/
│   ├── __init__.py           # from .user import User
│   ├── user.py               # User model (50-80 lines)
│   └── profile.py            # Profile model (40-60 lines)
├── services/
│   ├── __init__.py
│   ├── user_service.py       # CRUD operations (80-120 lines)
│   ├── auth_service.py       # Auth logic (60-100 lines)
│   └── notification_service.py  # Emails, SMS (50-80 lines)
├── selectors/
│   ├── __init__.py
│   └── user_selectors.py     # Query methods (40-60 lines)
├── serializers/
│   ├── __init__.py
│   ├── user_serializers.py   # API serializers (60-80 lines)
│   └── auth_serializers.py   # Auth serializers (40-60 lines)
├── views/
│   ├── __init__.py
│   ├── user_views.py         # User endpoints (60-80 lines)
│   └── auth_views.py         # Auth endpoints (60-80 lines)
├── permissions.py            # Permission classes (30-50 lines)
├── signals.py                # Signal handlers (30-50 lines)
├── admin.py                  # Admin config (40-60 lines)
├── urls.py                   # URL routing (20-30 lines)
└── tests/
    ├── __init__.py
    ├── test_models.py        # Model tests (80-120 lines)
    ├── test_services.py      # Service tests (100-150 lines)
    ├── test_views.py         # API tests (100-150 lines)
    └── factories.py          # Test factories (40-60 lines)
```

---

## Service Layer Pattern

### Service Definition

```python
# users/services/user_service.py (~100 lines)
from dataclasses import dataclass
from typing import Optional
from django.db import transaction

from users.models import User
from users.selectors import user_selectors


@dataclass
class UserCreateInput:
    email: str
    name: str
    password: str


@dataclass
class UserUpdateInput:
    name: Optional[str] = None
    avatar: Optional[str] = None


class UserService:
    @staticmethod
    @transaction.atomic
    def create(data: UserCreateInput) -> User:
        """Create new user with validation."""
        if user_selectors.email_exists(data.email):
            raise ValueError("Email already exists")

        user = User.objects.create_user(
            email=data.email,
            name=data.name,
            password=data.password,
        )
        return user

    @staticmethod
    @transaction.atomic
    def update(user: User, data: UserUpdateInput) -> User:
        """Update user fields."""
        if data.name is not None:
            user.name = data.name
        if data.avatar is not None:
            user.avatar = data.avatar
        user.save()
        return user

    @staticmethod
    def delete(user: User) -> None:
        """Soft delete user."""
        user.is_active = False
        user.save()
```

### Selector Pattern

```python
# users/selectors/user_selectors.py (~60 lines)
from django.db.models import QuerySet
from users.models import User


def get_active_users() -> QuerySet[User]:
    """Get all active users."""
    return User.objects.filter(is_active=True)


def get_by_email(email: str) -> User | None:
    """Find user by email."""
    return User.objects.filter(email=email).first()


def email_exists(email: str) -> bool:
    """Check if email is taken."""
    return User.objects.filter(email=email).exists()


def search(query: str) -> QuerySet[User]:
    """Search users by name or email."""
    return User.objects.filter(
        Q(name__icontains=query) | Q(email__icontains=query),
        is_active=True,
    )
```

### View Layer

```python
# users/views/user_views.py (~80 lines)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.services.user_service import UserService, UserCreateInput
from users.selectors import user_selectors
from users.serializers import UserSerializer, UserCreateSerializer
from users.permissions import IsOwnerOrAdmin


class UserViewSet(ViewSet):
    permission_classes = [IsOwnerOrAdmin]

    def list(self, request):
        users = user_selectors.get_active_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create(
            UserCreateInput(**serializer.validated_data)
        )
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        user = user_selectors.get_by_id(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
```

---

## Key Principles

1. **Service Layer** - Business logic extracted from views
2. **Selectors** - Read-only query methods
3. **Thin Models** - Only ORM-specific logic
4. **Thin Views** - Only HTTP request/response handling
5. **Dataclasses** - Explicit input/output contracts

---

## File Size Guidelines

| Type | Target | Max |
|------|--------|-----|
| Model | 50-80 | 150 |
| Service | 80-120 | 200 |
| Selector | 40-60 | 100 |
| View | 60-80 | 150 |
| Serializer | 60-80 | 120 |
| Test | 100-150 | 300 |

---

## Sources

- [Django Best Practices](https://django-best-practices.readthedocs.io/) - Community guidelines
- [Service Layer Pattern](https://www.dabapps.com/insights/django-models-and-encapsulation/) - Django architecture
- [Django Project Structure](https://realpython.com/django-project-best-practices/) - Organization patterns
- [Separation of Concerns](https://www.cosmicpython.com/) - Clean architecture book
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) - Django patterns

## Related

- [framework-decomposition-patterns.md](framework-decomposition-patterns.md) - All frameworks
- [decomposition-rails.md](decomposition-rails.md) - Ruby on Rails patterns
- [decomposition-react.md](decomposition-react.md) - React patterns
- [decomposition-laravel.md](decomposition-laravel.md) - Laravel patterns
- [django-services.md](django-services.md) - Django service layer
- [django-coding-standards.md](django-coding-standards.md) - Django standards
- [llm-friendly-architecture.md](llm-friendly-architecture.md) - LLM optimization
