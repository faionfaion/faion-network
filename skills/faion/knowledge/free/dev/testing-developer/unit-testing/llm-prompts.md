# LLM Prompts for Unit Test Generation

Optimized prompts for generating high-quality unit tests with LLMs (Claude, GPT, Gemini, Copilot).

## General Guidelines

### Before Generating Tests

1. **Provide context**: Include the function/class being tested
2. **Specify framework**: pytest, Jest, Go testing, etc.
3. **Share conventions**: Naming patterns, project structure
4. **List requirements**: Coverage targets, specific scenarios

### After Generating Tests

1. **Review all tests** before merging
2. **Verify assertions** are meaningful
3. **Check for hallucinations** (non-existent methods)
4. **Run mutation testing** to validate quality
5. **Match codebase style**

## Basic Test Generation

### Prompt Template 1: Simple Function

```
Generate unit tests for this function using pytest.

Function:
```python
{paste function code}
```

Requirements:
- Use Arrange-Act-Assert pattern
- Test happy path, edge cases, and error conditions
- Use descriptive test names: test_<function>_<scenario>_<expected>
- Include parametrized tests for multiple inputs
```

### Prompt Template 2: Class with Dependencies

```
Generate unit tests for this class using pytest with unittest.mock.

Class:
```python
{paste class code}
```

Dependencies to mock:
- {dependency1} - {brief description}
- {dependency2} - {brief description}

Requirements:
- Mock all external dependencies
- Test each public method
- Include both success and failure scenarios
- Use fixtures for common setup
```

### Prompt Template 3: TypeScript/Jest

```
Generate unit tests for this TypeScript module using Jest.

Code:
```typescript
{paste code}
```

Requirements:
- Use describe/it blocks with clear naming
- Mock dependencies with jest.fn() and jest.Mocked
- Test async functions with async/await
- Include type safety in mocks
```

## Specialized Prompts

### Edge Case Generation

```
Given this function, generate tests that cover:
1. Null/undefined inputs
2. Empty strings/arrays/objects
3. Boundary values (0, -1, MAX_INT)
4. Special characters in strings
5. Concurrent access scenarios
6. Timeout conditions

Function:
```{language}
{paste function code}
```

Use {testing_framework} and focus on cases that could cause production bugs.
```

### Error Handling Tests

```
Generate tests for error handling in this code using {framework}.

Code:
```{language}
{paste code}
```

Test scenarios:
1. All exception types that can be raised
2. Error message content validation
3. Error recovery and cleanup
4. Cascading failures
5. Retry logic (if applicable)

Ensure tests verify both the exception type AND meaningful error messages.
```

### API Endpoint Tests

```
Generate integration-style unit tests for this API endpoint.

Endpoint code:
```{language}
{paste endpoint code}
```

Test scenarios:
1. Valid request → success response
2. Invalid input → 400 Bad Request
3. Resource not found → 404
4. Unauthorized access → 401
5. Server error handling → 500

Mock the service layer and test HTTP status codes, response bodies, and headers.
```

### Database Layer Tests

```
Generate unit tests for this repository class.

Repository:
```{language}
{paste repository code}
```

Use an in-memory database or mocked connection.

Test:
1. CRUD operations
2. Query with filters
3. Pagination
4. Transaction handling
5. Constraint violations
```

## Advanced Prompts

### Mutation-Resistant Tests

```
Generate unit tests designed to catch mutations (small code changes).

Code:
```{language}
{paste code}
```

For each test:
1. Explain what mutation it would catch
2. Use precise assertions (not just "truthy")
3. Test boundary conditions exactly
4. Verify side effects

Goal: Tests should fail if any operator, constant, or condition is changed.
```

### Property-Based Test Generation

```
Generate property-based tests using {hypothesis/fast-check/quickcheck}.

Function:
```{language}
{paste function code}
```

Define properties that should always hold:
1. Invariants (what should always be true)
2. Roundtrip properties (encode/decode)
3. Commutativity/associativity if applicable
4. Size/bounds relationships
```

### Refactoring Safety Tests

```
I'm about to refactor this code. Generate tests that will catch regressions.

Current implementation:
```{language}
{paste code}
```

Create tests that:
1. Document current behavior (including edge cases)
2. Test public API contracts
3. Verify output format/structure
4. Check error handling behavior

These tests should pass before AND after refactoring if behavior is preserved.
```

### Test from Specification

```
Generate tests from this specification/user story.

Specification:
{paste specification or user story}

Implementation:
```{language}
{paste code}
```

Create tests that:
1. Map each acceptance criterion to test cases
2. Use Given-When-Then naming
3. Include positive and negative scenarios
4. Document any assumptions
```

## Framework-Specific Prompts

### pytest with Fixtures

```
Generate pytest tests with reusable fixtures.

Code to test:
```python
{paste code}
```

Create:
1. conftest.py with shared fixtures
2. Test file with fixture usage
3. Parametrized tests where appropriate
4. Markers for slow/integration tests
```

### Jest with TypeScript

```
Generate Jest tests for this TypeScript code with proper type safety.

Code:
```typescript
{paste code}
```

Requirements:
1. Use typed mocks (jest.Mocked<T>)
2. Test type guard functions
3. Handle Promise rejections properly
4. Use beforeEach for mock setup
```

### Go Table-Driven Tests

```
Generate Go table-driven tests for this function.

Code:
```go
{paste code}
```

Include:
1. Named test cases with descriptive names
2. Both success and error cases
3. Subtests using t.Run()
4. Helper functions if needed
```

## Review Prompts

### Test Quality Review

```
Review these tests for quality issues:

```{language}
{paste tests}
```

Check for:
1. Missing assertions (tests that can't fail)
2. Testing implementation vs behavior
3. Flakiness risks (time, randomness, order)
4. Over-mocking (testing mocks not code)
5. Missing edge cases
6. Poor naming
7. DRY violations

Suggest improvements with code examples.
```

### Coverage Gap Analysis

```
Given this code and its tests, identify coverage gaps.

Code:
```{language}
{paste code}
```

Existing tests:
```{language}
{paste tests}
```

Identify:
1. Untested branches/conditions
2. Missing edge cases
3. Error paths not covered
4. Implicit assumptions not tested
```

## Tips for Better Results

### Include Context

```
Project context:
- Framework: Django 5.0 / FastAPI
- Testing: pytest with pytest-asyncio
- Mocking: unittest.mock
- Style: Google docstrings, snake_case

Naming convention for tests:
test_<method>_<scenario>_<expected>
```

### Specify Constraints

```
Constraints:
- No database access (mock all repositories)
- Tests must be deterministic (mock datetime.now)
- Each test < 100ms
- No network calls
- Use factory functions for test data
```

### Request Explanations

```
For each test, add a brief comment explaining:
1. What scenario is being tested
2. Why this test is important
3. What production bug it would catch
```

## Anti-Pattern Detection Prompt

```
Review this test code and identify anti-patterns:

```{language}
{paste tests}
```

Check for:
1. Testing private methods directly
2. Tests that depend on execution order
3. Shared mutable state between tests
4. Assertions that always pass
5. Over-specified mocks (brittle tests)
6. Missing error case coverage
7. Tests that test the framework, not the code

Explain each issue and provide a fix.
```

## Batch Test Generation

```
Generate comprehensive tests for this module.

Module structure:
```{language}
{paste module with multiple functions/classes}
```

For EACH public function/method, generate:
1. Happy path test
2. Edge case test (empty, null, boundary)
3. Error handling test

Output format:
- Separate test class per source class
- Grouped by method (describe blocks)
- Include setup fixtures
```
