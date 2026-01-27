# Django Testing with pytest

## Overview

pytest-django is the preferred testing framework for Django projects, combining pytest's powerful fixtures, parametrization, and cleaner syntax with Django's database and request handling. This methodology covers test organization, fixtures, mocking, Factory Boy integration, and performance optimization.

**Key Benefits:**

| Feature | pytest-django | Django TestCase |
|---------|---------------|-----------------|
| Fixture system | Explicit, modular, reusable | setUp/tearDown per class |
| Parametrization | Built-in `@pytest.mark.parametrize` | Manual loops |
| Assertions | Simple `assert` statements | `self.assertEqual()` methods |
| Parallel testing | pytest-xdist (auto-detect cores) | `--parallel N` |
| Plugin ecosystem | 800+ plugins | Limited |

## When to Use

- Writing unit tests for Django models, services, and utilities
- Integration testing API endpoints (DRF)
- Testing database operations with transactions
- Mocking external services (Stripe, AWS, etc.)
- Setting up test data with Factory Boy
- Performance-sensitive test suites requiring parallelization

## Core Concepts

### Database Access

```python
# Mark test function for database access
@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create(email="test@example.com")
    assert user.pk is not None

# For fixtures needing database access
@pytest.fixture
def user(db):  # Request 'db' fixture explicitly
    return User.objects.create(email="test@example.com")
```

### Fixture Types

| Fixture | Use Case | Transaction |
|---------|----------|-------------|
| `db` | Basic database access | Auto-rollback |
| `transactional_db` | Testing transactions explicitly | No auto-rollback |
| `django_db_reset_sequences` | Reset auto-increment IDs | Yes |
| `django_db_serialized_rollback` | Serialized data rollback | Yes |

### Factory Boy Integration

pytest-factoryboy bridges Factory Boy with pytest fixtures:

```python
# factories.py
import factory
from apps.users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name = factory.Faker("name")

# conftest.py
from pytest_factoryboy import register
from .factories import UserFactory

register(UserFactory)  # Creates 'user' and 'user_factory' fixtures
```

## Directory Structure

```
tests/
├── conftest.py              # Root fixtures (shared across all tests)
├── factories/
│   ├── __init__.py
│   ├── users.py             # UserFactory, ProfileFactory
│   └── orders.py            # OrderFactory, OrderItemFactory
├── fixtures/
│   ├── __init__.py
│   ├── api.py               # API client fixtures
│   └── data.py              # Data fixtures
├── unit/
│   ├── conftest.py          # Unit-specific fixtures
│   ├── test_models.py
│   ├── test_services.py
│   └── test_validators.py
├── integration/
│   ├── conftest.py          # Integration-specific fixtures
│   ├── test_api.py
│   └── test_views.py
└── e2e/
    ├── conftest.py
    └── test_flows.py
```

## LLM Usage Tips

### For Code Generation

1. **Provide context about your models:**
   ```
   Generate pytest tests for UserService.create_user() that:
   - Takes email, name, user_type
   - Sends welcome email via Celery
   - Raises ValidationError for duplicate emails
   ```

2. **Specify fixture requirements:**
   ```
   Create a pytest fixture for authenticated API client using:
   - DRF's APIClient
   - force_authenticate() method
   - Custom User model with uid field
   ```

3. **Request parametrized tests for validators:**
   ```
   Write parametrized tests for password_validator() checking:
   - Minimum 8 characters
   - At least one uppercase
   - At least one digit
   - At least one special character
   ```

### For Test Refactoring

1. **Convert unittest to pytest:**
   ```
   Convert this Django TestCase to pytest style:
   [paste existing test class]
   Use fixtures instead of setUp(), parametrize similar tests
   ```

2. **Add Factory Boy factories:**
   ```
   Create Factory Boy factories for these models:
   [paste model definitions]
   Include SubFactory for relationships, Faker for realistic data
   ```

### For Debugging

1. **Analyze test failures:**
   ```
   This test is failing with TransactionManagementError.
   [paste test code]
   Should I use transactional_db instead of db?
   ```

2. **Performance optimization:**
   ```
   These tests are slow (5 minutes for 200 tests).
   [paste conftest.py]
   Suggest optimizations for fixture scope and database access.
   ```

## Key Patterns

### Arrange-Act-Assert (AAA)

```python
def test_order_total_calculation(order_factory, product):
    # Arrange
    order = order_factory(items=[
        {"product": product, "quantity": 2}
    ])

    # Act
    total = order.calculate_total()

    # Assert
    assert total == product.price * 2
```

### Test Behavior, Not Implementation

```python
# Bad: Testing internal method calls
def test_create_order_calls_validate(self, user):
    with patch.object(service, '_validate') as mock:
        service.create_order(user, items=[])
        mock.assert_called()

# Good: Testing observable behavior
def test_create_order_rejects_empty_cart(self, user):
    with pytest.raises(ValidationError, match="Cart is empty"):
        service.create_order(user, items=[])
```

### Fixture Composition

```python
@pytest.fixture
def order_with_payment(order_factory, payment_factory):
    """Order with completed payment for testing fulfillment."""
    order = order_factory(status="pending")
    payment_factory(order=order, status="completed")
    return order
```

## Performance Optimization

| Technique | Impact | Implementation |
|-----------|--------|----------------|
| Parallel testing | 2-4x faster | `pytest -n auto` (pytest-xdist) |
| Reuse database | Skip migrations | `--reuse-db` |
| Session-scoped fixtures | Reduce setup | `scope="session"` |
| Simpler password hasher | Faster auth | `MD5PasswordHasher` in test settings |
| Disable unused plugins | Reduce overhead | `pytest -p no:doctest` |

## External Links

### Official Documentation

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [pytest-factoryboy Documentation](https://pytest-factoryboy.readthedocs.io/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)

### Recommended Reading

- [Real Python: Django pytest Fixtures](https://realpython.com/django-pytest-fixtures/)
- [pytest-with-eric: Django REST API Testing](https://pytest-with-eric.com/pytest-advanced/pytest-django-restapi-testing/)
- [Django Tests Cheatsheet 2025](https://medium.com/@jonathan.hoffman91/django-tests-cheatsheet-2025-4fae3d32c3c5)
- [Making Your Django Tests Faster](https://schegel.net/posts/making-your-django-tests-faster/)

### Tools

- [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) - Parallel test execution
- [pytest-randomly](https://github.com/pytest-dev/pytest-randomly) - Randomize test order
- [pytest-cov](https://github.com/pytest-dev/pytest-cov) - Coverage reporting
- [responses](https://github.com/getsentry/responses) - Mock HTTP requests
- [freezegun](https://github.com/spulec/freezegun) - Mock datetime

## Related Files

- [checklist.md](checklist.md) - Step-by-step pytest-django checklist
- [examples.md](examples.md) - Real-world testing examples
- [templates.md](templates.md) - Copy-paste configurations
- [llm-prompts.md](llm-prompts.md) - Effective prompts for LLM-assisted testing
