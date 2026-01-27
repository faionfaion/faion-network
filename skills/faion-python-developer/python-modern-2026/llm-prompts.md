# LLM Prompts for Modern Python Development

Effective prompts for LLM-assisted Python 3.12-3.14 development.

---

## 1. Project Setup Prompts

### Initialize Modern Python Project

```
Create a new Python 3.13 project with:
- pyproject.toml with hatchling build system
- uv as package manager
- Ruff for linting/formatting (rules: E, F, I, B, UP, N, S, C4, PT)
- mypy in strict mode
- pytest with pytest-asyncio (auto mode)
- src/ layout with my_project/ package
- tests/ directory with conftest.py
- .pre-commit-config.yaml with ruff hooks
- .github/workflows/ci.yml testing Python 3.12-3.14

Project name: [PROJECT_NAME]
Description: [DESCRIPTION]
```

### Add Dependencies

```
Add the following to my Python project's pyproject.toml:

Production dependencies:
- [LIST DEPENDENCIES]

Development dependencies:
- pytest, pytest-asyncio, pytest-cov
- ruff, mypy

Use modern pyproject.toml format with [project.optional-dependencies].
```

---

## 2. Type Hints Prompts

### Modernize Type Hints

```
Modernize the following Python code to use Python 3.12+ type hints:
- Replace typing.List/Dict/Set with builtin generics
- Replace Optional[X] with X | None
- Replace Union[A, B] with A | B
- Convert TypeVar to PEP 695 syntax where applicable
- Use type aliases with the 'type' statement

Code:
```python
[PASTE CODE]
```
```

### Add Type Hints

```
Add comprehensive type hints to this Python code:
- Use Python 3.13 syntax (X | None, built-in generics)
- Include return types for all functions
- Use TypedDict for dictionary structures
- Use Protocol for duck typing
- Add docstrings with type information

Code:
```python
[PASTE CODE]
```
```

### Create Protocol

```
Create a Python Protocol for the following interface:
- Name: [PROTOCOL_NAME]
- Methods:
  - [METHOD_NAME]([PARAMS]) -> [RETURN_TYPE]
  - ...
- Make it @runtime_checkable
- Use Python 3.12+ syntax
- Include docstrings
```

### Generic Class

```
Create a generic class in Python 3.12+ with:
- Name: [CLASS_NAME]
- Type parameters: [T, K, V, etc.]
- Type bounds/constraints: [BOUNDS]
- Methods: [LIST METHODS]

Use PEP 695 syntax (class Name[T]:) not TypeVar.
Include type hints for all methods and attributes.
```

---

## 3. Async Patterns Prompts

### Convert to Async

```
Convert this synchronous Python code to async:
- Use asyncio.TaskGroup for concurrent operations
- Use asyncio.timeout() for timeouts
- Use asyncio.Semaphore for rate limiting (max [N] concurrent)
- Handle exceptions with except* for ExceptionGroups
- Add proper cleanup with try/finally

Code:
```python
[PASTE CODE]
```
```

### Create Async Service

```
Create an async Python service class:
- Name: [SERVICE_NAME]
- Dependencies: [LIST DEPENDENCIES]
- Methods:
  - [METHOD_NAME]: [DESCRIPTION]
  - ...

Requirements:
- Use asyncio.TaskGroup for concurrent operations
- Implement retry logic with exponential backoff
- Add proper timeout handling
- Include type hints (Python 3.13+)
- Add logging
```

### Async Context Manager

```
Create an async context manager for [RESOURCE_TYPE]:
- Setup: [SETUP_LOGIC]
- Cleanup: [CLEANUP_LOGIC]
- Use @asynccontextmanager decorator
- Handle exceptions properly
- Include type hints with AsyncIterator
```

### TaskGroup Pattern

```
Refactor this code to use asyncio.TaskGroup:
- Replace asyncio.gather() with TaskGroup
- Handle exceptions with except* syntax
- Ensure all tasks are cancelled on failure
- Add proper result collection

Code:
```python
[PASTE CODE]
```
```

---

## 4. Testing Prompts

### Generate pytest Tests

```
Generate pytest tests for this Python code:
- Include happy path and edge cases
- Use @pytest.mark.asyncio for async functions
- Use @pytest.mark.parametrize for multiple inputs
- Mock external dependencies with AsyncMock
- Use fixtures for test data
- Target 90%+ coverage

Code:
```python
[PASTE CODE]
```
```

### Create Test Fixtures

```
Create pytest fixtures for testing:
- [FIXTURE_NAME]: [DESCRIPTION]
- ...

Requirements:
- Use @pytest_asyncio.fixture for async fixtures
- Implement proper cleanup with yield
- Use appropriate scope (function/class/module/session)
- Include type hints
```

### Integration Tests

```
Create integration tests for this API endpoint:
- Endpoint: [METHOD] [PATH]
- Request body: [SCHEMA]
- Response: [SCHEMA]

Test cases:
- Success case
- Validation errors
- Not found
- Authentication errors

Use:
- pytest-asyncio
- httpx AsyncClient
- Proper status code assertions
```

---

## 5. Refactoring Prompts

### Refactor for Modern Python

```
Refactor this code to follow modern Python 3.13+ best practices:
- Use dataclasses or Pydantic models
- Apply PEP 695 type parameter syntax
- Use structural pattern matching where appropriate
- Use walrus operator where it improves readability
- Apply f-string improvements (PEP 701)
- Add comprehensive type hints

Code:
```python
[PASTE CODE]
```
```

### Extract Protocol

```
Extract a Protocol from this concrete class:
- Identify the public interface
- Create a @runtime_checkable Protocol
- Keep implementation in original class
- Update type hints to use Protocol

Code:
```python
[PASTE CODE]
```
```

### Convert to Dataclass

```
Convert this class to a modern Python dataclass:
- Use @dataclass decorator
- Add type hints for all fields
- Use field() for defaults and metadata
- Implement __post_init__ if needed
- Consider frozen=True for immutability

Code:
```python
[PASTE CODE]
```
```

---

## 6. FastAPI Prompts

### Create FastAPI Endpoint

```
Create a FastAPI endpoint:
- Method: [GET/POST/PUT/DELETE]
- Path: [PATH]
- Request model: [DESCRIBE FIELDS]
- Response model: [DESCRIBE FIELDS]
- Dependencies: [LIST DEPENDENCIES]

Include:
- Pydantic models with validation
- Proper HTTP status codes
- Error handling with HTTPException
- Type hints (Python 3.13+)
- Docstring for OpenAPI
```

### Create FastAPI Service

```
Create a FastAPI application with:
- Lifespan management (startup/shutdown)
- Database dependency injection
- CORS configuration
- Error handlers
- Health check endpoint

Routes:
- [LIST ROUTES]

Use:
- Python 3.13+ type hints
- Pydantic v2 models
- Async database operations
```

### Pydantic Models

```
Create Pydantic v2 models for:
- Entity: [ENTITY_NAME]
- Fields: [LIST FIELDS WITH TYPES]

Create these variations:
- [Entity]Create - for creation (no id)
- [Entity]Update - for updates (all optional)
- [Entity]Response - for API response (with id, timestamps)

Use:
- Field() for validation
- model_config for configuration
- Python 3.13+ type hints
```

---

## 7. Code Review Prompts

### Security Review

```
Review this Python code for security issues:
- SQL injection vulnerabilities
- Command injection
- Path traversal
- Secrets in code
- Insecure deserialization
- Missing input validation

Suggest fixes using Ruff S rules as reference.

Code:
```python
[PASTE CODE]
```
```

### Performance Review

```
Review this Python code for performance:
- Inefficient algorithms
- Memory issues
- Blocking operations in async
- N+1 query problems
- Missing caching opportunities

Suggest optimizations with examples.

Code:
```python
[PASTE CODE]
```
```

### Type Safety Review

```
Review this Python code for type safety:
- Missing type hints
- Incorrect types
- Any types that could be narrowed
- Missing None checks
- Protocol opportunities

Suggest improvements following mypy strict mode rules.

Code:
```python
[PASTE CODE]
```
```

---

## 8. Documentation Prompts

### Generate Docstrings

```
Add Google-style docstrings to this Python code:
- Function/method description
- Args with types and descriptions
- Returns with type and description
- Raises with exception types
- Examples where helpful

Code:
```python
[PASTE CODE]
```
```

### Create README

```
Create a README.md for this Python project:
- Project name: [NAME]
- Description: [DESCRIPTION]
- Python version: 3.13+

Sections:
- Features
- Installation (with uv)
- Quick start
- Configuration
- Development setup
- Testing
- API documentation (if applicable)
```

---

## 9. Migration Prompts

### Migrate to Python 3.13

```
Migrate this Python code from 3.10 to 3.13:
- Update type hints to modern syntax
- Use TaskGroup instead of gather where appropriate
- Use asyncio.timeout() instead of wait_for
- Apply PEP 695 type parameter syntax
- Use except* for ExceptionGroups
- Use TypeIs for type narrowing

Code:
```python
[PASTE CODE]
```
```

### Migrate from requirements.txt to pyproject.toml

```
Convert this requirements.txt to pyproject.toml:
- Use [project] table format
- Separate dev dependencies to [project.optional-dependencies]
- Add Ruff, mypy, pytest configuration
- Use modern version constraints

requirements.txt:
```
[PASTE REQUIREMENTS]
```
```

---

## 10. Specific Feature Prompts

### Free-Threading Preparation

```
Review this code for free-threading compatibility (Python 3.13+):
- Identify shared mutable state
- Check for race conditions
- Suggest thread-safe alternatives
- Add necessary locks
- Identify thread-local needs

Code:
```python
[PASTE CODE]
```
```

### Template Strings (Python 3.14)

```
Convert these f-strings to t-strings for safety:
- SQL queries (prevent injection)
- HTML output (prevent XSS)
- Shell commands (prevent injection)

Create appropriate template processors.

Code:
```python
[PASTE CODE]
```
```

---

## Prompt Tips

### Be Specific About Python Version

```
# Good
Using Python 3.13 with strict type hints...

# Bad
Using Python...
```

### Request Modern Patterns

```
# Good
Use PEP 695 type parameter syntax, asyncio.TaskGroup, and Pydantic v2.

# Bad
Create a generic class with async methods.
```

### Include Context

```
# Good
This is a FastAPI service using SQLAlchemy async ORM with PostgreSQL.

# Bad
This is a web service.
```

### Request Tests Together

```
# Good
Create the function AND pytest tests with 90% coverage.

# Bad
Create the function. (tests requested separately)
```

---

## Quick Reference

| Task | Key Prompt Elements |
|------|---------------------|
| New project | Python version, package manager (uv), tooling (ruff, mypy) |
| Type hints | Python version, PEP 695, strict mode |
| Async code | TaskGroup, timeout, semaphore, except* |
| Testing | pytest-asyncio, fixtures, parametrize, AsyncMock |
| FastAPI | Pydantic v2, lifespan, dependencies |
| Refactoring | Target version, specific patterns |

---

*LLM Prompts v2.0 - Modern Python 2026*
