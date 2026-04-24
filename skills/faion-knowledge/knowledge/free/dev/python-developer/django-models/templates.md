# Django Model Templates

Copy-paste templates for common model patterns. Replace placeholders in `{CURLY_BRACES}`.

---

## BaseModel Template

```python
# core/models.py
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with UUID and timestamps.

    All domain models should inherit from this class.
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

---

## SoftDeleteModel Template

```python
# core/models.py
from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that supports bulk soft delete."""

    def delete(self):
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class AllObjectsManager(models.Manager):
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

## Standard Model Template

```python
# apps/{APP_NAME}/models/{MODEL_NAME_LOWER}.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
from apps.{APP_NAME} import constants


class {MODEL_NAME}QuerySet(models.QuerySet):
    """{MODEL_NAME} chainable queries."""

    def active(self):
        return self.filter(is_active=True)

    def by_status(self, status: str):
        return self.filter(status=status)


class {MODEL_NAME}Manager(models.Manager):
    """{MODEL_NAME} manager with factory methods."""

    def get_queryset(self):
        return {MODEL_NAME}QuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class {MODEL_NAME}(BaseModel):
    """
    {MODEL_DESCRIPTION}

    Attributes:
        name: {FIELD_DESCRIPTION}
        status: Current status of the {MODEL_NAME_LOWER}
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=constants.{MODEL_NAME}Status.choices,
        default=constants.{MODEL_NAME}Status.{DEFAULT_STATUS},
    )

    is_active = models.BooleanField(default=True)

    objects = {MODEL_NAME}Manager()

    class Meta:
        db_table = '{DB_TABLE_NAME}'
        ordering = ['-created_at']
        verbose_name = '{MODEL_NAME}'
        verbose_name_plural = '{MODEL_NAME_PLURAL}'
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['slug']),
        ]

    def __str__(self) -> str:
        return self.name
```

---

## Constants Template

```python
# apps/{APP_NAME}/constants.py
from django.db import models


class {MODEL_NAME}Status(models.TextChoices):
    """Status choices for {MODEL_NAME}."""
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    ARCHIVED = 'archived', 'Archived'


class {MODEL_NAME}Type(models.TextChoices):
    """Type choices for {MODEL_NAME}."""
    TYPE_A = 'type_a', 'Type A'
    TYPE_B = 'type_b', 'Type B'


# Limits
MAX_{FIELD}_LENGTH = 200
DEFAULT_PAGE_SIZE = 20
MAX_ITEMS = 100
```

---

## ForeignKey Model Template

```python
# apps/{APP_NAME}/models/{MODEL_NAME_LOWER}.py
from django.db import models
from core.models import BaseModel


class {MODEL_NAME}(BaseModel):
    """
    {MODEL_DESCRIPTION}

    Relations:
        {PARENT_MODEL_LOWER}: Parent {PARENT_MODEL} (required)
        {OPTIONAL_REL_LOWER}: Optional {OPTIONAL_REL}
    """

    # Required FK - PROTECT from deletion
    {PARENT_MODEL_LOWER} = models.ForeignKey(
        '{PARENT_APP}.{PARENT_MODEL}',
        on_delete=models.PROTECT,
        related_name='{RELATED_NAME}',
    )

    # Optional FK - SET_NULL on deletion
    {OPTIONAL_REL_LOWER} = models.ForeignKey(
        '{OPTIONAL_APP}.{OPTIONAL_REL}',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='{OPTIONAL_RELATED_NAME}',
    )

    # ... other fields

    class Meta:
        db_table = '{DB_TABLE_NAME}'
        indexes = [
            models.Index(fields=['{PARENT_MODEL_LOWER}', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"{self.__class__.__name__} for {self.{PARENT_MODEL_LOWER}}"
```

---

## Child Model Template (CASCADE)

```python
# apps/{APP_NAME}/models/{CHILD_MODEL_LOWER}.py
from django.db import models
from core.models import BaseModel


class {CHILD_MODEL}(BaseModel):
    """
    {CHILD_DESCRIPTION}

    Deleted when parent {PARENT_MODEL} is deleted.
    """

    {PARENT_MODEL_LOWER} = models.ForeignKey(
        '{PARENT_APP}.{PARENT_MODEL}',
        on_delete=models.CASCADE,
        related_name='{CHILDREN_NAME}',
    )

    # ... child-specific fields

    class Meta:
        db_table = '{DB_TABLE_NAME}'
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['{PARENT_MODEL_LOWER}', '{UNIQUE_FIELD}'],
                name='unique_{PARENT_MODEL_LOWER}_{UNIQUE_FIELD}',
            ),
        ]
```

---

## ManyToMany with Through Model Template

```python
# apps/{APP_NAME}/models/{MODEL_NAME_LOWER}.py
from django.db import models
from core.models import BaseModel


class {MODEL_A}(BaseModel):
    """Model A in M2M relationship."""

    name = models.CharField(max_length=200)

    {MODEL_B_PLURAL_LOWER} = models.ManyToManyField(
        '{APP_B}.{MODEL_B}',
        through='{THROUGH_MODEL}',
        related_name='{MODEL_A_PLURAL_LOWER}',
    )


class {THROUGH_MODEL}(BaseModel):
    """
    Through model for {MODEL_A} <-> {MODEL_B} relationship.

    Stores additional data about the relationship.
    """

    {MODEL_A_LOWER} = models.ForeignKey(
        {MODEL_A},
        on_delete=models.CASCADE,
        related_name='{THROUGH_RELATED_A}',
    )
    {MODEL_B_LOWER} = models.ForeignKey(
        '{APP_B}.{MODEL_B}',
        on_delete=models.CASCADE,
        related_name='{THROUGH_RELATED_B}',
    )

    # Relationship metadata
    {EXTRA_FIELD} = models.{FIELD_TYPE}()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '{THROUGH_TABLE_NAME}'
        constraints = [
            models.UniqueConstraint(
                fields=['{MODEL_A_LOWER}', '{MODEL_B_LOWER}'],
                name='unique_{MODEL_A_LOWER}_{MODEL_B_LOWER}',
            ),
        ]
```

---

## QuerySet Template

```python
# apps/{APP_NAME}/models/{MODEL_NAME_LOWER}.py
from django.db import models
from django.utils import timezone


class {MODEL_NAME}QuerySet(models.QuerySet):
    """Chainable query methods for {MODEL_NAME}."""

    def active(self):
        """Filter to active records."""
        return self.filter(is_active=True)

    def by_status(self, status: str):
        """Filter by status."""
        return self.filter(status=status)

    def by_{FK_NAME}(self, {FK_NAME}):
        """Filter by {FK_NAME}."""
        return self.filter({FK_NAME}={FK_NAME})

    def recent(self, days: int = 7):
        """Filter to records from last N days."""
        cutoff = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=cutoff)

    def with_counts(self):
        """Annotate with related object counts."""
        return self.annotate(
            {RELATED_NAME}_count=models.Count('{RELATED_NAME}'),
        )

    def with_aggregates(self):
        """Annotate with computed aggregates."""
        return self.annotate(
            total_{FIELD}=models.Sum('{FIELD}'),
            avg_{FIELD}=models.Avg('{FIELD}'),
        )
```

---

## Manager Template

```python
# apps/{APP_NAME}/models/{MODEL_NAME_LOWER}.py
from django.db import models


class {MODEL_NAME}Manager(models.Manager):
    """Manager for {MODEL_NAME} with factory methods."""

    def get_queryset(self):
        return {MODEL_NAME}QuerySet(self.model, using=self._db)

    # Proxy QuerySet methods
    def active(self):
        return self.get_queryset().active()

    def by_status(self, status: str):
        return self.get_queryset().by_status(status)

    # Factory methods
    def create_{DEFAULT_TYPE}(self, *, {REQUIRED_FIELD}: str, **kwargs):
        """Create a {DEFAULT_TYPE} {MODEL_NAME_LOWER}."""
        return self.create(
            {REQUIRED_FIELD}={REQUIRED_FIELD},
            status='{DEFAULT_STATUS}',
            **kwargs,
        )
```

---

## Mixin Templates

### Timestamped Mixin

```python
class TimestampedMixin(models.Model):
    """Mixin adding created_at and updated_at."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### Addressable Mixin

```python
class AddressableMixin(models.Model):
    """Mixin for models with address fields."""

    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='US')

    class Meta:
        abstract = True

    @property
    def full_address(self) -> str:
        return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}, {self.country}"
```

### Orderable Mixin

```python
class OrderableMixin(models.Model):
    """Mixin for models with custom ordering."""

    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ['position']

    def move_up(self):
        if self.position > 0:
            self.position -= 1
            self.save(update_fields=['position'])

    def move_down(self):
        self.position += 1
        self.save(update_fields=['position'])
```

### Publishable Mixin

```python
class PublishableMixin(models.Model):
    """Mixin for content with publish status."""

    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    def publish(self):
        from django.utils import timezone
        self.is_published = True
        self.published_at = timezone.now()
        self.save(update_fields=['is_published', 'published_at', 'updated_at'])

    def unpublish(self):
        self.is_published = False
        self.save(update_fields=['is_published', 'updated_at'])
```

---

## Migration Templates

### Data Migration

```python
# apps/{APP_NAME}/migrations/XXXX_{MIGRATION_NAME}.py
from django.db import migrations


def forwards_func(apps, schema_editor):
    """Forward migration: {DESCRIPTION}."""
    {MODEL_NAME} = apps.get_model('{APP_NAME}', '{MODEL_NAME}')

    # Example: Set default values
    {MODEL_NAME}.objects.filter({FIELD}__isnull=True).update({FIELD}='{DEFAULT}')


def backwards_func(apps, schema_editor):
    """Reverse migration."""
    # Usually pass or reverse the operation
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('{APP_NAME}', '{PREVIOUS_MIGRATION}'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]
```

### Add Field with Default Then Remove Default

```python
# Step 1: Add nullable field
# python manage.py makemigrations --name add_{FIELD}_nullable

# Step 2: Data migration to populate
# apps/{APP_NAME}/migrations/XXXX_populate_{FIELD}.py
def forwards_func(apps, schema_editor):
    {MODEL_NAME} = apps.get_model('{APP_NAME}', '{MODEL_NAME}')
    for obj in {MODEL_NAME}.objects.filter({FIELD}__isnull=True):
        obj.{FIELD} = compute_value(obj)
        obj.save(update_fields=['{FIELD}'])

# Step 3: Make field required
# python manage.py makemigrations --name make_{FIELD}_required
```
