# Python Testing with pytest

**Comprehensive pytest patterns for testing Python applications.**

---

## Overview

pytest is the de facto standard testing framework for Python, offering powerful features like fixtures, parametrization, and a rich plugin ecosystem. This methodology covers modern pytest patterns for 2025-2026, including async testing, parallel execution, coverage analysis, and integration with Django.

---

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| New Python project | Always use pytest over unittest |
| Django/FastAPI projects | pytest with pytest-django/pytest-asyncio |
| Large test suites | pytest-xdist for parallel execution |
| CI/CD pipelines | pytest-cov for coverage reporting |
| Async applications | pytest-asyncio for coroutine testing |
| Complex test data | Factory fixtures with pytest-factoryboy |

---

## Why pytest Over unittest

| Feature | pytest | unittest |
|---------|--------|----------|
| Assertions | Simple `assert` | `self.assertEqual()` methods |
| Fixtures | Dependency injection | setUp/tearDown methods |
| Parametrization | Built-in `@pytest.mark.parametrize` | Manual loops |
| Plugins | 1000+ plugins available | Limited ecosystem |
| Output | Rich, colorful reports | Basic output |
| Discovery | Automatic | Requires test loader |

---

## Core Concepts

### 1. Fixtures

Fixtures provide reusable setup/teardown logic with dependency injection:

```python
@pytest.fixture
def database():
    conn = create_connection()
    yield conn  # Teardown after yield
    conn.close()

def test_query(database):  # Automatic injection
    result = database.execute("SELECT 1")
    assert result == 1
```

**Fixture Scopes:**
- `function` (default): New instance per test
- `class`: Shared within test class
- `module`: Shared within test file
- `package`: Shared within package
- `session`: Single instance for entire test run

### 2. Parametrization

Run the same test with different inputs:

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("world", 5),
    ("", 0),
])
def test_length(input, expected):
    assert len(input) == expected
```

### 3. Markers

Categorize and control test execution:

```python
@pytest.mark.slow
@pytest.mark.integration
def test_external_api():
    ...

# Run only fast tests
# pytest -m "not slow"
```

---

## Essential Plugins (2025)

| Plugin | Purpose | Monthly Downloads |
|--------|---------|-------------------|
| pytest-cov | Coverage reporting | 87M+ |
| pytest-xdist | Parallel execution | 60M+ |
| pytest-asyncio | Async test support | 58M+ |
| pytest-mock | Mocking utilities | 50M+ |
| pytest-django | Django integration | 20M+ |
| pytest-timeout | Prevent hanging tests | 19M+ |
| pytest-randomly | Randomize test order | 10M+ |
| pytest-sugar | Beautiful output | 8M+ |
| pytest-factoryboy | Factory fixtures | 5M+ |

---

## Project Structure

```
project/
|-- src/
|   |-- myapp/
|       |-- __init__.py
|       |-- models.py
|       |-- services.py
|-- tests/
|   |-- __init__.py
|   |-- conftest.py           # Shared fixtures
|   |-- unit/
|   |   |-- __init__.py
|   |   |-- test_models.py
|   |   |-- test_services.py
|   |-- integration/
|   |   |-- __init__.py
|   |   |-- test_api.py
|   |-- fixtures/
|       |-- factories.py      # Factory Boy factories
|       |-- data.py           # Test data
|-- pyproject.toml            # pytest configuration
```

---

## LLM Usage Tips

### Effective Prompting Patterns

When asking an LLM to write tests:

1. **Provide context about the function:**
   ```
   Write pytest tests for this function that validates email addresses.
   Include edge cases for empty strings, missing @ symbol, and valid emails.
   ```

2. **Specify the testing style:**
   ```
   Use pytest parametrization for the validation tests.
   Follow the AAA pattern (Arrange, Act, Assert).
   ```

3. **Request specific fixtures:**
   ```
   Create a factory fixture for User model that allows customizing email and name.
   Use pytest-factoryboy patterns.
   ```

### Common LLM Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Using unittest syntax | Request pytest assertions |
| Forgetting async markers | Specify pytest-asyncio usage |
| Mock at wrong level | Specify "mock where used, not where defined" |
| Missing cleanup | Request yield fixtures with teardown |
| Hardcoded paths | Request tmp_path fixture usage |

### Prompt Templates

See [llm-prompts.md](llm-prompts.md) for ready-to-use prompts.

---

## Key Patterns

### AAA Pattern (Arrange-Act-Assert)

```python
def test_user_creation():
    # Arrange
    user_data = {"email": "test@example.com", "name": "Test"}

    # Act
    user = create_user(**user_data)

    # Assert
    assert user.email == "test@example.com"
    assert user.is_active is True
```

### Factory Fixture Pattern

```python
@pytest.fixture
def user_factory(db):
    def create(email="test@example.com", **kwargs):
        return User.objects.create(email=email, **kwargs)
    return create

def test_multiple_users(user_factory):
    user1 = user_factory(email="user1@example.com")
    user2 = user_factory(email="user2@example.com")
    assert User.objects.count() == 2
```

### Async Testing Pattern

```python
import pytest

@pytest.mark.asyncio
async def test_async_operation():
    result = await fetch_data()
    assert result["status"] == "ok"
```

---

## Configuration

### pyproject.toml (Recommended)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/migrations/*", "*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
fail_under = 80
```

---

## Quick Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run in parallel
pytest -n auto

# Run specific markers
pytest -m "not slow"

# Run failed tests first
pytest --lf

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l
```

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step testing checklist |
| [examples.md](examples.md) | Real-world code examples |
| [templates.md](templates.md) | Copy-paste configurations |
| [llm-prompts.md](llm-prompts.md) | Effective LLM prompts |

---

## External Resources

### Official Documentation
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

### Best Practices Guides
- [Python Testing Best Practices 2025](https://danielsarney.com/blog/python-testing-best-practices-2025-building-reliable-applications/)
- [pytest Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [Advanced pytest Patterns](https://www.fiddler.ai/blog/advanced-pytest-patterns-harnessing-the-power-of-parametrization-and-factory-methods)
- [Five Advanced pytest Fixture Patterns](https://www.inspiredpython.com/article/five-advanced-pytest-fixture-patterns)

### Tutorials
- [Pytest with Eric](https://pytest-with-eric.com/)
- [Real Python Django pytest Fixtures](https://realpython.com/django-pytest-fixtures/)
- [A Practical Guide to pytest-asyncio](https://pytest-with-eric.com/pytest-advanced/pytest-asyncio/)

---

## Agent Integration

**Executed by:** faion-test-agent, faion-code-agent, faion-python-developer

**Related Skills:**
- [faion-testing-developer](../../faion-testing-developer/SKILL.md) - Testing strategies
- [faion-python-developer](../SKILL.md) - Python development

---

*Python Testing with pytest v2.0*
*Layer 3 Technical Skill*
*pytest | Fixtures | Mocking | Async | Django | Coverage*
