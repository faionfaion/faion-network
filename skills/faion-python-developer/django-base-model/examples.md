# Django Base Model Examples

Real-world implementations of base model patterns for production Django applications.

---

## Example 1: Complete Base Model with Mixins

A full-featured base model system for a SaaS application.

### File Structure

```
core/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── mixins.py
│   └── managers.py
└── utils.py
```

### core/models/managers.py

```python
"""Custom managers for base models."""
from django.db import models
from django.db.models import QuerySet


class SoftDeleteQuerySet(QuerySet):
    """QuerySet that supports soft delete operations."""

    def delete(self):
        """Soft delete all objects in queryset."""
        from django.utils import timezone
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all objects in queryset."""
        return super().delete()

    def restore(self):
        """Restore all soft-deleted objects in queryset."""
        return self.update(deleted_at=None)

    def active(self):
        """Return only non-deleted objects."""
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        """Return only deleted objects."""
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records by default."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).active()

    def with_deleted(self):
        """Include soft-deleted records."""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted_only(self):
        """Return only soft-deleted records."""
        return SoftDeleteQuerySet(self.model, using=self._db).deleted()


class AllObjectsManager(models.Manager):
    """Manager that includes all records (deleted and active)."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)
```

### core/models/mixins.py

```python
"""Reusable model mixins."""
import uuid
from django.db import models
from django.utils import timezone

from .managers import SoftDeleteManager, AllObjectsManager


class UUIDMixin(models.Model):
    """Adds UUID field for external identification."""

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="Public identifier for external use",
    )

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """Adds created_at and updated_at timestamps."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When this record was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this record was last updated",
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteMixin(models.Model):
    """Adds soft delete capability."""

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="When this record was soft deleted",
    )

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete: mark as deleted instead of removing."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete from database."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""
        return self.deleted_at is not None


class VersionMixin(models.Model):
    """Adds optimistic locking via version field."""

    version = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)
```

### core/models/base.py

```python
"""Base model classes."""
from django.db import models

from .mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin


class BaseModel(UUIDMixin, TimestampMixin, models.Model):
    """
    Standard base model with UUID and timestamps.

    Use for most domain models that need:
    - External UUID for API exposure
    - Automatic timestamp tracking
    """

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.uid})"


class SoftDeleteModel(UUIDMixin, TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Base model with soft delete support.

    Use for models where data should be recoverable:
    - User accounts
    - Important business data
    - Audit-sensitive records
    """

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        status = " [DELETED]" if self.is_deleted else ""
        return f"{self.__class__.__name__}({self.uid}){status}"
```

---

## Example 2: E-Commerce Models

Production e-commerce models using base patterns.

### apps/products/models.py

```python
"""Product models."""
from decimal import Decimal
from django.db import models
from django.db.models import F
from core.models import SoftDeleteModel


class Category(SoftDeleteModel):
    """Product category with hierarchical structure."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'product_categories'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class ProductQuerySet(models.QuerySet):
    """Custom queryset for products."""

    def active(self):
        """Return only active, in-stock products."""
        return self.filter(
            is_active=True,
            stock__gt=0,
            deleted_at__isnull=True,
        )

    def in_category(self, category):
        """Filter by category or its children."""
        categories = [category.id]
        categories.extend(
            category.children.values_list('id', flat=True)
        )
        return self.filter(category_id__in=categories)

    def price_range(self, min_price=None, max_price=None):
        """Filter by price range."""
        qs = self
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        return qs

    def with_discount(self):
        """Return products with active discount."""
        return self.filter(discount_percent__gt=0)


class ProductManager(models.Manager):
    """Custom manager for products."""

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )

    def active(self):
        return self.get_queryset().active()


class Product(SoftDeleteModel):
    """Product with pricing and inventory."""

    # Basic info
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
    )

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField(default=0)

    # Computed field (Django 5.x)
    final_price = models.GeneratedField(
        expression=F('price') * (100 - F('discount_percent')) / 100,
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
    )

    # Inventory
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)

    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)

    # Managers
    objects = ProductManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self) -> str:
        return self.name

    def reduce_stock(self, quantity: int) -> bool:
        """Reduce stock by quantity. Returns True if successful."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save(update_fields=['stock', 'updated_at'])
            return True
        return False
```

### apps/orders/models.py

```python
"""Order models with proper FK patterns."""
from decimal import Decimal
from django.db import models
from django.conf import settings
from core.models import BaseModel


class OrderStatus(models.TextChoices):
    """Order status choices."""
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'
    REFUNDED = 'refunded', 'Refunded'


class Order(BaseModel):
    """Customer order."""

    # Customer - PROTECT prevents accidental user deletion
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
    )

    # Pricing
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    # Shipping
    shipping_address = models.TextField()

    # Timestamps
    confirmed_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    # Soft reference - order survives if handler deleted
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_orders',
    )

    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self) -> str:
        return f"Order {self.uid} - {self.status}"

    def calculate_total(self):
        """Recalculate order total from items."""
        self.subtotal = sum(
            item.total for item in self.items.all()
        )
        self.total = self.subtotal + self.tax + self.shipping_cost
        self.save(update_fields=['subtotal', 'total', 'updated_at'])


class OrderItem(BaseModel):
    """Line item in an order."""

    # CASCADE - items have no meaning without order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )

    # PROTECT - preserve product info even if product deleted
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='order_items',
    )

    # Snapshot at time of purchase (prices may change)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    # Computed total
    total = models.GeneratedField(
        expression=models.F('unit_price') * models.F('quantity'),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=True,
    )

    class Meta:
        db_table = 'order_items'

    def __str__(self) -> str:
        return f"{self.product_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Snapshot product info at time of order
        if not self.product_name:
            self.product_name = self.product.name
        if not self.unit_price:
            self.unit_price = self.product.final_price
        super().save(*args, **kwargs)
```

---

## Example 3: Multi-Tenant SaaS

Complete multi-tenant implementation.

### tenants/models.py

```python
"""Tenant models."""
import uuid
from django.db import models
from core.models import BaseModel


class TenantPlan(models.TextChoices):
    """Subscription plan choices."""
    FREE = 'free', 'Free'
    STARTER = 'starter', 'Starter'
    PRO = 'pro', 'Professional'
    ENTERPRISE = 'enterprise', 'Enterprise'


class Tenant(BaseModel):
    """Organization/company in multi-tenant system."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    # Subscription
    plan = models.CharField(
        max_length=20,
        choices=TenantPlan.choices,
        default=TenantPlan.FREE,
    )
    is_active = models.BooleanField(default=True, db_index=True)

    # Limits based on plan
    max_users = models.PositiveIntegerField(default=5)
    max_projects = models.PositiveIntegerField(default=10)

    class Meta:
        db_table = 'tenants'

    def __str__(self) -> str:
        return self.name
```

### tenants/middleware.py

```python
"""Tenant middleware for multi-tenant support."""
import threading
from django.http import Http404
from .models import Tenant

_thread_locals = threading.local()


def get_current_tenant():
    """Get the current tenant from thread-local storage."""
    return getattr(_thread_locals, 'tenant', None)


def set_current_tenant(tenant):
    """Set the current tenant in thread-local storage."""
    _thread_locals.tenant = tenant


class TenantMiddleware:
    """
    Middleware to extract tenant from request.

    Supports:
    - Subdomain: acme.app.com
    - Header: X-Tenant-ID
    - URL prefix: /t/acme/
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = self._get_tenant_from_request(request)
        set_current_tenant(tenant)
        request.tenant = tenant

        response = self.get_response(request)

        # Clean up after request
        set_current_tenant(None)

        return response

    def _get_tenant_from_request(self, request):
        """Extract tenant from subdomain or header."""
        # Try header first (for API clients)
        tenant_id = request.headers.get('X-Tenant-ID')
        if tenant_id:
            try:
                return Tenant.objects.get(uid=tenant_id, is_active=True)
            except Tenant.DoesNotExist:
                raise Http404("Tenant not found")

        # Try subdomain
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]

        if subdomain and subdomain not in ['www', 'app', 'api']:
            try:
                return Tenant.objects.get(slug=subdomain, is_active=True)
            except Tenant.DoesNotExist:
                raise Http404("Tenant not found")

        return None
```

### tenants/managers.py

```python
"""Tenant-aware managers."""
from django.db import models
from .middleware import get_current_tenant


class TenantQuerySet(models.QuerySet):
    """QuerySet that filters by current tenant."""

    def for_tenant(self, tenant):
        """Explicitly filter by tenant."""
        return self.filter(tenant=tenant)


class TenantManager(models.Manager):
    """Manager that automatically filters by current tenant."""

    def get_queryset(self):
        qs = TenantQuerySet(self.model, using=self._db)
        tenant = get_current_tenant()
        if tenant:
            return qs.filter(tenant=tenant)
        return qs

    def for_tenant(self, tenant):
        """Explicitly filter by tenant."""
        return TenantQuerySet(self.model, using=self._db).for_tenant(tenant)


class UnscopedManager(models.Manager):
    """Manager that returns all records regardless of tenant."""
    pass
```

### tenants/mixins.py

```python
"""Tenant-aware model mixin."""
from django.db import models
from .managers import TenantManager, UnscopedManager
from .middleware import get_current_tenant


class TenantAwareMixin(models.Model):
    """
    Mixin that adds tenant scoping to models.

    Usage:
        class Project(TenantAwareMixin, BaseModel):
            name = models.CharField(max_length=100)
    """

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_set',
        db_index=True,
    )

    objects = TenantManager()
    unscoped = UnscopedManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Auto-assign tenant if not set
        if not self.tenant_id:
            tenant = get_current_tenant()
            if tenant:
                self.tenant = tenant
            else:
                raise ValueError("Cannot save without tenant context")
        super().save(*args, **kwargs)
```

### apps/projects/models.py (Tenant-Scoped)

```python
"""Project models scoped to tenant."""
from django.db import models
from django.conf import settings
from core.models import SoftDeleteModel
from tenants.mixins import TenantAwareMixin


class Project(TenantAwareMixin, SoftDeleteModel):
    """Project within a tenant."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_projects',
    )
    is_archived = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'projects'
        # Unique within tenant, not globally
        unique_together = [['tenant', 'name']]
        indexes = [
            models.Index(fields=['tenant', 'is_archived']),
        ]

    def __str__(self) -> str:
        return self.name


class Task(TenantAwareMixin, SoftDeleteModel):
    """Task within a project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
    )
    status = models.CharField(max_length=20, default='todo')
    priority = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'tasks'
        ordering = ['-priority', '-created_at']

    def __str__(self) -> str:
        return self.title
```

---

## Example 4: Audit Trail with django-simple-history

### apps/contracts/models.py

```python
"""Contract models with audit trail."""
from decimal import Decimal
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from core.models import BaseModel


class ContractStatus(models.TextChoices):
    """Contract status choices."""
    DRAFT = 'draft', 'Draft'
    PENDING = 'pending', 'Pending Approval'
    ACTIVE = 'active', 'Active'
    EXPIRED = 'expired', 'Expired'
    TERMINATED = 'terminated', 'Terminated'


class Contract(BaseModel):
    """Contract with full change history."""

    # Basic info
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Parties
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='contracts',
    )

    # Terms
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    currency = models.CharField(max_length=3, default='USD')

    # Dates
    start_date = models.DateField()
    end_date = models.DateField()

    # Status
    status = models.CharField(
        max_length=20,
        choices=ContractStatus.choices,
        default=ContractStatus.DRAFT,
    )

    # Audit trail - tracks all changes
    history = HistoricalRecords(
        excluded_fields=['updated_at'],  # Don't track auto field
        history_change_reason_field=models.TextField(null=True),
    )

    class Meta:
        db_table = 'contracts'
        indexes = [
            models.Index(fields=['client', 'status']),
            models.Index(fields=['status', 'end_date']),
        ]

    def __str__(self) -> str:
        return self.title


# Usage examples:

# Get all historical versions
# contract.history.all()

# Get version at specific time
# contract.history.as_of(some_datetime)

# Get most recent change
# contract.history.most_recent()

# Get changes between dates
# contract.history.filter(
#     history_date__range=(start, end)
# )

# Revert to previous version
# old_version = contract.history.first()
# old_version.instance.save()
```

---

## Example 5: Using django-model-utils

Leveraging built-in base models from django-model-utils.

```python
"""Models using django-model-utils."""
from django.db import models
from model_utils.models import (
    TimeStampedModel,
    SoftDeletableModel,
    StatusModel,
    UUIDModel,
)
from model_utils import Choices


class Article(TimeStampedModel, SoftDeletableModel):
    """
    Article using django-model-utils base models.

    Inherits:
    - created, modified (from TimeStampedModel)
    - is_removed (from SoftDeletableModel)
    """

    STATUS = Choices('draft', 'published', 'archived')

    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default=STATUS.draft,
    )

    class Meta:
        db_table = 'articles'


class Subscription(UUIDModel, TimeStampedModel, StatusModel):
    """
    Subscription using multiple model-utils mixins.

    Inherits:
    - id (UUID primary key from UUIDModel)
    - created, modified (from TimeStampedModel)
    - status, status_changed (from StatusModel)
    """

    STATUS = Choices(
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    plan = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'subscriptions'
```

---

## Quick Reference: Model Selection

| Scenario | Base Model | Mixins |
|----------|------------|--------|
| Standard CRUD | `BaseModel` | - |
| User data (recoverable) | `SoftDeleteModel` | - |
| Multi-tenant | `BaseModel` | `TenantAwareMixin` |
| Financial records | `BaseModel` | `HistoricalRecords` |
| Multi-tenant + recoverable | `SoftDeleteModel` | `TenantAwareMixin` |
| Using model-utils | `TimeStampedModel` | `SoftDeletableModel` |

---

*Last updated: 2026-01-25*
