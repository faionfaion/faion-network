# M-PY-002: Django Patterns

## Metadata
- **Category:** Development/Python
- **Difficulty:** Intermediate
- **Tags:** #dev, #python, #django, #methodology
- **Agent:** faion-code-agent

---

## Problem

Django's "batteries included" approach offers many ways to solve problems. Without patterns, codebases become inconsistent, hard to maintain, and difficult to scale. You need established patterns that work.

## Promise

After this methodology, you will write Django code that is consistent, maintainable, and follows community best practices.

## Overview

Django patterns cover project structure, models, views, forms, and common operations. These patterns come from years of community experience.

---

## Framework

### Step 1: Project Structure

```
project/
├── config/                 # Project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py        # Common settings
│   │   ├── local.py       # Development
│   │   ├── production.py  # Production
│   │   └── test.py        # Testing
│   ├── urls.py
│   └── wsgi.py
├── apps/                   # Django apps
│   ├── users/
│   ├── orders/
│   └── products/
├── templates/              # Global templates
├── static/                 # Global static files
├── media/                  # User uploads
├── tests/                  # Integration tests
├── manage.py
└── pyproject.toml
```

### Step 2: Model Patterns

**Base Model:**
```python
# apps/core/models.py
from django.db import models
import uuid

class BaseModel(models.Model):
    """Abstract base model with common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

**Domain Model:**
```python
# apps/products/models.py
from django.db import models
from apps.core.models import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:detail', kwargs={'slug': self.slug})
```

**Manager Pattern:**
```python
class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def expensive(self, threshold=100):
        return self.filter(price__gte=threshold)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

class Product(BaseModel):
    # ... fields ...
    objects = ProductManager()

# Usage
Product.objects.active().expensive(50)
```

### Step 3: View Patterns

**Class-Based Views:**
```python
# apps/products/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.active()

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    slug_url_kwarg = 'slug'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

**API Views (DRF):**
```python
# apps/products/api/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.active()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.get_queryset().filter(is_featured=True)[:5]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
```

### Step 4: Form Patterns

```python
# apps/products/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be positive")
        return price

    def clean(self):
        cleaned_data = super().clean()
        # Cross-field validation
        return cleaned_data
```

### Step 5: Service Layer Pattern

```python
# apps/products/services.py
from django.db import transaction
from .models import Product

class ProductService:
    @staticmethod
    @transaction.atomic
    def create_product(name: str, price: float, **kwargs) -> Product:
        """Create product with validation and side effects."""
        product = Product.objects.create(
            name=name,
            price=price,
            **kwargs
        )
        # Trigger side effects
        ProductService._notify_created(product)
        return product

    @staticmethod
    def _notify_created(product: Product):
        # Send notifications, update caches, etc.
        pass

# Usage in views
from .services import ProductService

product = ProductService.create_product(
    name="Widget",
    price=29.99,
    description="A great widget"
)
```

### Step 6: Signal Patterns

```python
# apps/products/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if created:
        # New product created
        pass
    else:
        # Product updated
        pass

@receiver(pre_delete, sender=Product)
def product_deleting(sender, instance, **kwargs):
    # Cleanup before deletion
    pass
```

```python
# apps/products/apps.py
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    name = 'apps.products'

    def ready(self):
        import apps.products.signals  # noqa
```

---

## Templates

### Settings Split

```python
# config/settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'apps.users',
    'apps.products',
]

# config/settings/local.py
from .base import *

DEBUG = True
SECRET_KEY = 'dev-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# config/settings/production.py
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### URL Patterns

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('products/', include('apps.products.urls', namespace='products')),
]

# apps/products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
]
```

---

## Examples

### Custom User Model

```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

```python
# config/settings/base.py
AUTH_USER_MODEL = 'users.User'
```

### Middleware Pattern

```python
# apps/core/middleware.py
import time
import logging

logger = logging.getLogger(__name__)

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start

        logger.info(f"{request.method} {request.path} - {duration:.2f}s")
        return response
```

---

## Common Mistakes

1. **Fat views** - Move business logic to services
2. **No indexes** - Add indexes for filtered/ordered fields
3. **N+1 queries** - Use `select_related()` and `prefetch_related()`
4. **Hardcoded settings** - Use environment variables
5. **Circular imports** - Use string references in ForeignKey

---

## Checklist

- [ ] Settings split into base/local/production
- [ ] Custom user model before first migration
- [ ] Base model with common fields
- [ ] Custom managers for complex queries
- [ ] Service layer for business logic
- [ ] Signals in separate file
- [ ] URLs with namespaces
- [ ] Database indexes defined

---

## Next Steps

- M-PY-004: Pytest Testing
- M-API-001: REST API Design
- M-DO-003: Docker Basics

---

*Methodology M-PY-002 v1.0*
