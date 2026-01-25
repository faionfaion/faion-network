---
name: faion-testing-patterns
user-invocable: false
description: "Testing patterns: AAA, fixtures, mocking strategies, coverage, TDD"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(coverage:*)
---

# Testing Patterns & Best Practices

## Test Structure Patterns

### Arrange-Act-Assert (AAA)

```python
def test_user_creation():
    # Arrange - Set up test data and conditions
    service = UserService()
    user_data = {"name": "John", "email": "john@example.com"}

    # Act - Perform the action being tested
    user = service.create(user_data)

    # Assert - Verify the expected outcome
    assert user.id is not None
    assert user.name == "John"
```

### Given-When-Then (BDD)

```python
def test_user_login():
    # Given - A registered user exists
    user = create_user("john@example.com", "password123")

    # When - The user logs in with correct credentials
    result = auth_service.login("john@example.com", "password123")

    # Then - A valid session token is returned
    assert result.token is not None
    assert result.user_id == user.id
```

## Test Isolation

```python
class TestUserService:
    """Each test is independent, no shared state."""

    @pytest.fixture(autouse=True)
    def setup(self, db):
        db.clear_all()
        yield
        db.clear_all()

    def test_create_user(self, user_service):
        user = user_service.create({"name": "John"})
        assert user.id == 1  # First user in fresh db

    def test_list_users(self, user_service):
        users = user_service.list_all()
        assert len(users) == 0  # Fresh db
```

## Test Pyramid

```
            /\
           / E2E \        ← Few, slow, expensive (10%)
          /------\
         / Integration \  ← Some, medium speed (20%)
        /--------------\
       /   Unit Tests   \ ← Many, fast, cheap (70%)
      /------------------\
```

**Recommended ratio:** 70% Unit, 20% Integration, 10% E2E

## Mocking Strategies

### When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Your own code logic |
| Database in unit tests | Simple utilities |
| File system | Pure functions |
| Network calls | Domain logic |
| Time/randomness | Data structures |

### Builder Pattern

```python
class UserBuilder:
    def __init__(self):
        self._name = "Default User"
        self._email = "default@example.com"
        self._role = "user"

    def with_name(self, name: str) -> "UserBuilder":
        self._name = name
        return self

    def as_admin(self) -> "UserBuilder":
        self._role = "admin"
        return self

    def build(self) -> User:
        return User(name=self._name, email=self._email, role=self._role)

# Usage
user = UserBuilder().with_name("John").as_admin().build()
```

### Factory Pattern

```python
import factory
from factory.faker import Faker

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = Faker("name")
    email = Faker("email")
    created_at = factory.LazyFunction(datetime.now)

# Usage
user = UserFactory()  # Random user
user = UserFactory(name="John")  # Override field
users = UserFactory.create_batch(10)  # Create many
```

## Coverage

### Commands

```bash
# Python
pytest --cov=src --cov-report=html --cov-fail-under=80

# JavaScript
npx jest --coverage
npx vitest run --coverage

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Best Practices

1. **Set realistic thresholds** - 70-80%, not 100%
2. **Focus on critical paths** - business logic > boilerplate
3. **Exclude generated code** - don't test auto-generated files
4. **Branch coverage matters** - not just line coverage
5. **Don't game metrics** - tests should verify behavior

## TDD Workflow

### Red-Green-Refactor

```
RED: Write failing test
    ↓
GREEN: Write minimum code to pass
    ↓
REFACTOR: Improve code quality
    ↓
(repeat)
```

### Example

```python
# Step 1: RED - Write failing test
def test_calculate_discount():
    calculator = PriceCalculator()
    result = calculator.calculate_discount(100, 10)
    assert result == 90  # FAILS - class doesn't exist

# Step 2: GREEN - Minimal implementation
class PriceCalculator:
    def calculate_discount(self, price: float, percent: float) -> float:
        return price - (price * percent / 100)

# Step 3: REFACTOR - Improve
class PriceCalculator:
    def calculate_discount(self, price: float, percent: float) -> float:
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        return round(price * (1 - percent / 100), 2)
```

## CI Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4

  test-javascript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test -- --coverage
```

## Quick Reference

| Framework | Run All | Run Specific | Coverage |
|-----------|---------|--------------|----------|
| pytest | `pytest` | `pytest tests/test_x.py -k name` | `pytest --cov=src` |
| Jest | `npx jest` | `npx jest -t "name"` | `npx jest --coverage` |
| Vitest | `npx vitest` | `npx vitest -t "name"` | `npx vitest --coverage` |
| Go | `go test ./...` | `go test -run TestName` | `go test -cover` |

## Sources

- [Test Pyramid - Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html) - testing strategy
- [AAA Pattern](https://xp123.com/articles/3a-arrange-act-assert/) - test structure
- [Test Double Patterns](https://martinfowler.com/bliki/TestDouble.html) - types of test doubles
- [Codecov Documentation](https://docs.codecov.com/docs) - coverage reporting
- [GitHub Actions CI/CD](https://docs.github.com/en/actions) - continuous integration
