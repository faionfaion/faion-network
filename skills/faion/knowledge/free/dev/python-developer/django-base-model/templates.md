# Django Base Model Templates

Copy-paste templates for common base model patterns. Ready for production use.

---

## Template 1: Standard Base Model

The most common pattern - UUID + timestamps.

```python
# core/models/base.py
"""Base model classes for the application."""
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with UUID and timestamps.

    All domain models should inherit from this class.

    Fields:
        uid: Public UUID for external use (API, URLs)
        created_at: When record was created
        updated_at: When record was last modified

    Usage:
        class Product(BaseModel):
            name = models.CharField(max_length=100)
    """

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="Public identifier for external use",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.uid})"
```

---

## Template 2: Complete Soft Delete System

Full soft delete with managers and queryset.

```python
# core/models/soft_delete.py
"""Soft delete base model and managers."""
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):
    """QuerySet supporting soft delete operations."""

    def delete(self):
        """Soft delete all objects in queryset."""
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all objects."""
        return super().delete()

    def restore(self):
        """Restore all soft-deleted objects."""
        return self.update(deleted_at=None)

    def active(self):
        """Return only non-deleted objects."""
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        """Return only soft-deleted objects."""
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records by default."""

    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model, using=self._db
        ).filter(deleted_at__isnull=True)

    def with_deleted(self):
        """Include soft-deleted records."""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted_only(self):
        """Return only soft-deleted records."""
        return SoftDeleteQuerySet(self.model, using=self._db).deleted()


class AllObjectsManager(models.Manager):
    """Manager that includes all records."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteModel(models.Model):
    """
    Base model with soft delete support.

    Instead of deleting records from the database,
    marks them as deleted with a timestamp.

    Managers:
        objects: Default manager (excludes deleted)
        all_objects: Includes deleted records

    Methods:
        delete(): Soft delete (sets deleted_at)
        hard_delete(): Permanently remove
        restore(): Undelete record

    Usage:
        class Document(SoftDeleteModel):
            title = models.CharField(max_length=100)

        # Soft delete
        doc.delete()

        # Check if deleted
        doc.is_deleted  # True

        # Restore
        doc.restore()

        # Include deleted in query
        Document.all_objects.all()
    """

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
        """Soft delete: mark as deleted."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete from database."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Restore soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""
        return self.deleted_at is not None
```

---

## Template 3: Combined Base with Soft Delete

Full-featured base model combining UUID, timestamps, and soft delete.

```python
# core/models/__init__.py
"""Core model exports."""
import uuid
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


# --- Managers ---

class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(deleted_at=None)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model, using=self._db
        ).filter(deleted_at__isnull=True)

    def with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


# --- Base Models ---

class BaseModel(models.Model):
    """Standard base: UUID + timestamps."""

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.uid})"


class SoftDeleteModel(BaseModel):
    """Base with soft delete: UUID + timestamps + soft delete."""

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

---

## Template 4: Multi-Tenant Base Model

Complete multi-tenant system with middleware.

### tenants/models.py

```python
"""Tenant model."""
import uuid
from django.db import models


class Tenant(models.Model):
    """Organization in multi-tenant system."""

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tenants'

    def __str__(self) -> str:
        return self.name
```

### tenants/middleware.py

```python
"""Tenant middleware."""
import threading
from django.http import Http404

_thread_locals = threading.local()


def get_current_tenant():
    """Get tenant from thread-local storage."""
    return getattr(_thread_locals, 'tenant', None)


def set_current_tenant(tenant):
    """Set tenant in thread-local storage."""
    _thread_locals.tenant = tenant


class TenantMiddleware:
    """
    Extract tenant from request.

    Supports:
    - Header: X-Tenant-ID (UUID)
    - Subdomain: acme.app.com
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from .models import Tenant

        tenant = None

        # Try header first
        tenant_uid = request.headers.get('X-Tenant-ID')
        if tenant_uid:
            try:
                tenant = Tenant.objects.get(uid=tenant_uid, is_active=True)
            except Tenant.DoesNotExist:
                raise Http404("Tenant not found")

        # Try subdomain
        if not tenant:
            host = request.get_host().split(':')[0]
            subdomain = host.split('.')[0]
            if subdomain not in ['www', 'app', 'api', 'localhost']:
                try:
                    tenant = Tenant.objects.get(
                        slug=subdomain, is_active=True
                    )
                except Tenant.DoesNotExist:
                    pass

        set_current_tenant(tenant)
        request.tenant = tenant

        response = self.get_response(request)

        set_current_tenant(None)
        return response
```

### tenants/mixins.py

```python
"""Tenant-aware model mixin."""
from django.db import models
from .middleware import get_current_tenant


class TenantManager(models.Manager):
    """Auto-filters by current tenant."""

    def get_queryset(self):
        qs = super().get_queryset()
        tenant = get_current_tenant()
        if tenant:
            return qs.filter(tenant=tenant)
        return qs


class TenantAwareMixin(models.Model):
    """
    Add tenant scoping to any model.

    Usage:
        class Project(TenantAwareMixin, BaseModel):
            name = models.CharField(max_length=100)

    Notes:
        - Tenant auto-assigned on save if not set
        - queries filtered by current tenant
        - Use .unscoped for admin access
    """

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_set',
        db_index=True,
    )

    objects = TenantManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            tenant = get_current_tenant()
            if tenant:
                self.tenant = tenant
            else:
                raise ValueError("No tenant context")
        super().save(*args, **kwargs)
```

---

## Template 5: Audit Trail Model

Base model with django-simple-history.

```python
# core/models/audited.py
"""Audited base model with full change history."""
import uuid
from django.db import models
from simple_history.models import HistoricalRecords


class AuditedModel(models.Model):
    """
    Base model with automatic audit trail.

    Every create, update, delete is tracked with:
    - Who made the change (user)
    - When it happened (timestamp)
    - What changed (field values)

    Requires: pip install django-simple-history

    Usage:
        class Contract(AuditedModel):
            title = models.CharField(max_length=100)
            value = models.DecimalField(...)

        # View history
        contract.history.all()

        # Version at specific time
        contract.history.as_of(datetime)

        # Revert to previous
        old = contract.history.first()
        old.instance.save()
    """

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords(
        inherit=True,
        excluded_fields=['updated_at'],
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.uid})"
```

---

## Template 6: Custom Manager + QuerySet Pattern

Reusable pattern for custom queries.

```python
# core/managers.py
"""Custom manager pattern template."""
from django.db import models
from django.db.models import QuerySet


class BaseQuerySet(QuerySet):
    """
    Base queryset with common methods.

    Extend this for model-specific queries.
    """

    def active(self):
        """Return only active records."""
        return self.filter(is_active=True)

    def inactive(self):
        """Return only inactive records."""
        return self.filter(is_active=False)


class BaseManager(models.Manager):
    """Base manager using BaseQuerySet."""

    queryset_class = BaseQuerySet

    def get_queryset(self):
        return self.queryset_class(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


# --- Example: Article QuerySet/Manager ---

class ArticleQuerySet(BaseQuerySet):
    """Article-specific queries."""

    def published(self):
        return self.filter(status='published')

    def draft(self):
        return self.filter(status='draft')

    def by_author(self, author):
        return self.filter(author=author)

    def featured(self):
        return self.filter(is_featured=True)

    def recent(self, days=30):
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)


class ArticleManager(BaseManager):
    """Article manager with custom methods."""

    queryset_class = ArticleQuerySet

    def published(self):
        return self.get_queryset().published()

    def featured(self):
        return self.get_queryset().featured()

    def recent(self, days=30):
        return self.get_queryset().recent(days)


# Usage in model:
# class Article(BaseModel):
#     objects = ArticleManager()
```

---

## Template 7: Django 5.x Features

Using GeneratedField and db_default.

```python
# models/django5_features.py
"""Django 5.x model features template."""
from django.db import models
from django.db.models import F, Value, Q
from django.db.models.functions import Concat, Now, Lower


class Person(models.Model):
    """Example using GeneratedField for computed columns."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Computed column: stored in database
    full_name = models.GeneratedField(
        expression=Concat(
            F('first_name'),
            Value(' '),
            F('last_name'),
        ),
        output_field=models.CharField(max_length=201),
        db_persist=True,  # Required for PostgreSQL
    )

    # db_default: database computes default
    created_at = models.DateTimeField(db_default=Now())


class Order(models.Model):
    """Example with computed total."""

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField(default=0)

    # Computed subtotal
    subtotal = models.GeneratedField(
        expression=F('quantity') * F('unit_price'),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=True,
    )

    # Computed total with discount
    total = models.GeneratedField(
        expression=(
            F('quantity') * F('unit_price') *
            (100 - F('discount_percent')) / 100
        ),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=True,
    )


class Article(models.Model):
    """Example with auto-generated slug."""

    title = models.CharField(max_length=200)

    # Note: This works for simple cases
    # For complex slug generation, use pre_save signal
    slug = models.SlugField(
        max_length=200,
        db_default=Lower(F('title')),  # Simplified
    )
```

---

## Template 8: API Serializer Pattern

Serializers that use uid instead of id.

```python
# api/serializers/base.py
"""Base serializers for consistent API responses."""
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer that uses uid for identification.

    Never expose internal integer IDs in API responses.
    """

    # Always include uid
    uid = serializers.UUIDField(read_only=True)

    class Meta:
        # Subclasses define model and fields
        abstract = True

    def to_representation(self, instance):
        """Ensure uid is always present."""
        data = super().to_representation(instance)
        # Remove 'id' if accidentally included
        data.pop('id', None)
        return data


class TimestampSerializer(BaseModelSerializer):
    """Serializer with timestamps."""

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


# --- Example Usage ---

class ProductSerializer(TimestampSerializer):
    """Product API serializer."""

    class Meta:
        model = None  # Set in subclass
        fields = [
            'uid',  # Not 'id'
            'name',
            'price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uid', 'created_at', 'updated_at']


# View example:
# class ProductDetailView(APIView):
#     def get(self, request, uid):  # Use uid in URL
#         product = get_object_or_404(Product, uid=uid)
#         return Response(ProductSerializer(product).data)
```

---

## Template 9: Version Mixin (Optimistic Locking)

For concurrent update protection.

```python
# core/models/version.py
"""Optimistic locking mixin."""
from django.db import models
from django.core.exceptions import ValidationError


class ConcurrencyError(Exception):
    """Raised when concurrent update detected."""
    pass


class VersionMixin(models.Model):
    """
    Adds optimistic locking via version field.

    Prevents lost updates in concurrent scenarios.

    Usage:
        class Document(VersionMixin, BaseModel):
            content = models.TextField()

        # In view:
        doc = Document.objects.get(uid=uid)
        doc.content = new_content
        doc.save()  # Version auto-incremented

        # In API with version check:
        if request_version != doc.version:
            raise ConcurrencyError("Document modified")
    """

    version = models.PositiveIntegerField(default=1, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk:
            # Update: increment version
            self.version += 1
        super().save(*args, **kwargs)

    def save_with_version_check(self, expected_version: int):
        """
        Save only if version matches.

        Raises ConcurrencyError if version mismatch.
        """
        if self.version != expected_version:
            raise ConcurrencyError(
                f"Version mismatch: expected {expected_version}, "
                f"got {self.version}"
            )
        self.save()
```

---

## Quick Copy Reference

| Need | Template |
|------|----------|
| Basic UUID + timestamps | Template 1 |
| Soft delete system | Template 2 |
| Combined base models | Template 3 |
| Multi-tenant | Template 4 |
| Audit trail | Template 5 |
| Custom queries | Template 6 |
| Django 5.x features | Template 7 |
| API serializers | Template 8 |
| Optimistic locking | Template 9 |

---

*Last updated: 2026-01-25*
