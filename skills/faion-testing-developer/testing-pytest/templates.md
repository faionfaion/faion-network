# pytest Templates

Copy-paste templates for pytest configuration, fixtures, and common patterns.

---

## Configuration Templates

### pyproject.toml - Complete Configuration

```toml
# pyproject.toml

[tool.pytest.ini_options]
# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Execution options
addopts = [
    "-ra",                    # Show extra test summary for all except passed
    "-q",                     # Quiet mode
    "--strict-markers",       # Error on unknown markers
    "--strict-config",        # Error on config issues
    "--import-mode=importlib",# Better import handling
    "--tb=short",             # Shorter traceback
]

# Markers
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: integration tests requiring external services",
    "e2e: end-to-end tests",
    "unit: unit tests",
    "smoke: smoke tests for quick validation",
    "requires_db: tests requiring database connection",
    "requires_redis: tests requiring Redis connection",
]

# Async configuration (pytest-asyncio)
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

# Logging
log_cli = true
log_cli_level = "WARNING"
log_cli_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"

# Warnings
filterwarnings = [
    "error",                              # Treat warnings as errors
    "ignore::DeprecationWarning",         # Ignore deprecations
    "ignore::PendingDeprecationWarning",
]

# Minimum version
minversion = "8.0"


[tool.coverage.run]
branch = true
source = ["src"]
omit = [
    "tests/*",
    "*/__init__.py",
    "*/migrations/*",
    "*/_version.py",
]
parallel = true  # For pytest-xdist

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
    "@abc.abstractmethod",
]
fail_under = 80
show_missing = true
skip_covered = true
precision = 2

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

### pyproject.toml - Minimal Configuration

```toml
# pyproject.toml - Minimal

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-ra", "--strict-markers"]
markers = [
    "slow: slow tests",
    "integration: integration tests",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
```

### pytest.ini (Legacy)

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -ra --strict-markers --tb=short
markers =
    slow: marks tests as slow
    integration: integration tests
    e2e: end-to-end tests
asyncio_mode = auto
filterwarnings =
    error
    ignore::DeprecationWarning
```

### .coveragerc (Standalone Coverage Config)

```ini
# .coveragerc
[run]
branch = True
source = src
omit =
    tests/*
    */__init__.py
    */migrations/*
parallel = True

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if TYPE_CHECKING:
    @abstractmethod
fail_under = 80
show_missing = True

[html]
directory = htmlcov

[xml]
output = coverage.xml
```

---

## conftest.py Templates

### Basic conftest.py

```python
# tests/conftest.py
"""
Shared fixtures for all tests.

Fixtures are automatically discovered by pytest.
"""
import pytest
from typing import Generator


# ============================================
# Environment Setup
# ============================================

@pytest.fixture(autouse=True)
def set_test_environment(monkeypatch) -> Generator[None, None, None]:
    """Set test environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    yield


# ============================================
# Database Fixtures
# ============================================

@pytest.fixture(scope="session")
def db_engine():
    """Create database engine (session scope)."""
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    """Database session with transaction rollback."""
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


# ============================================
# Factory Fixtures
# ============================================

@pytest.fixture
def user_factory(db_session):
    """Factory for creating test users."""
    from myapp.models import User

    counter = 0

    def _create(**kwargs):
        nonlocal counter
        counter += 1
        defaults = {
            "name": f"User {counter}",
            "email": f"user{counter}@example.com",
            "is_active": True,
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db_session.add(user)
        db_session.commit()
        return user

    return _create


# ============================================
# Common Test Data
# ============================================

@pytest.fixture
def sample_user(user_factory):
    """Pre-created sample user."""
    return user_factory(name="Test User", email="test@example.com")


# ============================================
# Mock Fixtures
# ============================================

@pytest.fixture
def mock_external_api(mocker):
    """Mock external API calls."""
    mock = mocker.patch("myapp.client.external_api")
    mock.return_value = {"status": "ok"}
    return mock
```

### conftest.py with Async Support

```python
# tests/conftest.py
"""Async-aware test configuration."""
import pytest
import asyncio
from typing import AsyncGenerator


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session-scoped async fixtures."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_db_pool():
    """Async database connection pool."""
    import asyncpg
    pool = await asyncpg.create_pool(
        "postgresql://test:test@localhost/test_db",
        min_size=2,
        max_size=10,
    )
    yield pool
    await pool.close()


@pytest.fixture
async def async_db(async_db_pool) -> AsyncGenerator:
    """Async database connection with transaction."""
    async with async_db_pool.acquire() as conn:
        tr = conn.transaction()
        await tr.start()
        yield conn
        await tr.rollback()


@pytest.fixture
async def async_client():
    """Async HTTP client."""
    import httpx
    async with httpx.AsyncClient() as client:
        yield client
```

### conftest.py for pytest-xdist

```python
# tests/conftest.py
"""Configuration for parallel test execution."""
import pytest


@pytest.fixture(scope="session")
def worker_id(request):
    """Get xdist worker ID or 'master' if not parallel."""
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    return "master"


@pytest.fixture(scope="session")
def database_url(worker_id):
    """Unique database per worker."""
    if worker_id == "master":
        return "postgresql://test@localhost/test_db"
    return f"postgresql://test@localhost/test_db_{worker_id}"


@pytest.fixture(scope="session")
def redis_db(worker_id):
    """Unique Redis DB per worker."""
    if worker_id == "master":
        return 15
    # Extract number from worker_id like "gw0", "gw1"
    worker_num = int(worker_id.replace("gw", ""))
    return 10 + worker_num  # DB 10, 11, 12, etc.
```

### conftest.py for Django

```python
# tests/conftest.py
"""Django test configuration."""
import pytest


@pytest.fixture(scope="session")
def django_db_setup():
    """Configure Django test database."""
    from django.conf import settings
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }


@pytest.fixture
def api_client():
    """Django REST framework API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user_factory):
    """Authenticated API client."""
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, user_factory):
    """Admin-authenticated API client."""
    admin = user_factory(is_staff=True, is_superuser=True)
    api_client.force_authenticate(user=admin)
    return api_client
```

### conftest.py for FastAPI

```python
# tests/conftest.py
"""FastAPI test configuration."""
import pytest
from typing import Generator
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def app():
    """FastAPI application instance."""
    from myapp.main import create_app
    return create_app()


@pytest.fixture
def client(app) -> Generator:
    """Synchronous test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client(app):
    """Async test client."""
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def auth_headers(user_factory):
    """Authorization headers with valid token."""
    from myapp.auth import create_access_token
    user = user_factory()
    token = create_access_token(user.id)
    return {"Authorization": f"Bearer {token}"}
```

---

## Fixture Templates

### Factory Pattern

```python
@pytest.fixture
def entity_factory(db_session):
    """
    Generic factory fixture pattern.

    Usage:
        def test_example(entity_factory):
            entity = entity_factory(name="Custom Name")
    """
    from myapp.models import Entity

    created = []
    counter = 0

    def _create(**kwargs):
        nonlocal counter
        counter += 1

        # Default values
        defaults = {
            "name": f"Entity {counter}",
            "created_at": datetime.utcnow(),
            "is_active": True,
        }

        # Override with provided kwargs
        defaults.update(kwargs)

        # Create and persist
        entity = Entity(**defaults)
        db_session.add(entity)
        db_session.commit()
        created.append(entity)
        return entity

    yield _create

    # Cleanup
    for entity in created:
        db_session.delete(entity)
    db_session.commit()
```

### Builder Pattern

```python
@pytest.fixture
def order_builder(db_session, user_factory, product_factory):
    """
    Builder pattern for complex entities.

    Usage:
        order = (order_builder
            .with_customer(name="John")
            .with_items([{"product": "Widget", "qty": 2}])
            .with_status("paid")
            .build())
    """
    class OrderBuilder:
        def __init__(self):
            self._customer = None
            self._items = []
            self._status = "pending"
            self._discount = 0

        def with_customer(self, **kwargs):
            self._customer = user_factory(**kwargs)
            return self

        def with_items(self, items):
            for item in items:
                product = product_factory(name=item.get("product", "Product"))
                self._items.append({
                    "product": product,
                    "quantity": item.get("qty", 1),
                })
            return self

        def with_status(self, status):
            self._status = status
            return self

        def with_discount(self, discount):
            self._discount = discount
            return self

        def build(self):
            from myapp.models import Order, OrderItem

            if not self._customer:
                self._customer = user_factory()

            if not self._items:
                product = product_factory()
                self._items = [{"product": product, "quantity": 1}]

            order = Order(
                customer=self._customer,
                status=self._status,
                discount=self._discount,
            )
            db_session.add(order)

            for item in self._items:
                order_item = OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
                db_session.add(order_item)

            db_session.commit()
            return order

    return OrderBuilder()
```

### Context Manager Fixture

```python
@pytest.fixture
def temp_directory():
    """
    Temporary directory that auto-cleans.

    Usage:
        def test_files(temp_directory):
            file_path = temp_directory / "test.txt"
            file_path.write_text("content")
    """
    import tempfile
    import shutil
    from pathlib import Path

    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def capture_logs():
    """
    Capture log messages during test.

    Usage:
        def test_logging(capture_logs):
            do_something_that_logs()
            assert "Expected message" in capture_logs.text
    """
    import logging
    from io import StringIO

    class LogCapture:
        def __init__(self):
            self.stream = StringIO()
            self.handler = logging.StreamHandler(self.stream)
            self.handler.setLevel(logging.DEBUG)

        @property
        def text(self):
            return self.stream.getvalue()

        def clear(self):
            self.stream.truncate(0)
            self.stream.seek(0)

    capture = LogCapture()
    root_logger = logging.getLogger()
    root_logger.addHandler(capture.handler)

    yield capture

    root_logger.removeHandler(capture.handler)
```

---

## Test Class Templates

### Standard Test Class

```python
class TestUserService:
    """Tests for UserService."""

    # ============================================
    # Fixtures
    # ============================================

    @pytest.fixture
    def service(self, db_session):
        """UserService instance."""
        from myapp.services import UserService
        return UserService(db_session)

    @pytest.fixture
    def valid_user_data(self):
        """Valid user creation data."""
        return {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123!",
        }

    # ============================================
    # Create User Tests
    # ============================================

    def test_create_user_with_valid_data_succeeds(self, service, valid_user_data):
        # Act
        user = service.create(valid_user_data)

        # Assert
        assert user.id is not None
        assert user.name == valid_user_data["name"]
        assert user.email == valid_user_data["email"]

    def test_create_user_with_duplicate_email_raises_error(
        self, service, valid_user_data
    ):
        # Arrange
        service.create(valid_user_data)

        # Act & Assert
        with pytest.raises(ValueError, match="Email already exists"):
            service.create(valid_user_data)

    @pytest.mark.parametrize("invalid_email", [
        "",
        "invalid",
        "@example.com",
        "user@",
    ])
    def test_create_user_with_invalid_email_raises_error(
        self, service, valid_user_data, invalid_email
    ):
        valid_user_data["email"] = invalid_email

        with pytest.raises(ValueError, match="Invalid email"):
            service.create(valid_user_data)

    # ============================================
    # Get User Tests
    # ============================================

    def test_get_user_by_id_returns_user(self, service, valid_user_data):
        created = service.create(valid_user_data)

        user = service.get_by_id(created.id)

        assert user.id == created.id

    def test_get_nonexistent_user_returns_none(self, service):
        user = service.get_by_id(99999)

        assert user is None

    # ============================================
    # Update User Tests
    # ============================================

    def test_update_user_changes_fields(self, service, valid_user_data):
        user = service.create(valid_user_data)

        updated = service.update(user.id, {"name": "Jane Doe"})

        assert updated.name == "Jane Doe"
        assert updated.email == valid_user_data["email"]  # Unchanged

    # ============================================
    # Delete User Tests
    # ============================================

    def test_delete_user_removes_from_database(self, service, valid_user_data):
        user = service.create(valid_user_data)

        service.delete(user.id)

        assert service.get_by_id(user.id) is None
```

### Async Test Class

```python
class TestAsyncUserService:
    """Async tests for UserService."""

    @pytest.fixture
    async def service(self, async_db):
        from myapp.async_services import AsyncUserService
        return AsyncUserService(async_db)

    @pytest.mark.asyncio
    async def test_create_user_async(self, service):
        user = await service.create({
            "name": "Async User",
            "email": "async@example.com",
        })

        assert user.id is not None

    @pytest.mark.asyncio
    async def test_batch_create_users(self, service):
        import asyncio

        users_data = [
            {"name": f"User {i}", "email": f"user{i}@example.com"}
            for i in range(10)
        ]

        users = await asyncio.gather(*[
            service.create(data) for data in users_data
        ])

        assert len(users) == 10
```

---

## Marker Templates

### conftest.py Marker Registration

```python
# tests/conftest.py

def pytest_configure(config):
    """Register custom markers."""
    markers = [
        "slow: marks tests as slow running",
        "integration: integration tests requiring external services",
        "e2e: end-to-end tests",
        "unit: unit tests",
        "smoke: smoke tests for quick validation",
        "regression: regression tests",
        "security: security-related tests",
        "performance: performance tests",
        "requires_db: tests requiring database",
        "requires_redis: tests requiring Redis",
        "requires_network: tests requiring network access",
        "flaky: known flaky tests",
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)
```

### Conditional Skip Markers

```python
import pytest
import sys
import os


# Skip based on Python version
requires_python_311 = pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="Requires Python 3.11+"
)

# Skip based on environment
ci_only = pytest.mark.skipif(
    not os.environ.get("CI"),
    reason="Only runs in CI"
)

local_only = pytest.mark.skipif(
    os.environ.get("CI"),
    reason="Only runs locally"
)

# Skip based on platform
linux_only = pytest.mark.skipif(
    sys.platform != "linux",
    reason="Linux only"
)


# Usage:
@requires_python_311
def test_task_group():
    pass


@ci_only
def test_deployment():
    pass
```

---

## CI/CD Templates

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-report=html -n auto

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
          fail_ci_if_error: true

      - name: Upload HTML coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report-${{ matrix.python-version }}
          path: htmlcov/


  # Separate job for slow/integration tests
  integration:
    runs-on: ubuntu-latest
    needs: test  # Run after unit tests pass

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
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

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run integration tests
        run: |
          pytest -m integration --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
```

### GitLab CI Configuration

```yaml
# .gitlab-ci.yml
stages:
  - test
  - coverage

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/

unit-tests:
  stage: test
  image: python:3.11
  script:
    - pip install -e ".[dev]"
    - pytest tests/unit -n auto --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml

integration-tests:
  stage: test
  image: python:3.11
  services:
    - postgres:15
    - redis:7
  variables:
    DATABASE_URL: postgresql://test:test@postgres/test
    REDIS_URL: redis://redis:6379
  script:
    - pip install -e ".[dev]"
    - pytest tests/integration -m integration

coverage:
  stage: coverage
  image: python:3.11
  script:
    - pip install -e ".[dev]"
    - pytest --cov=src --cov-report=html --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    paths:
      - htmlcov/
```

---

## Makefile Commands

```makefile
# Makefile
.PHONY: test test-unit test-integration test-cov test-fast test-watch

# Run all tests
test:
	pytest

# Run unit tests only
test-unit:
	pytest tests/unit -v

# Run integration tests only
test-integration:
	pytest tests/integration -m integration -v

# Run with coverage
test-cov:
	pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report: htmlcov/index.html"

# Run fast (parallel, no slow tests)
test-fast:
	pytest -n auto -m "not slow" -q

# Run in watch mode (requires pytest-watch)
test-watch:
	ptw -- -v

# Run specific test file
test-file:
	pytest $(FILE) -v

# Run tests matching pattern
test-match:
	pytest -k "$(PATTERN)" -v

# Run failed tests from last run
test-failed:
	pytest --lf -v

# Run with debugger on failure
test-debug:
	pytest --pdb -x

# Generate coverage badge (requires coverage-badge)
coverage-badge:
	pytest --cov=src --cov-report=xml
	coverage-badge -o coverage.svg
```

---

*Templates based on pytest 8.x best practices (2025-2026)*
