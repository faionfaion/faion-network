# pytest-django Templates

Copy-paste configurations and boilerplate for Django testing with pytest.

---

## 1. Configuration Files

### pyproject.toml (Recommended)

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "-ra",
    "--reuse-db",
]
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
testpaths = ["tests"]

[tool.coverage.run]
source = ["apps"]
branch = true
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__init__.py",
    "*/admin.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
fail_under = 80
show_missing = true

[tool.coverage.html]
directory = "htmlcov"
```

### pytest.ini (Alternative)

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py *_test.py
python_functions = test_*
python_classes = Test*
addopts = -v --tb=short --strict-markers -ra --reuse-db
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
filterwarnings =
    ignore::DeprecationWarning
testpaths = tests
```

### setup.cfg (Legacy)

```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
addopts = -v --tb=short --strict-markers

[coverage:run]
source = apps
omit = */migrations/*,*/tests/*
```

---

## 2. Test Settings

### config/settings/test.py

```python
"""
Test settings for Django project.
Optimized for fast test execution.
"""
from .base import *  # noqa: F401, F403

# Debug
DEBUG = False
TEMPLATE_DEBUG = False

# Database - Use in-memory SQLite for speed
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {
            "NAME": ":memory:",
        },
    }
}

# Faster password hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Celery - run tasks synchronously
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Cache - use local memory
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Disable logging during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
        "level": "CRITICAL",
    },
}

# Media files - use temporary directory
import tempfile

MEDIA_ROOT = tempfile.mkdtemp()

# Static files
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Disable CSRF for API tests
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # type: ignore # noqa: F405
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# Stripe test mode (if using)
STRIPE_TEST_MODE = True
STRIPE_SECRET_KEY = "sk_test_fake"

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()
```

### config/settings/test_postgres.py (For CI)

```python
"""
Test settings with PostgreSQL for CI.
Use when testing Postgres-specific features.
"""
from .test import *  # noqa: F401, F403

# Use PostgreSQL in CI
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
        "TEST": {
            "NAME": "test_db",
        },
    }
}

# Enable migrations for Postgres
MIGRATION_MODULES = {}
```

---

## 3. conftest.py Templates

### Root conftest.py

```python
"""
Root conftest.py - Shared fixtures for all tests.
"""
import pytest
from rest_framework.test import APIClient

# Register factories
from pytest_factoryboy import register
from tests.factories.users import UserFactory, AdminUserFactory
from tests.factories.orders import ProductFactory, OrderFactory

register(UserFactory)
register(AdminUserFactory, _name="admin_user")
register(ProductFactory)
register(OrderFactory)


# ============================================================
# API Client Fixtures
# ============================================================

@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated DRF API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client: APIClient, user) -> APIClient:
    """API client authenticated as regular user."""
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def admin_client(api_client: APIClient, admin_user) -> APIClient:
    """API client authenticated as admin user."""
    api_client.force_authenticate(user=admin_user)
    yield api_client
    api_client.force_authenticate(user=None)


# ============================================================
# Database Fixtures
# ============================================================

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Load initial data once per session (optional)."""
    with django_db_blocker.unblock():
        # Load fixtures if needed
        # call_command("loaddata", "categories.json")
        pass


# ============================================================
# Settings Fixtures
# ============================================================

@pytest.fixture
def settings_debug(settings):
    """Enable DEBUG mode for a test."""
    settings.DEBUG = True
    return settings


@pytest.fixture
def settings_no_celery(settings):
    """Disable Celery eager mode for async testing."""
    settings.CELERY_TASK_ALWAYS_EAGER = False
    return settings


# ============================================================
# Utility Fixtures
# ============================================================

@pytest.fixture
def mailoutbox(mailoutbox):
    """Access sent emails (provided by pytest-django)."""
    return mailoutbox
```

### tests/factories/__init__.py

```python
"""
Test factories module.
Import all factories here for easy access.
"""
from .users import UserFactory, AdminUserFactory, ProfileFactory
from .orders import ProductFactory, OrderFactory, OrderItemFactory

__all__ = [
    "UserFactory",
    "AdminUserFactory",
    "ProfileFactory",
    "ProductFactory",
    "OrderFactory",
    "OrderItemFactory",
]
```

### tests/factories/users.py

```python
"""
User-related factories.
"""
import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating regular users."""

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Faker("email")
    name = factory.Faker("name")
    user_type = "regular"
    is_active = True
    is_staff = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "testpass123"
        self.set_password(password)
        if create:
            self.save(update_fields=["password"])


class AdminUserFactory(UserFactory):
    """Factory for creating admin users."""

    user_type = "admin"
    is_staff = True
    is_superuser = True


class ProfileFactory(factory.django.DjangoModelFactory):
    """Factory for user profiles."""

    class Meta:
        model = "users.Profile"  # String reference

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("text", max_nb_chars=200)
    location = factory.Faker("city")
```

### tests/factories/orders.py

```python
"""
Order-related factories.
"""
import factory
from decimal import Decimal


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for products."""

    class Meta:
        model = "products.Product"

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.fuzzy.FuzzyDecimal(10.00, 500.00, precision=2)
    stock = factory.fuzzy.FuzzyInteger(1, 100)
    is_active = True


class OrderFactory(factory.django.DjangoModelFactory):
    """Factory for orders."""

    class Meta:
        model = "orders.Order"

    user = factory.SubFactory("tests.factories.users.UserFactory")
    status = "pending"
    shipping_address = factory.Faker("address")

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        """Create order items if specified."""
        if not create or not extracted:
            return
        for item_data in extracted:
            OrderItemFactory(order=self, **item_data)


class OrderItemFactory(factory.django.DjangoModelFactory):
    """Factory for order items."""

    class Meta:
        model = "orders.OrderItem"

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 5)
    unit_price = factory.LazyAttribute(lambda o: o.product.price)
```

---

## 4. CI/CD Templates

### GitHub Actions (.github/workflows/test.yml)

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: "3.11"
  DJANGO_SETTINGS_MODULE: config.settings.test

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
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

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements/test.txt

      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db
        run: |
          pytest -n auto --cov=apps --cov-report=xml --cov-report=html

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

      - name: Upload coverage HTML
        uses: actions/upload-artifact@v4
        with:
          name: coverage-html
          path: htmlcov/
```

### GitLab CI (.gitlab-ci.yml)

```yaml
stages:
  - test

variables:
  POSTGRES_DB: test_db
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  DATABASE_URL: postgres://postgres:postgres@postgres:5432/test_db
  DJANGO_SETTINGS_MODULE: config.settings.test

test:
  stage: test
  image: python:3.11
  services:
    - postgres:15
  before_script:
    - pip install -r requirements/test.txt
  script:
    - pytest -n auto --cov=apps --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

---

## 5. Test File Templates

### Unit Test Template

```python
"""
Unit tests for {module} service.
"""
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from apps.{module}.services import {Service}
from apps.{module}.exceptions import {Exception}


@pytest.mark.django_db
class Test{Service}:
    """Tests for {Service}."""

    def test_{method}_with_valid_input(self, user, {fixture}):
        """Test happy path for {method}."""
        # Arrange
        # ...

        # Act
        result = {Service}.{method}(...)

        # Assert
        assert result is not None

    def test_{method}_raises_for_invalid_input(self, user):
        """Test error handling for {method}."""
        with pytest.raises({Exception}):
            {Service}.{method}(invalid_param=...)

    @patch("apps.{module}.services.external_service")
    def test_{method}_calls_external_service(self, mock_service, user):
        """Test external service integration."""
        mock_service.return_value = MagicMock(id="123")

        result = {Service}.{method}(...)

        mock_service.assert_called_once()
```

### API Test Template

```python
"""
Integration tests for {resource} API.
"""
import pytest
from rest_framework import status


@pytest.mark.django_db
class Test{Resource}ListAPI:
    """Tests for GET /api/v1/{resources}/."""

    endpoint = "/api/v1/{resources}/"

    def test_requires_authentication(self, api_client):
        """Unauthenticated request returns 401."""
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_list(self, authenticated_client, {resource}_factory):
        """Returns paginated list of {resources}."""
        {resource}_factory.create_batch(3)

        response = authenticated_client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 3


@pytest.mark.django_db
class Test{Resource}CreateAPI:
    """Tests for POST /api/v1/{resources}/."""

    endpoint = "/api/v1/{resources}/"

    def test_creates_with_valid_data(self, admin_client):
        """Creates {resource} with valid payload."""
        payload = {
            # ...
        }

        response = admin_client.post(self.endpoint, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize("field,value,error", [
        ("required_field", "", "This field may not be blank"),
        ("email_field", "invalid", "Enter a valid email"),
    ])
    def test_validation_errors(self, admin_client, field, value, error):
        """Returns validation errors for invalid data."""
        payload = {"field": "value"}
        payload[field] = value

        response = admin_client.post(self.endpoint, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert error in str(response.data)


@pytest.mark.django_db
class Test{Resource}DetailAPI:
    """Tests for GET/PATCH/DELETE /api/v1/{resources}/{uid}/."""

    def test_retrieves_by_uid(self, authenticated_client, {resource}):
        """Retrieves {resource} by UID."""
        response = authenticated_client.get(
            f"/api/v1/{resources}/{{resource}.uid}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["uid"] == str({resource}.uid)

    def test_updates_own_resource(self, authenticated_client, {resource}):
        """User can update their own {resource}."""
        response = authenticated_client.patch(
            f"/api/v1/{resources}/{{resource}.uid}/",
            {"field": "updated"},
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_deletes_resource(self, admin_client, {resource}):
        """Admin can delete {resource}."""
        response = admin_client.delete(
            f"/api/v1/{resources}/{{resource}.uid}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
```

---

## 6. requirements/test.txt

```txt
# Testing
pytest>=8.0.0
pytest-django>=4.8.0
pytest-cov>=4.1.0
pytest-xdist>=3.5.0
pytest-randomly>=3.15.0
pytest-asyncio>=0.23.0
pytest-timeout>=2.2.0

# Factories
factory-boy>=3.3.0
pytest-factoryboy>=2.6.0
Faker>=22.0.0

# Mocking
responses>=0.24.0
requests-mock>=1.11.0
freezegun>=1.4.0

# Code quality (optional but recommended)
coverage>=7.4.0
```

---

## 7. Makefile Commands

```makefile
.PHONY: test test-fast test-cov test-parallel test-unit test-integration

# Run all tests
test:
	pytest

# Run tests with short output
test-fast:
	pytest -q --tb=line

# Run with coverage
test-cov:
	pytest --cov=apps --cov-report=html --cov-report=term-missing

# Run in parallel
test-parallel:
	pytest -n auto

# Run only unit tests
test-unit:
	pytest -m unit

# Run only integration tests
test-integration:
	pytest -m integration

# Run excluding slow tests
test-quick:
	pytest -m "not slow"

# Show slowest tests
test-slow:
	pytest --durations=10

# Rerun failed tests
test-failed:
	pytest --lf

# Run tests matching pattern
test-match:
	pytest -k "$(pattern)"

# Clean test artifacts
test-clean:
	rm -rf .pytest_cache htmlcov .coverage coverage.xml
```

---

## 8. VS Code Settings

### .vscode/settings.json

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--tb=short"
  ],
  "python.testing.cwd": "${workspaceFolder}",
  "python.envFile": "${workspaceFolder}/.env.test"
}
```
