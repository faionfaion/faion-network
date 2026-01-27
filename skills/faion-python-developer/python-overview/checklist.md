# Python Development Checklist

Step-by-step checklist for Python project setup, development, and deployment.

---

## Project Initialization

### Environment Setup

- [ ] Install Python 3.12+ (or 3.13+ for free-threading)
- [ ] Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Create project: `uv init project-name`
- [ ] Navigate to project: `cd project-name`
- [ ] Verify virtualenv created: `ls .venv`

### Project Structure

- [ ] Create source directory: `mkdir -p src/package_name`
- [ ] Create tests directory: `mkdir tests`
- [ ] Create `src/package_name/__init__.py`
- [ ] Create `src/package_name/py.typed` (for type hints)
- [ ] Verify structure:
  ```
  project-name/
  ├── pyproject.toml
  ├── README.md
  ├── src/
  │   └── package_name/
  │       ├── __init__.py
  │       └── py.typed
  └── tests/
      └── __init__.py
  ```

### pyproject.toml Configuration

- [ ] Set project metadata (name, version, description)
- [ ] Set Python version requirement: `requires-python = ">=3.12"`
- [ ] Configure ruff linting rules
- [ ] Configure ruff formatting
- [ ] Configure pytest settings
- [ ] Configure mypy/pyright settings
- [ ] Add project dependencies
- [ ] Add development dependencies

---

## Development Workflow

### Adding Dependencies

- [ ] Add runtime dependency: `uv add package-name`
- [ ] Add dev dependency: `uv add --dev package-name`
- [ ] Verify `uv.lock` updated
- [ ] Commit `pyproject.toml` and `uv.lock`

### Code Quality Setup

- [ ] Install dev tools: `uv add --dev ruff pytest pytest-cov mypy`
- [ ] Create `ruff.toml` or configure in `pyproject.toml`
- [ ] Run formatter: `uv run ruff format .`
- [ ] Run linter: `uv run ruff check . --fix`
- [ ] Run type checker: `uv run mypy src/`

### Pre-commit Hooks

- [ ] Install pre-commit: `uv add --dev pre-commit`
- [ ] Create `.pre-commit-config.yaml`:
  ```yaml
  repos:
    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.8.0
      hooks:
        - id: ruff
          args: [--fix]
        - id: ruff-format
    - repo: https://github.com/astral-sh/uv-pre-commit
      rev: 0.5.0
      hooks:
        - id: uv-lock
  ```
- [ ] Install hooks: `uv run pre-commit install`
- [ ] Test hooks: `uv run pre-commit run --all-files`

---

## Code Standards

### Type Hints

- [ ] Add type hints to all function signatures
- [ ] Use `TypedDict` for structured dictionaries
- [ ] Use `Protocol` for structural typing
- [ ] Import from `collections.abc` not `typing` (Python 3.9+)
- [ ] Use `X | None` instead of `Optional[X]` (Python 3.10+)
- [ ] Use `list[T]` instead of `List[T]` (Python 3.9+)
- [ ] Create `py.typed` marker file

### Docstrings

- [ ] Add module-level docstrings
- [ ] Add class docstrings
- [ ] Add function docstrings (Google style recommended)
- [ ] Document parameters, returns, raises
- [ ] Include usage examples for public API

### Error Handling

- [ ] Use specific exception types
- [ ] Create custom exceptions when needed
- [ ] Log exceptions with context
- [ ] Never catch bare `Exception` without re-raising
- [ ] Use `raise ... from e` for exception chaining

### Async Code

- [ ] Use `async/await` for I/O-bound operations
- [ ] Use `asyncio.gather()` for concurrent tasks
- [ ] Use `asyncio.Semaphore` for rate limiting
- [ ] Use `httpx` or `aiohttp` for async HTTP
- [ ] Avoid mixing sync and async code

---

## Testing

### Test Setup

- [ ] Create `tests/__init__.py`
- [ ] Create `tests/conftest.py` for fixtures
- [ ] Configure pytest in `pyproject.toml`:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  asyncio_mode = "auto"
  ```

### Test Coverage

- [ ] Write unit tests for all public functions
- [ ] Write integration tests for API endpoints
- [ ] Test edge cases and error conditions
- [ ] Test async functions with `pytest-asyncio`
- [ ] Run tests: `uv run pytest`
- [ ] Check coverage: `uv run pytest --cov=src --cov-report=term-missing`
- [ ] Aim for 80%+ coverage

### Test Organization

- [ ] Mirror source structure in tests
- [ ] Use descriptive test names: `test_function_does_x_when_y`
- [ ] Group related tests in classes
- [ ] Use fixtures for common setup
- [ ] Use parametrize for multiple test cases

---

## Web Framework Specific

### FastAPI

- [ ] Create Pydantic models for request/response
- [ ] Use dependency injection for services
- [ ] Add proper error handling with HTTPException
- [ ] Configure CORS if needed
- [ ] Add OpenAPI metadata
- [ ] Create health check endpoint
- [ ] Configure logging

### Django

- [ ] Create apps for logical separation
- [ ] Use Django REST Framework for APIs
- [ ] Configure database settings
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Configure static files
- [ ] Set up admin interface

---

## Documentation

### Project Documentation

- [ ] Write comprehensive README.md
- [ ] Include installation instructions
- [ ] Include usage examples
- [ ] Document environment variables
- [ ] Add contributing guidelines
- [ ] Add changelog (CHANGELOG.md)

### API Documentation

- [ ] FastAPI: Auto-generated at `/docs`
- [ ] Django REST: Use drf-spectacular
- [ ] Document authentication requirements
- [ ] Provide example requests/responses

---

## Performance

### Profiling

- [ ] Profile with cProfile: `python -m cProfile -s cumulative script.py`
- [ ] Identify bottlenecks
- [ ] Optimize algorithms first
- [ ] Use NumPy for numeric operations
- [ ] Consider Rust/PyO3 for critical paths

### Memory

- [ ] Use generators for large datasets
- [ ] Use `__slots__` for memory-heavy classes
- [ ] Profile memory with `memory_profiler`
- [ ] Clear large objects when done

---

## Security

### Dependencies

- [ ] Run security audit: `uv run pip-audit`
- [ ] Keep dependencies updated
- [ ] Pin dependency versions in production
- [ ] Review dependency licenses

### Code Security

- [ ] Never hardcode secrets
- [ ] Use environment variables for config
- [ ] Validate all user input
- [ ] Use parameterized queries
- [ ] Escape output in templates
- [ ] Use HTTPS in production

---

## CI/CD

### GitHub Actions

- [ ] Create `.github/workflows/ci.yml`
- [ ] Run tests on push/PR
- [ ] Run linting and type checking
- [ ] Check code formatting
- [ ] Upload coverage reports
- [ ] Cache dependencies

### Deployment

- [ ] Create Dockerfile
- [ ] Use multi-stage builds
- [ ] Set non-root user
- [ ] Configure health checks
- [ ] Set up environment variables
- [ ] Configure logging

---

## Pre-Release Checklist

### Final Checks

- [ ] All tests passing
- [ ] Coverage meets threshold
- [ ] No linting errors
- [ ] No type errors
- [ ] Documentation up to date
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Dependencies audited

### Release

- [ ] Tag release: `git tag v1.0.0`
- [ ] Push tag: `git push --tags`
- [ ] Publish to PyPI (if library): `uv publish`
- [ ] Deploy to production
- [ ] Verify deployment
- [ ] Monitor for errors

---

*Python Development Checklist v1.0*
