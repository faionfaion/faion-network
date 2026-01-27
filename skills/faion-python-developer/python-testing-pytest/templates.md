# pytest Templates

Copy-paste templates for pytest configurations, fixtures, and test patterns.

---

## Table of Contents

1. [Configuration Templates](#configuration-templates)
2. [Fixture Templates](#fixture-templates)
3. [Test Class Templates](#test-class-templates)
4. [Django Templates](#django-templates)
5. [FastAPI Templates](#fastapi-templates)
6. [CI/CD Templates](#cicd-templates)
7. [Plugin Configurations](#plugin-configurations)

---

## Configuration Templates

### pyproject.toml - Complete Configuration

```toml
[tool.pytest.ini_options]
# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Output
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--strict-config",
    "-ra",  # Show summary of all except passed
]

# Markers
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "e2e: marks tests as end-to-end tests",
]

# Async
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

# Warnings
filterwarnings = [
    "error",
    "ignore::DeprecationWarning",
    "ignore::PendingDeprecationWarning",
]

# Minimum pytest version
minversion = "8.0"

# Timeout (requires pytest-timeout)
timeout = 300

[tool.coverage.run]
source = ["src"]
branch = true
parallel = true
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]

[tool.coverage.paths]
source = ["src"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
    "@overload",
]
fail_under = 80
show_missing = true
skip_covered = true

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

### pytest.ini - Minimal Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
asyncio_mode = auto
```

### Django pyproject.toml

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--reuse-db",
    "--create-db",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["apps"]
branch = true
omit = ["*/migrations/*", "*/tests/*", "*/admin.py"]
```

---

## Fixture Templates

### conftest.py - Base Template

```python
"""
Pytest configuration and shared fixtures.
"""
import pytest
from typing import Generator, Callable, Any


# -----------------------------------------------------------------------------
# Markers
# -----------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks as integration test")


# -----------------------------------------------------------------------------
# Basic Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Sample data for tests."""
    return {
        "name": "Test",
        "email": "test@example.com",
        "value": 100,
    }


@pytest.fixture
def mock_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up test configuration."""
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("DEBUG", "false")


# -----------------------------------------------------------------------------
# Factory Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def data_factory() -> Callable[..., dict[str, Any]]:
    """Factory for creating test data."""
    counter = 0

    def create(
        name: str | None = None,
        email: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        nonlocal counter
        counter += 1
        return {
            "id": counter,
            "name": name or f"Test {counter}",
            "email": email or f"test{counter}@example.com",
            **kwargs,
        }

    return create


# -----------------------------------------------------------------------------
# Database Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="session")
def database_engine():
    """Create database engine for the test session."""
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(database_engine) -> Generator:
    """Fresh database session with rollback."""
    from sqlalchemy.orm import Session

    connection = database_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# -----------------------------------------------------------------------------
# HTTP Client Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def http_client():
    """HTTP client for API testing."""
    import httpx

    with httpx.Client(timeout=30.0) as client:
        yield client


@pytest.fixture
def mock_responses(mocker):
    """Mock HTTP responses."""
    import responses

    with responses.RequestsMock() as rsps:
        yield rsps
```

### conftest.py - Django Template

```python
"""
Django pytest configuration and fixtures.
"""
import pytest
from django.test import Client
from rest_framework.test import APIClient
from pytest_factoryboy import register

from tests.factories import UserFactory, TeamFactory

# Register factories as fixtures
register(UserFactory)
register(TeamFactory)


# -----------------------------------------------------------------------------
# Django Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def client() -> Client:
    """Django test client."""
    return Client()


@pytest.fixture
def api_client() -> APIClient:
    """DRF API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client: APIClient, user) -> APIClient:
    """Authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client: APIClient, admin_user) -> APIClient:
    """Admin authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


# -----------------------------------------------------------------------------
# User Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def user(db, user_factory):
    """Create a default user."""
    return user_factory()


@pytest.fixture
def admin_user(db, user_factory):
    """Create an admin user."""
    return user_factory(is_staff=True, is_superuser=True)


@pytest.fixture
def user_with_team(db, user_factory, team_factory):
    """Create a user with a team."""
    user = user_factory()
    team = team_factory(owner=user)
    return user, team


# -----------------------------------------------------------------------------
# Settings Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def settings(settings):
    """Override Django settings for tests."""
    settings.DEBUG = False
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    return settings


@pytest.fixture
def celery_eager(settings):
    """Run Celery tasks synchronously."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
```

### conftest.py - Async/FastAPI Template

```python
"""
Async pytest configuration and fixtures.
"""
import pytest
import pytest_asyncio
import httpx
from typing import AsyncGenerator


# -----------------------------------------------------------------------------
# Async Fixtures
# -----------------------------------------------------------------------------


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Async HTTP client."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client


@pytest_asyncio.fixture
async def app_client(app) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Async client for FastAPI app."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def database():
    """Async database setup."""
    from app.database import async_engine, Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(database):
    """Async database session with rollback."""
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession(database) as session:
        async with session.begin():
            yield session
            await session.rollback()


# -----------------------------------------------------------------------------
# Mock Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def mock_redis(mocker):
    """Mock Redis client."""
    mock = mocker.AsyncMock()
    mock.get = mocker.AsyncMock(return_value=None)
    mock.set = mocker.AsyncMock(return_value=True)
    mock.delete = mocker.AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_external_api(mocker):
    """Mock external API calls."""

    async def mock_fetch(*args, **kwargs):
        return {"status": "ok", "data": []}

    return mocker.patch(
        "app.services.external_api.fetch",
        new_callable=mocker.AsyncMock,
        side_effect=mock_fetch,
    )
```

---

## Test Class Templates

### Unit Test Template

```python
"""
Unit tests for UserService.
"""
import pytest
from unittest.mock import MagicMock

from app.services import UserService
from app.exceptions import ValidationError, NotFoundError


class TestUserServiceCreate:
    """Tests for UserService.create method."""

    def test_create_with_valid_data_returns_user(self, mocker):
        # Arrange
        mock_repo = mocker.Mock()
        mock_repo.save.return_value = MagicMock(id=1, email="test@example.com")
        service = UserService(repository=mock_repo)

        # Act
        result = service.create(email="test@example.com", name="Test User")

        # Assert
        assert result.id == 1
        assert result.email == "test@example.com"
        mock_repo.save.assert_called_once()

    def test_create_with_invalid_email_raises_error(self, mocker):
        # Arrange
        mock_repo = mocker.Mock()
        service = UserService(repository=mock_repo)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.create(email="invalid", name="Test User")

        assert "email" in str(exc_info.value).lower()
        mock_repo.save.assert_not_called()

    @pytest.mark.parametrize(
        "email,expected_valid",
        [
            ("user@example.com", True),
            ("user.name@domain.co.uk", True),
            ("invalid", False),
            ("", False),
            (None, False),
        ],
    )
    def test_email_validation(self, email, expected_valid, mocker):
        # Arrange
        mock_repo = mocker.Mock()
        service = UserService(repository=mock_repo)

        # Act & Assert
        if expected_valid:
            mock_repo.save.return_value = MagicMock(email=email)
            result = service.create(email=email, name="Test")
            assert result.email == email
        else:
            with pytest.raises(ValidationError):
                service.create(email=email, name="Test")


class TestUserServiceGet:
    """Tests for UserService.get method."""

    def test_get_existing_user_returns_user(self, mocker):
        # Arrange
        mock_repo = mocker.Mock()
        mock_repo.get_by_id.return_value = MagicMock(id=1, email="test@example.com")
        service = UserService(repository=mock_repo)

        # Act
        result = service.get(user_id=1)

        # Assert
        assert result.id == 1
        mock_repo.get_by_id.assert_called_once_with(1)

    def test_get_nonexistent_user_raises_not_found(self, mocker):
        # Arrange
        mock_repo = mocker.Mock()
        mock_repo.get_by_id.return_value = None
        service = UserService(repository=mock_repo)

        # Act & Assert
        with pytest.raises(NotFoundError):
            service.get(user_id=999)
```

### Integration Test Template

```python
"""
Integration tests for User API.
"""
import pytest
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.integration
class TestUserAPI:
    """Integration tests for /api/users/ endpoints."""

    # -------------------------------------------------------------------------
    # List Tests
    # -------------------------------------------------------------------------

    def test_list_returns_all_users(self, authenticated_client, user_factory):
        user_factory.create_batch(3)

        response = authenticated_client.get("/api/users/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_list_filters_by_status(self, authenticated_client, user_factory):
        user_factory(is_active=True)
        user_factory(is_active=False)

        response = authenticated_client.get("/api/users/?is_active=true")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_list_requires_authentication(self, api_client):
        response = api_client.get("/api/users/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -------------------------------------------------------------------------
    # Create Tests
    # -------------------------------------------------------------------------

    def test_create_with_valid_data(self, authenticated_client):
        data = {
            "email": "new@example.com",
            "name": "New User",
            "password": "SecurePass123!",
        }

        response = authenticated_client.post("/api/users/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "new@example.com"
        assert "password" not in response.data  # Password not returned

    def test_create_with_duplicate_email_fails(
        self, authenticated_client, user_factory
    ):
        existing = user_factory(email="existing@example.com")

        response = authenticated_client.post(
            "/api/users/",
            {
                "email": existing.email,
                "name": "Another User",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    # -------------------------------------------------------------------------
    # Retrieve Tests
    # -------------------------------------------------------------------------

    def test_retrieve_returns_user_details(self, authenticated_client, user):
        response = authenticated_client.get(f"/api/users/{user.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.id
        assert response.data["email"] == user.email

    def test_retrieve_nonexistent_returns_404(self, authenticated_client):
        response = authenticated_client.get("/api/users/99999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # -------------------------------------------------------------------------
    # Update Tests
    # -------------------------------------------------------------------------

    def test_update_user_details(self, authenticated_client, user):
        response = authenticated_client.patch(
            f"/api/users/{user.id}/",
            {"name": "Updated Name"},
        )

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.name == "Updated Name"

    # -------------------------------------------------------------------------
    # Delete Tests
    # -------------------------------------------------------------------------

    def test_delete_user(self, authenticated_client, user_factory):
        from apps.users.models import User

        user = user_factory()
        user_id = user.id

        response = authenticated_client.delete(f"/api/users/{user_id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user_id).exists()
```

---

## Django Templates

### factories.py - Factory Boy Template

```python
"""
Factory Boy factories for test data.
"""
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password

from apps.users.models import User
from apps.teams.models import Team, Membership


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True
    is_staff = False

    @factory.lazy_attribute
    def password(self):
        return make_password("testpass123")

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for group in extracted:
            self.groups.add(group)


class TeamFactory(DjangoModelFactory):
    """Factory for Team model."""

    class Meta:
        model = Team

    name = factory.Sequence(lambda n: f"Team {n}")
    description = factory.Faker("paragraph")
    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                Membership.objects.create(team=self, user=user)


class MembershipFactory(DjangoModelFactory):
    """Factory for Team Membership."""

    class Meta:
        model = Membership

    team = factory.SubFactory(TeamFactory)
    user = factory.SubFactory(UserFactory)
    role = "member"
```

### settings/test.py - Test Settings Template

```python
"""
Django test settings.
"""
from .base import *  # noqa: F401, F403

# Faster password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# In-memory database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Logging
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
    },
}
```

---

## FastAPI Templates

### conftest.py - FastAPI Template

```python
"""
FastAPI pytest configuration.
"""
import pytest
import pytest_asyncio
import httpx
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings


# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """Create database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    """Database session with rollback."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Test client with database override."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def authenticated_client(client, user) -> httpx.AsyncClient:
    """Authenticated test client."""
    from app.auth import create_access_token

    token = create_access_token({"sub": str(user.id)})
    client.headers["Authorization"] = f"Bearer {token}"
    return client
```

---

## CI/CD Templates

### GitHub Actions - pytest.yml

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: "3.12"

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
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
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379/0
        run: |
          pytest -n auto --cov=src --cov-report=xml --junitxml=junit.xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: true

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: junit.xml
```

### Makefile Template

```makefile
.PHONY: test test-cov test-fast test-parallel lint format

# Run all tests
test:
	pytest -v

# Run tests with coverage
test-cov:
	pytest --cov=src --cov-report=html --cov-report=term-missing

# Run fast tests only (skip slow and integration)
test-fast:
	pytest -v -m "not slow and not integration"

# Run tests in parallel
test-parallel:
	pytest -n auto

# Run specific test file
test-file:
	pytest -v $(FILE)

# Run tests and stop on first failure
test-x:
	pytest -x

# Run only failed tests
test-failed:
	pytest --lf

# Debug mode
test-debug:
	pytest --pdb -x -s

# Show slowest tests
test-slow:
	pytest --durations=10

# Lint
lint:
	ruff check src tests
	mypy src

# Format
format:
	ruff check --fix src tests
	ruff format src tests

# All checks
check: lint test
```

---

## Plugin Configurations

### pytest-timeout Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
timeout = 300  # 5 minutes default
timeout_method = "signal"  # or "thread" for Windows

# In tests:
# @pytest.mark.timeout(60)  # Override for specific test
```

### pytest-randomly Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "-p randomly"

# CLI options:
# --randomly-seed=12345  # Reproducible order
# --randomly-dont-shuffle  # Disable shuffling
# -p no:randomly  # Disable plugin
```

### pytest-xdist Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "-n auto --dist loadscope"

# Distribution modes:
# --dist load      # Default, load balance
# --dist loadscope # Group by module/class
# --dist loadfile  # Group by file
# --dist worksteal # Reassign from slow workers
```

### pytest-sugar Configuration

```toml
# pyproject.toml - just install, no config needed
# pip install pytest-sugar

# Disable with:
# pytest -p no:sugar
```

---

*pytest Templates v2.0*
