# Django Models Guide

## Overview

Django models are the foundation of data persistence in Django applications. This guide covers modern best practices for model design, focusing on BaseModel patterns, field choices, managers, QuerySets, and database optimization.

## Model Design Patterns

### 1. Abstract Base Model Pattern

Every Django project should have a `BaseModel` that provides consistent fields across all models.

```python
# core/models.py
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with UUID and timestamps.

    Provides:
    - uid: External-safe identifier (never expose auto-increment IDs)
    - created_at: Record creation timestamp
    - updated_at: Last modification timestamp
    """
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
        get_latest_by = 'created_at'

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.uid})"
```

**Key Points:**
- `uid` for external APIs (never expose `id`)
- `created_at` indexed for sorting performance
- `abstract = True` prevents table creation
- Override `__str__` in child models

### 2. Soft Delete Pattern

For data that should be preserved but hidden from normal queries.

```python
# core/models.py
from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that supports bulk soft delete."""

    def delete(self):
        """Soft delete all records in queryset."""
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all records."""
        return super().delete()

    def alive(self):
        """Filter to non-deleted records."""
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        """Filter to deleted records only."""
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records by default."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class AllObjectsManager(models.Manager):
    """Manager that includes all records (including deleted)."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteModel(BaseModel):
    """Base model with soft delete support."""

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete instead of hard delete."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete from database."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Restore soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

**GDPR Warning:** Soft delete is NOT appropriate for personal data that users have requested to be permanently deleted.

### 3. Service Layer Pattern (HackSoft)

Models should be thin. Business logic belongs in services.

```python
# apps/users/services.py
from apps.users.models import User


def user_create(*, email: str, name: str, password: str) -> User:
    """Create a new user with validation."""
    user = User(email=email, name=name)
    user.set_password(password)
    user.full_clean()
    user.save()
    return user


def user_update(*, user: User, data: dict) -> User:
    """Update user with provided data."""
    for field, value in data.items():
        setattr(user, field, value)
    user.full_clean()
    user.save()
    return user
```

---

## Field Choices and Constraints

### TextChoices (Recommended)

```python
# apps/orders/constants.py
from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'


class PaymentMethod(models.TextChoices):
    CARD = 'card', 'Credit Card'
    PAYPAL = 'paypal', 'PayPal'
    BANK = 'bank', 'Bank Transfer'
```

```python
# apps/orders/models.py
from apps.orders import constants


class Order(BaseModel):
    status = models.CharField(
        max_length=20,
        choices=constants.OrderStatus.choices,
        default=constants.OrderStatus.PENDING,
    )
    payment_method = models.CharField(
        max_length=20,
        choices=constants.PaymentMethod.choices,
    )
```

### IntegerChoices

```python
class Priority(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'
    CRITICAL = 4, 'Critical'
```

### Database Constraints

```python
from django.db.models import Q, CheckConstraint, UniqueConstraint


class Order(BaseModel):
    quantity = models.PositiveIntegerField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints = [
            # Check constraint
            CheckConstraint(
                check=Q(discount_percent__gte=0) & Q(discount_percent__lte=100),
                name='valid_discount_percent',
            ),
            # Unique together
            UniqueConstraint(
                fields=['user', 'product'],
                condition=Q(deleted_at__isnull=True),
                name='unique_active_user_product',
            ),
        ]
```

---

## Manager and QuerySet Patterns

### Custom QuerySet

```python
# apps/articles/models.py
from django.db import models


class ArticleQuerySet(models.QuerySet):
    """Chainable query methods for Article."""

    def published(self):
        """Filter to published articles only."""
        return self.filter(status='published', published_at__isnull=False)

    def by_author(self, user):
        """Filter by author."""
        return self.filter(author=user)

    def with_stats(self):
        """Annotate with computed statistics."""
        return self.annotate(
            comment_count=models.Count('comments'),
            avg_rating=models.Avg('ratings__score'),
        )

    def recent(self, days=7):
        """Filter to articles from last N days."""
        from django.utils import timezone
        cutoff = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=cutoff)
```

### Custom Manager

```python
class ArticleManager(models.Manager):
    """Manager for Article with factory methods."""

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def create_draft(self, *, title: str, author, content: str = ''):
        """Factory method for creating draft articles."""
        return self.create(
            title=title,
            author=author,
            content=content,
            status='draft',
        )
```

### Combining Manager and QuerySet

```python
class Article(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.PROTECT)
    status = models.CharField(max_length=20, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)

    # Best pattern: Manager.from_queryset()
    objects = ArticleManager.from_queryset(ArticleQuerySet)()

    class Meta:
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['author', 'status']),
        ]
```

**Usage:**
```python
# QuerySet methods are chainable
Article.objects.published().by_author(user).with_stats()

# Manager factory method
Article.objects.create_draft(title='New Post', author=user)
```

---

## ForeignKey Patterns

### on_delete Options

| Option | Use When | Example |
|--------|----------|---------|
| `PROTECT` | Deletion should be blocked | `user = FK(User, on_delete=PROTECT)` |
| `CASCADE` | Child has no meaning without parent | `order_items` when deleting `order` |
| `SET_NULL` | Reference is optional | `assigned_to` when employee leaves |
| `SET_DEFAULT` | Has sensible default | `category` with default category |
| `DO_NOTHING` | Manual DB handling | Rare, avoid |

```python
class Order(BaseModel):
    # PROTECT: Cannot delete user with orders
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='orders',
    )

    # SET_NULL: Handler can be removed
    handled_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_orders',
    )


class OrderItem(BaseModel):
    # CASCADE: Items deleted with order
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='items',
    )
```

### Related Names

Always set explicit `related_name`:

```python
# Good
author = models.ForeignKey(User, related_name='authored_articles')
editor = models.ForeignKey(User, related_name='edited_articles')

# Bad - auto-generated names are confusing
author = models.ForeignKey(User)  # article_set
```

To disable reverse relation:
```python
author = models.ForeignKey(User, related_name='+')
```

---

## Django 5.x Features

### db_default (Django 5.0+)

Database-computed default values:

```python
from django.db.models.functions import Now, Lower


class Article(BaseModel):
    title = models.CharField(max_length=200)

    # Database computes default at INSERT time
    created_at = models.DateTimeField(db_default=Now())

    # Slug computed from title
    slug = models.SlugField(db_default=Lower('title'))
```

### GeneratedField (Django 5.0+)

Database-computed columns:

```python
from django.db.models import F, Value
from django.db.models.functions import Concat


class Product(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    # Computed column stored in DB
    total_value = models.GeneratedField(
        expression=F('price') * F('quantity'),
        output_field=models.DecimalField(max_digits=15, decimal_places=2),
        db_persist=True,  # Stored column (not virtual)
    )

    # Computed display name
    display_name = models.GeneratedField(
        expression=Concat('name', Value(' ('), F('sku'), Value(')')),
        output_field=models.CharField(max_length=150),
        db_persist=False,  # Virtual column
    )
```

**Note:** After `save()`, call `refresh_from_db()` to get computed values.

---

## Performance Optimization

### Indexing Strategy

```python
class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, db_index=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            # Composite index for common queries
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),

            # Partial index (PostgreSQL)
            models.Index(
                fields=['created_at'],
                condition=Q(status='pending'),
                name='pending_orders_idx',
            ),

            # Covering index
            models.Index(
                fields=['user', 'status'],
                include=['total'],
                name='order_summary_idx',
            ),
        ]
```

### Query Optimization

```python
# Bad: N+1 queries
for order in Order.objects.all():
    print(order.user.email)  # Query per order!

# Good: select_related for FK
for order in Order.objects.select_related('user'):
    print(order.user.email)  # Single query

# Good: prefetch_related for reverse FK/M2M
for user in User.objects.prefetch_related('orders'):
    print(user.orders.count())  # 2 queries total
```

---

## Validation

### Model-level Validation

```python
from django.core.exceptions import ValidationError


class Order(BaseModel):
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        """Model-level validation."""
        super().clean()

        if self.discount < 0 or self.discount > 100:
            raise ValidationError({
                'discount': 'Discount must be between 0 and 100.'
            })

        if self.quantity > 1000 and self.discount > 50:
            raise ValidationError(
                'Large orders cannot have more than 50% discount.'
            )
```

### Field-level Validators

```python
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Product(BaseModel):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    sku = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}-\d{6}$',
                message='SKU must be format: ABC-123456'
            ),
        ],
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
```

---

## Project Structure

```
project/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── celery.py
├── core/
│   ├── models.py          # BaseModel, SoftDeleteModel
│   ├── exceptions.py
│   └── utils.py
├── apps/
│   ├── users/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── services/
│   │   ├── selectors/
│   │   ├── constants.py
│   │   └── tests/
│   └── orders/
│       ├── models/
│       ├── services/
│       └── constants.py
└── tests/
    └── conftest.py
```

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Model design checklist |
| [examples.md](examples.md) | Complete model examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for model generation |

---

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
- [Django Models](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Model Field Reference](https://docs.djangoproject.com/en/5.2/ref/models/fields/)
- [Model Meta Options](https://docs.djangoproject.com/en/5.2/ref/models/options/)
- [Django Managers](https://docs.djangoproject.com/en/5.2/topics/db/managers/)
- [Django Indexes](https://docs.djangoproject.com/en/5.2/ref/models/indexes/)
- [Django 5.0 Release Notes](https://docs.djangoproject.com/en/5.2/releases/5.0/) (GeneratedField, db_default)

### Community Resources
- [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide)
- [Django Best Practices](https://www.ryanthomson.net/articles/django-model-best-practices/)
- [Django Stars - Models Best Practices](https://djangostars.com/blog/django-models-best-practices/)
- [django-model-utils](https://django-model-utils.readthedocs.io/en/latest/models.html)
