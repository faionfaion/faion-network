# pytest Examples

Real-world code examples demonstrating pytest patterns and best practices.

---

## Table of Contents

1. [Basic Testing Patterns](#basic-testing-patterns)
2. [Fixture Patterns](#fixture-patterns)
3. [Parametrization Patterns](#parametrization-patterns)
4. [Mocking Patterns](#mocking-patterns)
5. [Async Testing Patterns](#async-testing-patterns)
6. [Django Testing Patterns](#django-testing-patterns)
7. [Coverage Patterns](#coverage-patterns)
8. [Parallel Execution Patterns](#parallel-execution-patterns)
9. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Basic Testing Patterns

### AAA Pattern (Arrange-Act-Assert)

```python
# Good: Clear separation of concerns
def test_user_registration_success():
    # Arrange
    user_data = {
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "name": "New User",
    }

    # Act
    user = UserService.register(**user_data)

    # Assert
    assert user.email == "newuser@example.com"
    assert user.is_active is True
    assert user.check_password("SecurePass123!")


# Bad: Mixed concerns, unclear structure
def test_user_registration_bad():
    user = UserService.register(
        email="newuser@example.com",
        password="SecurePass123!",
        name="New User",
    )
    assert user.email == "newuser@example.com"
    assert user.is_active is True
    # What if this fails? Hard to debug
    assert user.check_password("SecurePass123!")
```

### Descriptive Test Names

```python
# Good: Test names describe behavior
class TestUserAuthentication:
    def test_login_with_valid_credentials_returns_token(self):
        ...

    def test_login_with_invalid_password_raises_auth_error(self):
        ...

    def test_login_with_nonexistent_email_raises_user_not_found(self):
        ...

    def test_login_with_locked_account_raises_account_locked_error(self):
        ...


# Bad: Vague test names
class TestUserAuthentication:
    def test_login(self):
        ...

    def test_login_fail(self):
        ...

    def test_login_error(self):
        ...
```

### Testing Exceptions

```python
import pytest

def test_division_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError) as exc_info:
        validate_email("invalid-email")

    assert "Invalid email format" in str(exc_info.value)
    assert exc_info.value.field == "email"


def test_multiple_validation_errors():
    with pytest.raises(ValidationError) as exc_info:
        validate_user({"email": "bad", "age": -1})

    errors = exc_info.value.errors
    assert len(errors) == 2
    assert any(e["field"] == "email" for e in errors)
    assert any(e["field"] == "age" for e in errors)
```

---

## Fixture Patterns

### Basic Fixture with Cleanup

```python
import pytest


@pytest.fixture
def temp_database():
    """Create a temporary database for testing."""
    db = create_temp_database()
    yield db  # Test runs here
    db.drop()  # Cleanup after test


@pytest.fixture
def redis_client():
    """Redis client with cleanup."""
    client = redis.Redis(host="localhost", port=6379, db=15)
    client.flushdb()  # Clean before test
    yield client
    client.flushdb()  # Clean after test
    client.close()
```

### Factory Fixture Pattern

```python
@pytest.fixture
def user_factory(db):
    """Factory for creating users with customizable attributes."""
    created_users = []

    def create(
        email: str | None = None,
        name: str = "Test User",
        is_active: bool = True,
        **kwargs,
    ) -> User:
        if email is None:
            email = f"user{len(created_users) + 1}@example.com"

        user = User.objects.create(
            email=email,
            name=name,
            is_active=is_active,
            **kwargs,
        )
        created_users.append(user)
        return user

    return create


def test_user_list_returns_active_users(user_factory):
    active_user = user_factory(is_active=True)
    inactive_user = user_factory(is_active=False)

    result = UserService.list_active_users()

    assert active_user in result
    assert inactive_user not in result
```

### Fixture Composition

```python
@pytest.fixture
def user(user_factory):
    """A default user for tests that need a single user."""
    return user_factory()


@pytest.fixture
def admin_user(user_factory):
    """An admin user."""
    return user_factory(email="admin@example.com", is_admin=True)


@pytest.fixture
def team(user_factory, team_factory):
    """A team with members."""
    owner = user_factory(email="owner@example.com")
    team = team_factory(owner=owner)
    team.add_member(user_factory(email="member1@example.com"))
    team.add_member(user_factory(email="member2@example.com"))
    return team
```

### Session-Scoped Fixture

```python
@pytest.fixture(scope="session")
def database_engine():
    """Create database engine once for all tests."""
    engine = create_engine(TEST_DATABASE_URL)

    # Run migrations
    run_migrations(engine)

    yield engine

    # Cleanup after all tests
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(database_engine):
    """Fresh database session for each test with rollback."""
    connection = database_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### Parametrized Fixture

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def database(request):
    """Run tests against multiple database backends."""
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.cleanup()


def test_query_performance(database):
    # This test runs twice: once for SQLite, once for PostgreSQL
    result = database.execute("SELECT * FROM users")
    assert len(result) >= 0
```

---

## Parametrization Patterns

### Basic Parametrization

```python
@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("user.name@example.co.uk", True),
    ("user+tag@example.com", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
    ("", False),
    (None, False),
])
def test_email_validation(email, is_valid):
    assert validate_email(email) == is_valid
```

### Parametrization with IDs

```python
@pytest.mark.parametrize(
    "input_data,expected_error",
    [
        pytest.param(
            {"email": ""},
            "Email is required",
            id="empty_email",
        ),
        pytest.param(
            {"email": "invalid"},
            "Invalid email format",
            id="invalid_format",
        ),
        pytest.param(
            {"email": "existing@example.com"},
            "Email already exists",
            id="duplicate_email",
        ),
    ],
)
def test_registration_validation_errors(input_data, expected_error, user_factory):
    if expected_error == "Email already exists":
        user_factory(email="existing@example.com")

    with pytest.raises(ValidationError) as exc_info:
        register_user(**input_data)

    assert expected_error in str(exc_info.value)
```

### Stacked Parametrization (Cartesian Product)

```python
@pytest.mark.parametrize("status", ["active", "inactive", "suspended"])
@pytest.mark.parametrize("role", ["user", "admin", "moderator"])
def test_permission_matrix(status, role):
    """Test all combinations of status and role (9 tests total)."""
    user = create_user(status=status, role=role)
    permissions = get_user_permissions(user)
    assert_valid_permissions(permissions, status, role)
```

### Indirect Parametrization

```python
@pytest.fixture
def user_with_plan(request, user_factory):
    """Create user with specified subscription plan."""
    plan = request.param
    user = user_factory()
    user.subscription = create_subscription(plan)
    return user


@pytest.mark.parametrize(
    "user_with_plan,expected_features",
    [
        ("free", ["basic_feature"]),
        ("pro", ["basic_feature", "pro_feature"]),
        ("enterprise", ["basic_feature", "pro_feature", "enterprise_feature"]),
    ],
    indirect=["user_with_plan"],
)
def test_user_features_by_plan(user_with_plan, expected_features):
    features = get_user_features(user_with_plan)
    assert set(features) == set(expected_features)
```

### Skip/Xfail in Parametrization

```python
@pytest.mark.parametrize("browser", [
    "chrome",
    "firefox",
    pytest.param("safari", marks=pytest.mark.skip(reason="Safari not installed")),
    pytest.param("edge", marks=pytest.mark.xfail(reason="Known bug #123")),
])
def test_browser_compatibility(browser):
    result = run_browser_test(browser)
    assert result.success
```

---

## Mocking Patterns

### Basic Mocking with pytest-mock

```python
def test_send_notification_calls_email_service(mocker):
    # Arrange
    mock_send_email = mocker.patch("app.services.email_client.send")
    mock_send_email.return_value = {"status": "sent", "id": "123"}

    # Act
    result = NotificationService.send_notification(
        user_id=1,
        message="Hello!",
    )

    # Assert
    assert result["status"] == "sent"
    mock_send_email.assert_called_once_with(
        to="user1@example.com",
        subject="Notification",
        body="Hello!",
    )
```

### Mocking External APIs

```python
def test_fetch_weather_data(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "temperature": 22,
        "conditions": "sunny",
    }
    mock_response.status_code = 200

    mocker.patch("requests.get", return_value=mock_response)

    result = WeatherService.get_current_weather("London")

    assert result["temperature"] == 22
    assert result["conditions"] == "sunny"


def test_fetch_weather_handles_api_error(mocker):
    mocker.patch(
        "requests.get",
        side_effect=requests.RequestException("Connection failed"),
    )

    with pytest.raises(WeatherServiceError) as exc_info:
        WeatherService.get_current_weather("London")

    assert "Unable to fetch weather data" in str(exc_info.value)
```

### Mocking with Context Manager

```python
from unittest.mock import patch, MagicMock

def test_database_transaction(mocker):
    mock_db = mocker.MagicMock()

    with patch("app.database.get_connection", return_value=mock_db):
        result = process_order(order_id=123)

    # Verify transaction was committed
    mock_db.commit.assert_called_once()
    mock_db.rollback.assert_not_called()


def test_database_transaction_rollback_on_error(mocker):
    mock_db = mocker.MagicMock()
    mock_db.execute.side_effect = DatabaseError("Constraint violation")

    with patch("app.database.get_connection", return_value=mock_db):
        with pytest.raises(ProcessingError):
            process_order(order_id=123)

    # Verify transaction was rolled back
    mock_db.rollback.assert_called_once()
    mock_db.commit.assert_not_called()
```

### Spy Pattern

```python
def test_logging_called_on_error(mocker):
    spy_logger = mocker.spy(app.services.logger, "error")

    with pytest.raises(ValidationError):
        validate_user({"email": "invalid"})

    spy_logger.assert_called_once()
    call_args = spy_logger.call_args[0][0]
    assert "Validation failed" in call_args
```

### Mock with Autospec

```python
def test_user_repository_save(mocker):
    # autospec ensures mock matches real signature
    mock_repo = mocker.create_autospec(UserRepository)
    mock_repo.save.return_value = User(id=1, email="test@example.com")

    service = UserService(repository=mock_repo)
    result = service.create_user(email="test@example.com")

    assert result.id == 1
    mock_repo.save.assert_called_once()
```

---

## Async Testing Patterns

### Basic Async Test

```python
import pytest


@pytest.mark.asyncio
async def test_async_fetch_user():
    user = await UserRepository.fetch_by_id(1)
    assert user.email == "user1@example.com"


@pytest.mark.asyncio
async def test_concurrent_operations():
    # Run multiple async operations concurrently
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )

    assert len(results) == 3
    assert all(r is not None for r in results)
```

### Async Fixtures

```python
import pytest_asyncio


@pytest_asyncio.fixture
async def async_client():
    """Async HTTP client for API testing."""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def database():
    """Async database connection."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_api_endpoint(async_client, database):
    response = await async_client.post(
        "/api/users",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

### Async Mocking

```python
@pytest.mark.asyncio
async def test_async_external_service(mocker):
    mock_fetch = mocker.patch(
        "app.services.external_api.fetch_data",
        new_callable=mocker.AsyncMock,
    )
    mock_fetch.return_value = {"data": "mocked"}

    result = await process_external_data()

    assert result["data"] == "mocked"
    mock_fetch.assert_awaited_once()


@pytest.mark.asyncio
async def test_async_exception_handling(mocker):
    mocker.patch(
        "app.services.external_api.fetch_data",
        new_callable=mocker.AsyncMock,
        side_effect=ConnectionError("Service unavailable"),
    )

    with pytest.raises(ServiceError):
        await process_external_data()
```

### Testing Timeouts

```python
@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_slow_operation_completes():
    result = await slow_async_operation()
    assert result is not None


@pytest.mark.asyncio
async def test_operation_timeout_handling():
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(1):
            await very_slow_operation()
```

---

## Django Testing Patterns

### Model Testing

```python
import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_valid_data(self):
        user = User.objects.create(
            email="test@example.com",
            name="Test User",
        )

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.created_at is not None

    def test_email_must_be_unique(self, user):
        with pytest.raises(ValidationError):
            User.objects.create(email=user.email, name="Another User")

    def test_user_str_representation(self, user):
        assert str(user) == user.email
```

### API Testing with DRF

```python
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestUserAPI:
    def test_list_users_requires_auth(self, api_client):
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_users_returns_all_users(self, authenticated_client, user_factory):
        user_factory(email="user1@example.com")
        user_factory(email="user2@example.com")

        response = authenticated_client.get("/api/users/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_user(self, authenticated_client):
        response = authenticated_client.post(
            "/api/users/",
            {
                "email": "new@example.com",
                "name": "New User",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "new@example.com"
        assert User.objects.filter(email="new@example.com").exists()

    def test_update_user(self, authenticated_client, user):
        response = authenticated_client.patch(
            f"/api/users/{user.id}/",
            {"name": "Updated Name"},
        )

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.name == "Updated Name"
```

### Factory Boy Integration

```python
# tests/factories.py
import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True

    @factory.lazy_attribute
    def password(self):
        return make_password("defaultpass123")


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: f"Team {n}")
    owner = factory.SubFactory(UserFactory)


# tests/conftest.py
from pytest_factoryboy import register

register(UserFactory)
register(TeamFactory)


# tests/test_teams.py
@pytest.mark.django_db
def test_team_creation(user, team_factory):
    team = team_factory(owner=user)

    assert team.owner == user
    assert team.name.startswith("Team ")
```

### Transaction Testing

```python
@pytest.mark.django_db(transaction=True)
def test_atomic_operation():
    """Test that requires real transactions (not wrapped in savepoint)."""
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            User.objects.create(email="test@example.com")
            User.objects.create(email="test@example.com")  # Duplicate

    # Verify rollback worked
    assert User.objects.filter(email="test@example.com").count() == 0
```

---

## Coverage Patterns

### Branch Coverage Example

```python
# Code to test
def get_discount(user, amount):
    if user.is_premium:
        if amount > 100:
            return amount * 0.2  # Branch 1
        return amount * 0.1      # Branch 2
    return 0                      # Branch 3


# Tests with full branch coverage
@pytest.mark.parametrize("is_premium,amount,expected", [
    (True, 150, 30),    # Branch 1: premium, high amount
    (True, 50, 5),      # Branch 2: premium, low amount
    (False, 150, 0),    # Branch 3: not premium
])
def test_get_discount_all_branches(user_factory, is_premium, amount, expected):
    user = user_factory(is_premium=is_premium)
    discount = get_discount(user, amount)
    assert discount == expected
```

### Coverage Exclusion Patterns

```python
# Exclude from coverage with pragma
def complex_function():
    if __debug__:  # pragma: no cover
        logging.debug("Debug mode")

    if TYPE_CHECKING:  # Automatically excluded
        from typing import TypeVar

    result = do_something()
    return result


# Exclude abstract methods
class BaseHandler:
    @abstractmethod
    def handle(self):  # pragma: no cover
        raise NotImplementedError
```

---

## Parallel Execution Patterns

### Test Isolation for Parallel Execution

```python
# Good: Uses tmp_path for isolation
def test_file_processing(tmp_path):
    test_file = tmp_path / "data.txt"
    test_file.write_text("test content")

    result = process_file(test_file)

    assert result["lines"] == 1


# Good: Uses unique database entries
@pytest.mark.django_db
def test_user_creation(user_factory):
    # Factory creates unique emails
    user = user_factory()
    assert User.objects.filter(email=user.email).count() == 1


# Bad: Hardcoded path (will conflict in parallel)
def test_file_processing_bad():
    with open("/tmp/test_data.txt", "w") as f:
        f.write("test content")

    result = process_file("/tmp/test_data.txt")
    assert result["lines"] == 1
```

### Grouping Tests for Parallel Execution

```python
# Group tests that share expensive fixtures
@pytest.mark.xdist_group(name="database_heavy")
class TestDatabaseMigrations:
    def test_migration_01(self):
        ...

    def test_migration_02(self):
        ...


# Or use loadscope to group by module
# pytest -n auto --dist loadscope
```

---

## Anti-Patterns to Avoid

### Test Interdependency

```python
# Bad: Tests depend on execution order
class TestBadOrder:
    user_id = None

    def test_create_user(self):
        user = User.objects.create(email="test@example.com")
        TestBadOrder.user_id = user.id  # Storing state!

    def test_get_user(self):
        # This fails if run alone or in different order
        user = User.objects.get(id=TestBadOrder.user_id)
        assert user.email == "test@example.com"


# Good: Tests are independent
class TestGoodIndependent:
    def test_create_user(self, user_factory):
        user = user_factory(email="test@example.com")
        assert user.id is not None

    def test_get_user(self, user_factory):
        user = user_factory(email="test@example.com")
        fetched = User.objects.get(id=user.id)
        assert fetched.email == "test@example.com"
```

### Over-Mocking

```python
# Bad: Mocking too much, test doesn't test real behavior
def test_user_service_over_mocked(mocker):
    mocker.patch.object(UserService, "validate_email", return_value=True)
    mocker.patch.object(UserService, "check_duplicate", return_value=False)
    mocker.patch.object(UserRepository, "save", return_value=User(id=1))
    mocker.patch.object(EmailService, "send_welcome", return_value=True)

    # This tests nothing useful!
    result = UserService.register(email="test@example.com")
    assert result.id == 1


# Good: Mock only external dependencies
def test_user_service_minimal_mocking(mocker, db):
    mocker.patch("app.services.email_client.send", return_value=True)

    result = UserService.register(email="test@example.com")

    assert result.id is not None
    assert User.objects.filter(email="test@example.com").exists()
```

### Incorrect Mock Target

```python
# module_a.py
from module_b import helper_function

def my_function():
    return helper_function()

# Bad: Mocking where defined (doesn't work)
def test_bad_mock_target(mocker):
    mocker.patch("module_b.helper_function", return_value="mocked")
    result = my_function()
    # This still calls real helper_function!

# Good: Mock where used
def test_good_mock_target(mocker):
    mocker.patch("module_a.helper_function", return_value="mocked")
    result = my_function()
    assert result == "mocked"
```

### Flaky Tests

```python
# Bad: Flaky due to timing
def test_flaky_timing():
    start = time.time()
    slow_operation()
    elapsed = time.time() - start
    assert elapsed < 1.0  # Might fail randomly


# Good: Use appropriate tolerance or mock time
def test_stable_timing(mocker):
    mock_time = mocker.patch("time.time")
    mock_time.side_effect = [0, 0.5]  # Controlled time

    start = time.time()
    slow_operation()
    elapsed = time.time() - start

    assert elapsed == 0.5


# Bad: Flaky due to dict ordering (Python 3.7+ fixed this, but still)
def test_flaky_order():
    result = get_items()
    assert list(result.keys()) == ["a", "b", "c"]


# Good: Order-independent assertion
def test_stable_order():
    result = get_items()
    assert set(result.keys()) == {"a", "b", "c"}
```

---

*pytest Examples v2.0*
