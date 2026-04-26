# pytest Checklist

Step-by-step checklists for common pytest workflows.

---

## Project Setup Checklist

### Initial Configuration

- [ ] **Install pytest and plugins**
  ```bash
  pip install pytest pytest-cov pytest-mock pytest-asyncio pytest-xdist
  ```

- [ ] **Create pyproject.toml configuration**
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  addopts = ["--strict-markers", "--strict-config", "-ra"]
  ```

- [ ] **Set up project structure**
  ```
  project/
  ├── src/mypackage/
  ├── tests/
  │   ├── conftest.py
  │   ├── unit/
  │   └── integration/
  └── pyproject.toml
  ```

- [ ] **Create initial conftest.py** with common fixtures

- [ ] **Register custom markers** in pyproject.toml

- [ ] **Configure coverage settings** in pyproject.toml or .coveragerc

- [ ] **Add pytest to CI/CD pipeline**

---

## Writing Tests Checklist

### Before Writing

- [ ] **Identify test type** (unit, integration, E2E)
- [ ] **Determine scope** - what behavior to test
- [ ] **Check existing fixtures** - reuse when possible
- [ ] **Plan parametrization** - identify input variations

### During Writing

- [ ] **Follow naming convention**: `test_{action}_{condition}_{expected}`
  ```python
  def test_create_user_with_invalid_email_raises_validation_error():
  ```

- [ ] **Use AAA pattern**
  ```python
  def test_example():
      # Arrange - set up test data
      # Act - execute the code under test
      # Assert - verify the result
  ```

- [ ] **One assertion focus** per test (can have multiple related asserts)

- [ ] **Use descriptive assertion messages**
  ```python
  assert result == expected, f"Expected {expected}, got {result}"
  ```

- [ ] **Handle expected exceptions**
  ```python
  with pytest.raises(ValueError, match="Invalid email"):
      service.validate(invalid_email)
  ```

- [ ] **Use fixtures for test data** instead of setup methods

- [ ] **Parametrize for multiple inputs**
  ```python
  @pytest.mark.parametrize("input,expected", [...])
  ```

### After Writing

- [ ] **Run the test** to verify it passes/fails as expected
- [ ] **Check coverage** for the new code
- [ ] **Add markers** if needed (slow, integration, etc.)
- [ ] **Document complex test logic** with comments

---

## Fixture Design Checklist

### Creating Fixtures

- [ ] **Determine scope** - function, class, module, session
  - Function: test-specific data
  - Class: shared within test class
  - Module: shared within file
  - Session: shared across all tests

- [ ] **Use yield for cleanup**
  ```python
  @pytest.fixture
  def db_connection():
      conn = create_connection()
      yield conn
      conn.close()
  ```

- [ ] **Consider factory pattern** for flexible test data
  ```python
  @pytest.fixture
  def user_factory():
      def _create(**kwargs):
          return User(**{**defaults, **kwargs})
      return _create
  ```

- [ ] **Use autouse sparingly** - only for truly global setup

- [ ] **Place in appropriate conftest.py**
  - `tests/conftest.py` - all tests
  - `tests/unit/conftest.py` - unit tests only

- [ ] **Document fixture purpose** with docstrings

### Fixture Dependencies

- [ ] **Check scope compatibility**
  - Session can use: session only
  - Module can use: session, module
  - Class can use: session, module, class
  - Function can use: all scopes

- [ ] **Avoid circular dependencies**

- [ ] **Keep dependency chain shallow** when possible

---

## Parametrization Checklist

### Basic Parametrization

- [ ] **Use meaningful IDs**
  ```python
  @pytest.mark.parametrize("email,valid", [
      pytest.param("user@example.com", True, id="valid_email"),
      pytest.param("invalid", False, id="missing_at_symbol"),
  ])
  ```

- [ ] **Cover edge cases**
  - Empty inputs
  - Boundary values
  - Invalid types
  - None values

- [ ] **Keep test data readable** - use variables for complex data
  ```python
  valid_user = {"name": "John", "email": "john@example.com"}
  invalid_user = {"name": "", "email": "invalid"}

  @pytest.mark.parametrize("user_data,expected", [
      (valid_user, True),
      (invalid_user, False),
  ])
  ```

### Fixture Parametrization

- [ ] **Parametrize fixtures** for multiple configurations
  ```python
  @pytest.fixture(params=["sqlite", "postgres"])
  def db(request):
      return create_db(request.param)
  ```

- [ ] **Use indirect parametrization** when needed
  ```python
  @pytest.mark.parametrize("db", ["sqlite"], indirect=True)
  ```

---

## Markers Checklist

### Using Markers

- [ ] **Register all custom markers** in configuration
  ```toml
  [tool.pytest.ini_options]
  markers = [
      "slow: marks tests as slow",
      "integration: integration tests",
      "e2e: end-to-end tests",
  ]
  ```

- [ ] **Enable strict markers** to catch typos
  ```toml
  addopts = ["--strict-markers"]
  ```

- [ ] **Apply markers consistently**
  ```python
  @pytest.mark.integration
  def test_database_connection():
      pass

  @pytest.mark.slow
  class TestHeavyComputations:
      pass
  ```

- [ ] **Use built-in markers appropriately**
  - `@pytest.mark.skip(reason="...")` - skip test
  - `@pytest.mark.skipif(condition, reason="...")` - conditional skip
  - `@pytest.mark.xfail(reason="...")` - expected failure
  - `@pytest.mark.parametrize(...)` - parametrization

### Filtering with Markers

- [ ] **Run specific markers**: `pytest -m slow`
- [ ] **Exclude markers**: `pytest -m "not slow"`
- [ ] **Combine markers**: `pytest -m "integration and not slow"`

---

## Mocking Checklist

### Setting Up Mocks

- [ ] **Install pytest-mock**: `pip install pytest-mock`

- [ ] **Mock at the right level**
  - Mock where imported, not where defined
  ```python
  # If service.py imports: from utils import send_email
  mocker.patch("service.send_email")  # Not "utils.send_email"
  ```

- [ ] **Set return values**
  ```python
  mock_api = mocker.patch("service.api_client")
  mock_api.get.return_value = {"status": "ok"}
  ```

- [ ] **Configure side effects** for exceptions or sequences
  ```python
  mock_api.side_effect = [ConnectionError, {"status": "ok"}]
  ```

### Verifying Mocks

- [ ] **Check call count**
  ```python
  assert mock_api.call_count == 2
  mock_api.assert_called_once()
  ```

- [ ] **Verify arguments**
  ```python
  mock_api.assert_called_with(expected_arg)
  mock_api.assert_called_once_with(arg1, arg2)
  ```

- [ ] **Reset mocks between tests** (usually automatic with function scope)

---

## Coverage Checklist

### Configuration

- [ ] **Configure coverage source**
  ```toml
  [tool.coverage.run]
  source = ["src"]
  branch = true
  omit = ["tests/*", "*/__init__.py"]
  ```

- [ ] **Set fail threshold**
  ```toml
  [tool.coverage.report]
  fail_under = 80
  ```

- [ ] **Exclude non-testable code**
  ```toml
  exclude_lines = [
      "pragma: no cover",
      "if TYPE_CHECKING:",
      "raise NotImplementedError",
  ]
  ```

### Running Coverage

- [ ] **Generate coverage report**
  ```bash
  pytest --cov=src --cov-report=html --cov-report=term-missing
  ```

- [ ] **Review uncovered lines** in HTML report

- [ ] **Add tests for critical uncovered paths**

- [ ] **Check branch coverage** for conditionals

---

## Parallel Execution Checklist

### Configuration

- [ ] **Install pytest-xdist**: `pip install pytest-xdist`

- [ ] **Ensure test isolation** - no shared state between tests

- [ ] **Use appropriate fixtures** - session scope for shared resources

- [ ] **Handle database isolation**
  - Separate databases per worker
  - Transaction rollback between tests

### Running Parallel

- [ ] **Use auto for CPU detection**: `pytest -n auto`

- [ ] **Choose distribution mode**
  - `--dist loadscope` - group by module/class
  - `--dist loadfile` - group by file
  - `--dist loadgroup` - group by marker

- [ ] **Combine with coverage**
  ```bash
  pytest -n auto --cov=src --cov-report=html
  ```

- [ ] **Monitor for flaky tests** - run multiple times

---

## Async Testing Checklist

### Configuration

- [ ] **Install pytest-asyncio**: `pip install pytest-asyncio`

- [ ] **Configure asyncio mode**
  ```toml
  [tool.pytest.ini_options]
  asyncio_mode = "auto"  # or "strict"
  ```

### Writing Async Tests

- [ ] **Use async test functions**
  ```python
  @pytest.mark.asyncio
  async def test_async_function():
      result = await async_operation()
      assert result is not None
  ```

- [ ] **Create async fixtures**
  ```python
  @pytest.fixture
  async def async_client():
      client = await AsyncClient.connect()
      yield client
      await client.close()
  ```

- [ ] **Handle timeouts** for async operations
  ```python
  @pytest.mark.timeout(5)
  @pytest.mark.asyncio
  async def test_with_timeout():
      await potentially_slow_operation()
  ```

---

## Debugging Tests Checklist

### Command-Line Options

- [ ] **Stop on first failure**: `pytest -x`
- [ ] **Run last failed**: `pytest --lf`
- [ ] **Run failed first**: `pytest --ff`
- [ ] **Verbose output**: `pytest -v` or `pytest -vv`
- [ ] **Show print statements**: `pytest -s`
- [ ] **Show slowest tests**: `pytest --durations=10`

### Using Debugger

- [ ] **Drop to PDB on failure**: `pytest --pdb`
- [ ] **Break at start**: `pytest --trace`
- [ ] **Set breakpoints in code**
  ```python
  def test_something():
      breakpoint()  # or import pdb; pdb.set_trace()
      result = function_to_debug()
  ```

- [ ] **Use enhanced debuggers** (pdbpp, ipdb)
  ```bash
  pip install pdbpp
  pytest --pdb  # Now uses pdbpp automatically
  ```

### VS Code Integration

- [ ] **Configure Python extension** for pytest
- [ ] **Use Test Explorer** for visual test management
- [ ] **Set breakpoints** and use Debug Test option
- [ ] **Configure launch.json** for custom debug settings

---

## CI/CD Checklist

### GitHub Actions

- [ ] **Create workflow file** `.github/workflows/tests.yml`

- [ ] **Run tests with coverage**
  ```yaml
  - name: Run tests
    run: pytest --cov=src --cov-report=xml
  ```

- [ ] **Upload coverage to service** (Codecov, Coveralls)

- [ ] **Cache dependencies** for faster runs

- [ ] **Run parallel tests** in CI
  ```yaml
  - name: Run tests
    run: pytest -n auto
  ```

### Quality Gates

- [ ] **Enforce coverage threshold**
  ```bash
  pytest --cov=src --cov-fail-under=80
  ```

- [ ] **Run specific marker groups**
  ```bash
  pytest -m "not slow"  # Fast CI
  pytest -m "slow"      # Nightly
  ```

- [ ] **Generate test reports** (JUnit XML for CI tools)
  ```bash
  pytest --junitxml=report.xml
  ```

---

## Pre-Commit Checklist

Before committing test changes:

- [ ] All tests pass locally
- [ ] Coverage meets threshold
- [ ] No flaky tests introduced
- [ ] Markers registered
- [ ] Fixtures documented
- [ ] Test names are descriptive
- [ ] AAA pattern followed
- [ ] Mocks verified correctly
- [ ] CI configuration updated if needed

---

*Use these checklists as guides. Adapt to your project's specific needs.*
