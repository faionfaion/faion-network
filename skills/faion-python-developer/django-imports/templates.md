# Django Import Templates

Copy-paste templates for common Django import patterns and configurations.

## Ruff Configuration

### Full Django Project Configuration

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "migrations",
    "staticfiles",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "DJ",     # flake8-django
    "UP",     # pyupgrade
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # function call in default argument (DRF uses this)
    "DJ001",  # null=True on CharField (sometimes needed)
]

[tool.ruff.lint.isort]
known-first-party = ["apps", "config"]
known-third-party = ["django", "rest_framework", "celery"]
section-order = [
    "future",
    "standard-library",
    "third-party",
    "first-party",
    "local-folder",
]
force-single-line = false
combine-as-imports = true
split-on-trailing-comma = true

[tool.ruff.lint.per-file-ignores]
"*/migrations/*" = ["E501", "DJ"]
"*/tests/*" = ["S101"]
"conftest.py" = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### Minimal Ruff Configuration

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "DJ"]

[tool.ruff.lint.isort]
known-first-party = ["apps"]
```

### isort Configuration (Standalone)

```toml
# pyproject.toml (if not using Ruff for isort)
[tool.isort]
profile = "django"
line_length = 88
known_first_party = ["apps", "config"]
known_third_party = ["django", "rest_framework", "celery"]
sections = [
    "FUTURE",
    "STDLIB",
    "THIRDPARTY",
    "FIRSTPARTY",
    "LOCALFOLDER",
]
skip = [".venv", "migrations"]
```

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Optional: mypy for type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - django-stubs
          - djangorestframework-stubs
```

## Import Block Templates

### Django View

```python
"""Views for the {app_name} app."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import MyForm
from .models import MyModel
from .serializers import MySerializer
from .services import MyService

if TYPE_CHECKING:
    from apps.users.models import User

logger = logging.getLogger(__name__)
```

### Django Model

```python
"""Models for the {app_name} app."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel

if TYPE_CHECKING:
    from apps.related_app.models import RelatedModel
```

### Django Service

```python
"""Business logic for the {app_name} app."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.apps import apps
from django.db import transaction

from .models import MyModel

if TYPE_CHECKING:
    from apps.users.models import User

logger = logging.getLogger(__name__)
```

### Django Serializer

```python
"""Serializers for the {app_name} app."""
from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import serializers

from apps.related_app import serializers as related_serializers

from .models import MyModel

if TYPE_CHECKING:
    from apps.users.models import User
```

### Django Admin

```python
"""Admin configuration for the {app_name} app."""
from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html

from .models import MyModel, RelatedModel
```

### Django Forms

```python
"""Forms for the {app_name} app."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.core.exceptions import ValidationError

from .models import MyModel

if TYPE_CHECKING:
    from apps.users.models import User
```

### Django Signals/Receivers

```python
"""Signal receivers for the {app_name} app."""
from __future__ import annotations

import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import MyModel

logger = logging.getLogger(__name__)


@receiver(post_save, sender=MyModel)
def handle_mymodel_save(sender, instance, created, **kwargs):
    """Handle MyModel save signal."""
    if created:
        logger.info("Created new MyModel: %s", instance.pk)
```

### Django AppConfig

```python
"""App configuration for the {app_name} app."""
from __future__ import annotations

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    """Configuration for myapp."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.myapp"
    verbose_name = "My Application"

    def ready(self):
        """Import signal receivers when app is ready."""
        from . import receivers  # noqa: F401
```

### Celery Task

```python
"""Celery tasks for the {app_name} app."""
from __future__ import annotations

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_something(self, item_id: int) -> None:
    """Process an item asynchronously."""
    # Lazy imports for better task startup time
    from .models import MyModel
    from .services import MyService

    try:
        item = MyModel.objects.get(pk=item_id)
        MyService.process(item)
    except MyModel.DoesNotExist:
        logger.warning("Item %s not found", item_id)
    except Exception as exc:
        logger.exception("Error processing item %s", item_id)
        raise self.retry(exc=exc, countdown=60)
```

### Django Test

```python
"""Tests for the {app_name} app."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.factories import UserFactory

from .factories import MyModelFactory
from .models import MyModel

if TYPE_CHECKING:
    from apps.users.models import User


pytestmark = pytest.mark.django_db
```

### Django Management Command

```python
"""Management command for {description}."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.core.management.base import BaseCommand, CommandError

if TYPE_CHECKING:
    from argparse import ArgumentParser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command to do something."""

    help = "Description of what this command does"

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run without making changes",
        )

    def handle(self, *args, **options) -> None:
        """Execute the command."""
        from .models import MyModel  # Lazy import
        from .services import MyService

        dry_run = options["dry_run"]

        self.stdout.write("Starting command...")

        try:
            count = MyService.run_batch(dry_run=dry_run)
            self.stdout.write(
                self.style.SUCCESS(f"Processed {count} items")
            )
        except Exception as e:
            raise CommandError(f"Command failed: {e}")
```

## TYPE_CHECKING Templates

### Basic TYPE_CHECKING

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.orders.models import Order


def process(user: User, order: Order) -> None:
    """Process user order."""
    pass
```

### TYPE_CHECKING with Protocol

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from apps.payments.models import Payment


class PaymentProcessor(Protocol):
    """Protocol for payment processors."""

    def charge(self, amount: int) -> Payment:
        """Charge the given amount."""
        ...

    def refund(self, payment: Payment) -> None:
        """Refund a payment."""
        ...
```

### TYPE_CHECKING with TypeVar

```python
from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from django.db.models import Model

T = TypeVar("T", bound="Model")


def get_or_none(model_class: type[T], **kwargs) -> T | None:
    """Get model instance or None."""
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        return None
```

## Cross-App Import Template

```python
"""Using models and services from other apps."""
from __future__ import annotations

from typing import TYPE_CHECKING

# Cross-app imports with aliases
from apps.catalog import models as catalog_models
from apps.catalog import selectors as catalog_selectors
from apps.catalog import services as catalog_services
from apps.users import models as user_models
from apps.users import services as user_services

# Local imports
from .models import Order

if TYPE_CHECKING:
    from apps.payments.models import Payment


def create_order_for_product(
    user: user_models.User,
    product: catalog_models.Product,
) -> Order:
    """Create order for a product."""
    return Order.objects.create(
        user=user,
        product=product,
        total=product.price,
    )
```

## apps.get_model() Template

```python
"""Dynamic model loading with apps.get_model()."""
from __future__ import annotations

from django.apps import apps


def get_user_by_email(email: str):
    """Get user by email using dynamic model loading."""
    User = apps.get_model("users", "User")
    return User.objects.filter(email=email).first()


def create_notification(user_id: int, message: str):
    """Create notification using dynamic model loading."""
    User = apps.get_model("users", "User")
    Notification = apps.get_model("notifications", "Notification")

    user = User.objects.get(pk=user_id)
    return Notification.objects.create(user=user, message=message)
```
