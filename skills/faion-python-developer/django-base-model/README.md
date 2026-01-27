# Django Base Model Pattern

## Overview

The Base Model pattern provides a consistent foundation for all Django models with common fields (UUID, timestamps) and behaviors. This methodology covers abstract base models, mixins, custom managers, and advanced patterns for production Django applications.

**Complexity:** Intermediate
**Django Version:** 5.0+ (with 5.2 LTS features)
**Key Libraries:** django-model-utils, django-simple-history, django-tenants

---

## Why Use Base Models?

| Benefit | Description |
|---------|-------------|
| **Consistency** | All models share common fields and behaviors |
| **DRY** | No repeated code for timestamps, UUIDs, soft delete |
| **Security** | UUID exposure prevents ID enumeration attacks |
| **Audit Trail** | Built-in tracking of creation/modification |
| **Maintainability** | Single place to modify common behavior |

---

## Core Patterns

### 1. Abstract Base Model

The foundation pattern - provides UUID and timestamps to all models.

```python
# core/models.py
import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base with UUID and timestamps."""

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
```

**Key Decision: UUID as Separate Field vs Primary Key**

| Approach | Pros | Cons |
|----------|------|------|
| **UUID as `uid` field** (recommended) | Better FK performance, integer clustering | Extra column |
| **UUID as `pk`** | Simpler model, no extra column | Poor insert performance at scale |

For most applications, keeping integer `id` as PK and adding `uid` for external exposure is the optimal pattern.

### 2. Timestamp Mixin

Lightweight mixin for projects that don't need UUID.

```python
class TimestampMixin(models.Model):
    """Adds created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### 3. Soft Delete Pattern

Enables "trash" functionality without permanent data loss.

```python
from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Excludes soft-deleted records by default."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class AllObjectsManager(models.Manager):
    """Includes all records (deleted and active)."""
    pass


class SoftDeleteMixin(models.Model):
    """Adds soft delete capability."""

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete instead of hard delete."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def hard_delete(self):
        """Permanently delete from database."""
        super().delete()

    def restore(self):
        """Restore soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

### 4. UUID Primary Key (When Needed)

For distributed systems or when you truly need UUID as PK.

```python
import uuid
from django.db import models


class UUIDPrimaryKeyModel(models.Model):
    """Model with UUID as primary key."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

**Performance Note:** UUID v4 primary keys cause index fragmentation. Consider:
- UUID v7 (timestamp-based, coming in Postgres 18)
- Clustering on `created_at` column
- Keeping integer PK with separate UUID field

---

## Custom Managers and QuerySets

### Manager Pattern

```python
from django.db import models


class ActiveManager(models.Manager):
    """Returns only active records."""

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PublishedManager(models.Manager):
    """Returns only published records."""

    def get_queryset(self):
        return super().get_queryset().filter(
            status='published',
            published_at__isnull=False,
        )
```

### QuerySet with Manager Pattern

```python
from django.db import models


class ArticleQuerySet(models.QuerySet):
    """Custom queryset for articles."""

    def published(self):
        return self.filter(status='published')

    def draft(self):
        return self.filter(status='draft')

    def by_author(self, author):
        return self.filter(author=author)

    def recent(self, days=30):
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)


class ArticleManager(models.Manager):
    """Manager using ArticleQuerySet."""

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def recent(self, days=30):
        return self.get_queryset().recent(days)


# Alternative: Manager from QuerySet
ArticleManager = ArticleQuerySet.as_manager()
```

---

## Django 5.x Features

### db_default (Database-Level Defaults)

```python
from django.db import models
from django.db.models.functions import Now


class Article(models.Model):
    """Using db_default for database-computed defaults."""

    title = models.CharField(max_length=200)
    # Default computed by database, not Python
    created_at = models.DateTimeField(db_default=Now())
```

### GeneratedField (Computed Columns)

```python
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat


class Person(models.Model):
    """Using GeneratedField for computed columns."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Computed column stored in database
    full_name = models.GeneratedField(
        expression=Concat(F('first_name'), Value(' '), F('last_name')),
        output_field=models.CharField(max_length=201),
        db_persist=True,  # Store in DB (required for PostgreSQL)
    )


class Order(models.Model):
    """Boolean computed column."""

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    total = models.GeneratedField(
        expression=F('quantity') * F('price'),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=True,
    )
```

---

## Audit Trail with django-simple-history

```python
from django.db import models
from simple_history.models import HistoricalRecords


class AuditedModel(models.Model):
    """Base model with audit trail."""

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class Contract(AuditedModel):
    """Contract with full change history."""

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20)

    # Access history:
    # contract.history.all()  # All versions
    # contract.history.most_recent()  # Latest
    # contract.history.as_of(some_datetime)  # Version at time
```

---

## Multi-Tenant Models

### Shared Schema Pattern (Recommended)

```python
from django.db import models
from django.conf import settings


class TenantManager(models.Manager):
    """Manager that filters by current tenant."""

    def get_queryset(self):
        from .middleware import get_current_tenant
        tenant = get_current_tenant()
        if tenant:
            return super().get_queryset().filter(tenant=tenant)
        return super().get_queryset()


class TenantAwareModel(models.Model):
    """Abstract base for tenant-scoped models."""

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
    )

    objects = TenantManager()
    unscoped = models.Manager()  # Access all tenants (admin only)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            from .middleware import get_current_tenant
            self.tenant = get_current_tenant()
        super().save(*args, **kwargs)
```

---

## Combining Mixins

```python
class FullFeaturedModel(
    TimestampMixin,
    SoftDeleteMixin,
    TenantAwareModel,
):
    """Combines all mixins for full-featured base."""

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    class Meta:
        abstract = True
```

---

## ForeignKey Best Practices

| Scenario | on_delete | Why |
|----------|-----------|-----|
| User owns Order | `PROTECT` | Don't lose order history |
| Order has Items | `CASCADE` | Items meaningless without order |
| Task assigned to User | `SET_NULL` | Task survives user deletion |
| Comment by User | `SET_NULL` | Preserve content, clear author |
| Config belongs to Tenant | `CASCADE` | Config meaningless without tenant |

---

## LLM Usage Tips

### When to Use This Pattern

- Starting a new Django project
- Refactoring legacy models
- Building APIs with external IDs
- Multi-tenant SaaS applications
- Systems requiring audit trails

### Key Questions to Ask

1. Do you need soft delete?
2. Is UUID required for external exposure?
3. Do you need audit trail?
4. Is this a multi-tenant system?
5. What FK cascading behavior is needed?

### Common Mistakes

1. Using UUID as PK without understanding performance impact
2. Forgetting to index `uid` field
3. Using CASCADE when PROTECT is safer
4. Not considering soft delete for important data
5. Exposing auto-increment IDs in APIs

---

## External Resources

### Official Documentation
- [Django Model Field Reference](https://docs.djangoproject.com/en/5.2/ref/models/fields/)
- [Django Model Meta Options](https://docs.djangoproject.com/en/5.2/ref/models/options/)
- [Django 5.2 Release Notes](https://docs.djangoproject.com/en/5.2/releases/5.2/)
- [Django Managers](https://docs.djangoproject.com/en/6.0/topics/db/managers/)

### Libraries
- [django-model-utils](https://django-model-utils.readthedocs.io/) - TimeStampedModel, SoftDeletableModel, StatusModel
- [django-simple-history](https://django-simple-history.readthedocs.io/) - Audit trail
- [django-tenants](https://django-tenants.readthedocs.io/) - Multi-tenant PostgreSQL schemas
- [django-soft-delete](https://pypi.org/project/django-soft-delete/) - Soft delete utilities

### Articles
- [Django Best Practices - Models](https://mshaeri.com/blog/django-best-practices-part-1/)
- [Implementing Soft Delete in Django](https://www.tomisin.dev/blog/implementing-soft-delete-in-django-an-intuitive-guide)
- [Django Multi-Tenant Architectures](https://medium.com/simform-engineering/mastering-multi-tenant-architectures-in-django-three-powerful-approaches-178ff527c03f)
- [UUID Primary Keys Performance](https://andyatkinson.com/avoid-uuid-version-4-primary-keys)
- [Building Multi-Tenant SaaS in Django 2026](https://medium.com/@yogeshkrishnanseeniraj/building-a-multi-tenant-saas-in-django-complete-2026-architecture-e956e9f5086a)
- [Django Audit Logging Libraries](https://medium.com/@mariliabontempo/django-audit-logging-the-best-libraries-for-tracking-model-changes-with-postgresql-2c7396564e97)

---

## Related Methodologies

- [django-models/](../django-models/) - General model patterns
- [django-services/](../django-services/) - Service layer patterns
- [django-api/](../django-api/) - API patterns with serializers
- [django-coding-standards/](../django-coding-standards/) - Project structure

---

*Last updated: 2026-01-25*
