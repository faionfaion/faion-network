# LLM Prompts for Testing

Effective prompts for using AI assistants to generate, review, and improve tests.

## Prompt Engineering Principles

### Context is Critical

LLMs produce better tests when given:
1. **The code under test** - Full implementation
2. **Test framework** - pytest, Jest, Go testing, etc.
3. **Pattern preference** - AAA, Given-When-Then, etc.
4. **Coverage requirements** - Happy path, edge cases, errors

### Output Format Specification

Always specify:
- Programming language
- Test framework
- Assertion library (if separate)
- Any project conventions

## Unit Test Generation Prompts

### Basic Unit Test Prompt

```
Write unit tests for the following [Python/JavaScript/Go] function using [pytest/Jest/testing].

Use the AAA (Arrange-Act-Assert) pattern with clear section comments.

Cover these scenarios:
1. Happy path with valid input
2. Edge case: empty/null input
3. Edge case: boundary values
4. Error case: invalid input

Function:
```[paste function here]```

Requirements:
- Use descriptive test names that explain what is being tested
- One assertion per test (or one logical concept)
- Mock external dependencies if any
```

### Comprehensive Unit Test Prompt

```
Generate comprehensive unit tests for this [language] [class/module].

Framework: [pytest/Jest/Vitest/Go]
Pattern: AAA (Arrange-Act-Assert)

Test requirements:
1. Test each public method
2. Cover happy paths and error paths
3. Test edge cases (null, empty, boundary values)
4. Test any state changes
5. Verify exception handling

For each test:
- Use clear, behavior-describing names
- Add comments explaining test purpose
- Use test data builders or factories for complex objects

Code to test:
```[paste code here]```

Context:
- This is a [describe component role]
- It depends on [list dependencies]
- Key business rules: [list rules]
```

### Edge Case Discovery Prompt

```
Analyze this function and identify all edge cases that should be tested.

Function:
```[paste function here]```

For each edge case identified:
1. Describe the scenario
2. Explain why it's an edge case
3. Specify expected behavior
4. Write the test code

Consider:
- Null/undefined/nil inputs
- Empty collections/strings
- Boundary values (0, -1, MAX_INT)
- Unicode/special characters
- Concurrent access (if applicable)
- Resource limits
```

## Test Data Builder Prompts

### Builder Pattern Generation

```
Create a Test Data Builder for this [language] entity/model.

Entity:
```[paste entity definition]```

Requirements:
1. Fluent API (chainable methods)
2. Sensible defaults for all fields
3. withX() methods for each field
4. Convenience methods for common scenarios (e.g., asAdmin(), asActive())
5. build() method returns new instance

Include usage examples showing:
- Creating default object
- Customizing specific fields
- Creating common test scenarios
```

### Object Mother Generation

```
Create an Object Mother pattern implementation for test data.

Entities:
```[paste entity definitions]```

Requirements:
1. Static factory methods for common scenarios
2. Return builders (not final objects) for flexibility
3. Methods should have clear, scenario-based names
4. Cover these scenarios: [list scenarios]

Example method names:
- regularUser(), adminUser(), guestUser()
- pendingOrder(), paidOrder(), shippedOrder()
- validCreditCard(), expiredCreditCard()
```

## Integration Test Prompts

### API Integration Test Prompt

```
Write integration tests for this REST API endpoint.

Endpoint: [method] [path]
Framework: [pytest/Jest/supertest]

Endpoint details:
- Request body: [schema]
- Response: [schema]
- Authentication: [type]

Test scenarios:
1. Successful request with valid data
2. Validation error (invalid input)
3. Authentication error (missing/invalid token)
4. Authorization error (insufficient permissions)
5. Resource not found
6. Conflict/duplicate

Requirements:
- Use real database (or Testcontainers)
- Clean up test data after each test
- Test response status codes and body
- Verify database state changes
```

### Database Integration Test Prompt

```
Write integration tests for this repository/DAO class.

Repository:
```[paste repository code]```

Framework: [pytest with SQLAlchemy/TypeORM/GORM]
Database: [PostgreSQL/MySQL/MongoDB]

Requirements:
1. Use transaction rollback for isolation
2. Test CRUD operations
3. Test query methods with various filters
4. Test edge cases (not found, duplicate key)
5. Test any cascade operations

Setup should:
- Create test database/schema
- Seed required reference data
- Begin transaction before each test
- Rollback after each test
```

## E2E Test Prompts

### Page Object Model Prompt

```
Create Page Object classes for these web pages using [Playwright/Cypress].

Pages to model:
1. [Page name] - [URL path]
   - Elements: [list key elements]
   - Actions: [list user actions]

Requirements:
1. Encapsulate all locators
2. Use data-testid selectors (preferred)
3. Create action methods that return appropriate page objects
4. Handle waits internally
5. No assertions in page objects (optional)

Include:
- BasePage with common functionality
- Page-specific classes
- Navigation methods that return new page instances
```

### E2E Test Scenario Prompt

```
Write E2E tests for this user journey using [Playwright/Cypress].

User Journey: [name]
Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Requirements:
1. Use Page Object Model
2. Test happy path completely
3. Add one negative test case
4. Take screenshots on failure
5. Include setup/teardown for test data

Existing Page Objects:
- LoginPage
- DashboardPage
- [others]
```

## Mock and Stub Prompts

### Mock Generation Prompt

```
Create mocks/stubs for these dependencies in my tests.

Dependencies to mock:
1. [Dependency 1] - interface/class
2. [Dependency 2] - interface/class

Testing framework: [Jest/unittest.mock/gomock]

For each mock:
1. Show how to create the mock
2. Set up return values for key methods
3. Set up error scenarios
4. Show verification of calls

Include examples of:
- Returning different values per call
- Throwing errors
- Verifying call arguments
- Verifying call count
```

### Spy Implementation Prompt

```
Create spy implementations for tracking these method calls.

Interface:
```[paste interface]```

Requirements:
1. Record all method calls with arguments
2. Allow inspection of call history
3. Optionally delegate to real implementation
4. Reset capability between tests
```

## Property-Based Testing Prompts

### Property Discovery Prompt

```
Identify properties that should always hold true for this function/system.

Code:
```[paste code]```

For each property:
1. Describe the property in plain English
2. Explain why it should always be true
3. Show the property test implementation

Consider these property types:
- Round-trip (encode/decode)
- Idempotence (f(f(x)) == f(x))
- Invariants (conditions that must hold)
- Commutativity (order doesn't matter)
- Associativity (grouping doesn't matter)
- Identity (neutral element)
```

### Property Test Generation Prompt

```
Write property-based tests using [Hypothesis/fast-check/QuickCheck].

Function to test:
```[paste function]```

Generate tests for these properties:
1. [Property 1]
2. [Property 2]

Requirements:
1. Define appropriate generators/arbitraries
2. Add shrinking for better failure messages
3. Set reasonable example counts
4. Handle preconditions with assume/filter
```

## Test Refactoring Prompts

### Test Smell Detection Prompt

```
Review these tests for common test smells and anti-patterns.

Tests:
```[paste tests]```

Check for:
1. Unclear test names
2. Multiple assertions testing different things
3. Test interdependence
4. Magic numbers/strings
5. Excessive setup
6. Mocking too much
7. Testing implementation details
8. Flaky patterns (timing, random)
9. Missing edge cases
10. Poor error messages

For each issue found:
- Explain the problem
- Suggest a fix
- Show refactored code
```

### Test Improvement Prompt

```
Improve these tests for better maintainability and reliability.

Current tests:
```[paste tests]```

Improvements to apply:
1. Extract common setup to fixtures/beforeEach
2. Use test data builders
3. Improve test names to describe behavior
4. Add missing edge cases
5. Reduce duplication
6. Make assertions more specific

Return the refactored tests with comments explaining changes.
```

## Flaky Test Analysis Prompts

### Flaky Test Diagnosis Prompt

```
Analyze this flaky test and identify potential causes.

Test code:
```[paste test]```

Test behavior:
- Passes: [X]% of the time
- Failure message: [message]
- Environment: [CI/local]

Check for:
1. Race conditions
2. Timing dependencies
3. Shared state
4. External service dependencies
5. Non-deterministic data
6. Order dependencies
7. Resource leaks

Provide:
1. Most likely cause
2. How to confirm the cause
3. Fix recommendation
4. Refactored test code
```

### Flaky Test Fix Prompt

```
Fix this flaky test that fails intermittently.

Flaky test:
```[paste test]```

Known issues:
- [describe observed failures]

Apply these fixes:
1. Replace sleep/timeouts with explicit waits
2. Use stable selectors
3. Isolate test data
4. Mock unreliable dependencies
5. Add retry logic if appropriate

Return the fixed test with explanations.
```

## Test Documentation Prompts

### Test Suite Documentation Prompt

```
Generate documentation for this test suite.

Test files:
```[paste test file list or code]```

Create:
1. Overview of what is being tested
2. Test categories and their purposes
3. Setup requirements
4. How to run tests (commands)
5. Coverage information
6. Known limitations

Format as markdown suitable for README.
```

### Test Case Documentation Prompt

```
Add documentation to these tests explaining their purpose.

Tests:
```[paste tests]```

For each test, add:
1. Description comment explaining the scenario
2. Why this test exists (regression, edge case, etc.)
3. Any related requirements/tickets
4. Expected behavior description
```

## Quick Reference Prompts

### Generate Test for Function

```
Write [framework] tests for this function using AAA pattern. Cover happy path, edge cases, and errors.

```[function code]```
```

### Generate Page Object

```
Create a Playwright Page Object for [page name] at [URL] with these elements: [list]. Include navigation and action methods.
```

### Generate Test Data Builder

```
Create a fluent test data builder for this entity with sensible defaults and withX() methods:

```[entity definition]```
```

### Review Tests for Issues

```
Review these tests for: unclear names, missing cases, flaky patterns, over-mocking, and test smells. Suggest fixes.

```[test code]```
```

### Generate Property Tests

```
Write property-based tests using [library] for this function. Identify 3 properties that should always hold:

```[function code]```
```

## Tips for Better Results

### Do

- Provide complete code context
- Specify exact frameworks and versions
- Describe the purpose of the code being tested
- List specific scenarios to cover
- Mention any constraints or conventions

### Avoid

- Vague requests ("write some tests")
- Missing framework specification
- No code context
- Expecting perfect results without iteration

### Iteration Pattern

1. Generate initial tests
2. Review for coverage gaps
3. Ask for specific edge cases
4. Request refactoring for maintainability
5. Verify assertions are meaningful
