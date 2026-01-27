# pytest Checklist

Step-by-step checklists for effective pytest usage.

---

## Project Setup Checklist

### Initial Configuration

- [ ] Install pytest and essential plugins
  ```bash
  pip install pytest pytest-cov pytest-xdist pytest-asyncio pytest-mock
  ```
- [ ] Create `tests/` directory at project root
- [ ] Create `tests/conftest.py` for shared fixtures
- [ ] Configure `pyproject.toml` with pytest settings
- [ ] Add `tests/__init__.py` (optional, for imports)
- [ ] Configure coverage settings
- [ ] Add test commands to Makefile/scripts

### Django Project Setup

- [ ] Install Django-specific plugins
  ```bash
  pip install pytest-django pytest-factoryboy
  ```
- [ ] Set `DJANGO_SETTINGS_MODULE` in configuration
- [ ] Create `conftest.py` with Django fixtures
- [ ] Configure database fixtures (db, transactional_db)
- [ ] Set up Factory Boy factories

### FastAPI/Async Project Setup

- [ ] Install async plugins
  ```bash
  pip install pytest-asyncio httpx
  ```
- [ ] Set `asyncio_mode = "auto"` in configuration
- [ ] Create async fixtures for database/clients
- [ ] Configure event loop scope if needed

---

## Writing Tests Checklist

### Before Writing Tests

- [ ] Identify the unit/component to test
- [ ] Determine test type (unit, integration, E2E)
- [ ] List edge cases and error scenarios
- [ ] Identify required fixtures
- [ ] Check if similar tests exist (avoid duplication)

### Test Structure (AAA Pattern)

- [ ] **Arrange**: Set up test data and dependencies
- [ ] **Act**: Execute the code under test
- [ ] **Assert**: Verify the expected outcome
- [ ] Add cleanup if not using fixtures

### Test Quality

- [ ] Test name describes what is being tested
- [ ] One logical assertion per test (or related group)
- [ ] Tests are independent (no shared state)
- [ ] No hardcoded paths (use tmp_path)
- [ ] No sleep() calls (use proper async handling)
- [ ] Mocks are specific and minimal

---

## Fixture Checklist

### Creating Fixtures

- [ ] Use appropriate scope (function/class/module/session)
- [ ] Use `yield` for setup/teardown patterns
- [ ] Keep fixtures focused and single-purpose
- [ ] Use factory pattern for flexible fixtures
- [ ] Document fixture with docstring

### Fixture Organization

- [ ] Shared fixtures in `conftest.py`
- [ ] Domain-specific fixtures in separate files
- [ ] Avoid circular fixture dependencies
- [ ] Consider fixture composition over inheritance

### Fixture Best Practices

- [ ] Prefer smaller scopes unless performance requires larger
- [ ] Use `autouse=True` sparingly
- [ ] Avoid fixtures that depend on test execution order
- [ ] Clean up resources in teardown (after yield)

---

## Parametrization Checklist

### Basic Parametrization

- [ ] Use `@pytest.mark.parametrize` for multiple inputs
- [ ] Include edge cases in parameters
- [ ] Use descriptive IDs for test cases
- [ ] Group related parameters together

### Advanced Parametrization

- [ ] Use `pytest.param()` for marks and IDs
- [ ] Use `indirect=True` for fixture parametrization
- [ ] Consider pytest-lazy-fixtures for fixture references
- [ ] Use `@pytest.mark.parametrize` stacking for combinations

---

## Mocking Checklist

### Before Mocking

- [ ] Verify mocking is necessary (not over-mocking)
- [ ] Identify the correct patch target
- [ ] Mock at the usage location, not definition

### Mock Setup

- [ ] Use `mocker` fixture from pytest-mock
- [ ] Configure return values appropriately
- [ ] Set up side effects for exceptions
- [ ] Use `autospec=True` for signature validation

### Mock Verification

- [ ] Verify mock was called (if expected)
- [ ] Check call arguments when relevant
- [ ] Use `assert_called_once_with()` for single calls
- [ ] Check `call_count` for multiple invocations

---

## Coverage Checklist

### Configuration

- [ ] Set source directories in coverage config
- [ ] Configure branch coverage (`branch = true`)
- [ ] Set up exclusion patterns (migrations, tests)
- [ ] Define minimum coverage threshold

### Analysis

- [ ] Generate HTML coverage report
- [ ] Review uncovered lines
- [ ] Check branch coverage for conditionals
- [ ] Identify dead code

### CI Integration

- [ ] Add coverage to CI pipeline
- [ ] Configure coverage upload (Codecov, Coveralls)
- [ ] Set coverage gate for PRs
- [ ] Track coverage trends

---

## Parallel Execution Checklist

### Prerequisites

- [ ] Tests are isolated and independent
- [ ] No shared mutable state between tests
- [ ] Database fixtures handle isolation
- [ ] File operations use unique paths

### Configuration

- [ ] Install pytest-xdist
- [ ] Choose distribution mode (load, loadscope, loadfile)
- [ ] Set appropriate worker count
- [ ] Configure worker timeout

### Troubleshooting

- [ ] Run tests sequentially first to verify
- [ ] Check for test order dependencies
- [ ] Verify database isolation
- [ ] Review fixture scopes

---

## Async Testing Checklist

### Setup

- [ ] Install pytest-asyncio
- [ ] Configure asyncio_mode (auto/strict)
- [ ] Create async fixtures with `@pytest_asyncio.fixture`

### Writing Async Tests

- [ ] Add `@pytest.mark.asyncio` marker (if not auto mode)
- [ ] Use `await` for all async operations
- [ ] Handle timeouts for network operations
- [ ] Clean up async resources properly

### Common Issues

- [ ] Check event loop lifecycle
- [ ] Avoid mixing sync/async in tests
- [ ] Handle database transactions correctly
- [ ] Verify async mock setup

---

## Django Testing Checklist

### Database Access

- [ ] Use `@pytest.mark.django_db` marker
- [ ] Choose correct fixture (db, transactional_db)
- [ ] Use Factory Boy for model creation
- [ ] Avoid Django JSON fixtures

### API Testing

- [ ] Use DRF APIClient fixture
- [ ] Create authenticated client fixture
- [ ] Test all HTTP methods
- [ ] Verify response status and data

### Model Testing

- [ ] Test model creation and validation
- [ ] Test model methods and properties
- [ ] Test custom managers and querysets
- [ ] Verify constraints and unique fields

---

## CI/CD Checklist

### Pipeline Configuration

- [ ] Run tests on every push/PR
- [ ] Configure test parallelization
- [ ] Set up coverage reporting
- [ ] Cache pip dependencies

### Test Selection

- [ ] Run full suite on main branch
- [ ] Run affected tests on feature branches
- [ ] Skip slow tests in quick checks
- [ ] Run integration tests on schedule

### Reporting

- [ ] Generate JUnit XML for CI systems
- [ ] Upload coverage to tracking service
- [ ] Fail on coverage decrease
- [ ] Report flaky tests

---

## Code Review Checklist

### Test Review

- [ ] Tests cover the changed code
- [ ] Edge cases are tested
- [ ] Error paths are tested
- [ ] Tests are readable and maintainable

### Quality Review

- [ ] No flaky tests introduced
- [ ] Appropriate use of fixtures
- [ ] Mocking is minimal and correct
- [ ] Test names are descriptive

### Coverage Review

- [ ] New code has test coverage
- [ ] Coverage doesn't decrease
- [ ] Critical paths are covered
- [ ] Branch coverage for conditionals

---

## Debugging Checklist

### Test Failures

- [ ] Read the full error message
- [ ] Check fixture setup/teardown
- [ ] Verify test isolation
- [ ] Run single test in verbose mode

### Debugging Tools

- [ ] Use `-v` for verbose output
- [ ] Use `-l` to show local variables
- [ ] Use `--tb=long` for full tracebacks
- [ ] Use `pytest --pdb` for debugger
- [ ] Use `pytest -x` to stop on first failure

### Performance Issues

- [ ] Profile slow tests with `--durations`
- [ ] Check fixture scope optimization
- [ ] Consider parallel execution
- [ ] Review database queries

---

## Quick Reference

### Essential Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run in parallel
pytest -n auto

# Run specific markers
pytest -m "not slow"

# Run failed tests only
pytest --lf

# Debug mode
pytest --pdb -x

# Show slowest tests
pytest --durations=10
```

### Common Markers

```python
@pytest.mark.skip(reason="...")
@pytest.mark.skipif(condition, reason="...")
@pytest.mark.xfail(reason="...")
@pytest.mark.parametrize("input,expected", [...])
@pytest.mark.django_db
@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.integration
```

---

*pytest Checklist v2.0*
