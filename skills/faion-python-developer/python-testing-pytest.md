---
name: faion-python-testing-pytest
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(pytest:*, coverage:*)
---

# Python Testing with pytest

**Comprehensive pytest patterns for testing Python applications.**

---

## Purpose

Provides patterns and best practices for pytest-based testing. Used by faion-test-agent and faion-code-agent for:
- Test structure and organization
- Fixtures and factory patterns
- Mocking and patching
- Parametrization
- Django integration tests
- Coverage analysis

---

## Problem

Python projects need consistent testing with fixtures, mocking, parametrization, and coverage.

---

## Framework

### Test Structure

```
tests/
|-- __init__.py
|-- conftest.py               # Shared fixtures
|-- test_models.py
|-- test_services.py
|-- test_views.py
|-- integration/
|   |-- __init__.py
|   |-- test_api.py
|-- fixtures/
    |-- users.py
    |-- items.py
```

### conftest.py (Shared Fixtures)

```python
# conftest.py
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_db():
    """Mock database session."""
    return MagicMock()


@pytest.fixture
def sample_user_data():
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "name": "Test User",
    }


# Django-specific
@pytest.fixture
def api_client():
    """DRF API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client
```

### Fixtures with Factory Pattern

```python
# fixtures/users.py
import pytest
from apps.users.models import User


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create(
        email="user@example.com",
        name="Test User",
    )


@pytest.fixture
def user_factory(db):
    """Factory for creating users."""
    def create_user(
        email: str = "user@example.com",
        name: str = "Test User",
        **kwargs,
    ) -> User:
        return User.objects.create(
            email=email,
            name=name,
            **kwargs,
        )
    return create_user


@pytest.fixture
def users(user_factory):
    """Create multiple test users."""
    return [
        user_factory(email=f"user{i}@example.com")
        for i in range(3)
    ]
```

---

## Mocking

### Basic Mocking

```python
# test_services.py
from unittest.mock import patch, MagicMock
import pytest

from apps.users import services


class TestCreateUser:
    def test_create_user_success(self, sample_user_data):
        """Test successful user creation."""
        with patch.object(services, 'send_welcome_email') as mock_email:
            user = services.create_user(**sample_user_data)

            assert user.email == sample_user_data['email']
            mock_email.assert_called_once_with(user)

    def test_create_user_duplicate_email(self, user, sample_user_data):
        """Test duplicate email raises error."""
        sample_user_data['email'] = user.email

        with pytest.raises(ValueError, match="Email already exists"):
            services.create_user(**sample_user_data)


class TestExternalAPI:
    @patch('apps.users.services.external_api.get_user_info')
    def test_sync_user_from_external(self, mock_get_info):
        """Test syncing user from external API."""
        mock_get_info.return_value = {
            "id": "ext-123",
            "name": "External User",
        }

        result = services.sync_from_external("ext-123")

        assert result.external_id == "ext-123"
        mock_get_info.assert_called_once_with("ext-123")
```

---

## Parametrization

### Basic Parametrization

```python
# test_validators.py
import pytest
from apps.users.validators import validate_email, validate_password


class TestEmailValidation:
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("user.name@example.co.uk", True),
        ("invalid", False),
        ("@example.com", False),
        ("user@", False),
        ("", False),
    ])
    def test_validate_email(self, email, expected):
        """Test email validation with various inputs."""
        assert validate_email(email) == expected


class TestPasswordValidation:
    @pytest.mark.parametrize("password,error_msg", [
        ("short", "Password must be at least 8 characters"),
        ("nodigits", "Password must contain a digit"),
        ("12345678", "Password must contain a letter"),
    ])
    def test_invalid_passwords(self, password, error_msg):
        """Test password validation error messages."""
        with pytest.raises(ValueError, match=error_msg):
            validate_password(password)
```

---

## Django Integration Tests

### API Testing

```python
# test_views.py
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestUserAPI:
    def test_create_user(self, api_client):
        """Test user creation endpoint."""
        response = api_client.post("/api/v1/users/", {
            "email": "new@example.com",
            "name": "New User",
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "new@example.com"

    def test_get_user_requires_auth(self, api_client):
        """Test that user endpoint requires authentication."""
        response = api_client.get("/api/v1/users/me/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, authenticated_client, user):
        """Test getting current user info."""
        response = authenticated_client.get("/api/v1/users/me/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
```

---

## Running Tests

### Command Line

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/test_services.py

# Run specific test class
pytest tests/test_services.py::TestCreateUser

# Run specific test
pytest tests/test_services.py::TestCreateUser::test_create_user_success

# Run with verbose output
pytest -v

# Run failed tests only
pytest --lf

# Run and stop on first failure
pytest -x

# Run in parallel
pytest -n auto

# Run with markers
pytest -m "not slow"
```

---

## Configuration

### pytest.ini

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### pyproject.toml

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
testpaths = ["tests"]

[tool.coverage.run]
source = ["apps"]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

---

## Advanced Patterns

### Async Tests

```python
import pytest


@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await some_async_function()
    assert result == expected_value
```

### Fixtures with Setup/Teardown

```python
@pytest.fixture
def database_connection():
    """Database connection with cleanup."""
    conn = create_connection()
    yield conn
    conn.close()
```

### Parameterized Fixtures

```python
@pytest.fixture(params=[1, 2, 3])
def sample_number(request):
    """Parametrized fixture."""
    return request.param


def test_with_parametrized_fixture(sample_number):
    """Test runs 3 times with different values."""
    assert sample_number > 0
```

---

## Mock Assertions

```python
# Verify calls
mock.assert_called()
mock.assert_called_once()
mock.assert_called_with(arg1, arg2)
mock.assert_called_once_with(arg1, arg2)
mock.assert_not_called()

# Call count
assert mock.call_count == 3

# Call arguments
mock.call_args
mock.call_args_list
```

---

## Testing Best Practices

### Test Organization

- **Unit tests**: Test single functions/methods in isolation
- **Integration tests**: Test multiple components together
- **E2E tests**: Test entire user workflows
- Use factories for flexible test data
- Keep tests independent and isolated

### Naming Conventions

```python
# Clear, descriptive test names
def test_create_user_with_valid_data_returns_user():
    pass

def test_create_user_with_duplicate_email_raises_error():
    pass

def test_get_user_by_id_when_not_found_returns_none():
    pass
```

### AAA Pattern

```python
def test_example():
    # Arrange
    user = create_test_user()

    # Act
    result = service.do_something(user)

    # Assert
    assert result.success is True
```

---

## Quick Reference

### Common Fixtures

| Fixture | Purpose |
|---------|---------|
| `db` | Enable database access (Django) |
| `client` | Django test client |
| `api_client` | DRF API client |
| `settings` | Override Django settings |
| `tmp_path` | Temporary directory (built-in) |
| `monkeypatch` | Modify objects/environment (built-in) |

### Markers

```python
@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.skip(reason="Not implemented")
@pytest.mark.skipif(condition, reason="...")
@pytest.mark.xfail(reason="Known bug")
@pytest.mark.django_db
@pytest.mark.asyncio
```

---

## Agent

Executed by: faion-test-agent, faion-code-agent

---

## Sources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

*Python Testing with pytest v1.0*
*Layer 3 Technical Skill*
*pytest Patterns | Fixtures | Mocking | Django Integration*
