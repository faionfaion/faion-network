# Testing Patterns Checklist

Step-by-step checklist for designing and implementing tests using proven patterns.

## Pre-Test Design

### 1. Identify Test Scope

- [ ] What am I testing? (function, class, API, UI flow)
- [ ] What is the expected behavior?
- [ ] What are the inputs and outputs?
- [ ] What side effects exist?
- [ ] What dependencies need to be handled?

### 2. Choose Test Level

| Level | When to Use | Pattern |
|-------|-------------|---------|
| Unit | Isolated logic, pure functions | AAA |
| Integration | Multiple components, DB, API | Given-When-Then |
| E2E | Critical user journeys | Page Object Model |

### 3. List Test Cases

- [ ] Happy path (normal successful execution)
- [ ] Edge cases (boundary values, empty inputs)
- [ ] Error cases (invalid inputs, exceptions)
- [ ] Null/undefined handling
- [ ] Concurrent access (if applicable)

## Test Structure Checklist

### AAA Pattern (Unit Tests)

```
[ ] ARRANGE
    [ ] Create test data (Builder/Factory/Object Mother)
    [ ] Set up mocks/stubs
    [ ] Configure system under test
    [ ] Clear separation from Act

[ ] ACT
    [ ] Single method call or action
    [ ] Capture result if needed
    [ ] Clear separation from Assert

[ ] ASSERT
    [ ] One logical concept verified
    [ ] Meaningful assertion messages
    [ ] No additional actions after assertions
```

### Given-When-Then (Integration/BDD)

```
[ ] GIVEN (preconditions)
    [ ] Describe initial state clearly
    [ ] Set up required data
    [ ] Configure environment

[ ] WHEN (action)
    [ ] Describe the trigger event
    [ ] Execute the action

[ ] THEN (expected outcome)
    [ ] Describe expected result
    [ ] Verify behavior, not implementation
```

## Test Data Checklist

### Using Builder Pattern

- [ ] Default values are sensible and valid
- [ ] WithX() methods are chainable
- [ ] Only relevant properties are customized
- [ ] Builder is reusable across tests
- [ ] Build() creates a fresh instance each time

### Using Object Mother

- [ ] Named methods describe scenarios (e.g., `typicalUser()`, `adminUser()`)
- [ ] Returns builders for flexibility (optional)
- [ ] Common scenarios are covered
- [ ] No hardcoded values that could cause conflicts

### Test Data Best Practices

- [ ] Use unique identifiers per test (UUIDs, timestamps)
- [ ] Avoid shared mutable state
- [ ] Clean up created data after test (if not using transactions)
- [ ] Use realistic but not production data

## Test Double Checklist

### Before Adding Test Double

- [ ] Is this dependency external (API, DB, filesystem)?
- [ ] Does the real implementation slow tests?
- [ ] Is the real implementation non-deterministic?
- [ ] Would using real implementation require complex setup?

### Choosing Test Double Type

| Situation | Use |
|-----------|-----|
| Need to fill parameter, won't use it | Dummy |
| Need specific return values | Stub |
| Need to verify method was called | Mock |
| Need to verify calls after the fact | Spy |
| Need working alternative implementation | Fake |

### Mock/Stub Setup

- [ ] Mock only what you need
- [ ] Verify essential interactions only
- [ ] Don't verify internal implementation details
- [ ] Set up all expected return values
- [ ] Consider using real objects when practical

## Test Isolation Checklist

### Before Each Test

- [ ] No dependency on previous test results
- [ ] No shared mutable state
- [ ] Fresh test data created
- [ ] Clean database state (if applicable)
- [ ] Mocks/stubs reset

### After Each Test

- [ ] Resources cleaned up
- [ ] Database transactions rolled back
- [ ] Temp files deleted
- [ ] No side effects left for next test

### Signs of Poor Isolation

- [ ] Tests pass individually but fail together
- [ ] Tests pass in different order
- [ ] Tests fail randomly (flaky)
- [ ] Tests depend on specific execution order

## Test Pyramid Checklist

### Unit Test Layer (70%)

- [ ] Tests individual functions/methods
- [ ] No external dependencies (mocked)
- [ ] Runs in milliseconds
- [ ] Covers business logic thoroughly
- [ ] Easy to maintain

### Integration Test Layer (20%)

- [ ] Tests component interactions
- [ ] Uses real dependencies (DB, cache)
- [ ] Tests API contracts
- [ ] Verifies configuration
- [ ] Tests data persistence

### E2E Test Layer (10%)

- [ ] Tests critical user journeys
- [ ] Uses Page Object Model
- [ ] Covers happy paths
- [ ] Minimal, high-value scenarios
- [ ] Stable selectors (data-testid)

## Page Object Model Checklist

### Page Class Design

- [ ] One class per page/major section
- [ ] Locators encapsulated in class
- [ ] Methods represent user actions
- [ ] No test assertions in page objects (optional)
- [ ] Meaningful method names

### Locator Strategy

| Priority | Selector Type | Example |
|----------|---------------|---------|
| 1 | data-testid | `[data-testid="submit-btn"]` |
| 2 | Role + Name | `getByRole('button', { name: 'Submit' })` |
| 3 | Text | `getByText('Submit')` |
| 4 | CSS class | `.submit-button` (avoid) |

### Page Object Methods

- [ ] Clear, action-based names (`login()`, `addToCart()`)
- [ ] Return page objects for navigation
- [ ] Handle waits internally
- [ ] No hardcoded sleeps

## Property-Based Testing Checklist

### Defining Properties

- [ ] Identify invariants (what should always be true)
- [ ] Consider round-trip properties (encode/decode)
- [ ] Look for idempotent operations
- [ ] Compare against reference implementation

### Generator Setup

- [ ] Generators produce valid inputs
- [ ] Edge cases included (empty, null, max values)
- [ ] Generators are composable
- [ ] Shrinking produces minimal examples

### Execution Configuration

- [ ] Appropriate number of examples (100-1000)
- [ ] Reasonable timeout per test
- [ ] CI runs more examples than local
- [ ] Seeds recorded for reproduction

## Flaky Test Prevention Checklist

### Common Causes

- [ ] No hardcoded sleeps (use explicit waits)
- [ ] No time-dependent assertions
- [ ] No shared state between tests
- [ ] No external service dependencies without mocks
- [ ] No order-dependent tests

### UI Test Stability

- [ ] Using stable selectors
- [ ] Waiting for elements before interacting
- [ ] Handling loading states
- [ ] Retrying flaky operations (with limits)

### Infrastructure

- [ ] Isolated test environments
- [ ] Consistent CI resources
- [ ] Deterministic test data
- [ ] Mocked external services

## Test Quality Checklist

### Test Readability

- [ ] Test name describes what is tested
- [ ] Clear Arrange-Act-Assert sections
- [ ] Minimal setup code
- [ ] No magic numbers (use named constants)
- [ ] Comments explain non-obvious setup

### Test Reliability

- [ ] Deterministic (same result every run)
- [ ] No external dependencies
- [ ] Fast execution
- [ ] Independent from other tests

### Test Maintainability

- [ ] DRY (Don't Repeat Yourself) in setup
- [ ] Uses test helpers/utilities
- [ ] Easy to update when code changes
- [ ] Clear failure messages

## Pre-Commit Test Checklist

Before pushing code:

- [ ] All new code has tests
- [ ] Tests follow project patterns
- [ ] No skipped tests
- [ ] No console.log/print statements in tests
- [ ] Tests pass locally
- [ ] No hardcoded paths or values
- [ ] Test coverage meets threshold
- [ ] No obvious flaky patterns

## Code Review Test Checklist

When reviewing test code:

- [ ] Tests verify behavior, not implementation
- [ ] Appropriate test level (unit vs integration)
- [ ] Meaningful test names
- [ ] Proper use of test doubles
- [ ] Edge cases covered
- [ ] No over-mocking
- [ ] Tests are readable
- [ ] Tests will survive refactoring
