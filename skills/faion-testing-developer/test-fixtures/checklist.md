# Test Fixtures Checklist

Step-by-step checklist for designing, implementing, and maintaining test fixtures.

---

## Phase 1: Planning

### 1.1 Identify Fixture Need

- [ ] Multiple tests require similar setup
- [ ] Object creation is complex (3+ fields or dependencies)
- [ ] Setup requires external resources (database, files, services)
- [ ] Cleanup/teardown is needed after tests
- [ ] Test isolation requires fresh state

### 1.2 Choose Fixture Pattern

| Pattern | Choose When |
|---------|-------------|
| **pytest Fixture** | Resource lifecycle, Python project |
| **Factory** | Domain objects with defaults |
| **Builder** | Complex objects, many optional params |
| **Object Mother** | Predefined domain scenarios |
| **Inline Creation** | Simple data, single-use, tells story |

### 1.3 Determine Scope

- [ ] `function` (default) - Tests modify fixture data
- [ ] `class` - Shared within class, no modifications
- [ ] `module` - Expensive setup, read-only access
- [ ] `session` - Very expensive (Docker, external services)

**Decision rule:** Start with `function`. Only increase scope if:
1. Setup is expensive (> 100ms)
2. Tests never modify shared state
3. Isolation is guaranteed by other means (transactions)

---

## Phase 2: Design

### 2.1 Fixture Interface

- [ ] Fixture name is descriptive (`user_with_orders` not `u1`)
- [ ] Factory accepts overrides for all configurable fields
- [ ] Builder methods are named after domain concepts
- [ ] Required vs optional parameters are clear

### 2.2 Default Values

- [ ] Defaults are minimal (only required fields)
- [ ] Defaults represent typical/valid state
- [ ] Unique values use sequences or UUIDs
- [ ] Timestamps use deterministic values for reproducibility

### 2.3 Dependencies

- [ ] Fixture dependencies are explicit (via parameters)
- [ ] No hidden global state dependencies
- [ ] Circular dependencies are avoided
- [ ] Dependency chain is shallow (3 levels max)

### 2.4 Cleanup Strategy

| Resource Type | Cleanup Method |
|---------------|----------------|
| Database records | Transaction rollback |
| Files | Yield fixture with `os.remove()` |
| External services | Yield fixture with cleanup call |
| In-memory objects | No cleanup needed |
| Docker containers | Yield fixture with `container.stop()` |

---

## Phase 3: Implementation

### 3.1 pytest Fixtures

- [ ] Use `@pytest.fixture` decorator
- [ ] Add docstring explaining what fixture provides
- [ ] Use `yield` for setup/teardown pattern
- [ ] Place in appropriate conftest.py level

```python
@pytest.fixture
def db_session(engine):
    """Provides a transactional database session.

    Session is rolled back after each test.
    """
    session = Session(engine)
    session.begin_nested()

    yield session

    session.rollback()
    session.close()
```

### 3.2 Factory Pattern

- [ ] Extend appropriate base (SQLAlchemyModelFactory, DjangoModelFactory)
- [ ] Use `Sequence` for unique fields
- [ ] Use `LazyAttribute` for computed fields
- [ ] Use `SubFactory` for relationships

```python
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    profile = factory.SubFactory(ProfileFactory)
```

### 3.3 Builder Pattern

- [ ] Each method returns `self` for chaining
- [ ] `build()` method creates final object
- [ ] Methods are named `with_*` or domain-specific
- [ ] Defaults are set in constructor

```python
class OrderBuilder:
    def __init__(self):
        self._user_id = "default"
        self._items = []

    def for_user(self, user_id):
        self._user_id = user_id
        return self

    def with_item(self, sku, qty=1):
        self._items.append(Item(sku, qty))
        return self

    def build(self):
        return Order(self._user_id, self._items)
```

### 3.4 conftest.py Organization

```
tests/
├── conftest.py              # Shared fixtures
│   ├── @pytest.fixture(scope="session") engine
│   ├── @pytest.fixture(scope="session") session_factory
│   └── @pytest.fixture db_session
├── factories/
│   ├── __init__.py          # Import all factories
│   ├── users.py             # UserFactory
│   └── orders.py            # OrderFactory
└── unit/
    └── conftest.py          # Unit-specific mocks
```

---

## Phase 4: Verification

### 4.1 Isolation Testing

- [ ] Run tests in random order (`pytest --random-order`)
- [ ] Run tests in parallel (`pytest -n auto`)
- [ ] Verify no test depends on another test's side effects
- [ ] Check database is clean between tests

### 4.2 Cleanup Verification

- [ ] Run test, check resources are released
- [ ] Force test failure, verify cleanup still runs
- [ ] Check for resource leaks (connections, files, handles)
- [ ] Monitor memory usage during test suite

### 4.3 Performance Check

- [ ] Measure fixture setup time
- [ ] Identify slow fixtures (candidates for higher scope)
- [ ] Check for unnecessary fixture creation
- [ ] Profile database queries in fixtures

```bash
# Check fixture setup times
pytest --setup-show

# Profile test run
pytest --durations=10
```

---

## Phase 5: Maintenance

### 5.1 Documentation

- [ ] Docstrings on all fixtures
- [ ] README in fixtures/ directory
- [ ] Usage examples in test files
- [ ] Document fixture dependencies

### 5.2 Refactoring Triggers

Refactor fixtures when:
- [ ] 3+ tests create similar objects inline
- [ ] Fixture is used in only one test (move inline or delete)
- [ ] Model changes break multiple fixtures
- [ ] Fixture setup exceeds 10 lines

### 5.3 Review Checklist

During code review, check:
- [ ] Fixture scope is appropriate
- [ ] No Mystery Guest (data source is clear)
- [ ] Cleanup is complete
- [ ] No shared mutable state
- [ ] Factory defaults are sensible

---

## Quick Reference

### Fixture Scope Decision

```
Is setup expensive (> 100ms)?
├── No  → function scope
└── Yes → Do tests modify fixture?
          ├── Yes → function scope (consider caching)
          └── No  → Is data shared across modules?
                    ├── No  → module scope
                    └── Yes → session scope
```

### Factory vs Builder vs Inline

```
How many fields to customize?
├── 0-1 → Inline creation
├── 2-4 → Factory with overrides
└── 5+  → Builder pattern

Is the scenario domain-specific?
├── Yes → Object Mother
└── No  → Factory
```

### conftest.py Placement

```
Who needs this fixture?
├── One test file     → Define in test file
├── One test package  → Package conftest.py
├── All tests         → Root conftest.py
└── External projects → Plugin
```

---

## Anti-Pattern Checklist

Avoid these common mistakes:

- [ ] **God Fixture** - One fixture sets up everything
  - Fix: Split into focused, composable fixtures

- [ ] **Mystery Guest** - Test uses data from unknown source
  - Fix: Create data in test or use explicit factory

- [ ] **Eager Fixture** - Fixture always created even when not needed
  - Fix: Use `autouse=False`, request explicitly

- [ ] **Fragile Fixture** - Changes in one test break others
  - Fix: Use function scope, transactional rollback

- [ ] **Hidden Side Effects** - Fixture modifies global state
  - Fix: Reset state in teardown, use isolation

- [ ] **Complex Fixture Graph** - Deep dependency chains
  - Fix: Flatten, use composition over inheritance
