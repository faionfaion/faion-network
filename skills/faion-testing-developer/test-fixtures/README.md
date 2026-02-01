# Test Fixtures

## Overview

Test fixtures provide consistent, reusable test data and setup procedures for automated testing. They establish predictable starting conditions, reduce code duplication, and improve test readability.

**Core Purpose:**
- Set up preconditions for tests
- Provide consistent test data
- Handle setup/teardown lifecycle
- Enable test isolation

## Fixture Patterns

### 1. Factory Pattern

Creates objects with sensible defaults that can be overridden. Preferred over static fixtures.

| Tool | Language | Use Case |
|------|----------|----------|
| Factory Boy | Python | Django, SQLAlchemy models |
| pytest-factoryboy | Python | Factory Boy + pytest integration |
| FactoryBot | Ruby | Rails models |
| Fishery | TypeScript | Type-safe factories |
| go-factory | Go | Struct factories |

**When to use:** Most scenarios. Factories are the default choice for test data creation.

### 2. Builder Pattern

Creates complex objects step-by-step with fluent interface. More verbose than factories but more explicit.

```
OrderBuilder()
    .with_item("SKU-001", quantity=2)
    .with_discount(10)
    .shipped_to(address)
    .build()
```

**When to use:** Objects with many optional parameters, complex configurations, or when you need explicit test scenarios.

### 3. Object Mother Pattern

Pre-configured factory methods for common test scenarios.

```python
class UserMother:
    @staticmethod
    def admin(): ...

    @staticmethod
    def inactive_user(): ...

    @staticmethod
    def user_with_expired_subscription(): ...
```

**When to use:** Repeated domain scenarios, integration tests with specific business states.

### 4. pytest Fixtures (Dependency Injection)

Python-specific pattern using `@pytest.fixture` decorator with automatic dependency injection.

```python
@pytest.fixture
def db_session(engine):
    session = Session(engine)
    yield session
    session.rollback()
```

**When to use:** Setup/teardown, resource management, test isolation.

## Fixture Scopes (pytest)

| Scope | Lifetime | Use Case |
|-------|----------|----------|
| `function` | Per test | Default, fresh state per test |
| `class` | Per test class | Shared within class |
| `module` | Per test file | Database connection per module |
| `package` | Per package | Shared across package |
| `session` | Entire run | Docker containers, expensive setup |

**Rule of thumb:** Start with `function` scope. Only increase scope when setup is expensive AND tests don't modify shared state.

## Fixture Composition

### Vertical Composition (Dependency Chain)

```python
@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def session_factory(engine):
    return sessionmaker(bind=engine)

@pytest.fixture
def db_session(session_factory):
    session = session_factory()
    yield session
    session.rollback()
```

### Horizontal Composition (Multiple Fixtures)

```python
@pytest.fixture
def order_with_user(db_session, user_factory, order_factory):
    user = user_factory()
    order = order_factory(user=user)
    return {"user": user, "order": order}
```

## Cleanup Strategies

### 1. Yield Fixtures (Recommended)

```python
@pytest.fixture
def temp_file():
    path = create_temp_file()
    yield path
    os.remove(path)  # Always runs, even on failure
```

### 2. Transactional Rollback

```python
@pytest.fixture
def db_session(session_factory):
    session = session_factory()
    session.begin_nested()  # Savepoint
    yield session
    session.rollback()      # Rollback to savepoint
    session.close()
```

### 3. Request Finalizers

```python
@pytest.fixture
def resource(request):
    r = acquire_resource()
    request.addfinalizer(lambda: release_resource(r))
    return r
```

## Database Fixtures

### Django (pytest-django)

| Marker/Fixture | Behavior |
|----------------|----------|
| `@pytest.mark.django_db` | Wraps test in transaction, auto-rollback |
| `@pytest.mark.django_db(transaction=True)` | Real transactions (for testing commits) |
| `django_db_reset_sequences` | Reset auto-increment IDs |

### SQLAlchemy

**Transactional test pattern:**
1. Create session-scoped engine
2. Create function-scoped session with nested transaction (savepoint)
3. Rollback after each test

### Key Principles

- **Use in-memory databases** for unit tests (faster)
- **Use testcontainers** for integration tests (real database)
- **Never share mutable state** between tests
- **Reset sequences** if tests depend on specific IDs

## conftest.py Organization

```
tests/
├── conftest.py           # Session/module fixtures (db, app)
├── fixtures/             # Reusable fixture modules
│   ├── __init__.py
│   ├── users.py
│   └── orders.py
├── unit/
│   └── conftest.py       # Unit-specific fixtures (mocks)
├── integration/
│   └── conftest.py       # Integration fixtures (real db)
└── e2e/
    └── conftest.py       # E2E fixtures (browser, API client)
```

**Fixture discovery order:**
1. Test class
2. Test module
3. conftest.py (bottom-up from test file)
4. Plugins

## When NOT to Use Fixtures

### Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| God Fixture | Sets up everything, tests use 10% | Split into focused fixtures |
| Mystery Guest | Data comes from unknown source | Use factories, create data in test |
| Shared Mutable Fixture | Tests interfere with each other | Use function scope, transactional rollback |
| Fixture Reuse Abuse | Session scope for mutable data | Match scope to data lifecycle |
| Over-Engineering | Complex factories for simple data | Inline literals for trivial cases |

### When to Avoid Fixtures

1. **Simple data** - Use inline literals instead
   ```python
   # Bad: fixture for simple string
   def test_greeting(greeting_message):
       assert greeting_message == "Hello"

   # Good: inline
   def test_greeting():
       assert format_greeting("World") == "Hello, World"
   ```

2. **Single-use data** - Create in test
   ```python
   # Bad: fixture used once
   @pytest.fixture
   def special_config():
       return {"mode": "special", "debug": True}

   # Good: inline
   def test_special_mode():
       config = {"mode": "special", "debug": True}
       assert process(config) == expected
   ```

3. **Data that tells the story** - Keep in test for clarity
   ```python
   # Good: data visible in test
   def test_discount_applied():
       order = create_order(
           items=[Item(price=100)],
           discount_code="SAVE20"
       )
       assert order.total == 80
   ```

## Fixtures vs Test Builders

| Aspect | Fixtures (pytest) | Test Builders |
|--------|-------------------|---------------|
| Syntax | Decorator + yield | Fluent methods |
| Reusability | Via conftest.py | Via builder class |
| Customization | Parameters, parametrize | Method chaining |
| Teardown | Built-in (yield) | Manual |
| Best for | Resource management | Complex objects |
| Language | Python-specific | Any language |

**Recommendation:** Use both together.
- Fixtures for resource lifecycle (db, files, services)
- Builders/factories for domain objects (users, orders)

## LLM Usage Tips

When working with LLMs to generate fixtures:

1. **Provide model definitions** - LLMs need to see your models/schemas
2. **Specify fixture scope** - State whether you need fresh or shared fixtures
3. **Mention cleanup requirements** - Transactional, file cleanup, etc.
4. **Reference existing patterns** - Point to conftest.py or existing factories
5. **Specify test type** - Unit/integration/E2E have different fixture needs

## External Resources

### Official Documentation

- [pytest Fixtures Documentation](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest Fixture Reference](https://docs.pytest.org/en/stable/reference/fixtures.html)
- [pytest-django Database Access](https://pytest-django.readthedocs.io/en/latest/database.html)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/en/stable/)
- [pytest-factoryboy](https://pytest-factoryboy.readthedocs.io/)

### Tutorials and Guides

- [Pytest with Eric - Fixture Scopes](https://pytest-with-eric.com/fixtures/pytest-fixture-scope/)
- [Pytest with Eric - Setup and Teardown](https://pytest-with-eric.com/pytest-best-practices/pytest-setup-teardown/)
- [CoderPad - Database Testing with SQLAlchemy](https://coderpad.io/blog/development/a-guide-to-database-unit-testing-with-pytest-and-sqlalchemy/)
- [Better Stack - Pytest Fixtures Guide](https://betterstack.com/community/guides/testing/pytest-fixtures-guide/)
- [Fiddler AI - Advanced Pytest Patterns](https://www.fiddler.ai/blog/advanced-pytest-patterns-harnessing-the-power-of-parametrization-and-factory-methods)

### Patterns and Anti-Patterns

- [Test Data Builders - TU Delft](https://ocw.tudelft.nl/course-readings/5-3-4-test-data-builder/)
- [Test Data Builder Pattern](https://ericvruder.dk/20191209/test-data-builder-pattern/)
- [Creating Test Objects via Design Patterns](https://blog.nimblepros.com/blogs/creating-test-objects-via-design-patterns/)
- [Replace Fixtures with Builders](https://dev.to/everlyhealth/replace-your-test-fixtures-with-builders-4602)
- [Software Testing Anti-patterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
- [Rails Fixtures and Factories](https://semaphore.io/blog/2014/01/14/rails-testing-antipatterns-fixtures-and-factories.html)

### Database Testing

- [Django Testing with pytest-django](https://djangostars.com/blog/django-pytest-testing/)
- [SQLAlchemy Transactional Tests](https://aalvarez.me/posts/python-transactional-tests-using-sqlalchemy-pytest-and-factory-boy/)
- [Pytest SQL Database Testing](https://pytest-with-eric.com/database-testing/pytest-sql-database-testing/)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Files

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step fixture design checklist |
| [examples.md](examples.md) | Real fixture implementations |
| [templates.md](templates.md) | Copy-paste fixture templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted fixture creation |
