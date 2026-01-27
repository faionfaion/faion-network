# Django Testing Templates

Copy-paste configurations for Django testing setup.

## Table of Contents

1. [pyproject.toml Configuration](#pyprojecttoml-configuration)
2. [pytest.ini Configuration](#pytestini-configuration)
3. [Coverage Configuration](#coverage-configuration)
4. [Testing Settings](#testing-settings)
5. [conftest.py Templates](#conftestpy-templates)
6. [Factory Templates](#factory-templates)
7. [GitHub Actions Workflows](#github-actions-workflows)
8. [Pre-commit Configuration](#pre-commit-configuration)

---

## pyproject.toml Configuration

### Complete Testing Setup

```toml
# pyproject.toml

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
testpaths = ["tests"]
addopts = """
    -v
    --tb=short
    --strict-markers
    --strict-config
    -ra
"""
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "e2e: marks tests as end-to-end tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::PendingDeprecationWarning",
]

[tool.coverage.run]
source = ["."]
branch = true
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/virtualenv/*",
    "manage.py",
    "*/wsgi.py",
    "*/asgi.py",
    "*/settings/*",
    "conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "def __str__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "if settings.DEBUG:",
    "@abstractmethod",
]
show_missing = true
skip_covered = true
fail_under = 80
precision = 2

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

### Minimal Setup

```toml
# pyproject.toml (minimal)

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["test_*.py"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["."]
omit = ["*/migrations/*", "*/tests/*"]

[tool.coverage.report]
fail_under = 70
```

---

## pytest.ini Configuration

### If Not Using pyproject.toml

```ini
# pytest.ini

[pytest]
DJANGO_SETTINGS_MODULE = config.settings.testing
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
testpaths = tests
addopts =
    -v
    --tb=short
    --strict-markers
    -ra

markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

filterwarnings =
    ignore::DeprecationWarning
```

---

## Coverage Configuration

### Standalone .coveragerc

```ini
# .coveragerc

[run]
source = .
branch = True
omit =
    */migrations/*
    */tests/*
    */__pycache__/*
    */venv/*
    manage.py
    */wsgi.py
    */asgi.py
    */settings/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

show_missing = True
skip_covered = True
fail_under = 80

[html]
directory = htmlcov

[xml]
output = coverage.xml
```

---

## Testing Settings

### Complete Testing Settings File

```python
# config/settings/testing.py
"""
Django settings for testing.

Optimized for fast test execution.
"""

from .base import *  # noqa: F401, F403

# Debug off for realistic testing
DEBUG = False
TEMPLATE_DEBUG = False

# Test database - in-memory SQLite for speed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Faster password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable email sending
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Disable throttling
REST_FRAMEWORK = {
    **getattr(globals().get('REST_FRAMEWORK', {}), 'items', lambda: {})(),
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {},
}

# Disable Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Simplified logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
        'level': 'DEBUG',
    },
}

# Media files - temp directory
import tempfile
MEDIA_ROOT = tempfile.mkdtemp()

# Disable migrations for faster tests (optional)
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

# Uncomment to disable migrations (use with caution)
# MIGRATION_MODULES = DisableMigrations()

# Security - relaxed for testing
SECRET_KEY = 'test-secret-key-not-for-production'
ALLOWED_HOSTS = ['*']
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
```

### Minimal Testing Settings

```python
# config/settings/testing.py (minimal)

from .base import *  # noqa

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
```

---

## conftest.py Templates

### Root conftest.py

```python
# conftest.py (project root)
"""
Pytest configuration and fixtures.
"""

import pytest
from rest_framework.test import APIClient
from model_bakery import baker


# ============================================================================
# API Clients
# ============================================================================

@pytest.fixture
def api_client():
    """DRF API client instance."""
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    """API client authenticated as regular user."""
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client


@pytest.fixture
def admin_api_client(api_client, admin_user):
    """API client authenticated as admin."""
    api_client.force_authenticate(user=admin_user)
    api_client.user = admin_user
    return api_client


# ============================================================================
# Django Test Client
# ============================================================================

@pytest.fixture
def authenticated_client(client, user):
    """Django test client logged in as user."""
    client.force_login(user)
    client.user = user
    return client


# ============================================================================
# Users
# ============================================================================

@pytest.fixture
def user(db):
    """Create a regular active user."""
    return baker.make(
        'users.User',
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return baker.make(
        'users.User',
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def inactive_user(db):
    """Create an inactive user."""
    return baker.make(
        'users.User',
        is_active=False,
    )


# ============================================================================
# Factory Boy Registration (if using pytest-factoryboy)
# ============================================================================

# from pytest_factoryboy import register
# from tests.factories import UserFactory, PostFactory
#
# register(UserFactory)
# register(PostFactory)
# register(UserFactory, 'admin', is_staff=True, is_superuser=True)


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Custom database setup.
    Add initial data that should be available for all tests.
    """
    with django_db_blocker.unblock():
        # Add any required initial data
        pass


# ============================================================================
# Settings Overrides
# ============================================================================

@pytest.fixture
def override_settings(settings):
    """
    Fixture to override settings in tests.

    Usage:
        def test_something(override_settings):
            override_settings.DEBUG = True
            ...
    """
    return settings


# ============================================================================
# File Upload Helpers
# ============================================================================

@pytest.fixture
def temp_media_root(settings, tmp_path):
    """Temporary media root for file upload tests."""
    settings.MEDIA_ROOT = str(tmp_path / 'media')
    return settings.MEDIA_ROOT


@pytest.fixture
def sample_image():
    """Create a sample image file for testing."""
    from io import BytesIO
    from PIL import Image
    from django.core.files.uploadedfile import SimpleUploadedFile

    image = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    return SimpleUploadedFile(
        name='test_image.png',
        content=buffer.read(),
        content_type='image/png'
    )


# ============================================================================
# Time Helpers
# ============================================================================

@pytest.fixture
def freeze_time():
    """
    Fixture to freeze time in tests.

    Usage:
        def test_something(freeze_time):
            with freeze_time('2024-01-01 12:00:00'):
                ...
    """
    from freezegun import freeze_time as ft
    return ft


# ============================================================================
# Mocking Helpers
# ============================================================================

@pytest.fixture
def mock_external_api(mocker):
    """
    Mock external API calls.

    Customize for your specific external services.
    """
    mock = mocker.patch('requests.request')
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {}
    return mock
```

### App-Specific conftest.py

```python
# apps/blog/tests/conftest.py
"""
Blog app test fixtures.
"""

import pytest
from model_bakery import baker


@pytest.fixture
def published_post(db, user):
    """Create a published post."""
    return baker.make(
        'blog.Post',
        author=user,
        status='published',
        title='Test Published Post',
    )


@pytest.fixture
def draft_post(db, user):
    """Create a draft post."""
    return baker.make(
        'blog.Post',
        author=user,
        status='draft',
        title='Test Draft Post',
    )


@pytest.fixture
def posts_batch(db, user):
    """Create multiple posts."""
    return baker.make(
        'blog.Post',
        author=user,
        status='published',
        _quantity=10,
    )


@pytest.fixture
def post_with_comments(db, published_post):
    """Create a post with comments."""
    baker.make(
        'blog.Comment',
        post=published_post,
        _quantity=5,
    )
    return published_post
```

---

## Factory Templates

### Complete factories.py

```python
# tests/factories.py
"""
Factory Boy factories for tests.
"""

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone


# ============================================================================
# User Factory
# ============================================================================

class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False

    # Password handling (creates hashed password)
    password = factory.django.Password('testpass123')

    class Params:
        """Traits for user variations."""
        admin = factory.Trait(
            is_staff=True,
            is_superuser=True,
            email=factory.Sequence(lambda n: f'admin{n}@example.com'),
        )
        inactive = factory.Trait(
            is_active=False,
        )
        staff = factory.Trait(
            is_staff=True,
        )


# ============================================================================
# Profile Factory (if User has OneToOne Profile)
# ============================================================================

class ProfileFactory(DjangoModelFactory):
    """Factory for Profile model."""

    class Meta:
        model = 'users.Profile'

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker('paragraph')
    website = factory.Faker('url')


# ============================================================================
# Post Factory
# ============================================================================

class PostFactory(DjangoModelFactory):
    """Factory for Post model."""

    class Meta:
        model = 'blog.Post'

    author = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=6)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    content = factory.Faker('paragraphs', nb=5)
    status = 'draft'
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

    class Params:
        """Traits for post variations."""
        published = factory.Trait(
            status='published',
            published_at=factory.LazyFunction(timezone.now),
        )
        scheduled = factory.Trait(
            status='scheduled',
            published_at=factory.LazyFunction(
                lambda: timezone.now() + timezone.timedelta(days=7)
            ),
        )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """Handle ManyToMany tags field."""
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)


# ============================================================================
# Comment Factory
# ============================================================================

class CommentFactory(DjangoModelFactory):
    """Factory for Comment model."""

    class Meta:
        model = 'blog.Comment'

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('paragraph')
    is_approved = True
    created_at = factory.LazyFunction(timezone.now)

    class Params:
        pending = factory.Trait(is_approved=False)


# ============================================================================
# Tag Factory
# ============================================================================

class TagFactory(DjangoModelFactory):
    """Factory for Tag model."""

    class Meta:
        model = 'blog.Tag'
        django_get_or_create = ('slug',)

    name = factory.Sequence(lambda n: f'Tag {n}')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


# ============================================================================
# Category Factory
# ============================================================================

class CategoryFactory(DjangoModelFactory):
    """Factory for Category model."""

    class Meta:
        model = 'blog.Category'
        django_get_or_create = ('slug',)

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    parent = None

    class Params:
        with_parent = factory.Trait(
            parent=factory.SubFactory('tests.factories.CategoryFactory')
        )


# ============================================================================
# Order Factory (E-commerce example)
# ============================================================================

class ProductFactory(DjangoModelFactory):
    """Factory for Product model."""

    class Meta:
        model = 'shop.Product'

    name = factory.Faker('catch_phrase')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=0, max=100)
    is_active = True


class OrderFactory(DjangoModelFactory):
    """Factory for Order model."""

    class Meta:
        model = 'shop.Order'

    user = factory.SubFactory(UserFactory)
    status = 'pending'
    total = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    created_at = factory.LazyFunction(timezone.now)

    class Params:
        paid = factory.Trait(status='paid')
        shipped = factory.Trait(status='shipped')
        cancelled = factory.Trait(status='cancelled')


class OrderItemFactory(DjangoModelFactory):
    """Factory for OrderItem model."""

    class Meta:
        model = 'shop.OrderItem'

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=5)
    price = factory.SelfAttribute('product.price')


# ============================================================================
# Helper Functions
# ============================================================================

def slugify(text):
    """Simple slugify function."""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')
```

---

## GitHub Actions Workflows

### Complete CI Workflow

```yaml
# .github/workflows/tests.yml

name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  DJANGO_SETTINGS_MODULE: config.settings.testing
  PYTHONUNBUFFERED: 1

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.11', '3.12']

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Load cached venv
        id: cached-poetry-dependencies
        uses: actions/cache@v4
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install dependencies
        if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
        run: poetry install --no-interaction --no-root

      - name: Install project
        run: poetry install --no-interaction

      - name: Run tests with coverage
        run: |
          poetry run pytest \
            --cov=. \
            --cov-report=xml \
            --cov-report=term-missing \
            --junitxml=junit.xml \
            -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
          fail_ci_if_error: true

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.python-version }}
          path: junit.xml
```

### Simple CI Workflow (pip-based)

```yaml
# .github/workflows/tests.yml

name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements/testing.txt

      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

### Coverage Comment on PRs

```yaml
# .github/workflows/coverage.yml

name: Coverage Report

on:
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements/testing.txt

      - name: Run tests with coverage
        run: |
          pytest --cov=. --cov-report=xml --cov-report=term-missing

      - name: Coverage comment
        uses: MishaKav/pytest-coverage-comment@main
        with:
          pytest-xml-coverage-path: coverage.xml
          junitxml-path: junit.xml
```

---

## Pre-commit Configuration

### Pre-commit with Tests

```yaml
# .pre-commit-config.yaml

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs]

  # Run tests on commit (optional - can be slow)
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest
        args: [--tb=short, -q, tests/]
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]
```

---

## requirements/testing.txt

```txt
# requirements/testing.txt

# Test framework
pytest>=8.0.0
pytest-django>=4.8.0
pytest-cov>=4.1.0

# Fixtures
factory-boy>=3.3.0
model-bakery>=1.18.0
faker>=22.0.0

# Coverage
coverage[toml]>=7.4.0

# Optional: parallel execution
pytest-xdist>=3.5.0

# Optional: random test order
pytest-randomly>=3.15.0

# Optional: time freezing
freezegun>=1.4.0

# Optional: mock helpers
pytest-mock>=3.12.0

# Optional: async testing
pytest-asyncio>=0.23.0

# Optional: snapshots
pytest-snapshot>=0.9.0
```

---

*See also: [examples.md](examples.md) for test examples, [llm-prompts.md](llm-prompts.md) for LLM prompts*
