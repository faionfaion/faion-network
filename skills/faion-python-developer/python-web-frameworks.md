---
name: faion-python-web-frameworks
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*, pip:*, poetry:*, django-admin:*, manage.py:*, uvicorn:*)
---

# Python Web Frameworks

**Django and FastAPI patterns for building web applications and APIs.**

---

## Purpose

Provides patterns and best practices for Django and FastAPI web development. Used by faion-code-agent for:
- Django web application development (models, views, serializers, admin)
- FastAPI REST API development (routes, dependencies, Pydantic schemas)
- Service layer patterns for business logic
- Cross-app organization

---

## Django Patterns

### Problem

Django projects need consistent architecture: models, views, serializers, services, and admin configuration.

### Framework

#### Project Structure

```
project/
|-- config/                    # Django settings
|   |-- __init__.py
|   |-- settings/
|   |   |-- __init__.py
|   |   |-- base.py           # Common settings
|   |   |-- development.py    # Dev overrides
|   |   |-- production.py     # Prod overrides
|   |-- urls.py
|   |-- wsgi.py
|   |-- asgi.py
|
|-- apps/
|   |-- users/
|   |   |-- __init__.py
|   |   |-- models.py
|   |   |-- views.py
|   |   |-- serializers.py
|   |   |-- services.py       # Business logic
|   |   |-- admin.py
|   |   |-- urls.py
|   |   |-- tests/
|   |   |   |-- __init__.py
|   |   |   |-- test_models.py
|   |   |   |-- test_views.py
|   |   |   |-- test_services.py
|   |   |-- migrations/
|
|-- manage.py
|-- pyproject.toml
```

#### Models Pattern

```python
import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserType(models.TextChoices):
    """User type choices."""
    REGULAR = 'regular', 'Regular User'
    PREMIUM = 'premium', 'Premium User'
    ADMIN = 'admin', 'Administrator'


class User(BaseModel):
    """User model."""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.REGULAR,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email
```

#### Services Pattern (Business Logic)

```python
# services.py
from django.db import transaction
from .models import User, UserType


def create_user(
    email: str,
    name: str,
    *,
    user_type: str = UserType.REGULAR,
) -> User:
    """Create a new user."""
    user = User.objects.create(
        email=email,
        name=name,
        user_type=user_type,
    )
    return user


def upgrade_to_premium(
    user: User,
    *,
    upgraded_by: User | None = None,
) -> User:
    """Upgrade user to premium."""
    user.user_type = UserType.PREMIUM
    user.save(update_fields=['user_type', 'updated_at'])
    return user


@transaction.atomic
def transfer_ownership(
    from_user: User,
    to_user: User,
    item_id: int,
) -> None:
    """Transfer item ownership between users."""
    from apps.items import models as item_models

    item = item_models.Item.objects.select_for_update().get(id=item_id)
    item.owner = to_user
    item.save(update_fields=['owner', 'updated_at'])
```

#### Views Pattern (Thin Views)

```python
# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import services
from .serializers import CreateUserRequest, UserResponse


class UserCreateView(APIView):
    """Create user endpoint."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateUserRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = services.create_user(
            email=serializer.validated_data['email'],
            name=serializer.validated_data['name'],
        )

        return Response(
            UserResponse(user).data,
            status=status.HTTP_201_CREATED,
        )
```

#### Serializers Pattern

```python
# serializers.py
from rest_framework import serializers
from .models import User


class CreateUserRequest(serializers.Serializer):
    """Request serializer for user creation."""
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)


class UserResponse(serializers.ModelSerializer):
    """Response serializer for user data."""
    class Meta:
        model = User
        fields = ['uid', 'email', 'name', 'user_type', 'created_at']
        read_only_fields = fields
```

#### Admin Pattern

```python
# admin.py
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'user_type', 'is_active', 'created_at']
    list_filter = ['user_type', 'is_active', 'created_at']
    search_fields = ['email', 'name']
    readonly_fields = ['uid', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = [
        (None, {'fields': ['email', 'name']}),
        ('Status', {'fields': ['user_type', 'is_active']}),
        ('Metadata', {'fields': ['uid', 'created_at', 'updated_at']}),
    ]
```

### Templates

**Cross-app imports:**
```python
# Always use aliases for cross-app imports
from apps.orders import models as order_models
from apps.users import services as user_services
```

### Agent

Executed by: faion-code-agent

---

## FastAPI Patterns

### Problem

FastAPI projects need consistent route organization, dependency injection, Pydantic models, and async handling.

### Framework

#### Project Structure

```
project/
|-- app/
|   |-- __init__.py
|   |-- main.py               # FastAPI app
|   |-- config.py             # Settings
|   |-- dependencies.py       # DI dependencies
|   |
|   |-- routers/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- items.py
|   |
|   |-- schemas/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- items.py
|   |
|   |-- models/
|   |   |-- __init__.py
|   |   |-- users.py
|   |
|   |-- services/
|   |   |-- __init__.py
|   |   |-- users.py
|   |
|   |-- db/
|       |-- __init__.py
|       |-- database.py
|       |-- session.py
|
|-- tests/
|-- pyproject.toml
```

#### Main Application

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import users, items
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    await init_db()
    yield


app = FastAPI(
    title="My API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### Routes with Dependencies

```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.schemas.users import UserCreate, UserResponse
from app.services import users as user_service
from app.models.users import User

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new user."""
    user = await user_service.create_user(db, user_data)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get user by ID."""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
```

#### Pydantic Schemas

```python
# schemas/users.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """User creation request."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update request."""
    name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None


class UserResponse(UserBase):
    """User response."""
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
```

#### Dependencies

```python
# dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.models.users import User
from app.services import auth as auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_db():
    """Database session dependency."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get current authenticated user."""
    user = await auth_service.get_user_from_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user


# Type alias for cleaner signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
```

#### Background Tasks

```python
# routers/notifications.py
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


def send_email(email: str, message: str) -> None:
    """Send email in background."""
    # Email sending logic
    pass


@router.post("/notify")
async def send_notification(
    email: str,
    message: str,
    background_tasks: BackgroundTasks,
):
    """Send notification email."""
    background_tasks.add_task(send_email, email, message)
    return {"status": "notification queued"}
```

### Templates

**Async service function:**
```python
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### Agent

Executed by: faion-code-agent

---

## Quick Reference

| Framework | Use Case |
|-----------|----------|
| **Django** | Full-featured web apps, admin panels, ORM |
| **FastAPI** | Modern async APIs, microservices, automatic docs |

### Django Commands

```bash
# Create project
django-admin startproject config .

# Create app
python manage.py startapp users

# Migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver

# Create superuser
python manage.py createsuperuser
```

### FastAPI Commands

```bash
# Run server
uvicorn app.main:app --reload

# With custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --workers 4
```

---

## Patterns Summary

| Pattern | Django | FastAPI |
|---------|--------|---------|
| **Request validation** | Serializers | Pydantic models |
| **Business logic** | Services | Services |
| **Database** | Django ORM | SQLAlchemy |
| **Dependency injection** | Class-based views | FastAPI Depends |
| **Admin panel** | Built-in | External (e.g., SQLAdmin) |
| **Async support** | Limited (ASGI) | Native |

---

## Sources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

*Python Web Frameworks v1.0*
*Layer 3 Technical Skill*
*2 Frameworks | Django + FastAPI Patterns*
