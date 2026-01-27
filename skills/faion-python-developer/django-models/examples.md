# Django Model Examples

## Table of Contents

1. [E-commerce Domain](#e-commerce-domain)
2. [Content Management](#content-management)
3. [Model Inheritance](#model-inheritance)
4. [Complex Relations](#complex-relations)
5. [Django 5.x Features](#django-5x-features)

---

## E-commerce Domain

### Product Model

```python
# apps/catalog/constants.py
from django.db import models


class ProductStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    DISCONTINUED = 'discontinued', 'Discontinued'


class ProductCategory(models.TextChoices):
    ELECTRONICS = 'electronics', 'Electronics'
    CLOTHING = 'clothing', 'Clothing'
    BOOKS = 'books', 'Books'
    HOME = 'home', 'Home & Garden'


# Limits
MAX_PRICE = 999999.99
MIN_PRICE = 0.01
MAX_IMAGES_PER_PRODUCT = 10
```

```python
# apps/catalog/models/product.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import SoftDeleteModel
from apps.catalog import constants


class ProductQuerySet(models.QuerySet):
    """Chainable queries for Product."""

    def active(self):
        return self.filter(status=constants.ProductStatus.ACTIVE)

    def in_category(self, category: str):
        return self.filter(category=category)

    def in_stock(self):
        return self.filter(stock_quantity__gt=0)

    def price_range(self, min_price=None, max_price=None):
        qs = self
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        return qs

    def with_ratings(self):
        return self.annotate(
            avg_rating=models.Avg('reviews__rating'),
            review_count=models.Count('reviews'),
        )


class ProductManager(models.Manager):
    """Manager with factory methods."""

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )

    def active(self):
        return self.get_queryset().active()

    def create_draft(self, *, name: str, price, category: str, **kwargs):
        """Create a draft product."""
        return self.create(
            name=name,
            price=price,
            category=category,
            status=constants.ProductStatus.DRAFT,
            **kwargs,
        )


class Product(SoftDeleteModel):
    """Product in the catalog."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(constants.MIN_PRICE),
            MaxValueValidator(constants.MAX_PRICE),
        ],
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    category = models.CharField(
        max_length=20,
        choices=constants.ProductCategory.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=constants.ProductStatus.choices,
        default=constants.ProductStatus.DRAFT,
    )

    stock_quantity = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    objects = ProductManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'catalog_products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['category', 'price']),
            models.Index(fields=['is_featured', 'status']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=constants.MIN_PRICE),
                name='product_price_positive',
            ),
            models.CheckConstraint(
                check=models.Q(stock_quantity__gte=0),
                name='product_stock_non_negative',
            ),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def is_in_stock(self) -> bool:
        return self.stock_quantity > 0

    @property
    def profit_margin(self) -> float | None:
        if self.cost and self.cost > 0:
            return float((self.price - self.cost) / self.price * 100)
        return None
```

### Order Model

```python
# apps/orders/constants.py
from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'
    REFUNDED = 'refunded', 'Refunded'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'
```

```python
# apps/orders/models/order.py
from django.db import models
from django.core.exceptions import ValidationError
from core.models import BaseModel
from apps.orders import constants


class OrderQuerySet(models.QuerySet):
    """Chainable queries for Order."""

    def pending(self):
        return self.filter(status=constants.OrderStatus.PENDING)

    def active(self):
        """Orders that are not cancelled or refunded."""
        return self.exclude(
            status__in=[
                constants.OrderStatus.CANCELLED,
                constants.OrderStatus.REFUNDED,
            ]
        )

    def by_user(self, user):
        return self.filter(user=user)

    def with_totals(self):
        return self.annotate(
            item_count=models.Count('items'),
            calculated_total=models.Sum(
                models.F('items__quantity') * models.F('items__unit_price')
            ),
        )


class Order(BaseModel):
    """Customer order."""

    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='orders',
    )

    status = models.CharField(
        max_length=20,
        choices=constants.OrderStatus.choices,
        default=constants.OrderStatus.PENDING,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=constants.PaymentStatus.choices,
        default=constants.PaymentStatus.PENDING,
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    shipping_address = models.TextField()
    billing_address = models.TextField()

    notes = models.TextField(blank=True)

    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager.from_queryset(OrderQuerySet)()

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self) -> str:
        return f"Order {self.uid} - {self.status}"

    def clean(self):
        super().clean()
        if self.total < 0:
            raise ValidationError({'total': 'Total cannot be negative.'})


class OrderItem(BaseModel):
    """Line item in an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.PROTECT,
        related_name='order_items',
    )

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_order_product',
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name='order_item_quantity_positive',
            ),
        ]

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name}"

    @property
    def line_total(self) -> float:
        return float(self.quantity * self.unit_price)
```

---

## Content Management

### Article with Tags

```python
# apps/blog/constants.py
from django.db import models


class ArticleStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    REVIEW = 'review', 'In Review'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'
```

```python
# apps/blog/models/article.py
from django.db import models
from django.utils import timezone
from core.models import SoftDeleteModel
from apps.blog import constants


class Tag(models.Model):
    """Tag for categorizing articles."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'blog_tags'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class ArticleQuerySet(models.QuerySet):
    """Chainable queries for Article."""

    def published(self):
        return self.filter(
            status=constants.ArticleStatus.PUBLISHED,
            published_at__lte=timezone.now(),
        )

    def drafts(self):
        return self.filter(status=constants.ArticleStatus.DRAFT)

    def by_author(self, author):
        return self.filter(author=author)

    def with_tag(self, tag_slug: str):
        return self.filter(tags__slug=tag_slug)

    def with_stats(self):
        return self.annotate(
            view_count=models.Count('views'),
            comment_count=models.Count('comments'),
        )

    def featured(self):
        return self.filter(is_featured=True)


class Article(SoftDeleteModel):
    """Blog article."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(max_length=500, blank=True)
    content = models.TextField()

    author = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='articles',
    )

    status = models.CharField(
        max_length=20,
        choices=constants.ArticleStatus.choices,
        default=constants.ArticleStatus.DRAFT,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True,
    )

    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)

    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = models.Manager.from_queryset(ArticleQuerySet)()

    class Meta:
        db_table = 'blog_articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['author', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def is_published(self) -> bool:
        return (
            self.status == constants.ArticleStatus.PUBLISHED
            and self.published_at is not None
            and self.published_at <= timezone.now()
        )

    def publish(self):
        """Publish the article."""
        self.status = constants.ArticleStatus.PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at', 'updated_at'])
```

---

## Model Inheritance

### Abstract Base Class

```python
# core/models.py
from django.db import models


class Addressable(models.Model):
    """Mixin for models with address."""

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    class Meta:
        abstract = True

    @property
    def full_address(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}"


class Contactable(models.Model):
    """Mixin for models with contact info."""

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        abstract = True


# Usage
class Warehouse(BaseModel, Addressable, Contactable):
    """Warehouse location."""

    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    class Meta:
        db_table = 'warehouses'
```

### Multi-table Inheritance (Use Sparingly)

```python
# apps/payments/models.py
from django.db import models
from core.models import BaseModel


class Payment(BaseModel):
    """Base payment record."""

    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'payments'


class CardPayment(Payment):
    """Credit card payment."""

    last_four = models.CharField(max_length=4)
    card_brand = models.CharField(max_length=20)
    authorization_code = models.CharField(max_length=50)

    class Meta:
        db_table = 'card_payments'


class BankTransfer(Payment):
    """Bank transfer payment."""

    bank_name = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=50)

    class Meta:
        db_table = 'bank_transfers'
```

**Note:** Multi-table inheritance creates JOINs. Prefer abstract base classes or composition.

### Proxy Model

```python
# apps/users/models.py
from django.db import models


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AdminUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class User(BaseModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()


class ActiveUser(User):
    """Proxy for active users only."""

    objects = ActiveUserManager()

    class Meta:
        proxy = True

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])


class AdminUser(User):
    """Proxy for admin users."""

    objects = AdminUserManager()

    class Meta:
        proxy = True
```

---

## Complex Relations

### Self-referential (Tree Structure)

```python
# apps/catalog/models/category.py
from django.db import models
from core.models import BaseModel


class Category(BaseModel):
    """Hierarchical product category."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    level = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['level', 'name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def get_ancestors(self):
        """Get all parent categories."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return list(reversed(ancestors))

    def get_descendants(self):
        """Get all child categories recursively."""
        descendants = list(self.children.all())
        for child in self.children.all():
            descendants.extend(child.get_descendants())
        return descendants
```

### Many-to-Many with Through Model

```python
# apps/courses/models.py
from django.db import models
from core.models import BaseModel


class Course(BaseModel):
    """Online course."""

    title = models.CharField(max_length=200)
    instructor = models.ForeignKey('users.User', on_delete=models.PROTECT)

    students = models.ManyToManyField(
        'users.User',
        through='Enrollment',
        related_name='enrolled_courses',
    )


class Enrollment(BaseModel):
    """Student enrollment in a course (through model)."""

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)  # Percentage
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        db_table = 'enrollments'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_enrollment',
            ),
            models.CheckConstraint(
                check=models.Q(progress__gte=0) & models.Q(progress__lte=100),
                name='valid_progress',
            ),
        ]

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None
```

---

## Django 5.x Features

### GeneratedField Examples

```python
# apps/products/models.py
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat, Upper


class Product(BaseModel):
    """Product with generated fields."""

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    # Computed: total inventory value
    inventory_value = models.GeneratedField(
        expression=F('price') * F('quantity'),
        output_field=models.DecimalField(max_digits=15, decimal_places=2),
        db_persist=True,
    )

    # Computed: discounted price
    discounted_price = models.GeneratedField(
        expression=F('price') * (1 - F('discount_percent') / 100),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
    )

    # Computed: display code
    display_code = models.GeneratedField(
        expression=Concat(Upper('sku'), Value('-'), F('id')),
        output_field=models.CharField(max_length=100),
        db_persist=False,  # Virtual column
    )
```

### db_default Examples

```python
from django.db import models
from django.db.models.functions import Now, Lower
from django.db.models import Value


class Article(BaseModel):
    """Article with db_default fields."""

    title = models.CharField(max_length=200)

    # Database-computed slug from title
    slug = models.SlugField(
        max_length=200,
        db_default=Lower('title'),
    )

    # Database-computed timestamp
    published_at = models.DateTimeField(
        db_default=Now(),
    )

    # Database-computed default string
    status = models.CharField(
        max_length=20,
        db_default=Value('draft'),
    )

    # Integer with database default
    view_count = models.IntegerField(db_default=0)
```

**Important:** After `save()`, call `refresh_from_db()` to access generated values:

```python
product = Product(name='Widget', price=10.00, quantity=5)
product.save()
product.refresh_from_db()
print(product.inventory_value)  # 50.00
```
