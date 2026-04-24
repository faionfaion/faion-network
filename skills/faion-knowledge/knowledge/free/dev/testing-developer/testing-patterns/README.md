# Testing Patterns

Comprehensive guide to software testing patterns for writing maintainable, reliable, and effective tests.

## Overview

Testing patterns are proven solutions to common testing challenges. They help you write tests that are readable, maintainable, and provide confidence in your code. This guide covers patterns from unit tests to E2E tests, applicable across Python, JavaScript, Go, and other languages.

## Pattern Categories

| Category | Patterns | Purpose |
|----------|----------|---------|
| **Structure** | AAA, Given-When-Then | Organize test code |
| **Data Creation** | Builder, Object Mother, Factory | Create test objects |
| **Test Doubles** | Mock, Stub, Spy, Fake, Dummy | Replace dependencies |
| **Architecture** | Test Pyramid, Testing Trophy | Balance test types |
| **UI Testing** | Page Object Model | Maintainable E2E tests |
| **Isolation** | Fresh Fixture, Sandbox | Prevent test interference |
| **Advanced** | Property-Based Testing | Generate test cases |

## Core Patterns

### 1. Arrange-Act-Assert (AAA)

The AAA pattern is the most widely adopted structure for unit tests, proposed by Bill Wake in 2001.

**Structure:**
- **Arrange** - Set up test data, dependencies, and preconditions
- **Act** - Execute the code under test (single action)
- **Assert** - Verify the expected outcome

**Benefits:**
- Clear separation of concerns within each test
- Easy to identify which part of a test is failing
- Consistent structure across the entire test suite

**Best Practices:**
- Keep each section clearly separated (blank line between sections)
- Act section should be a single method call or action
- Assert section should verify one logical concept (can be multiple assertions)

### 2. Given-When-Then (BDD)

BDD-style structure that reads like natural language, popularized by Daniel Terhorst-North and Chris Matts.

**Structure:**
- **Given** - Initial context or preconditions
- **When** - Action or event that triggers the behavior
- **Then** - Expected outcome or result

**Benefits:**
- Tests serve as executable documentation
- Non-technical stakeholders can understand tests
- Aligns tests with business requirements

**Mapping to AAA:**
| AAA | BDD |
|-----|-----|
| Arrange | Given |
| Act | When |
| Assert | Then |

### 3. Test Data Builder Pattern

Creates test objects step-by-step with fluent API, allowing customization of only relevant properties.

**Benefits:**
- Specifies only properties relevant to the test
- Provides sensible defaults for everything else
- Reads like a sentence describing the test object
- Easy to create variations without duplication

**When to Use:**
- Complex objects with many properties
- Need to vary specific attributes per test
- Want self-documenting test data creation

### 4. Object Mother Pattern

A factory class that produces pre-configured test objects.

**Benefits:**
- Quick creation of common test scenarios
- Reusable across multiple test files
- Consistent test data throughout the suite

**When to Use:**
- Standard test scenarios that repeat often
- Integration tests needing realistic data
- When consistency is more important than flexibility

**Combining Builder + Object Mother:**
Return builders from Object Mother methods for both convenience and flexibility:
```
ObjectMother.aTypicalUser()  // Returns UserBuilder
    .withRole("admin")       // Customize as needed
    .build()                 // Create final object
```

### 5. Test Double Patterns

Test doubles replace production dependencies for testing. Gerard Meszaros defined five types:

| Type | Purpose | Behavior |
|------|---------|----------|
| **Dummy** | Fill parameter lists | Never actually used |
| **Stub** | Provide canned answers | Returns predefined values |
| **Spy** | Record interactions | Logs method calls for later verification |
| **Fake** | Working implementation | Simplified version (e.g., in-memory DB) |
| **Mock** | Verify behavior | Expects specific calls, fails if not received |

**Key Distinction:**
- **Stubs** test state: "Does the result match expectations?"
- **Mocks** test behavior: "Were the right methods called?"

**When to Use Each:**
| Scenario | Test Double |
|----------|-------------|
| Need to fill unused parameters | Dummy |
| Need specific return values | Stub |
| Need to verify method calls | Mock |
| Need to record calls for later check | Spy |
| Need working alternative | Fake |

### 6. Test Pyramid

Mike Cohn's strategic framework (2009) for balancing test types.

```
        /\
       / E2E \        Few, slow, expensive (10%)
      /-------\
     / Integration \ Some, medium speed (20%)
    /---------------\
   /   Unit Tests   \  Many, fast, cheap (70%)
  /-------------------\
```

**Recommended Ratio:** 70% Unit / 20% Integration / 10% E2E

**Modern Alternatives:**
- **Testing Trophy** (Kent C. Dodds): Emphasizes integration tests and static analysis
- **Testing Honeycomb** (Spotify): For microservices, emphasizes contract testing

**Anti-pattern: Ice Cream Cone**
Inverted pyramid with many E2E tests and few unit tests:
- E2E tests taking 5 minutes each: 1,000 tests = 83 hours
- Unit tests taking 50ms each: 1,000 tests = 50 seconds
- 6,000x execution time difference

### 7. Page Object Model (POM)

Encapsulates page elements and interactions in separate classes for UI testing.

**Components:**
- **Page class** - Represents a page or major section
- **Locators** - Element selectors (preferably data-testid)
- **Actions** - Methods that perform user interactions
- **Assertions** - Optional verification methods

**Benefits:**
- UI changes require updates in one place
- Tests read like user actions
- Reusable across multiple test scenarios

**Project Structure:**
```
tests/
  pages/
    LoginPage.ts
    DashboardPage.ts
    CheckoutPage.ts
  specs/
    login.spec.ts
    checkout.spec.ts
```

### 8. Test Isolation Patterns

Prevent tests from interfering with each other.

**Fresh Fixture:**
Each test creates its own test data from scratch. No shared state between tests.

**Database Isolation:**
| Strategy | Speed | Isolation |
|----------|-------|-----------|
| Transaction rollback | Fast | Good |
| Truncate tables | Medium | Great |
| Fresh database | Slow | Perfect |

**Sandbox Pattern:**
Run tests in isolated temp directories to prevent file system conflicts.

### 9. Property-Based Testing

Instead of writing specific examples, define properties that should always hold true.

**Property Types:**
- **Round-trip** - encode(decode(x)) == x
- **Idempotence** - f(f(x)) == f(x)
- **Invariants** - balance >= 0 after any transaction
- **Oracle** - compare against reference implementation

**Benefits:**
- Discovers edge cases automatically
- Generates hundreds of test cases
- Shrinking finds minimal failing examples

**Tools:**
| Language | Library |
|----------|---------|
| Python | Hypothesis |
| Haskell | QuickCheck |
| JavaScript | fast-check |
| Rust | proptest, quickcheck |
| Go | gopter |

## Flaky Test Prevention

Flaky tests (tests that pass and fail inconsistently) consume ~40% of QA team time according to State of QA 2025.

**Common Causes:**
1. Race conditions and timing issues
2. Shared state between tests
3. Hardcoded waits instead of explicit waits
4. Unstable locators in UI tests
5. External service dependencies

**Prevention Strategies:**
1. Use explicit/dynamic waits instead of sleep()
2. Use stable selectors (data-testid)
3. Mock external services
4. Isolate test data
5. Avoid execution order dependencies
6. Run tests in parallel with process isolation

**Quarantine Strategy:**
- Move flaky tests to separate suite
- Run independently from main CI
- Track failure rates and owners
- Define re-integration criteria

## LLM Usage Tips

When using AI assistants to write tests:

### Prompt Structure

1. **Context First** - Provide the code under test
2. **Pattern Specification** - Request specific pattern (AAA, Given-When-Then)
3. **Coverage Request** - Specify edge cases to cover
4. **Framework Mention** - Name the testing framework

### Effective Requests

| Good Request | Why It Works |
|--------------|--------------|
| "Write AAA-style unit tests for this function covering happy path, empty input, and error cases" | Specifies pattern, coverage, scenarios |
| "Create a Page Object for LoginPage with login(), getErrorMessage() methods using Playwright" | Clear scope, named methods, framework |
| "Generate a test data builder for User entity with defaults and fluent API" | Pattern name, entity, API style |

### What to Verify

Always review AI-generated tests for:
- Meaningful assertions (not just "assert true")
- Actual edge case coverage
- Correct mock setup and verification
- Test independence (no shared state)
- Appropriate test double usage

### Test Generation Workflow

```
1. Provide function/class code
2. Request specific test pattern
3. Review and adjust assertions
4. Add edge cases if missing
5. Verify test isolation
```

## Quick Reference

| Pattern | Use For | Key Benefit |
|---------|---------|-------------|
| AAA | All unit tests | Clear structure |
| Given-When-Then | BDD, integration tests | Readable specs |
| Test Data Builder | Complex objects | Flexible creation |
| Object Mother | Common scenarios | Quick setup |
| Mock | Behavior verification | Explicit expectations |
| Stub | State verification | Simple returns |
| Fake | Working substitute | Realistic behavior |
| Page Object | UI tests | Maintainable selectors |
| Property-Based | Edge case discovery | Automatic generation |


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Sources

### Core Patterns
- [Arrange-Act-Assert (AAA) Pattern](https://semaphore.io/blog/aaa-pattern-test-automation) - Comprehensive AAA guide
- [Test Double Patterns](https://martinfowler.com/bliki/TestDouble.html) - Gerard Meszaros vocabulary
- [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) - Martin Fowler on test doubles

### Test Architecture
- [Modern Test Pyramid Guide 2025](https://fullscale.io/blog/modern-test-pyramid-guide/) - Updated pyramid strategies
- [Testing Skyscraper](https://automationpanda.com/2025/09/29/the-testing-skyscraper-a-modern-alternative-to-the-testing-pyramid/) - Modern alternative to pyramid
- [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) - Martin Fowler deep dive

### Test Data Patterns
- [Test Data Builders](https://www.arhohuttunen.com/test-data-builders/) - Builder pattern tutorial
- [Test Data Builders vs Object Mother](http://www.natpryce.com/articles/000714.html) - Pattern comparison
- [Combining Object Mother and Builder](https://reflectoring.io/objectmother-fluent-builder/) - Hybrid approach

### UI Testing
- [Page Object Model with Playwright](https://playwright.dev/docs/pom) - Official Playwright docs
- [Page Object Model Guide 2025](https://www.skyvern.com/blog/page-object-model-guide/) - Best practices

### Property-Based Testing
- [What is Property-Based Testing](https://hypothesis.works/articles/what-is-property-based-testing/) - Hypothesis guide
- [Property-Based Testing Tutorial](https://zetcode.com/terms-testing/property-based-testing/) - Patterns and practices

### Flaky Tests
- [Flaky Tests in 2026](https://www.accelq.com/blog/flaky-tests/) - Causes, fixes, prevention
- [Flaky Test Management Strategies](https://aqua-cloud.io/flaky-tests/) - 7 essential strategies
- [How to Fix Flaky Tests in 2025](https://reproto.com/how-to-fix-flaky-tests-in-2025-a-complete-guide-to-detection-prevention-and-management/) - Complete guide
