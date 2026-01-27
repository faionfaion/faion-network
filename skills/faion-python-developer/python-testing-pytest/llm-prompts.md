# LLM Prompts for pytest

Effective prompts for LLM-assisted pytest development.

---

## Table of Contents

1. [Writing Tests](#writing-tests)
2. [Fixtures](#fixtures)
3. [Mocking](#mocking)
4. [Django Testing](#django-testing)
5. [Async Testing](#async-testing)
6. [Configuration](#configuration)
7. [Debugging](#debugging)
8. [Refactoring](#refactoring)

---

## Writing Tests

### Generate Unit Tests

```
Write comprehensive pytest unit tests for this Python function:

```python
[PASTE YOUR FUNCTION HERE]
```

Requirements:
- Follow AAA pattern (Arrange, Act, Assert)
- Include edge cases and error scenarios
- Use descriptive test names (test_<action>_when_<condition>_returns_<result>)
- Use pytest.raises for exception testing
- Add parametrization for multiple input scenarios
```

### Generate Tests with Context

```
Write pytest tests for this service class:

```python
[PASTE YOUR CLASS HERE]
```

Context:
- This is a [Django/FastAPI/Flask] application
- Database is [PostgreSQL/SQLite/MongoDB]
- External dependencies: [list any APIs, services]

Requirements:
- Mock external dependencies
- Test both success and failure paths
- Include integration test for database operations
- Use factory pattern for test data
```

### Test Edge Cases

```
I have this function and existing tests:

Function:
```python
[PASTE FUNCTION]
```

Existing tests:
```python
[PASTE TESTS]
```

Add additional tests for:
- Edge cases I might have missed
- Boundary conditions
- Error handling scenarios
- Performance considerations (if applicable)
```

### Generate Parametrized Tests

```
Convert these repetitive tests to parametrized format:

```python
[PASTE REPETITIVE TESTS]
```

Requirements:
- Use @pytest.mark.parametrize
- Add descriptive IDs for each test case
- Group related parameters
- Include edge cases in the parameters
```

---

## Fixtures

### Create Fixture for Model

```
Create a pytest fixture for this model:

```python
[PASTE MODEL]
```

Requirements:
- Factory pattern with customizable attributes
- Handle foreign key relationships
- Include cleanup if needed
- Add docstring explaining usage
```

### Create conftest.py

```
Create a conftest.py file for a [Django/FastAPI] project with:

Project structure:
- tests/unit/
- tests/integration/
- tests/e2e/

Required fixtures:
- Database session with rollback
- API client (authenticated and unauthenticated)
- Factory fixtures for: [list your models]
- Mock fixtures for: [list external services]

Include:
- Custom markers registration
- Session-scoped fixtures for expensive setup
- Proper cleanup in teardown
```

### Fixture Composition

```
I have these fixtures:

```python
[PASTE EXISTING FIXTURES]
```

Create additional fixtures that:
1. Combine existing fixtures for common test scenarios
2. Add factory pattern for flexible data creation
3. Handle complex relationships between models
4. Provide both minimal and full data versions
```

### Session-Scoped Fixtures

```
Convert this function-scoped fixture to session-scoped for better performance:

```python
[PASTE FIXTURE]
```

Requirements:
- Maintain test isolation
- Add proper cleanup
- Handle potential state leakage
- Document scope implications
```

---

## Mocking

### Mock External API

```
Create mock fixtures for this external API integration:

```python
[PASTE API CLIENT CODE]
```

Requirements:
- Mock successful responses
- Mock error responses (timeout, 404, 500, rate limit)
- Use autospec for signature validation
- Allow customization of mock responses
- Handle async if applicable
```

### Mock Database Operations

```
Create mocks for these database operations:

```python
[PASTE REPOSITORY/DAO CODE]
```

Requirements:
- Mock CRUD operations
- Handle transactions
- Simulate errors (connection, constraint violations)
- Allow return value customization
```

### Mock with Side Effects

```
Create a mock with complex side effects for testing this code:

```python
[PASTE CODE THAT NEEDS MOCKING]
```

Requirements:
- Different behavior on successive calls
- Conditional responses based on arguments
- Simulate intermittent failures
- Track call history for assertions
```

### Verify Mock Calls

```
Add mock verification assertions to these tests:

```python
[PASTE TESTS]
```

Verify:
- Correct arguments were passed
- Correct number of calls
- Call order (if multiple mocks)
- No unexpected calls
```

---

## Django Testing

### API Endpoint Tests

```
Write pytest-django tests for this DRF viewset:

```python
[PASTE VIEWSET]
```

Requirements:
- Test all HTTP methods (GET, POST, PATCH, DELETE)
- Test authentication and permissions
- Test validation errors
- Test pagination and filtering
- Use Factory Boy for test data
- Include @pytest.mark.django_db
```

### Model Tests

```
Write comprehensive tests for this Django model:

```python
[PASTE MODEL]
```

Test:
- Model creation with valid data
- Validation rules
- Custom methods and properties
- Signals (if any)
- Constraints (unique, foreign key)
- Manager methods
- __str__ representation
```

### Factory Boy Factories

```
Create Factory Boy factories for these Django models:

```python
[PASTE MODELS]
```

Requirements:
- Handle all fields including optional ones
- Use SubFactory for relationships
- Add Sequence for unique fields
- Include lazy_attribute for computed fields
- Add post_generation for M2M relationships
```

### Django Settings Override

```
Write tests that require different Django settings:

Test scenarios:
1. [DESCRIBE SCENARIO 1]
2. [DESCRIBE SCENARIO 2]

Show how to:
- Override settings per test
- Use settings fixture
- Handle environment-specific behavior
```

---

## Async Testing

### Async Function Tests

```
Write pytest-asyncio tests for this async function:

```python
[PASTE ASYNC FUNCTION]
```

Requirements:
- Use @pytest.mark.asyncio marker
- Create async fixtures if needed
- Mock async dependencies
- Test concurrent execution
- Handle timeouts and cancellation
```

### FastAPI Endpoint Tests

```
Write async tests for this FastAPI endpoint:

```python
[PASTE FASTAPI ROUTER]
```

Requirements:
- Use httpx.AsyncClient with ASGI transport
- Test request/response serialization
- Test dependency injection
- Mock database and external services
- Test error responses
```

### Async Mock

```
Create async mocks for this service:

```python
[PASTE ASYNC SERVICE]
```

Requirements:
- Use AsyncMock for async methods
- Handle awaitable return values
- Mock async context managers
- Test exception handling in async code
```

---

## Configuration

### pyproject.toml Setup

```
Create a complete pytest configuration in pyproject.toml for:

Project type: [Django/FastAPI/CLI/Library]
Python version: 3.12
Key plugins: [list plugins you're using]

Include:
- Coverage settings with 80% threshold
- Custom markers for [slow, integration, e2e]
- Async configuration
- Strict mode settings
- Exclusion patterns
```

### CI Configuration

```
Create a GitHub Actions workflow for pytest with:

Requirements:
- Python [VERSION]
- Services: [PostgreSQL, Redis, etc.]
- Parallel test execution
- Coverage reporting to Codecov
- Artifact upload for test results
- Cache pip dependencies
```

### Makefile Commands

```
Create Makefile commands for:

- Running all tests
- Running tests with coverage
- Running only unit tests
- Running only integration tests
- Running tests in parallel
- Debugging failed tests
- Generating HTML coverage report
```

---

## Debugging

### Fix Failing Test

```
This test is failing:

```python
[PASTE FAILING TEST]
```

Error message:
```
[PASTE ERROR]
```

Context:
- Code under test: [PASTE OR DESCRIBE]
- Recent changes: [DESCRIBE]

Help me:
1. Understand why the test is failing
2. Determine if test or code needs fixing
3. Provide the corrected version
```

### Fix Flaky Test

```
This test is flaky (passes sometimes, fails sometimes):

```python
[PASTE FLAKY TEST]
```

Failure pattern:
- [DESCRIBE WHEN IT FAILS]

Help me:
1. Identify the source of flakiness
2. Make the test deterministic
3. Add proper isolation/cleanup
```

### Debug Fixture Issue

```
This fixture isn't working as expected:

```python
[PASTE FIXTURE AND TEST]
```

Problem:
[DESCRIBE THE ISSUE]

Expected behavior:
[DESCRIBE EXPECTED]

Actual behavior:
[DESCRIBE ACTUAL]
```

### Performance Optimization

```
These tests are too slow:

```python
[PASTE SLOW TESTS]
```

Current duration: [X] seconds
Target duration: [Y] seconds

Suggest optimizations:
- Fixture scope changes
- Parallel execution strategies
- Test data reduction
- Mock opportunities
```

---

## Refactoring

### Improve Test Organization

```
Refactor these tests for better organization:

```python
[PASTE TESTS]
```

Goals:
- Group related tests in classes
- Extract common setup to fixtures
- Reduce code duplication
- Improve readability
```

### Extract Shared Fixtures

```
Extract common fixtures from these test files:

File 1:
```python
[PASTE TESTS FROM FILE 1]
```

File 2:
```python
[PASTE TESTS FROM FILE 2]
```

Create a conftest.py with:
- Shared fixtures
- Factory fixtures
- Helper functions
```

### Convert to Parametrized

```
Refactor these tests to use parametrization:

```python
[PASTE REPETITIVE TESTS]
```

Maintain:
- All existing test cases
- Clear test IDs
- Easy extensibility
```

### Modernize Tests

```
Update these tests to modern pytest patterns:

```python
[PASTE OLD TESTS]
```

Modernize:
- Use pytest.raises context manager
- Use fixtures instead of setup methods
- Use parametrize instead of loops
- Use pytest-mock instead of unittest.mock
- Add type hints
```

---

## Quick Reference Prompts

### One-Liner Prompts

| Task | Prompt |
|------|--------|
| Basic test | "Write a pytest test for `[function_name]` that tests [scenario]" |
| Add edge case | "Add edge case tests for [function] covering [cases]" |
| Create fixture | "Create a pytest fixture for [model/class] with [requirements]" |
| Mock API | "Mock [service] API returning [response] for testing" |
| Add coverage | "Add tests to cover these uncovered lines: [lines]" |
| Fix test | "Fix this failing test: [error message]" |
| Parametrize | "Convert to parametrized test: [test code]" |

### Context Template

```
Context for pytest assistance:

Project: [Django/FastAPI/Flask/Library]
Python: [version]
Database: [type]
Plugins: [list]
Testing focus: [unit/integration/e2e]

Code to test:
```python
[CODE]
```

Request:
[SPECIFIC REQUEST]
```

---

## Best Practices for LLM Prompts

### Do

- Provide complete function/class code
- Include error messages verbatim
- Specify framework and dependencies
- Describe expected behavior clearly
- Mention any constraints or requirements

### Don't

- Assume LLM knows your codebase
- Omit relevant context
- Use vague terms ("make it better")
- Forget to mention async requirements
- Skip error details

### Iterative Refinement

```
Initial prompt result wasn't quite right because [reason].

Please adjust to:
- [Specific change 1]
- [Specific change 2]

Keep:
- [What was correct]
```

---

*LLM Prompts for pytest v2.0*
