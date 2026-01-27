# LLM Prompts for pytest

Effective prompts for LLM-assisted pytest development.

---

## Prompt Engineering Principles

### Context is Key

When requesting pytest help from LLMs, include:

1. **pytest version** (8.x has different features than 7.x)
2. **Installed plugins** (pytest-asyncio, pytest-mock, etc.)
3. **Project structure** (src layout, test organization)
4. **Existing patterns** (sample fixture or test from your codebase)
5. **Specific requirements** (coverage targets, markers used)

### Effective Prompt Structure

```
[Context] + [Specific Request] + [Constraints/Style Guide]
```

---

## Test Generation Prompts

### Generate Unit Tests for a Function

```
Using pytest 8.x, write unit tests for this function:

```python
def calculate_discount(price: float, quantity: int) -> float:
    """Calculate discount based on quantity."""
    if quantity < 0 or price < 0:
        raise ValueError("Price and quantity must be non-negative")
    if quantity >= 100:
        return price * 0.20
    elif quantity >= 50:
        return price * 0.15
    elif quantity >= 10:
        return price * 0.10
    elif quantity >= 5:
        return price * 0.05
    return 0
```

Requirements:
- Use AAA pattern (Arrange, Act, Assert)
- Include parametrization for all discount tiers
- Test edge cases (0, boundary values, negative inputs)
- Use pytest.raises for error cases
- Follow naming convention: test_{action}_{condition}_{expected}
```

### Generate Tests for a Class

```
Write pytest tests for this service class:

```python
class UserService:
    def __init__(self, db_session, email_client):
        self.db = db_session
        self.email = email_client

    def create_user(self, data: dict) -> User:
        # Creates user and sends welcome email
        pass

    def get_by_email(self, email: str) -> User | None:
        # Returns user or None
        pass

    def deactivate_user(self, user_id: int) -> bool:
        # Soft deletes user, sends notification
        pass
```

Requirements:
- Create fixtures for db_session and email_client mocks
- Test happy paths and error cases
- Mock email sending
- Use factory fixture for creating test users
- Include docstrings explaining what each test verifies
```

### Generate Tests from Docstring/Specification

```
Generate pytest tests based on this specification:

Feature: Shopping Cart
  - Add item to cart (increases quantity if already present)
  - Remove item from cart (raises error if not in cart)
  - Calculate total (with tax rate parameter)
  - Apply coupon code (max one per cart, validates expiration)
  - Clear cart

Constraints:
- Max 100 items per cart
- Items must have positive price
- Coupon codes are case-insensitive

Generate:
1. Test class with fixtures
2. Parametrized tests for edge cases
3. Tests for validation rules
4. Integration test for full checkout flow
```

---

## Fixture Generation Prompts

### Generate Factory Fixture

```
Create a pytest factory fixture for this SQLAlchemy model:

```python
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    total = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order")
```

Requirements:
- Include sensible defaults
- Support custom overrides via kwargs
- Auto-increment unique values (order numbers)
- Handle cleanup after tests
- Compose with existing user_factory fixture
```

### Generate Session-Scoped Fixture

```
Create a pytest fixture for a PostgreSQL test database that:
- Creates a fresh database at session start
- Runs migrations
- Provides connection pool
- Supports pytest-xdist (unique DB per worker)
- Cleans up after session ends

Current setup:
- SQLAlchemy 2.0
- Alembic migrations
- PostgreSQL 15
```

### Generate Async Fixtures

```
Create async pytest fixtures for testing this FastAPI application:

```python
# main.py
app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await create_db_pool()
    app.state.redis = await create_redis_client()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()
    await app.state.redis.close()
```

Need:
- async_client fixture using httpx.AsyncClient
- Mocked database pool
- Mocked Redis client
- Auth fixture that returns valid JWT token
```

---

## Parametrization Prompts

### Generate Comprehensive Parametrization

```
Create parametrized tests for this email validator:

```python
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

Generate test cases covering:
- Valid emails (various formats)
- Invalid emails (missing @, domain, TLD)
- Edge cases (Unicode, very long strings)
- Empty/None inputs

Use pytest.param with descriptive IDs for each case.
```

### Generate Cartesian Product Tests

```
I need to test a currency formatter with these variables:
- Amount: 0, 100, 1000.50, -50, 1000000
- Currency: USD, EUR, GBP, JPY
- Locale: en_US, de_DE, ja_JP

Generate parametrized tests that cover all combinations efficiently.
Include expected outputs for each combination.
```

---

## Mock Generation Prompts

### Generate Mock Setup

```
Generate pytest-mock setup for testing this service that:
1. Calls an external REST API
2. Stores result in database
3. Sends notification via webhook
4. Logs the operation

```python
class DataSyncService:
    def __init__(self, api_client, db, webhook_client, logger):
        self.api = api_client
        self.db = db
        self.webhook = webhook_client
        self.logger = logger

    def sync_user_data(self, user_id: int) -> SyncResult:
        # Fetches from API, saves to DB, notifies webhook
        pass
```

Include:
- Successful sync test with all mocks
- API failure test (retry logic)
- Database failure test (rollback verification)
- Webhook failure test (should not fail sync)
```

### Generate Mock for Complex Dependency

```
Generate mocks for testing code that uses AWS S3:

```python
class FileStorage:
    def __init__(self, s3_client, bucket_name):
        self.s3 = s3_client
        self.bucket = bucket_name

    async def upload(self, key: str, data: bytes) -> str:
        await self.s3.put_object(Bucket=self.bucket, Key=key, Body=data)
        return f"s3://{self.bucket}/{key}"

    async def download(self, key: str) -> bytes:
        response = await self.s3.get_object(Bucket=self.bucket, Key=key)
        return await response['Body'].read()

    async def delete(self, key: str) -> bool:
        await self.s3.delete_object(Bucket=self.bucket, Key=key)
        return True
```

Create:
- S3 client mock fixture
- Tests for upload, download, delete
- Error handling tests (NoSuchKey, AccessDenied)
- Test for large file handling
```

---

## Configuration Prompts

### Generate pytest Configuration

```
Generate pyproject.toml pytest configuration for a project with:

Structure:
src/
  mypackage/
tests/
  unit/
  integration/
  e2e/

Requirements:
- pytest 8.x with strict mode
- pytest-asyncio (auto mode)
- pytest-cov with 80% threshold
- pytest-xdist for parallel execution
- Custom markers: slow, integration, e2e, requires_db
- Exclude __init__.py and migrations from coverage
- Filter deprecation warnings
```

### Generate CI Configuration

```
Generate GitHub Actions workflow for pytest that:

1. Runs on Python 3.10, 3.11, 3.12
2. Unit tests run on all PRs (parallel, no slow tests)
3. Integration tests run on main branch only
4. Requires PostgreSQL and Redis services
5. Uploads coverage to Codecov
6. Fails if coverage drops below 80%
7. Caches pip dependencies

Current project uses:
- pytest with pytest-cov, pytest-asyncio, pytest-xdist
- PostgreSQL 15
- Redis 7
```

---

## Debugging Prompts

### Debug Failing Test

```
This test is failing intermittently. Help me debug:

```python
@pytest.mark.asyncio
async def test_concurrent_updates(async_db):
    user = await create_user(async_db)

    async def update_balance(amount):
        await async_db.execute(
            "UPDATE users SET balance = balance + $1 WHERE id = $2",
            amount, user.id
        )

    await asyncio.gather(*[update_balance(10) for _ in range(10)])

    result = await async_db.fetchval(
        "SELECT balance FROM users WHERE id = $1", user.id
    )
    assert result == 100  # Sometimes fails with 90 or 80
```

The test passes when run alone but fails when run with other tests.
What could cause this? How should I fix it?
```

### Fix Fixture Scope Issue

```
I'm getting this error:
"ScopeMismatch: You tried to access the 'function' scoped fixture 'user'
from a 'session' scoped fixture 'database'."

Here's my fixtures:

```python
@pytest.fixture(scope="session")
def database():
    db = create_database()
    yield db
    db.close()

@pytest.fixture
def user(database):  # function scope by default
    return database.create_user()

@pytest.fixture(scope="session")
def admin_user(user):  # This causes the error
    user.is_admin = True
    return user
```

How do I restructure these fixtures correctly?
```

---

## Refactoring Prompts

### Convert unittest to pytest

```
Convert this unittest test class to idiomatic pytest:

```python
import unittest
from unittest.mock import Mock, patch

class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PaymentProcessor()
        self.mock_gateway = Mock()

    def tearDown(self):
        self.processor.cleanup()

    @patch('payments.gateway.charge')
    def test_process_payment_success(self, mock_charge):
        mock_charge.return_value = {'status': 'success', 'id': '123'}
        result = self.processor.process(amount=100, card='4111...')
        self.assertEqual(result.status, 'success')
        mock_charge.assert_called_once_with(100, '4111...')

    def test_process_invalid_amount_raises_error(self):
        with self.assertRaises(ValueError) as context:
            self.processor.process(amount=-100, card='4111...')
        self.assertIn('positive', str(context.exception))
```

Convert to pytest with:
- Fixtures instead of setUp/tearDown
- pytest-mock instead of unittest.mock.patch
- Native pytest assertions
- Parametrization where applicable
```

### Improve Test Coverage

```
These tests have 60% coverage. Suggest additional tests to reach 80%:

```python
# src/calculator.py
class Calculator:
    def __init__(self, precision=2):
        self.precision = precision
        self.history = []

    def add(self, a, b):
        result = round(a + b, self.precision)
        self.history.append(('add', a, b, result))
        return result

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = round(a / b, self.precision)
        self.history.append(('divide', a, b, result))
        return result

    def get_history(self):
        return self.history.copy()

    def clear_history(self):
        self.history = []
```

Current tests only cover add() and divide() happy paths.
What's missing? Generate the additional tests.
```

---

## Best Practice Prompts

### Review Test Quality

```
Review these tests and suggest improvements:

```python
def test_user():
    u = User("John", "john@test.com")
    assert u.name == "John"
    assert u.email == "john@test.com"
    assert u.is_active == True
    u.deactivate()
    assert u.is_active == False
    u.activate()
    assert u.is_active == True
    u.update_email("new@test.com")
    assert u.email == "new@test.com"

def test_user2():
    u = User("", "invalid")
    try:
        u.validate()
        assert False
    except:
        pass
```

Consider:
- Test isolation
- Single assertion principle
- Naming conventions
- Error handling
- Readability
```

### Generate Test Strategy

```
I'm starting a new FastAPI project. Help me create a testing strategy:

Project structure:
- REST API with 20+ endpoints
- PostgreSQL database with SQLAlchemy
- Redis for caching
- External payment API integration
- Background tasks with Celery

Questions:
1. How should I organize tests (unit/integration/e2e)?
2. What fixtures should be session vs function scoped?
3. How to handle external API mocking?
4. How to test Celery tasks?
5. What coverage target is realistic?
6. How to structure CI/CD test runs?

Provide a recommended pytest configuration and folder structure.
```

---

## Quick Reference Prompts

### One-Liner Requests

```
# Generate basic test
"Write a pytest test for a function that calculates BMI given height and weight"

# Generate fixture
"Create a pytest fixture that provides a temporary SQLite database"

# Generate parametrization
"Parametrize tests for a password validator (min 8 chars, uppercase, number)"

# Generate mock
"Mock a requests.get call that returns JSON data"

# Generate marker
"Create a custom pytest marker for tests requiring API keys"

# Fix error
"Why does pytest show 'fixture not found' when it's defined in conftest.py?"
```

---

## Prompt Templates

### Template: New Test File

```
Create a new pytest test file for [MODULE_NAME]:

Module path: [PATH]
Module purpose: [DESCRIPTION]
Main functions/classes: [LIST]

Existing patterns in project:
```python
[PASTE EXAMPLE FROM CODEBASE]
```

pytest.ini markers: [LIST MARKERS]
Installed plugins: [LIST PLUGINS]

Generate:
1. Test class with proper fixtures
2. Happy path tests
3. Error case tests
4. Edge case tests with parametrization
```

### Template: Fix Failing Test

```
Help me fix this failing test:

Test file: [PATH]
Error message:
```
[PASTE ERROR]
```

Test code:
```python
[PASTE TEST]
```

Code under test:
```python
[PASTE IMPLEMENTATION]
```

conftest.py fixtures used:
```python
[PASTE RELEVANT FIXTURES]
```

What's causing the failure? How do I fix it?
```

### Template: Optimize Test Suite

```
My test suite is slow. Help me optimize:

Current stats:
- Total tests: [NUMBER]
- Run time: [TIME]
- Slowest tests: [LIST]

Current configuration:
```toml
[PASTE CONFIG]
```

I'm using: [LIST PLUGINS]
Database: [TYPE]
CI environment: [DETAILS]

Suggest:
1. Quick wins for speed improvement
2. Fixture scope optimizations
3. Parallelization strategy
4. Tests to mark as 'slow'
```

---

*Prompts optimized for pytest 8.x (2025-2026)*
