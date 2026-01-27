# Modern Python Adoption Checklist

Step-by-step checklist for adopting modern Python (3.12-3.14) practices.

---

## 1. Project Setup

### Environment

- [ ] Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Install Python 3.13+: `uv python install 3.13 3.14`
- [ ] Initialize project: `uv init my_project --python 3.13`
- [ ] Pin Python version: `uv python pin 3.13`

### Configuration Files

- [ ] Create `pyproject.toml` with modern structure
- [ ] Add `[project]` table (not `[tool.poetry]`)
- [ ] Configure dependencies and optional-dependencies
- [ ] Set `requires-python = ">=3.12"`

### Development Dependencies

- [ ] Add Ruff: `uv add --dev ruff`
- [ ] Add type checker: `uv add --dev mypy` or `pyright`
- [ ] Add pytest: `uv add --dev pytest pytest-asyncio pytest-cov`
- [ ] Configure pre-commit hooks (optional)

---

## 2. Ruff Configuration

### Basic Setup

- [ ] Set target version: `target-version = "py313"`
- [ ] Configure line length (88 recommended)
- [ ] Enable rule categories:
  - [ ] `E` - pycodestyle errors
  - [ ] `F` - pyflakes
  - [ ] `I` - isort (import sorting)
  - [ ] `B` - flake8-bugbear
  - [ ] `UP` - pyupgrade

### Extended Rules (Recommended)

- [ ] `N` - pep8-naming
- [ ] `S` - flake8-bandit (security)
- [ ] `C4` - flake8-comprehensions
- [ ] `PT` - flake8-pytest-style
- [ ] `RUF` - Ruff-specific rules

### Format Configuration

- [ ] Configure quote style: `quote-style = "double"`
- [ ] Configure docstring format: `docstring-code-format = true`

### IDE Integration

- [ ] Install Ruff VS Code extension
- [ ] Configure format on save
- [ ] Configure fix on save

---

## 3. Type Hints Modernization

### Basic Updates

- [ ] Replace `List[T]` with `list[T]`
- [ ] Replace `Dict[K, V]` with `dict[K, V]`
- [ ] Replace `Set[T]` with `set[T]`
- [ ] Replace `Tuple[T, ...]` with `tuple[T, ...]`
- [ ] Replace `Optional[T]` with `T | None`
- [ ] Replace `Union[A, B]` with `A | B`

### PEP 695 Generics (Python 3.12+)

- [ ] Convert `TypeVar` declarations to inline syntax
- [ ] Update generic classes to use `class Name[T]:`
- [ ] Update generic functions to use `def func[T](...):`
- [ ] Use `type` statement for type aliases

### Advanced Typing (Python 3.13+)

- [ ] Use `TypeIs` for type narrowing
- [ ] Use `ReadOnly` for immutable TypedDict fields
- [ ] Implement `Protocol` for structural typing
- [ ] Use `ParamSpec` for decorator typing

### Type Checker Setup

- [ ] Enable strict mode in mypy/pyright
- [ ] Configure per-module overrides if needed
- [ ] Add type stubs for untyped libraries

---

## 4. Async Patterns

### TaskGroup (Python 3.11+)

- [ ] Replace `asyncio.gather()` with `asyncio.TaskGroup()`
- [ ] Handle `ExceptionGroup` with `except*` syntax
- [ ] Implement proper cleanup with `try...finally`

### Timeouts

- [ ] Use `asyncio.timeout()` context manager
- [ ] Set appropriate timeout values
- [ ] Handle `asyncio.TimeoutError`

### Rate Limiting

- [ ] Implement `asyncio.Semaphore` for concurrency limits
- [ ] Use `asyncio.Queue` for producer-consumer patterns
- [ ] Consider `aiolimiter` for rate limiting

### Testing Async Code

- [ ] Install pytest-asyncio
- [ ] Configure `asyncio_mode = "auto"` in pyproject.toml
- [ ] Use `@pytest.mark.asyncio` decorator
- [ ] Create async fixtures with `@pytest_asyncio.fixture`

---

## 5. F-String Improvements (Python 3.12+)

### New Capabilities

- [ ] Use same quotes inside expressions: `f"Hello {data['name']}"`
- [ ] Use backslashes in expressions: `f"Path: {p.replace('\\', '/')}"`
- [ ] Use multiline expressions in f-strings
- [ ] Use nested f-strings where appropriate

### Debug Format

- [ ] Use `=` for debug output: `f"{variable=}"`
- [ ] Combine with formatting: `f"{value=:.2f}"`

---

## 6. Free-Threading (Python 3.13+)

### Prerequisites

- [ ] Install free-threaded Python build (python3.13t)
- [ ] Verify with: `python -VV` (shows "free-threading build")
- [ ] Check GIL status: `sys._is_gil_enabled()`

### Code Audit

- [ ] Identify shared mutable state
- [ ] Review global variables for thread safety
- [ ] Check third-party libraries for free-threading support
- [ ] Test C extensions compatibility

### Thread Safety

- [ ] Use `threading.Lock` for critical sections
- [ ] Consider `queue.Queue` for thread-safe data passing
- [ ] Use `threading.local()` for thread-local storage
- [ ] Avoid mutable default arguments

### Testing

- [ ] Run tests with `PYTHON_GIL=0`
- [ ] Test under high concurrency
- [ ] Profile for race conditions

---

## 7. Python 3.14 Features

### Template Strings (t-strings)

- [ ] Identify string formatting that needs sanitization
- [ ] Replace f-strings with t-strings for user input
- [ ] Implement template processors for SQL, HTML

### Deferred Annotations

- [ ] Remove `from __future__ import annotations`
- [ ] Simplify forward references
- [ ] Update code using `typing.get_type_hints()`

### New Standard Library

- [ ] Use `compression.zstd` for Zstandard
- [ ] Use `uuid.uuid7()` for time-ordered UUIDs
- [ ] Use simplified `except` syntax without parentheses

---

## 8. Testing Setup

### pytest Configuration

- [ ] Configure in pyproject.toml `[tool.pytest.ini_options]`
- [ ] Set `testpaths = ["tests"]`
- [ ] Enable `asyncio_mode = "auto"`
- [ ] Configure coverage reporting

### Test Structure

- [ ] Create `tests/` directory
- [ ] Add `conftest.py` with shared fixtures
- [ ] Organize by module/feature
- [ ] Follow naming convention: `test_*.py`

### Fixtures

- [ ] Use `@pytest.fixture` for test data
- [ ] Use `@pytest_asyncio.fixture` for async fixtures
- [ ] Implement proper scope (function, class, module, session)
- [ ] Use `yield` for cleanup

### Coverage

- [ ] Configure pytest-cov
- [ ] Set minimum coverage threshold
- [ ] Exclude non-testable code

---

## 9. CI/CD Pipeline

### GitHub Actions

- [ ] Create `.github/workflows/ci.yml`
- [ ] Test on multiple Python versions (3.12, 3.13, 3.14)
- [ ] Run linting with Ruff
- [ ] Run type checking
- [ ] Run tests with coverage

### Pre-commit

- [ ] Create `.pre-commit-config.yaml`
- [ ] Add Ruff hooks (lint + format)
- [ ] Add mypy hook (optional)
- [ ] Install: `pre-commit install`

---

## 10. Documentation

### Code Documentation

- [ ] Add docstrings to public functions/classes
- [ ] Use Google or NumPy docstring style
- [ ] Document type parameters
- [ ] Include usage examples

### Project Documentation

- [ ] Create comprehensive README.md
- [ ] Document installation steps
- [ ] Include development setup
- [ ] Add API documentation (if library)

---

## Quick Validation Commands

```bash
# Format and lint
uv run ruff format .
uv run ruff check . --fix

# Type check
uv run mypy src/

# Run tests
uv run pytest -v --cov=src --cov-report=term-missing

# Check Python version
python -VV

# Check if free-threading is enabled
python -c "import sys; print(sys._is_gil_enabled())"
```

---

## Migration Priorities

### High Priority

1. Switch to pyproject.toml
2. Use uv for package management
3. Adopt Ruff for linting/formatting
4. Enable strict type checking

### Medium Priority

1. Modernize type hints syntax
2. Update to TaskGroup for async
3. Use PEP 695 generics

### Lower Priority (Wait for Ecosystem)

1. Free-threading adoption
2. Template strings
3. Multiple interpreters

---

*Checklist v2.0 - Modern Python 2026*
