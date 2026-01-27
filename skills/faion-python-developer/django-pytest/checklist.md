# pytest-django Checklist

## Project Setup

### 1. Install Dependencies

```bash
# Core testing
pip install pytest pytest-django

# Factory Boy integration
pip install factory-boy pytest-factoryboy faker

# Performance & utilities
pip install pytest-xdist pytest-cov pytest-randomly

# Mocking HTTP
pip install responses requests-mock

# Time mocking
pip install freezegun
```

- [ ] pytest installed
- [ ] pytest-django installed
- [ ] Factory Boy + pytest-factoryboy installed
- [ ] pytest-xdist for parallel testing
- [ ] pytest-cov for coverage

### 2. Configure pytest

- [ ] Create `pyproject.toml` or `pytest.ini`
- [ ] Set `DJANGO_SETTINGS_MODULE`
- [ ] Define test file patterns
- [ ] Add custom markers
- [ ] Configure warning filters

### 3. Create Test Settings

- [ ] Create `config/settings/test.py`
- [ ] Use in-memory SQLite or faster database
- [ ] Disable password hashing complexity
- [ ] Configure email backend as locmem
- [ ] Set DEBUG = False

### 4. Create Directory Structure

```
tests/
├── conftest.py
├── factories/
├── fixtures/
├── unit/
├── integration/
└── e2e/
```

- [ ] Root `conftest.py` created
- [ ] `factories/` directory for Factory Boy
- [ ] `fixtures/` directory for complex fixtures
- [ ] `unit/` for unit tests
- [ ] `integration/` for API/view tests
- [ ] `e2e/` for end-to-end tests (optional)

---

## Writing Fixtures

### 5. Database Fixtures

- [ ] Use `@pytest.fixture` decorator
- [ ] Request `db` fixture for database access
- [ ] Use `transactional_db` for transaction tests
- [ ] Set appropriate scope (`function`, `class`, `module`, `session`)
- [ ] Document fixture purpose with docstrings

### 6. API Client Fixtures

- [ ] Create `api_client` fixture with `APIClient()`
- [ ] Create `authenticated_client` with `force_authenticate()`
- [ ] Create `admin_client` for admin-only endpoints
- [ ] Clear credentials after tests with yield

### 7. Factory Boy Setup

- [ ] Create factory classes in `factories/`
- [ ] Use `factory.django.DjangoModelFactory`
- [ ] Define `SubFactory` for relationships
- [ ] Use `factory.Faker()` for realistic data
- [ ] Register factories in `conftest.py`

### 8. Fixture Organization

- [ ] Shared fixtures in root `conftest.py`
- [ ] Domain-specific fixtures in subdirectories
- [ ] Use `pytest_plugins` for modular fixtures
- [ ] Avoid global mutable state
- [ ] Compose fixtures for complex setups

---

## Writing Tests

### 9. Test Structure (AAA Pattern)

```python
def test_something(fixture):
    # Arrange - setup test data
    # Act - perform action
    # Assert - verify result
```

- [ ] Clear separation of Arrange/Act/Assert
- [ ] One primary assertion per test
- [ ] Descriptive test names
- [ ] Test docstrings for complex scenarios

### 10. Database Tests

- [ ] Mark with `@pytest.mark.django_db`
- [ ] Use `transaction=True` when needed
- [ ] Use `reset_sequences=True` for ID tests
- [ ] Avoid test interdependence
- [ ] Clean up any non-transactional side effects

### 11. API Tests (DRF)

- [ ] Test authentication requirements
- [ ] Test permission checks
- [ ] Test valid input scenarios
- [ ] Test validation errors (400)
- [ ] Test not found errors (404)
- [ ] Test server errors are handled

### 12. Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("valid", True),
    ("invalid", False),
])
def test_validation(input, expected):
    assert validate(input) == expected
```

- [ ] Group similar test cases
- [ ] Use descriptive parameter IDs
- [ ] Keep parameter lists maintainable
- [ ] Consider fixtures for complex parameters

### 13. Mocking External Services

- [ ] Mock at the boundary (API calls, not internals)
- [ ] Use `unittest.mock.patch` for functions
- [ ] Use `responses` library for HTTP mocking
- [ ] Verify mock calls when relevant
- [ ] Reset mocks between tests

---

## Test Organization

### 14. Test Naming Convention

```
test_{unit}_{scenario}_{expected_result}
```

- [ ] Descriptive, searchable names
- [ ] Consistent naming pattern
- [ ] Group related tests in classes
- [ ] Use markers for categorization

### 15. Custom Markers

```python
@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.unit
```

- [ ] Define markers in `pytest.ini`
- [ ] Mark slow tests
- [ ] Mark integration tests
- [ ] Mark tests requiring external services
- [ ] Use markers in CI for selective runs

### 16. Test Isolation

- [ ] No shared mutable state
- [ ] Each test independent
- [ ] Use fixtures for setup, not class attributes
- [ ] Clean up created files/external resources
- [ ] No test order dependencies

---

## Performance Optimization

### 17. Parallel Testing

```bash
pytest -n auto  # Use all CPU cores
pytest -n 4     # Use 4 processes
```

- [ ] Install pytest-xdist
- [ ] Tests are isolated (no shared state)
- [ ] Database per worker (automatic)
- [ ] Avoid file system conflicts

### 18. Database Optimization

- [ ] Use `--reuse-db` for faster local runs
- [ ] Use `--no-migrations` when possible
- [ ] Use SQLite in-memory for unit tests
- [ ] Session-scoped fixtures for immutable data
- [ ] Consider `setUpTestData` pattern

### 19. Fixture Scope Optimization

| Scope | When to Use |
|-------|-------------|
| `function` | Mutable data, default |
| `class` | Shared within test class |
| `module` | Shared within test file |
| `session` | Immutable, expensive setup |

- [ ] Use session scope for expensive immutable fixtures
- [ ] Use module scope for shared test data
- [ ] Default to function scope for safety
- [ ] Profile fixtures with `--setup-show`

### 20. Settings Optimization

- [ ] Use MD5PasswordHasher in tests
- [ ] Disable unnecessary middleware
- [ ] Use locmem email backend
- [ ] Disable logging or set to WARNING
- [ ] Cache template loaders

---

## CI/CD Integration

### 21. GitHub Actions

```yaml
- name: Run tests
  run: pytest -n auto --cov --cov-report=xml
```

- [ ] Run tests in CI pipeline
- [ ] Generate coverage reports
- [ ] Fail on coverage threshold
- [ ] Cache pip dependencies
- [ ] Run parallel tests

### 22. Coverage Configuration

```toml
[tool.coverage.run]
source = ["apps"]
omit = ["*/migrations/*", "*/tests/*"]
```

- [ ] Configure coverage source
- [ ] Exclude migrations and tests
- [ ] Set minimum coverage threshold
- [ ] Generate HTML reports locally
- [ ] Upload XML to coverage service

### 23. Pre-commit Hooks

- [ ] Run quick tests pre-commit (optional)
- [ ] Run linting pre-commit
- [ ] Full test suite in CI

---

## Debugging & Maintenance

### 24. Debugging Failing Tests

```bash
pytest -x              # Stop on first failure
pytest --pdb           # Drop to debugger
pytest -v              # Verbose output
pytest --tb=long       # Full traceback
pytest --lf            # Run last failed
```

- [ ] Use `-x` for fast feedback
- [ ] Use `--pdb` for interactive debugging
- [ ] Use `--tb=short` for CI
- [ ] Use `--lf` to rerun failures

### 25. Finding Slow Tests

```bash
pytest --durations=10  # Show 10 slowest tests
```

- [ ] Profile test durations regularly
- [ ] Optimize or mark slow tests
- [ ] Consider async tests for I/O bound
- [ ] Split slow tests to separate CI job

### 26. Test Maintenance

- [ ] Review tests during code review
- [ ] Update tests with code changes
- [ ] Remove obsolete tests
- [ ] Refactor common patterns to fixtures
- [ ] Document complex test setups

---

## Quick Reference Commands

```bash
# Run all tests
pytest

# Run specific file
pytest tests/unit/test_services.py

# Run specific test
pytest tests/unit/test_services.py::test_create_order

# Run by marker
pytest -m "unit and not slow"

# Parallel with coverage
pytest -n auto --cov=apps --cov-report=html

# Verbose with short traceback
pytest -v --tb=short

# Rerun failures
pytest --lf

# Show fixture setup
pytest --setup-show
```

---

## Verification Checklist

Before merging:

- [ ] All tests pass locally
- [ ] No flaky tests (run 3x with `--count=3`)
- [ ] Coverage threshold met
- [ ] No test warnings
- [ ] Tests run in under 5 minutes (or marked slow)
- [ ] New code has corresponding tests
