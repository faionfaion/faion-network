---
name: faion-testing-pytest
user-invocable: false
description: "pytest testing framework: fixtures, parametrization, mocking, async"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(pytest:*)
---

# pytest Testing (Python)

## Overview

pytest is the most popular Python testing framework. Powerful fixtures, parametrization, and plugin ecosystem.

## Installation

```bash
pip install pytest pytest-cov pytest-mock pytest-asyncio pytest-xdist
```

## Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = ["-v", "--strict-markers", "--tb=short"]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
asyncio_mode = "auto"

[tool.coverage.run]
branch = true
source = ["src"]
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = ["pragma: no cover", "if TYPE_CHECKING:", "raise NotImplementedError"]
fail_under = 80
```

## Basic Test

```python
import pytest
from myapp.services import UserService

class TestUserService:
    def test_create_user_with_valid_data(self):
        # Arrange
        service = UserService()
        user_data = {"name": "John", "email": "john@example.com"}

        # Act
        user = service.create(user_data)

        # Assert
        assert user.id is not None
        assert user.name == "John"

    def test_create_user_with_invalid_email_raises_error(self):
        service = UserService()
        user_data = {"name": "John", "email": "invalid"}

        with pytest.raises(ValueError, match="Invalid email"):
            service.create(user_data)
```

## Fixtures

### Basic Fixtures

```python
# conftest.py
import pytest
from myapp.database import Database
from myapp.services import UserService

@pytest.fixture
def db():
    """Create test database connection."""
    database = Database(":memory:")
    database.create_tables()
    yield database
    database.close()

@pytest.fixture
def user_service(db):
    """Create UserService with test database."""
    return UserService(db)

@pytest.fixture
def sample_user(user_service):
    """Create a sample user for testing."""
    return user_service.create({
        "name": "Test User",
        "email": "test@example.com"
    })
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: new for each test
def per_test_fixture():
    pass

@pytest.fixture(scope="class")  # Once per test class
def per_class_fixture():
    pass

@pytest.fixture(scope="module")  # Once per test module
def per_module_fixture():
    pass

@pytest.fixture(scope="session")  # Once per test session
def per_session_fixture():
    pass
```

### Factory Fixtures

```python
@pytest.fixture
def user_factory(db):
    """Factory for creating test users."""
    created_users = []

    def _create_user(**kwargs):
        defaults = {
            "name": "Test User",
            "email": f"user{len(created_users)}@example.com"
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db.add(user)
        created_users.append(user)
        return user

    yield _create_user

    # Cleanup
    for user in created_users:
        db.delete(user)
```

## Parametrization

### Basic Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
])
def test_double(input, expected):
    assert double(input) == expected
```

### With IDs

```python
@pytest.mark.parametrize("email,valid", [
    pytest.param("user@example.com", True, id="valid_email"),
    pytest.param("invalid", False, id="no_at_symbol"),
    pytest.param("@example.com", False, id="no_local_part"),
])
def test_email_validation(email, valid):
    assert validate_email(email) == valid
```

## Mocking

### Using pytest-mock

```python
def test_send_email_calls_smtp(mocker):
    # Arrange
    mock_smtp = mocker.patch("myapp.email.smtplib.SMTP")
    service = EmailService()

    # Act
    service.send("test@example.com", "Hello", "Body")

    # Assert
    mock_smtp.return_value.sendmail.assert_called_once()

def test_external_api_call(mocker):
    # Mock external API response
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.status_code = 200

    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_data("https://api.example.com")
    assert result["status"] == "ok"
```

### Side Effects

```python
def test_retry_on_failure(mocker):
    mock_api = mocker.patch("myapp.api.external_call")
    mock_api.side_effect = [
        ConnectionError("Network error"),
        ConnectionError("Network error"),
        {"result": "success"},
    ]

    result = api_with_retry(max_retries=3)
    assert result == {"result": "success"}
    assert mock_api.call_count == 3
```

## Markers

### Built-in Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_new_syntax():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_known_issue():
    pass
```

### Custom Markers

```python
# Run specific markers
# pytest -m "slow"
# pytest -m "not integration"

@pytest.mark.slow
def test_heavy_computation():
    pass

@pytest.mark.integration
def test_database_connection():
    pass
```

## Async Testing

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_concurrent_operations():
    results = await asyncio.gather(
        async_operation_1(),
        async_operation_2(),
    )
    assert len(results) == 2

# Async fixture
@pytest.fixture
async def async_db():
    db = await AsyncDatabase.connect()
    yield db
    await db.close()
```

## Running pytest

```bash
pytest                                    # Run all tests
pytest -v                                 # Verbose output
pytest tests/test_services.py             # Run specific file
pytest tests/test_services.py::TestUserService::test_create_user  # Specific test
pytest -k "create or delete"              # Run tests matching pattern
pytest -m integration                     # Run tests with marker
pytest -n auto                            # Parallel execution (pytest-xdist)
pytest --cov=src --cov-report=html        # Show coverage
pytest -x                                 # Stop on first failure
pytest --lf                               # Run last failed tests
```

## Sources

- [pytest Documentation](https://docs.pytest.org/) - official pytest docs
- [pytest Fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html) - fixtures guide
- [pytest-mock](https://pytest-mock.readthedocs.io/) - mocking plugin
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - async testing
- [pytest-xdist](https://pytest-xdist.readthedocs.io/) - parallel execution
