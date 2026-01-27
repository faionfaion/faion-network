# Django Code Templates

> Copy-paste templates for common Django patterns. LLM-optimized.

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Models](#models)
3. [Services](#services)
4. [Selectors](#selectors)
5. [APIs/Views](#apisviews)
6. [Serializers](#serializers)
7. [Constants](#constants)
8. [Tests](#tests)
9. [Configuration](#configuration)

---

## Project Setup

### App Structure

```bash
# Create new app with proper structure
python manage.py startapp {app_name}

# Then organize as:
apps/{app_name}/
├── __init__.py
├── apps.py
├── constants.py        # Create manually
├── models.py
├── services.py         # Create manually
├── selectors.py        # Create manually
├── apis.py             # Rename from views.py
├── serializers.py      # Create manually
├── urls.py             # Create manually
├── admin.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    ├── test_selectors.py
    └── test_apis.py
```

### pyproject.toml

```toml
[project]
name = "myproject"
version = "1.0.0"
requires-python = ">=3.12"

[tool.black]
line-length = 88
target-version = ['py312']
exclude = '''
/(
    \.git
    | \.venv
    | migrations
)/
'''

[tool.isort]
profile = "django"
line_length = 88
known_first_party = ["apps", "core", "config"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "DJANGO", "FIRSTPARTY", "LOCALFOLDER"]
known_django = ["django", "rest_framework"]

[tool.mypy]
python_version = "3.12"
plugins = ["mypy_django_plugin.main"]
strict = true
ignore_missing_imports = true

[tool.django-stubs]
django_settings_module = "config.settings.development"

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = "test_*.py"
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["apps"]
omit = ["*/migrations/*", "*/tests/*"]
```

---

## Models

### Base Model

```python
# core/models.py
from __future__ import annotations

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model with timestamps.

    All models should inherit from this.
    """

    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.now,
        editable=False,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### Domain Model

```python
# apps/{app_name}/models.py
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel
from .constants import {EntityStatus}

if TYPE_CHECKING:
    from apps.users.models import User


class {Entity}(BaseModel):
    """
    {Brief description of what this entity represents.}

    Attributes:
        user: The user who owns this entity
        status: Current lifecycle status
        {field}: {description}
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="{entities}",
        help_text="Owner of this {entity}",
    )
    status = models.CharField(
        max_length=20,
        choices={EntityStatus}.choices,
        default={EntityStatus}.{DEFAULT},
        db_index=True,
    )
    name = models.CharField(
        max_length=255,
        help_text="{Entity} display name",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Detailed description",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "{Entity}"
        verbose_name_plural = "{Entities}"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "is_active"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gte=0),
                name="{entity}_amount_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} (#{self.id})"

    def clean(self) -> None:
        """Validate model state."""
        super().clean()

        if self.status == {EntityStatus}.COMPLETED and not self.is_active:
            raise ValidationError({
                "status": "Completed {entities} must be active",
            })

    @property
    def is_editable(self) -> bool:
        """Check if entity can be modified."""
        return self.status in [
            {EntityStatus}.DRAFT,
            {EntityStatus}.PENDING,
        ]
```

### Model with Related Items

```python
# apps/orders/models.py
class Order(BaseModel):
    """Customer order."""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
    )
    shipping_address = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.id}"

    def calculate_total(self) -> Decimal:
        """Recalculate order total from items."""
        total = sum(
            item.unit_price * item.quantity
            for item in self.items.all()
        )
        self.total = total
        self.save(update_fields=["total", "updated_at"])
        return total


class OrderItem(BaseModel):
    """Line item in an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.product.name} x{self.quantity}"

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity
```

---

## Services

### Service Module

```python
# apps/{app_name}/services.py
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction
from django.utils import timezone

from core.exceptions import ValidationError, NotFoundError
from .models import {Entity}
from .constants import {EntityStatus}

if TYPE_CHECKING:
    from apps.users.models import User


def {entity}_create(
    *,
    user: User,
    name: str,
    description: str = "",
    amount: Decimal | None = None,
) -> {Entity}:
    """
    Create a new {entity}.

    Args:
        user: The user creating the {entity}
        name: Display name
        description: Optional detailed description
        amount: Optional monetary amount

    Returns:
        Created {Entity} instance

    Raises:
        ValidationError: If validation fails
    """
    {entity} = {Entity}(
        user=user,
        name=name,
        description=description,
        status={EntityStatus}.DRAFT,
    )

    if amount is not None:
        {entity}.amount = amount

    {entity}.full_clean()
    {entity}.save()

    return {entity}


def {entity}_update(
    *,
    {entity}: {Entity},
    name: str | None = None,
    description: str | None = None,
    amount: Decimal | None = None,
) -> {Entity}:
    """
    Update {entity} fields.

    Args:
        {entity}: The {entity} to update
        name: New name (optional)
        description: New description (optional)
        amount: New amount (optional)

    Returns:
        Updated {Entity} instance

    Raises:
        ValidationError: If {entity} is not editable
    """
    if not {entity}.is_editable:
        raise ValidationError(
            f"{Entity} in status {{{entity}.status}} cannot be edited"
        )

    fields_to_update: list[str] = []

    if name is not None:
        {entity}.name = name
        fields_to_update.append("name")

    if description is not None:
        {entity}.description = description
        fields_to_update.append("description")

    if amount is not None:
        {entity}.amount = amount
        fields_to_update.append("amount")

    if fields_to_update:
        {entity}.full_clean()
        {entity}.save(update_fields=[*fields_to_update, "updated_at"])

    return {entity}


def {entity}_submit(*, {entity}: {Entity}) -> {Entity}:
    """
    Submit {entity} for processing.

    Args:
        {entity}: The {entity} to submit

    Returns:
        Submitted {Entity} instance

    Raises:
        ValidationError: If {entity} cannot be submitted
    """
    if {entity}.status != {EntityStatus}.DRAFT:
        raise ValidationError(
            f"Only draft {entities} can be submitted"
        )

    {entity}.status = {EntityStatus}.PENDING
    {entity}.save(update_fields=["status", "updated_at"])

    # Queue background task
    from config.tasks import process_{entity}
    process_{entity}.enqueue({entity}_id={entity}.id)

    return {entity}


def {entity}_cancel(
    *,
    {entity}: {Entity},
    reason: str,
) -> {Entity}:
    """
    Cancel {entity}.

    Args:
        {entity}: The {entity} to cancel
        reason: Cancellation reason

    Returns:
        Cancelled {Entity} instance

    Raises:
        ValidationError: If {entity} cannot be cancelled
    """
    if {entity}.status in [{EntityStatus}.COMPLETED, {EntityStatus}.CANCELLED]:
        raise ValidationError(
            f"{Entity} in status {{{entity}.status}} cannot be cancelled"
        )

    with transaction.atomic():
        {entity}.status = {EntityStatus}.CANCELLED
        {entity}.is_active = False
        {entity}.save(update_fields=["status", "is_active", "updated_at"])

        # Log cancellation reason
        {Entity}Log.objects.create(
            {entity}={entity},
            action="cancelled",
            details={"reason": reason},
        )

    return {entity}
```

---

## Selectors

### Selector Module

```python
# apps/{app_name}/selectors.py
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import QuerySet, Prefetch, Count, Q

from .models import {Entity}
from .constants import {EntityStatus}

if TYPE_CHECKING:
    from apps.users.models import User


def {entity}_list(
    *,
    user: User | None = None,
    status: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
) -> QuerySet[{Entity}]:
    """
    List {entities} with optional filters.

    Args:
        user: Filter by owner
        status: Filter by status
        is_active: Filter by active state
        search: Search in name and description

    Returns:
        Filtered and optimized QuerySet
    """
    queryset = {Entity}.objects.select_related("user")

    if user is not None:
        queryset = queryset.filter(user=user)

    if status is not None:
        queryset = queryset.filter(status=status)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    return queryset.order_by("-created_at")


def {entity}_list_with_stats(
    *,
    user: User,
) -> QuerySet[{Entity}]:
    """
    List {entities} with aggregated statistics.

    Args:
        user: Filter by owner

    Returns:
        QuerySet with annotated counts
    """
    return (
        {Entity}.objects
        .filter(user=user)
        .annotate(
            items_count=Count("items"),
            active_items_count=Count("items", filter=Q(items__is_active=True)),
        )
        .select_related("user")
        .order_by("-created_at")
    )


def {entity}_get_by_id(
    *,
    {entity}_id: int,
    user: User | None = None,
) -> {Entity}:
    """
    Get single {entity} by ID.

    Args:
        {entity}_id: The primary key
        user: Optional ownership filter

    Returns:
        {Entity} instance

    Raises:
        {Entity}.DoesNotExist: If not found
    """
    queryset = {Entity}.objects.select_related("user").prefetch_related(
        Prefetch(
            "items",
            queryset={EntityItem}.objects.select_related("product"),
        )
    )

    if user is not None:
        queryset = queryset.filter(user=user)

    return queryset.get(id={entity}_id)


def {entity}_exists(
    *,
    user: User,
    name: str,
    exclude_id: int | None = None,
) -> bool:
    """
    Check if {entity} with name exists for user.

    Args:
        user: The owner
        name: Name to check
        exclude_id: ID to exclude (for updates)

    Returns:
        True if exists, False otherwise
    """
    queryset = {Entity}.objects.filter(user=user, name=name)

    if exclude_id is not None:
        queryset = queryset.exclude(id=exclude_id)

    return queryset.exists()
```

---

## APIs/Views

### API Module

```python
# apps/{app_name}/apis.py
from __future__ import annotations

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from . import services
from . import selectors
from .serializers import (
    {Entity}CreateRequest,
    {Entity}UpdateRequest,
    {Entity}Response,
    {Entity}ListResponse,
)


class {Entity}ListCreateAPI(APIView):
    """
    List and create {entities}.

    GET: List user's {entities}
    POST: Create new {entity}
    """

    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 20
        max_limit = 100

    def get(self, request):
        {entities} = selectors.{entity}_list(
            user=request.user,
            status=request.query_params.get("status"),
            is_active=request.query_params.get("is_active"),
            search=request.query_params.get("search"),
        )

        paginator = self.Pagination()
        page = paginator.paginate_queryset({entities}, request)

        return paginator.get_paginated_response(
            {Entity}ListResponse(page, many=True).data
        )

    def post(self, request):
        serializer = {Entity}CreateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        {entity} = services.{entity}_create(
            user=request.user,
            **serializer.validated_data,
        )

        return Response(
            {Entity}Response({entity}).data,
            status=status.HTTP_201_CREATED,
        )


class {Entity}DetailAPI(APIView):
    """
    Retrieve, update, and delete {entity}.

    GET: Get {entity} details
    PATCH: Update {entity}
    DELETE: Cancel {entity}
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, {entity}_id: int):
        {entity} = selectors.{entity}_get_by_id(
            {entity}_id={entity}_id,
            user=request.user,
        )

        return Response({Entity}Response({entity}).data)

    def patch(self, request, {entity}_id: int):
        {entity} = selectors.{entity}_get_by_id(
            {entity}_id={entity}_id,
            user=request.user,
        )

        serializer = {Entity}UpdateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        {entity} = services.{entity}_update(
            {entity}={entity},
            **serializer.validated_data,
        )

        return Response({Entity}Response({entity}).data)

    def delete(self, request, {entity}_id: int):
        {entity} = selectors.{entity}_get_by_id(
            {entity}_id={entity}_id,
            user=request.user,
        )

        services.{entity}_cancel(
            {entity}={entity},
            reason="Cancelled by user",
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class {Entity}SubmitAPI(APIView):
    """Submit {entity} for processing."""

    permission_classes = [IsAuthenticated]

    def post(self, request, {entity}_id: int):
        {entity} = selectors.{entity}_get_by_id(
            {entity}_id={entity}_id,
            user=request.user,
        )

        {entity} = services.{entity}_submit({entity}={entity})

        return Response({Entity}Response({entity}).data)
```

### URL Configuration

```python
# apps/{app_name}/urls.py
from django.urls import path

from . import apis

app_name = "{app_name}"

urlpatterns = [
    path(
        "",
        apis.{Entity}ListCreateAPI.as_view(),
        name="{entity}-list",
    ),
    path(
        "<int:{entity}_id>/",
        apis.{Entity}DetailAPI.as_view(),
        name="{entity}-detail",
    ),
    path(
        "<int:{entity}_id>/submit/",
        apis.{Entity}SubmitAPI.as_view(),
        name="{entity}-submit",
    ),
]
```

---

## Serializers

### Serializer Module

```python
# apps/{app_name}/serializers.py
from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from .constants import {EntityStatus}


class {Entity}CreateRequest(serializers.Serializer):
    """Input serializer for {entity} creation."""

    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=Decimal("0"),
    )


class {Entity}UpdateRequest(serializers.Serializer):
    """Input serializer for {entity} updates."""

    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=Decimal("0"),
    )


class {Entity}Response(serializers.Serializer):
    """Output serializer for single {entity}."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    status_display = serializers.CharField(source="get_status_display")
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_active = serializers.BooleanField()
    is_editable = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class {Entity}ListResponse(serializers.Serializer):
    """Output serializer for {entity} list (minimal fields)."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class {Entity}WithItemsResponse({Entity}Response):
    """Output serializer for {entity} with nested items."""

    items = serializers.SerializerMethodField()

    def get_items(self, obj) -> list[dict]:
        from .models import {EntityItem}

        items = obj.items.all()
        return {EntityItem}Response(items, many=True).data


class {EntityItem}Response(serializers.Serializer):
    """Output serializer for {entity} item."""

    id = serializers.IntegerField()
    product_id = serializers.IntegerField(source="product.id")
    product_name = serializers.CharField(source="product.name")
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2)
```

---

## Constants

### Constants Module

```python
# apps/{app_name}/constants.py
from django.db import models


class {EntityStatus}(models.TextChoices):
    """
    {Entity} lifecycle states.

    Flow: DRAFT -> PENDING -> PROCESSING -> COMPLETED
                          |-> CANCELLED
    """

    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class {EntityType}(models.TextChoices):
    """{Entity} types."""

    TYPE_A = "type_a", "Type A"
    TYPE_B = "type_b", "Type B"
    TYPE_C = "type_c", "Type C"


# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Business limits
MAX_{ENTITIES}_PER_USER = 100
MAX_ITEMS_PER_{ENTITY} = 50

# Validation
{ENTITY}_NAME_MAX_LENGTH = 255
{ENTITY}_DESCRIPTION_MAX_LENGTH = 5000
```

---

## Tests

### Test Models

```python
# apps/{app_name}/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError

from apps.{app_name}.models import {Entity}
from apps.{app_name}.constants import {EntityStatus}
from tests.factories import {Entity}Factory, UserFactory


class Test{Entity}Model:
    """Tests for {Entity} model."""

    def test_str_representation(self, db):
        """{Entity} string shows name and ID."""
        {entity} = {Entity}Factory(name="Test Item")

        assert str({entity}) == f"Test Item (#{{{entity}.id}})"

    def test_default_status_is_draft(self, db):
        """New {entity} has draft status."""
        {entity} = {Entity}Factory()

        assert {entity}.status == {EntityStatus}.DRAFT

    def test_is_editable_for_draft(self, db):
        """Draft {entity} is editable."""
        {entity} = {Entity}Factory(status={EntityStatus}.DRAFT)

        assert {entity}.is_editable is True

    def test_is_not_editable_for_completed(self, db):
        """Completed {entity} is not editable."""
        {entity} = {Entity}Factory(status={EntityStatus}.COMPLETED)

        assert {entity}.is_editable is False

    def test_clean_validates_completed_must_be_active(self, db):
        """Completed {entity} must be active."""
        {entity} = {Entity}Factory.build(
            status={EntityStatus}.COMPLETED,
            is_active=False,
        )

        with pytest.raises(ValidationError) as exc_info:
            {entity}.full_clean()

        assert "must be active" in str(exc_info.value)
```

### Test Services

```python
# apps/{app_name}/tests/test_services.py
import pytest
from decimal import Decimal

from apps.{app_name} import services
from apps.{app_name}.constants import {EntityStatus}
from core.exceptions import ValidationError
from tests.factories import {Entity}Factory, UserFactory


class Test{Entity}Create:
    """Tests for {entity}_create service."""

    def test_creates_{entity}_with_valid_data(self, db):
        """{Entity} is created when valid data provided."""
        user = UserFactory()

        {entity} = services.{entity}_create(
            user=user,
            name="Test {Entity}",
            description="Test description",
            amount=Decimal("99.99"),
        )

        assert {entity}.id is not None
        assert {entity}.user == user
        assert {entity}.name == "Test {Entity}"
        assert {entity}.description == "Test description"
        assert {entity}.amount == Decimal("99.99")
        assert {entity}.status == {EntityStatus}.DRAFT

    def test_creates_{entity}_with_minimal_data(self, db):
        """{Entity} created with only required fields."""
        user = UserFactory()

        {entity} = services.{entity}_create(
            user=user,
            name="Minimal",
        )

        assert {entity}.id is not None
        assert {entity}.description == ""


class Test{Entity}Update:
    """Tests for {entity}_update service."""

    def test_updates_single_field(self, db):
        """Single field update works correctly."""
        {entity} = {Entity}Factory(name="Original")

        updated = services.{entity}_update(
            {entity}={entity},
            name="Updated",
        )

        assert updated.name == "Updated"

    def test_raises_error_for_non_editable(self, db):
        """Cannot update completed {entity}."""
        {entity} = {Entity}Factory(status={EntityStatus}.COMPLETED)

        with pytest.raises(ValidationError) as exc_info:
            services.{entity}_update(
                {entity}={entity},
                name="New Name",
            )

        assert "cannot be edited" in str(exc_info.value)


class Test{Entity}Submit:
    """Tests for {entity}_submit service."""

    def test_submits_draft_{entity}(self, db):
        """Draft {entity} can be submitted."""
        {entity} = {Entity}Factory(status={EntityStatus}.DRAFT)

        submitted = services.{entity}_submit({entity}={entity})

        assert submitted.status == {EntityStatus}.PENDING

    def test_raises_error_for_non_draft(self, db):
        """Cannot submit non-draft {entity}."""
        {entity} = {Entity}Factory(status={EntityStatus}.PENDING)

        with pytest.raises(ValidationError) as exc_info:
            services.{entity}_submit({entity}={entity})

        assert "Only draft" in str(exc_info.value)
```

### Test Selectors

```python
# apps/{app_name}/tests/test_selectors.py
import pytest

from apps.{app_name} import selectors
from apps.{app_name}.constants import {EntityStatus}
from tests.factories import {Entity}Factory, UserFactory


class Test{Entity}List:
    """Tests for {entity}_list selector."""

    def test_returns_only_user_{entities}(self, db):
        """Selector returns only {entities} for specified user."""
        user = UserFactory()
        other_user = UserFactory()

        user_{entity} = {Entity}Factory(user=user)
        {Entity}Factory(user=other_user)

        result = selectors.{entity}_list(user=user)

        assert list(result) == [user_{entity}]

    def test_filters_by_status(self, db):
        """Selector filters by status correctly."""
        user = UserFactory()
        pending = {Entity}Factory(user=user, status={EntityStatus}.PENDING)
        {Entity}Factory(user=user, status={EntityStatus}.DRAFT)

        result = selectors.{entity}_list(
            user=user,
            status={EntityStatus}.PENDING,
        )

        assert list(result) == [pending]

    def test_search_in_name_and_description(self, db):
        """Selector searches in name and description."""
        user = UserFactory()
        match_name = {Entity}Factory(user=user, name="Test Item")
        match_desc = {Entity}Factory(user=user, description="Test description")
        {Entity}Factory(user=user, name="Other")

        result = selectors.{entity}_list(user=user, search="test")

        assert set(result) == {match_name, match_desc}


class Test{Entity}GetById:
    """Tests for {entity}_get_by_id selector."""

    def test_returns_{entity}_by_id(self, db):
        """Selector returns correct {entity}."""
        {entity} = {Entity}Factory()

        result = selectors.{entity}_get_by_id({entity}_id={entity}.id)

        assert result == {entity}

    def test_raises_for_nonexistent(self, db):
        """Selector raises DoesNotExist for invalid ID."""
        with pytest.raises({Entity}.DoesNotExist):
            selectors.{entity}_get_by_id({entity}_id=99999)

    def test_filters_by_user(self, db):
        """Selector filters by user when provided."""
        {entity} = {Entity}Factory()
        other_user = UserFactory()

        with pytest.raises({Entity}.DoesNotExist):
            selectors.{entity}_get_by_id(
                {entity}_id={entity}.id,
                user=other_user,
            )
```

### Test APIs

```python
# apps/{app_name}/tests/test_apis.py
import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status

from apps.{app_name}.constants import {EntityStatus}
from tests.factories import {Entity}Factory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client


class Test{Entity}ListCreateAPI:
    """Tests for {entity} list/create endpoint."""

    def test_list_requires_authentication(self, api_client, db):
        """Unauthenticated request returns 401."""
        response = api_client.get("/api/{entities}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_returns_user_{entities}(self, authenticated_client, db):
        """List returns only authenticated user's {entities}."""
        {Entity}Factory(user=authenticated_client.user)
        {Entity}Factory()  # Other user's {entity}

        response = authenticated_client.get("/api/{entities}/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_create_{entity}_success(self, authenticated_client, db):
        """Create {entity} with valid data."""
        data = {
            "name": "New {Entity}",
            "description": "Test description",
            "amount": "99.99",
        }

        response = authenticated_client.post("/api/{entities}/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New {Entity}"
        assert response.data["status"] == {EntityStatus}.DRAFT

    def test_create_validates_required_fields(self, authenticated_client, db):
        """Create fails without required fields."""
        response = authenticated_client.post("/api/{entities}/", {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data


class Test{Entity}DetailAPI:
    """Tests for {entity} detail endpoint."""

    def test_get_{entity}_detail(self, authenticated_client, db):
        """Get single {entity} returns full data."""
        {entity} = {Entity}Factory(user=authenticated_client.user)

        response = authenticated_client.get(f"/api/{entities}/{{{entity}.id}}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == {entity}.id

    def test_get_other_user_{entity}_returns_404(self, authenticated_client, db):
        """Cannot access other user's {entity}."""
        {entity} = {Entity}Factory()  # Other user's

        response = authenticated_client.get(f"/api/{entities}/{{{entity}.id}}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_{entity}(self, authenticated_client, db):
        """Update {entity} with valid data."""
        {entity} = {Entity}Factory(
            user=authenticated_client.user,
            status={EntityStatus}.DRAFT,
        )

        response = authenticated_client.patch(
            f"/api/{entities}/{{{entity}.id}}/",
            {"name": "Updated Name"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Name"

    def test_delete_{entity}(self, authenticated_client, db):
        """Delete cancels the {entity}."""
        {entity} = {Entity}Factory(
            user=authenticated_client.user,
            status={EntityStatus}.DRAFT,
        )

        response = authenticated_client.delete(f"/api/{entities}/{{{entity}.id}}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        {entity}.refresh_from_db()
        assert {entity}.status == {EntityStatus}.CANCELLED
```

### Test Factories

```python
# tests/factories/{app_name}.py
import factory
from factory.django import DjangoModelFactory
from decimal import Decimal

from apps.{app_name}.models import {Entity}, {EntityItem}
from apps.{app_name}.constants import {EntityStatus}


class {Entity}Factory(DjangoModelFactory):
    """Factory for {Entity} model."""

    class Meta:
        model = {Entity}

    user = factory.SubFactory("tests.factories.users.UserFactory")
    name = factory.Sequence(lambda n: f"{Entity} {n}")
    description = factory.Faker("paragraph")
    status = {EntityStatus}.DRAFT
    amount = factory.LazyFunction(
        lambda: Decimal(factory.Faker("pydecimal", left_digits=3, right_digits=2).generate())
    )
    is_active = True


class {EntityItem}Factory(DjangoModelFactory):
    """Factory for {EntityItem} model."""

    class Meta:
        model = {EntityItem}

    {entity} = factory.SubFactory({Entity}Factory)
    product = factory.SubFactory("tests.factories.products.ProductFactory")
    quantity = factory.Faker("random_int", min=1, max=10)
    unit_price = factory.LazyAttribute(lambda obj: obj.product.price)
```

---

## Configuration

### Settings Base

```python
# config/settings/base.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Apps
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
]

LOCAL_APPS = [
    "core",
    "apps.users",
    "apps.{app_name}",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "core.exception_handlers.custom_exception_handler",
}
```

### Exception Handler

```python
# core/exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from core.exceptions import (
    ApplicationError,
    NotFoundError,
    ValidationError,
    PermissionDeniedError,
)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses.

    Format: {"error": "message", "code": "error_code", "extra": {...}}
    """
    response = exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, NotFoundError):
        return Response(
            {
                "error": exc.message,
                "code": "not_found",
                "extra": exc.extra,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, ValidationError):
        return Response(
            {
                "error": exc.message,
                "code": "validation_error",
                "extra": exc.extra,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, PermissionDeniedError):
        return Response(
            {
                "error": exc.message,
                "code": "permission_denied",
                "extra": exc.extra,
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    if isinstance(exc, ApplicationError):
        return Response(
            {
                "error": exc.message,
                "code": "application_error",
                "extra": exc.extra,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return None
```
