# pytest Examples

Real-world pytest examples covering fixtures, parametrization, mocking, async testing, and more.

---

## Basic Test Structure

### Simple Test with AAA Pattern

```python
# tests/test_calculator.py
from myapp.calculator import Calculator


class TestCalculator:
    """Tests for Calculator class."""

    def test_add_positive_numbers_returns_sum(self):
        # Arrange
        calc = Calculator()
        a, b = 5, 3

        # Act
        result = calc.add(a, b)

        # Assert
        assert result == 8

    def test_divide_by_zero_raises_error(self):
        # Arrange
        calc = Calculator()

        # Act & Assert
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(10, 0)

    def test_subtract_returns_correct_difference(self):
        calc = Calculator()
        assert calc.subtract(10, 3) == 7
        assert calc.subtract(3, 10) == -7
        assert calc.subtract(5, 5) == 0
```

---

## Fixtures

### Basic Fixtures with Dependency Injection

```python
# tests/conftest.py
import pytest
from myapp.database import Database
from myapp.services import UserService, OrderService
from myapp.models import User


@pytest.fixture
def db():
    """Create in-memory test database."""
    database = Database(":memory:")
    database.create_tables()
    yield database
    database.close()


@pytest.fixture
def user_service(db):
    """UserService with test database."""
    return UserService(db)


@pytest.fixture
def order_service(db, user_service):
    """OrderService with dependencies."""
    return OrderService(db, user_service)


@pytest.fixture
def sample_user(user_service):
    """Create a sample user for testing."""
    return user_service.create({
        "name": "Test User",
        "email": "test@example.com",
        "role": "user"
    })
```

### Factory Fixtures

```python
# tests/conftest.py
import pytest
from myapp.models import User, Product, Order
from datetime import datetime, timedelta


@pytest.fixture
def user_factory(db):
    """Factory for creating test users with customizable attributes."""
    created_users = []
    counter = 0

    def _create_user(**kwargs):
        nonlocal counter
        counter += 1
        defaults = {
            "name": f"User {counter}",
            "email": f"user{counter}@example.com",
            "role": "user",
            "is_active": True,
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db.add(user)
        db.commit()
        created_users.append(user)
        return user

    yield _create_user

    # Cleanup
    for user in created_users:
        db.delete(user)
    db.commit()


@pytest.fixture
def product_factory(db):
    """Factory for creating test products."""
    counter = 0

    def _create_product(**kwargs):
        nonlocal counter
        counter += 1
        defaults = {
            "name": f"Product {counter}",
            "price": 99.99,
            "stock": 100,
            "category": "general",
        }
        defaults.update(kwargs)
        product = Product(**defaults)
        db.add(product)
        db.commit()
        return product

    return _create_product


@pytest.fixture
def order_factory(db, user_factory, product_factory):
    """Factory for creating test orders."""
    def _create_order(user=None, products=None, **kwargs):
        if user is None:
            user = user_factory()
        if products is None:
            products = [product_factory()]

        order = Order(
            user_id=user.id,
            products=products,
            status=kwargs.get("status", "pending"),
            created_at=kwargs.get("created_at", datetime.utcnow()),
        )
        db.add(order)
        db.commit()
        return order

    return _create_order
```

### Fixture Scopes

```python
# tests/conftest.py
import pytest
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def database_engine():
    """Create database engine once per test session."""
    engine = create_engine("postgresql://test:test@localhost/test_db")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def redis_client():
    """Redis client shared across all tests."""
    client = redis.Redis(host="localhost", port=6379, db=15)
    yield client
    client.flushdb()
    client.close()


@pytest.fixture(scope="module")
def db_session(database_engine):
    """Database session per test module."""
    Session = sessionmaker(bind=database_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="class")
def api_client():
    """API client per test class."""
    from myapp.client import APIClient
    client = APIClient(base_url="http://localhost:8000")
    yield client
    client.close()


@pytest.fixture  # scope="function" is default
def clean_user(db_session):
    """Fresh user for each test."""
    user = User(name="Clean User", email="clean@example.com")
    db_session.add(user)
    db_session.commit()
    yield user
    db_session.delete(user)
    db_session.commit()
```

### Autouse Fixtures

```python
# tests/conftest.py
import pytest
import os


@pytest.fixture(autouse=True)
def set_test_environment():
    """Set test environment variables for all tests."""
    original_env = os.environ.copy()
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "false"
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture(autouse=True, scope="session")
def setup_logging():
    """Configure logging once for test session."""
    import logging
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("myapp").setLevel(logging.DEBUG)


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests."""
    from myapp.config import Config
    Config._instance = None
    yield
    Config._instance = None
```

---

## Parametrization

### Basic Parametrization

```python
import pytest
from myapp.validators import validate_email, validate_password


@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user.name@example.co.uk", True),
    ("user+tag@example.com", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
    ("", False),
    (None, False),
])
def test_validate_email(email, expected):
    assert validate_email(email) == expected


@pytest.mark.parametrize("password,is_valid,reason", [
    ("SecureP@ss123", True, "valid_password"),
    ("short", False, "too_short"),
    ("nouppercase123!", False, "no_uppercase"),
    ("NOLOWERCASE123!", False, "no_lowercase"),
    ("NoNumbers!", False, "no_numbers"),
    ("NoSpecial123", False, "no_special_chars"),
])
def test_validate_password(password, is_valid, reason):
    result = validate_password(password)
    assert result.is_valid == is_valid, f"Failed for: {reason}"
```

### Parametrization with IDs

```python
import pytest
from myapp.pricing import calculate_discount


# Using pytest.param for custom IDs
@pytest.mark.parametrize("price,quantity,expected_discount", [
    pytest.param(100, 1, 0, id="no_discount_single_item"),
    pytest.param(100, 5, 5, id="5_percent_for_5_items"),
    pytest.param(100, 10, 10, id="10_percent_for_10_items"),
    pytest.param(100, 50, 15, id="15_percent_bulk_order"),
    pytest.param(100, 100, 20, id="20_percent_max_discount"),
])
def test_calculate_discount(price, quantity, expected_discount):
    result = calculate_discount(price, quantity)
    assert result == expected_discount


# Using dict for complex test data
VALIDATION_CASES = {
    "valid_user": {
        "input": {"name": "John", "email": "john@example.com", "age": 25},
        "expected": True,
        "errors": [],
    },
    "missing_name": {
        "input": {"email": "john@example.com", "age": 25},
        "expected": False,
        "errors": ["name is required"],
    },
    "invalid_age": {
        "input": {"name": "John", "email": "john@example.com", "age": -5},
        "expected": False,
        "errors": ["age must be positive"],
    },
}


@pytest.mark.parametrize(
    "case_name",
    VALIDATION_CASES.keys(),
    ids=list(VALIDATION_CASES.keys())
)
def test_user_validation(case_name):
    case = VALIDATION_CASES[case_name]
    result = validate_user(case["input"])
    assert result.is_valid == case["expected"]
    assert result.errors == case["errors"]
```

### Multiple Parametrization (Cartesian Product)

```python
import pytest
from myapp.format import format_currency


@pytest.mark.parametrize("amount", [0, 100, 1000.50, -50])
@pytest.mark.parametrize("currency", ["USD", "EUR", "GBP"])
@pytest.mark.parametrize("locale", ["en_US", "de_DE"])
def test_format_currency_combinations(amount, currency, locale):
    """Tests all combinations: 4 amounts x 3 currencies x 2 locales = 24 tests."""
    result = format_currency(amount, currency, locale)
    assert isinstance(result, str)
    assert len(result) > 0
```

### Fixture Parametrization

```python
import pytest


@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database(request):
    """Parametrized fixture - tests run with each database."""
    db_type = request.param

    if db_type == "sqlite":
        db = SQLiteDatabase(":memory:")
    elif db_type == "postgresql":
        db = PostgreSQLDatabase("postgresql://test@localhost/test")
    else:
        db = MySQLDatabase("mysql://test@localhost/test")

    db.connect()
    yield db
    db.disconnect()


def test_user_crud_operations(database):
    """This test runs 3 times, once per database type."""
    user = database.create_user(name="Test", email="test@example.com")
    assert database.get_user(user.id) is not None
    database.delete_user(user.id)
    assert database.get_user(user.id) is None
```

### Indirect Parametrization

```python
import pytest


@pytest.fixture
def user_with_role(request):
    """Fixture that receives parameters indirectly."""
    role = request.param
    return User(name=f"{role.title()} User", role=role)


@pytest.mark.parametrize(
    "user_with_role,expected_permissions",
    [
        ("admin", ["read", "write", "delete", "admin"]),
        ("editor", ["read", "write"]),
        ("viewer", ["read"]),
    ],
    indirect=["user_with_role"]  # Pass param to fixture
)
def test_user_permissions(user_with_role, expected_permissions):
    assert user_with_role.get_permissions() == expected_permissions
```

---

## Mocking

### Basic Mocking with pytest-mock

```python
import pytest
from myapp.services import EmailService, NotificationService


def test_send_email_calls_smtp(mocker):
    # Arrange
    mock_smtp = mocker.patch("myapp.services.smtplib.SMTP")
    mock_instance = mock_smtp.return_value
    service = EmailService()

    # Act
    service.send(
        to="user@example.com",
        subject="Hello",
        body="Test message"
    )

    # Assert
    mock_smtp.assert_called_once_with("smtp.example.com", 587)
    mock_instance.sendmail.assert_called_once()


def test_notification_service_uses_all_channels(mocker):
    # Mock multiple dependencies
    mock_email = mocker.patch.object(NotificationService, "_send_email")
    mock_sms = mocker.patch.object(NotificationService, "_send_sms")
    mock_push = mocker.patch.object(NotificationService, "_send_push")

    service = NotificationService()
    service.notify_user(user_id=123, message="Hello")

    # Verify all channels were used
    mock_email.assert_called_once()
    mock_sms.assert_called_once()
    mock_push.assert_called_once()
```

### Mocking Return Values and Side Effects

```python
import pytest
from myapp.client import APIClient
from myapp.services import DataService


def test_api_client_returns_data(mocker):
    # Mock with return value
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"users": [{"id": 1, "name": "John"}]}
    mock_response.status_code = 200

    mocker.patch("requests.get", return_value=mock_response)

    client = APIClient()
    result = client.get_users()

    assert result == [{"id": 1, "name": "John"}]


def test_retry_on_failure(mocker):
    # Mock with side_effect for sequence of responses
    mock_api = mocker.patch("myapp.services.external_api")
    mock_api.side_effect = [
        ConnectionError("Network error"),
        ConnectionError("Network error"),
        {"status": "success", "data": [1, 2, 3]},
    ]

    service = DataService(max_retries=3)
    result = service.fetch_data()

    assert result == {"status": "success", "data": [1, 2, 3]}
    assert mock_api.call_count == 3


def test_dynamic_side_effect(mocker):
    # Side effect as function
    def calculate_response(url, **kwargs):
        if "users" in url:
            return {"users": []}
        elif "products" in url:
            return {"products": [{"id": 1}]}
        raise ValueError(f"Unknown URL: {url}")

    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.side_effect = calculate_response

    # Test different URLs
    client = APIClient()
    assert client.get("/users") == {"users": []}
    assert client.get("/products") == {"products": [{"id": 1}]}
```

### Mocking Context Managers

```python
import pytest
from myapp.files import FileProcessor


def test_file_processing(mocker):
    # Mock file operations
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="test content"))

    processor = FileProcessor()
    result = processor.read_file("test.txt")

    assert result == "test content"
    mock_open.assert_called_once_with("test.txt", "r")


def test_database_transaction(mocker):
    # Mock context manager
    mock_session = mocker.MagicMock()
    mock_session.__enter__ = mocker.Mock(return_value=mock_session)
    mock_session.__exit__ = mocker.Mock(return_value=False)

    mocker.patch("myapp.database.get_session", return_value=mock_session)

    service = UserService()
    service.create_user(name="Test")

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
```

### Spying on Methods

```python
import pytest
from myapp.services import PaymentService


def test_payment_logging(mocker):
    # Spy on method - calls real implementation but tracks calls
    service = PaymentService()
    spy = mocker.spy(service, "log_transaction")

    service.process_payment(amount=100, user_id=123)

    # Verify the real method was called with specific args
    spy.assert_called_once_with(amount=100, user_id=123, status="success")


def test_partial_mock(mocker):
    # Mock only specific method, keep others real
    service = PaymentService()
    mocker.patch.object(service, "send_notification")  # Mock this
    # service.validate_payment is still real

    result = service.process_payment(amount=100, user_id=123)

    assert result.success  # Uses real validation
    service.send_notification.assert_called_once()  # But notification is mocked
```

---

## Async Testing

### Basic Async Tests

```python
import pytest
import asyncio
from myapp.async_client import AsyncAPIClient
from myapp.async_services import AsyncUserService


@pytest.mark.asyncio
async def test_async_api_call():
    client = AsyncAPIClient()
    result = await client.fetch("/users")
    assert result is not None
    assert "users" in result


@pytest.mark.asyncio
async def test_concurrent_operations():
    service = AsyncUserService()

    # Run multiple operations concurrently
    results = await asyncio.gather(
        service.get_user(1),
        service.get_user(2),
        service.get_user(3),
    )

    assert len(results) == 3
    assert all(user is not None for user in results)


@pytest.mark.asyncio
async def test_async_context_manager():
    async with AsyncAPIClient() as client:
        result = await client.fetch("/status")
        assert result["status"] == "ok"
```

### Async Fixtures

```python
import pytest
import asyncpg
from myapp.async_database import AsyncDatabase


@pytest.fixture
async def async_db():
    """Async fixture for database connection."""
    db = await AsyncDatabase.connect("postgresql://test@localhost/test")
    await db.execute("BEGIN")
    yield db
    await db.execute("ROLLBACK")
    await db.close()


@pytest.fixture
async def async_user_service(async_db):
    """Async service with database dependency."""
    from myapp.async_services import AsyncUserService
    return AsyncUserService(async_db)


@pytest.fixture(scope="session")
async def connection_pool():
    """Session-scoped async fixture."""
    pool = await asyncpg.create_pool(
        "postgresql://test@localhost/test",
        min_size=5,
        max_size=10
    )
    yield pool
    await pool.close()


@pytest.mark.asyncio
async def test_create_user(async_user_service):
    user = await async_user_service.create(
        name="Async User",
        email="async@example.com"
    )
    assert user.id is not None
```

### Mocking Async Functions

```python
import pytest
from unittest.mock import AsyncMock
from myapp.async_services import NotificationService


@pytest.mark.asyncio
async def test_async_notification(mocker):
    # Create async mock
    mock_send = AsyncMock(return_value={"status": "sent"})
    mocker.patch.object(NotificationService, "send_async", mock_send)

    service = NotificationService()
    result = await service.send_async(user_id=123, message="Hello")

    assert result["status"] == "sent"
    mock_send.assert_awaited_once_with(user_id=123, message="Hello")


@pytest.mark.asyncio
async def test_async_side_effects(mocker):
    # Async mock with side effects
    mock_fetch = AsyncMock(side_effect=[
        {"page": 1, "data": [1, 2]},
        {"page": 2, "data": [3, 4]},
        {"page": 3, "data": []},
    ])
    mocker.patch("myapp.client.fetch_page", mock_fetch)

    from myapp.client import fetch_all_pages
    result = await fetch_all_pages()

    assert result == [1, 2, 3, 4]
    assert mock_fetch.await_count == 3
```

### Testing Async Timeouts

```python
import pytest
import asyncio


@pytest.mark.asyncio
@pytest.mark.timeout(5)  # Requires pytest-timeout
async def test_operation_completes_in_time():
    result = await potentially_slow_operation()
    assert result is not None


@pytest.mark.asyncio
async def test_timeout_handling():
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(0.1):
            await very_slow_operation()


@pytest.mark.asyncio
async def test_cancel_handling():
    task = asyncio.create_task(long_running_task())

    await asyncio.sleep(0.1)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task
```

---

## Markers

### Custom Markers Usage

```python
# tests/conftest.py
import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "e2e: end-to-end tests")
    config.addinivalue_line("markers", "requires_db: requires database")
    config.addinivalue_line("markers", "requires_redis: requires Redis")


# tests/test_services.py
import pytest


@pytest.mark.slow
def test_heavy_computation():
    """Run with: pytest -m slow"""
    result = compute_large_dataset()
    assert result is not None


@pytest.mark.integration
@pytest.mark.requires_db
def test_database_integration():
    """Run with: pytest -m 'integration and requires_db'"""
    db = get_test_database()
    assert db.is_connected()


@pytest.mark.e2e
class TestUserJourney:
    """Run with: pytest -m e2e"""

    def test_user_registration(self):
        pass

    def test_user_login(self):
        pass

    def test_user_purchase(self):
        pass


# Combining with parametrization
@pytest.mark.parametrize("browser", [
    pytest.param("chrome", marks=pytest.mark.slow),
    pytest.param("firefox", marks=pytest.mark.slow),
    pytest.param("headless", marks=[]),  # Not marked as slow
])
def test_browser_compatibility(browser):
    pass
```

### Skip and XFail

```python
import pytest
import sys


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass


@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="Requires Python 3.11+ for TaskGroup"
)
def test_task_group():
    pass


@pytest.mark.skipif(
    not os.environ.get("CI"),
    reason="Only run in CI environment"
)
def test_ci_specific():
    pass


@pytest.mark.xfail(reason="Known bug in v2.0, fix in v2.1")
def test_known_issue():
    """Test will pass if it fails (expected failure)."""
    assert buggy_function() == expected_result


@pytest.mark.xfail(raises=NotImplementedError)
def test_not_implemented():
    raise NotImplementedError("Coming soon")


@pytest.mark.xfail(strict=True)
def test_must_fail():
    """If this passes, the test suite fails."""
    assert broken_function() == "works"
```

---

## Coverage Examples

### Running with Coverage

```bash
# Basic coverage
pytest --cov=src tests/

# With HTML report
pytest --cov=src --cov-report=html tests/

# With multiple reports
pytest --cov=src --cov-report=html --cov-report=xml --cov-report=term-missing

# With fail threshold
pytest --cov=src --cov-fail-under=80

# Specific module coverage
pytest --cov=src.services --cov=src.models tests/
```

### Excluding Code from Coverage

```python
# myapp/services.py

def always_tested():
    """This function should be tested."""
    return "tested"


def debug_only():  # pragma: no cover
    """Excluded from coverage - debug function."""
    import pdb; pdb.set_trace()


if TYPE_CHECKING:  # Excluded via .coveragerc
    from myapp.types import ComplexType


class AbstractBase:
    def must_implement(self):
        raise NotImplementedError  # Excluded via .coveragerc
```

---

## Parallel Execution Examples

### Basic Parallel Execution

```bash
# Auto-detect CPU cores
pytest -n auto

# Specific number of workers
pytest -n 4

# With coverage (combined automatically)
pytest -n auto --cov=src --cov-report=html
```

### Distribution Modes

```bash
# Group by module/class (minimize fixture recreation)
pytest -n auto --dist loadscope

# Group by file
pytest -n auto --dist loadfile

# Use xdist_group markers
pytest -n auto --dist loadgroup
```

### Worker-Aware Fixtures

```python
import pytest
import os


@pytest.fixture(scope="session")
def database_name(worker_id):
    """Create unique database per worker."""
    if worker_id == "master":
        # Not running in parallel
        return "test_db"
    return f"test_db_{worker_id}"


@pytest.fixture(scope="session")
def database(database_name):
    """Database fixture with worker isolation."""
    db = create_database(database_name)
    db.create_tables()
    yield db
    db.drop()


# Using xdist_group for tests that must run together
@pytest.mark.xdist_group("database_migration")
def test_migration_step_1():
    pass


@pytest.mark.xdist_group("database_migration")
def test_migration_step_2():
    pass
```

---

## Debugging Examples

### Using PDB

```python
def test_with_breakpoint():
    data = prepare_test_data()

    # Modern way (Python 3.7+)
    breakpoint()

    # Classic way
    # import pdb; pdb.set_trace()

    result = process_data(data)
    assert result.success


# Conditional breakpoint
def test_conditional_debug():
    for i in range(100):
        result = compute(i)
        if result.error:
            breakpoint()  # Only break on error
        assert result.success
```

### Command-Line Debugging

```bash
# Drop to PDB on first failure
pytest --pdb

# Drop to PDB at test start
pytest --trace

# Run specific failing test with debugger
pytest --pdb -k "test_specific_failure"

# Show print output (not captured)
pytest -s

# Extra verbose for debugging
pytest -vvs --tb=long
```

---

## Real-World Test Suite Example

```python
# tests/test_order_service.py
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from myapp.services import OrderService
from myapp.models import Order, OrderStatus
from myapp.exceptions import InsufficientStockError, PaymentFailedError


class TestOrderService:
    """Comprehensive tests for OrderService."""

    @pytest.fixture
    def order_service(self, db, user_factory, product_factory):
        """OrderService with dependencies."""
        return OrderService(db)

    @pytest.fixture
    def customer(self, user_factory):
        """Standard customer for tests."""
        return user_factory(role="customer", balance=Decimal("1000.00"))

    @pytest.fixture
    def product_in_stock(self, product_factory):
        """Product with available stock."""
        return product_factory(name="Widget", price=Decimal("29.99"), stock=100)

    # Happy path tests
    def test_create_order_with_valid_data(
        self, order_service, customer, product_in_stock
    ):
        order = order_service.create_order(
            customer_id=customer.id,
            items=[{"product_id": product_in_stock.id, "quantity": 2}]
        )

        assert order.id is not None
        assert order.status == OrderStatus.PENDING
        assert order.total == Decimal("59.98")
        assert len(order.items) == 1

    def test_create_order_reduces_stock(
        self, order_service, customer, product_in_stock, db
    ):
        initial_stock = product_in_stock.stock

        order_service.create_order(
            customer_id=customer.id,
            items=[{"product_id": product_in_stock.id, "quantity": 5}]
        )

        db.refresh(product_in_stock)
        assert product_in_stock.stock == initial_stock - 5

    # Error cases
    def test_create_order_with_insufficient_stock_raises_error(
        self, order_service, customer, product_factory
    ):
        low_stock_product = product_factory(stock=2)

        with pytest.raises(InsufficientStockError) as exc_info:
            order_service.create_order(
                customer_id=customer.id,
                items=[{"product_id": low_stock_product.id, "quantity": 10}]
            )

        assert "Only 2 items available" in str(exc_info.value)

    def test_create_order_with_invalid_customer_raises_error(
        self, order_service, product_in_stock
    ):
        with pytest.raises(ValueError, match="Customer not found"):
            order_service.create_order(
                customer_id=99999,
                items=[{"product_id": product_in_stock.id, "quantity": 1}]
            )

    # Parametrized tests
    @pytest.mark.parametrize("quantity,expected_total", [
        pytest.param(1, Decimal("29.99"), id="single_item"),
        pytest.param(5, Decimal("149.95"), id="five_items"),
        pytest.param(10, Decimal("299.90"), id="ten_items"),
    ])
    def test_order_total_calculation(
        self, order_service, customer, product_in_stock, quantity, expected_total
    ):
        order = order_service.create_order(
            customer_id=customer.id,
            items=[{"product_id": product_in_stock.id, "quantity": quantity}]
        )
        assert order.total == expected_total

    # Mocking external services
    def test_order_sends_confirmation_email(
        self, order_service, customer, product_in_stock, mocker
    ):
        mock_email = mocker.patch.object(order_service, "_send_confirmation_email")

        order = order_service.create_order(
            customer_id=customer.id,
            items=[{"product_id": product_in_stock.id, "quantity": 1}]
        )

        mock_email.assert_called_once_with(
            order_id=order.id,
            email=customer.email
        )

    def test_order_creation_with_payment_failure_rolls_back(
        self, order_service, customer, product_in_stock, mocker, db
    ):
        initial_stock = product_in_stock.stock
        mocker.patch.object(
            order_service,
            "_process_payment",
            side_effect=PaymentFailedError("Card declined")
        )

        with pytest.raises(PaymentFailedError):
            order_service.create_order(
                customer_id=customer.id,
                items=[{"product_id": product_in_stock.id, "quantity": 5}]
            )

        # Verify rollback
        db.refresh(product_in_stock)
        assert product_in_stock.stock == initial_stock  # Stock restored

    # Integration marker
    @pytest.mark.integration
    def test_full_order_lifecycle(
        self, order_service, customer, product_in_stock
    ):
        # Create
        order = order_service.create_order(
            customer_id=customer.id,
            items=[{"product_id": product_in_stock.id, "quantity": 1}]
        )
        assert order.status == OrderStatus.PENDING

        # Process
        order_service.process_order(order.id)
        assert order.status == OrderStatus.PROCESSING

        # Ship
        order_service.ship_order(order.id, tracking="TRACK123")
        assert order.status == OrderStatus.SHIPPED

        # Complete
        order_service.complete_order(order.id)
        assert order.status == OrderStatus.COMPLETED
```

---

*Examples based on pytest 8.x best practices (2025-2026)*
