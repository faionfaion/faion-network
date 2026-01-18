# M-PY-004: Pytest Testing

## Metadata
- **Category:** Development/Python
- **Difficulty:** Intermediate
- **Tags:** #dev, #python, #testing, #methodology
- **Agent:** faion-test-agent

---

## Problem

Writing tests is easy. Writing good tests is hard. Poor tests give false confidence, run slowly, and break when you refactor. You need a testing strategy that catches bugs without slowing you down.

## Promise

After this methodology, you will write tests that are fast, reliable, and maintainable. Your tests will catch real bugs and survive refactoring.

## Overview

Pytest is Python's most powerful testing framework. It uses fixtures for setup, parametrize for data-driven tests, and plugins for everything else.

---

## Framework

### Step 1: Project Setup

```bash
# Install pytest and plugins
poetry add --group dev pytest pytest-cov pytest-asyncio pytest-mock httpx

# Create test structure
mkdir -p tests/{unit,integration,e2e}
touch tests/__init__.py tests/conftest.py
```

**Test structure:**
```
tests/
├── __init__.py
├── conftest.py           # Global fixtures
├── unit/                 # Fast, isolated tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── integration/          # Tests with real dependencies
│   ├── __init__.py
│   └── test_api.py
└── e2e/                  # End-to-end tests
    ├── __init__.py
    └── test_workflows.py
```

### Step 2: Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["app"]
branch = true
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

### Step 3: Fixtures

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

# Simple fixture
@pytest.fixture
def user_id():
    return uuid4()

# Factory fixture
@pytest.fixture
def make_user():
    def _make_user(email: str = "test@example.com", **kwargs):
        defaults = {
            "id": uuid4(),
            "email": email,
            "full_name": "Test User",
            "is_active": True,
        }
        defaults.update(kwargs)
        return User(**defaults)
    return _make_user

# Async fixture
@pytest.fixture
async def db_session():
    # Setup
    async with async_session() as session:
        yield session
        # Teardown - rollback
        await session.rollback()

# Mock fixture
@pytest.fixture
def mock_user_repository():
    repository = AsyncMock()
    repository.get_by_id.return_value = None
    repository.get_by_email.return_value = None
    return repository

# Scoped fixture (once per module)
@pytest.fixture(scope="module")
def expensive_resource():
    # Created once, shared across tests in module
    resource = create_expensive_resource()
    yield resource
    resource.cleanup()
```

### Step 4: Unit Tests

```python
# tests/unit/test_services.py
import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse

class TestUserService:
    """Unit tests for UserService."""

    @pytest.fixture
    def service(self, mock_user_repository):
        return UserService(mock_user_repository)

    async def test_create_user_success(self, service, mock_user_repository):
        # Arrange
        user_in = UserCreate(email="new@example.com", password="password123")
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.create.return_value = User(
            id=uuid4(),
            email=user_in.email,
            full_name=None,
            is_active=True,
        )

        # Act
        result = await service.create_user(user_in)

        # Assert
        assert result.email == user_in.email
        mock_user_repository.create.assert_called_once()

    async def test_create_user_duplicate_email(self, service, mock_user_repository):
        # Arrange
        user_in = UserCreate(email="existing@example.com", password="password123")
        mock_user_repository.get_by_email.return_value = User(
            id=uuid4(),
            email=user_in.email,
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await service.create_user(user_in)

        assert exc_info.value.status_code == 400
        assert "already registered" in exc_info.value.detail
```

### Step 5: Parametrized Tests

```python
# tests/unit/test_validators.py
import pytest
from app.validators import validate_email, validate_password

class TestValidators:

    @pytest.mark.parametrize("email,expected", [
        ("valid@example.com", True),
        ("user.name@domain.co.uk", True),
        ("invalid", False),
        ("@nodomain.com", False),
        ("spaces @domain.com", False),
        ("", False),
    ])
    def test_validate_email(self, email, expected):
        assert validate_email(email) == expected

    @pytest.mark.parametrize("password,is_valid,reason", [
        ("short", False, "too short"),
        ("nouppercase123", False, "no uppercase"),
        ("NOLOWERCASE123", False, "no lowercase"),
        ("NoNumbers", False, "no numbers"),
        ("ValidPass123", True, None),
    ])
    def test_validate_password(self, password, is_valid, reason):
        result = validate_password(password)
        assert result.is_valid == is_valid
        if reason:
            assert reason in result.message.lower()
```

### Step 6: Integration Tests

```python
# tests/integration/test_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

class TestUserAPI:
    """Integration tests for User API."""

    async def test_create_user(self, client):
        # Act
        response = await client.post(
            "/api/v1/users/",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123",
            }
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "password" not in data  # Sensitive data excluded

    async def test_create_user_invalid_email(self, client):
        response = await client.post(
            "/api/v1/users/",
            json={
                "email": "invalid-email",
                "password": "SecurePass123",
            }
        )

        assert response.status_code == 422  # Validation error

    async def test_get_user_unauthorized(self, client):
        response = await client.get("/api/v1/users/me")

        assert response.status_code == 401

    @pytest.mark.parametrize("endpoint", [
        "/api/v1/users/",
        "/api/v1/products/",
    ])
    async def test_endpoints_return_json(self, client, endpoint):
        response = await client.get(endpoint)
        assert response.headers["content-type"] == "application/json"
```

### Step 7: Test Database

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.base import Base
from app.database import get_session
from app.main import app

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_engine):
    async_session = async_sessionmaker(test_engine, class_=AsyncSession)
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    """Client with test database."""
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
```

### Step 8: Mocking

```python
# tests/unit/test_email_service.py
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from app.services.email import EmailService

class TestEmailService:

    @patch("app.services.email.smtplib.SMTP")
    def test_send_email(self, mock_smtp):
        # Setup mock
        mock_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_instance

        # Act
        service = EmailService()
        result = service.send("to@example.com", "Subject", "Body")

        # Assert
        assert result is True
        mock_instance.sendmail.assert_called_once()

    @patch("app.services.email.external_api")
    async def test_async_external_call(self, mock_api):
        mock_api.fetch.return_value = {"data": "value"}

        result = await service.process()

        mock_api.fetch.assert_awaited_once()

    def test_with_pytest_mock(self, mocker):
        # pytest-mock provides cleaner API
        mock_func = mocker.patch("app.module.function")
        mock_func.return_value = "mocked"

        result = function_under_test()

        assert result == "mocked"
```

---

## Templates

### Test File Template

```python
"""Tests for {module}."""
import pytest
from unittest.mock import AsyncMock

from app.{module} import {Class}


class Test{Class}:
    """Tests for {Class}."""

    @pytest.fixture
    def instance(self):
        """Create instance under test."""
        return {Class}()

    # Happy path tests
    async def test_{method}_success(self, instance):
        """Test {method} with valid input."""
        # Arrange

        # Act
        result = await instance.{method}()

        # Assert
        assert result is not None

    # Edge cases
    async def test_{method}_empty_input(self, instance):
        """Test {method} with empty input."""
        pass

    # Error cases
    async def test_{method}_raises_on_invalid(self, instance):
        """Test {method} raises exception on invalid input."""
        with pytest.raises(ValueError):
            await instance.{method}(invalid_input)
```

### Makefile Commands

```makefile
.PHONY: test test-cov test-unit test-integration

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov --cov-report=term-missing --cov-report=html

test-unit:
	poetry run pytest tests/unit -v

test-integration:
	poetry run pytest tests/integration -v --slow

test-watch:
	poetry run pytest-watch
```

---

## Examples

### Testing Async Code

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected

# With pytest-asyncio auto mode, @pytest.mark.asyncio not needed
async def test_auto_async():
    result = await async_function()
    assert result == expected
```

### Testing Exceptions

```python
def test_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        raise_value_error()

    assert "expected message" in str(exc_info.value)

def test_raises_specific_exception():
    with pytest.raises(CustomException, match="pattern"):
        function_that_raises()
```

### Testing Time-Dependent Code

```python
from freezegun import freeze_time

@freeze_time("2026-01-01 12:00:00")
def test_time_dependent():
    result = get_current_timestamp()
    assert result == "2026-01-01T12:00:00"
```

---

## Common Mistakes

1. **Testing implementation, not behavior** - Test what, not how
2. **Flaky tests** - Isolate tests, avoid shared state
3. **Slow tests** - Mock external dependencies
4. **Over-mocking** - Integration tests still needed
5. **No assertions** - Tests without asserts always pass

---

## Checklist

- [ ] pytest.ini or pyproject.toml configured
- [ ] conftest.py with shared fixtures
- [ ] Separate unit/integration/e2e directories
- [ ] Test database setup
- [ ] Coverage reporting enabled
- [ ] CI pipeline runs tests
- [ ] Tests run in < 30 seconds

---

## Next Steps

- M-DO-001: CI/CD GitHub Actions
- M-PY-008: Code Quality

---

*Methodology M-PY-004 v1.0*
