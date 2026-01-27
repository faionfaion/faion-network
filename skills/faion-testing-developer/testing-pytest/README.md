# pytest Testing Framework

## Overview

pytest is Python's most popular testing framework, offering powerful fixtures, parametrization, and an extensive plugin ecosystem. As of 2025-2026, pytest 8.x brings improved assertion diffs, better async support, and enhanced type annotations.

## Key Features (pytest 8.x+)

| Feature | Description |
|---------|-------------|
| **Fixtures** | Dependency injection for test setup/teardown |
| **Parametrization** | Run same test with multiple inputs |
| **Markers** | Tag and filter tests |
| **Plugins** | 1000+ plugins on PyPI |
| **Parallel Execution** | pytest-xdist for multi-CPU testing |
| **Coverage** | pytest-cov for code coverage reporting |
| **Async Support** | pytest-asyncio for async/await testing |

## pytest 8.x New Features

### pytest 8.0.0+

- Dropped Python 3.7 support (EOL)
- Improved assertion diffs with syntax highlighting
- Better colored diffs in verbose mode (`-vv`)
- Enhanced set assertion rewrites (`!=`, `<=`, `>=`, `<`, `>`)
- Traceback output for XFAIL results with `-rx`

### pytest 8.3.x+

- `--xfail-tb` flag for XFAIL traceback control
- Marker keyword arguments filtering (`-m "device(serial='123')"`)
- Improved test selection by marker values

### pytest 8.4.x+

- Dropped Python 3.8 support (EOL 2024-10-07)
- Async tests now fail (instead of warn+skip) without proper plugin
- Tests returning non-None values now fail
- Test functions with `yield` cause explicit errors
- Native TOML configuration in pyproject.toml (`[tool.pytest]`)
- Enhanced typing documentation

## Installation

```bash
# Core pytest
pip install pytest

# Common plugins
pip install pytest-cov pytest-mock pytest-asyncio pytest-xdist

# Development setup
pip install pytest pytest-cov pytest-mock pytest-asyncio pytest-xdist pytest-timeout pytest-randomly
```

## Plugin Ecosystem (2025)

### Essential Plugins

| Plugin | Downloads/30d | Purpose |
|--------|---------------|---------|
| pytest-cov | 87M+ | Code coverage reporting |
| pytest-xdist | 50M+ | Parallel/distributed testing |
| pytest-mock | 40M+ | Thin-wrapper around unittest.mock |
| pytest-asyncio | 30M+ | Async/await support |
| pytest-timeout | 20M+ | Test timeouts |
| pytest-randomly | 15M+ | Randomize test order |

### Specialized Plugins

| Plugin | Purpose |
|--------|---------|
| pytest-django | Django integration |
| pytest-flask | Flask integration |
| pytest-httpx | HTTPX async client mocking |
| pytest-bdd | Behavior-driven development |
| pytest-benchmark | Performance benchmarking |
| pytest-sugar | Better progress display |
| pytest-instafail | Show failures immediately |
| pytest-rerunfailures | Retry flaky tests |

## Core Concepts

### Test Discovery

pytest automatically discovers tests following these conventions:

```
tests/                      # Test directory (configurable)
├── conftest.py             # Shared fixtures
├── test_users.py           # Test module (test_*.py)
│   ├── TestUserService     # Test class (Test*)
│   │   ├── test_create     # Test function (test_*)
│   │   └── test_delete
│   └── test_validate_email # Standalone test function
└── test_orders.py
```

### Fixture Scopes

| Scope | Lifecycle | Use Case |
|-------|-----------|----------|
| `function` | Each test (default) | Isolated test data |
| `class` | Each test class | Shared class state |
| `module` | Each test file | Expensive module setup |
| `package` | Each package | Package-level resources |
| `session` | Entire test run | Database connections, servers |

### Fixture Flow

```
Session fixtures (once)
    └── Package fixtures (per package)
        └── Module fixtures (per file)
            └── Class fixtures (per class)
                └── Function fixtures (per test)
                    └── TEST RUNS
                └── Function teardown
            └── Class teardown
        └── Module teardown
    └── Package teardown
└── Session teardown
```

## Configuration Priority

pytest uses the first configuration file found:

1. `pytest.ini` / `.pytest.ini`
2. `pyproject.toml` (`[tool.pytest.ini_options]` or `[tool.pytest]`)
3. `tox.ini`
4. `setup.cfg` (not recommended)

**Important:** Options from multiple config files are never merged.

## Best Practices

### Project Structure

Use the src layout for cleaner imports:

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── services.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── .coveragerc (optional)
```

### Configuration Best Practices

1. **Use `pyproject.toml`** - Modern standard, single config file
2. **Enable strict mode** - Catch typos and misconfigurations
3. **Set `testpaths`** - Explicit test directories
4. **Use `importlib` mode** - Better import handling
5. **Register markers** - Document custom markers

### Testing Best Practices

1. **Follow AAA pattern** - Arrange, Act, Assert
2. **One assertion focus** - Test one behavior per test
3. **Use descriptive names** - `test_create_user_with_invalid_email_raises_error`
4. **Isolate tests** - No test dependencies
5. **Mock external services** - Use pytest-mock for dependencies
6. **Use factories** - Factory fixtures for test data
7. **Parametrize** - Reduce code duplication

### Performance Best Practices

1. **Parallel execution** - `pytest -n auto` for multi-core
2. **Scope fixtures appropriately** - Session scope for expensive setup
3. **Use `loadscope` distribution** - Group related tests
4. **Minimize plugin overhead** - Only essential plugins
5. **Profile slow tests** - `pytest --durations=10`

## LLM Usage Tips

When using LLMs (Claude, GPT, etc.) for pytest work:

### Effective Context

1. **Include configuration** - Share `pyproject.toml` pytest section
2. **Show existing patterns** - Provide sample test from your codebase
3. **Specify pytest version** - pytest 8.x has different features
4. **List installed plugins** - `pip list | grep pytest`

### What LLMs Do Well

- Generate test cases from function signatures
- Create parametrized test variations
- Write fixture implementations
- Convert unittest to pytest
- Suggest edge cases and boundary tests
- Generate mock setups

### What LLMs Need Help With

- Complex fixture dependency chains
- Project-specific testing patterns
- Integration with custom plugins
- Performance optimization
- Flaky test diagnosis

### Prompt Tips

```
"Using pytest 8.x with pytest-asyncio, write tests for this async function.
Use fixtures from conftest.py and parametrize for edge cases."
```

```
"Generate a factory fixture for User model following our existing pattern:
[paste existing factory example]"
```

## External Resources

### Official Documentation

- [pytest Documentation](https://docs.pytest.org/) - Official docs
- [pytest Fixtures Guide](https://docs.pytest.org/en/stable/how-to/fixtures.html) - Fixtures deep dive
- [pytest Markers Guide](https://docs.pytest.org/en/stable/example/markers.html) - Custom markers
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/) - Coverage reporting
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/) - Parallel execution
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/) - Async testing

### Tutorials and Guides

- [Real Python pytest Guide](https://realpython.com/pytest-python-testing/) - Comprehensive tutorial
- [pytest-with-eric.com](https://pytest-with-eric.com/) - Advanced pytest patterns
- [PythonTest.com](https://pythontest.com/) - Testing best practices
- [Testing Python Blog](https://testingpython.com/) - Testing strategies

### Release Notes

- [pytest 8.0.0 Release](https://docs.pytest.org/en/stable/announce/release-8.0.0.html)
- [pytest 8.4.0 Release](https://docs.pytest.org/en/stable/announce/release-8.4.0.html)
- [pytest Changelog](https://docs.pytest.org/en/stable/changelog.html)

## Related Methodologies

| Methodology | Path |
|-------------|------|
| Testing Patterns | [../testing-patterns/](../testing-patterns/) |
| Unit Testing | [../unit-testing/](../unit-testing/) |
| Integration Testing | [../integration-testing/](../integration-testing/) |
| Mocking Strategies | [../mocking-strategies/](../mocking-strategies/) |
| Test Fixtures | [../test-fixtures/](../test-fixtures/) |

---

*Last updated: 2026-01-25*
*pytest version: 8.4.x*
