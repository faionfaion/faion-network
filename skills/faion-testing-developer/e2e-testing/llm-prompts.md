# LLM Prompts for E2E Testing

Effective prompts for AI-assisted E2E test generation, debugging, and optimization.

---

## Table of Contents

1. [Page Object Generation](#1-page-object-generation)
2. [Test Case Generation](#2-test-case-generation)
3. [Test Data & Factories](#3-test-data--factories)
4. [Debugging & Fixing](#4-debugging--fixing)
5. [Migration & Refactoring](#5-migration--refactoring)
6. [CI/CD Configuration](#6-cicd-configuration)
7. [Best Practices Review](#7-best-practices-review)

---

## 1. Page Object Generation

### Generate Page Object from HTML

```
Create a Playwright Page Object class for this HTML page.

Requirements:
- Use TypeScript with proper types
- Extend BasePage class (constructor accepts Page)
- Use getByTestId, getByRole, getByLabel for locators (prefer accessible selectors)
- Define locators as arrow functions returning Locator
- Create action methods for user interactions
- Add JSDoc comments for complex methods
- Follow Page Object Model best practices

HTML:
[paste HTML here]

Example output format:
```typescript
export class ExamplePage extends BasePage {
  // Locators
  readonly submitButton = () => this.page.getByRole('button', { name: 'Submit' });

  // Actions
  async submitForm() { ... }
}
```
```

### Generate Page Object from Figma/Design

```
Create a Playwright Page Object for a [page name] page with these elements:

UI Elements:
- Header with logo and navigation (Home, Products, About, Contact)
- Search bar with autocomplete dropdown
- Product grid with cards (image, title, price, add to cart button)
- Pagination (previous, page numbers, next)
- Footer with links and newsletter signup

Requirements:
- TypeScript Page Object extending BasePage
- Use semantic locators (getByRole, getByLabel, getByText)
- Assume data-testid attributes where appropriate
- Include all CRUD operations as methods
- Add helper methods for common interactions
- Return appropriate page objects from navigation methods
```

### Generate Component Page Object

```
Create a reusable Playwright component class for a [component name].

Component behavior:
[describe component behavior]

Requirements:
- Accept root Locator in constructor (not Page)
- Define child locators relative to root
- Create methods for all interactions
- Handle component states (loading, error, empty)
- Make it composable with page objects

Example structure:
```typescript
export class DataTableComponent {
  constructor(private root: Locator) {}

  readonly rows = () => this.root.getByRole('row');
  // ...
}
```
```

---

## 2. Test Case Generation

### Generate Tests from User Story

```
Generate Playwright E2E tests for this user story:

User Story:
As a [role]
I want to [action]
So that [benefit]

Acceptance Criteria:
- [AC1]
- [AC2]
- [AC3]

Requirements:
- Use describe/test structure
- Import from custom fixtures (../fixtures)
- Use Page Object pattern (import pages)
- Include positive and negative test cases
- Add edge cases where appropriate
- Use meaningful test descriptions
- Follow AAA pattern (Arrange, Act, Assert)

Existing Page Objects:
[list available page objects]
```

### Generate Tests from API Specification

```
Generate E2E tests that verify the UI correctly integrates with this API endpoint:

Endpoint: [METHOD] [path]
Request: [request body/params]
Response: [response structure]
Error cases: [list error responses]

Requirements:
- Test UI displays data correctly
- Test error handling in UI
- Test loading states
- Mock API responses using page.route()
- Verify request payloads where relevant
- Use data factories for test data
```

### Generate Visual Regression Tests

```
Generate Playwright visual regression tests for [page/component name].

Requirements:
- Test multiple states: default, hover, active, disabled, error
- Test responsive breakpoints: desktop (1920px), tablet (768px), mobile (375px)
- Mask dynamic content (timestamps, avatars, random data)
- Disable animations before screenshots
- Use meaningful screenshot names
- Include dark mode variants if applicable

States to capture:
[list specific states]
```

### Generate Mobile Test Cases

```
Generate Playwright mobile E2E tests for [feature name].

Device targets:
- iPhone 14 (iOS Safari)
- Pixel 7 (Android Chrome)

Requirements:
- Use devices from @playwright/test
- Test touch interactions (swipe, tap, long press)
- Test responsive navigation (hamburger menu)
- Test soft keyboard interactions
- Test orientation changes if relevant
- Consider mobile-specific UX patterns
```

---

## 3. Test Data & Factories

### Generate Data Factory

```
Create a TypeScript data factory for [entity name] with faker.js.

Entity schema:
[describe fields and types]

Requirements:
- Use @faker-js/faker
- Create base factory with create() and createMany() methods
- Support partial overrides
- Add specialized factory methods for common scenarios:
  - [scenario 1]
  - [scenario 2]
- Export types alongside factory
- Make data realistic and valid

Example:
```typescript
export const userFactory = {
  create: (overrides?: Partial<User>): User => ({...}),
  createMany: (count: number): User[] => [...],
  createAdmin: () => userFactory.create({ role: 'admin' }),
};
```
```

### Generate Test Fixtures

```
Create Playwright custom fixtures for [test scenario].

Requirements:
- Extend base test from @playwright/test
- Create page object fixtures
- Create authenticated context fixtures
- Create test data fixtures
- Handle setup and teardown properly
- Export typed test and expect

Needed fixtures:
[list specific fixtures needed]
```

### Generate API Mock Handlers

```
Create MSW handlers for [API domain] endpoints.

Endpoints:
- GET [path] - [description]
- POST [path] - [description]
- PUT [path] - [description]
- DELETE [path] - [description]

Requirements:
- Use msw v2 syntax (http, HttpResponse)
- Support query parameters and path params
- Return realistic mock data using factories
- Include error response handlers
- Add delay simulation for loading states
- Handle pagination if applicable
```

---

## 4. Debugging & Fixing

### Debug Flaky Test

```
Help me debug this flaky Playwright test. It passes sometimes but fails intermittently.

Test code:
```typescript
[paste test code]
```

Error message when it fails:
[paste error]

Failure rate: approximately [X]% of runs

Questions to answer:
1. What are potential causes of flakiness?
2. What debugging steps should I take?
3. How can I make this test more stable?
4. Are there any anti-patterns in this test?

Provide specific code fixes with explanations.
```

### Fix Selector Issues

```
Help me fix this selector that's not working reliably.

Current selector:
[paste selector]

HTML structure:
[paste relevant HTML]

Problem:
[describe what's happening]

Requirements:
- Suggest more stable selector alternatives
- Explain why each suggestion is better
- Consider accessibility best practices
- Prefer user-facing selectors
```

### Debug Authentication Issues

```
My Playwright authentication setup isn't working correctly.

Setup code:
```typescript
[paste auth setup]
```

Config:
```typescript
[paste relevant config]
```

Problem:
[describe the issue]

Expected behavior:
[what should happen]

Actual behavior:
[what's happening]

Help me fix this and explain what went wrong.
```

### Analyze Test Failure

```
Analyze this Playwright test failure and suggest fixes.

Test:
```typescript
[paste test]
```

Error:
[paste full error with stack trace]

Trace/Screenshot observations:
[describe what you see in trace]

Questions:
1. What caused this failure?
2. Is this a test issue or application bug?
3. How should I fix the test?
4. Are there any preventive measures?
```

---

## 5. Migration & Refactoring

### Migrate Cypress to Playwright

```
Convert this Cypress test to Playwright.

Cypress test:
```typescript
[paste Cypress test]
```

Requirements:
- Use Playwright syntax and APIs
- Convert cy.intercept to page.route
- Convert cy.session to storageState pattern
- Convert custom commands to fixtures or helpers
- Use Playwright's auto-waiting (remove explicit waits)
- Update assertions to Playwright's expect
- Maintain test coverage and intent

Provide the converted test with comments explaining key differences.
```

### Refactor Tests to Page Objects

```
Refactor these Playwright tests to use Page Object pattern.

Current tests:
```typescript
[paste tests with inline selectors]
```

Requirements:
- Extract page objects for each page
- Move selectors to page object locators
- Convert repeated actions to page object methods
- Update tests to use page objects
- Maintain all test assertions
- Create fixtures for page object injection
```

### Optimize Test Suite

```
Review and optimize this Playwright test suite for better performance and maintainability.

Current structure:
[describe current structure or paste code]

Issues:
- [issue 1]
- [issue 2]

Requirements:
- Identify performance bottlenecks
- Suggest parallelization strategies
- Recommend test organization improvements
- Find duplicate code to extract
- Suggest which tests can be consolidated
- Recommend tests that should be unit/integration instead
```

---

## 6. CI/CD Configuration

### Generate GitHub Actions Workflow

```
Create a GitHub Actions workflow for Playwright E2E tests.

Requirements:
- Run on push to main and PRs
- Use matrix strategy for sharding ([N] shards)
- Cache Playwright browsers
- Upload artifacts on failure (screenshots, traces, videos)
- Merge reports from all shards
- Support environment variables for secrets
- Include status badge

Additional requirements:
[any specific needs]
```

### Configure Test Parallelization

```
Help me configure optimal parallelization for my Playwright test suite.

Current situation:
- Total tests: [N]
- Average test duration: [X] seconds
- CI runners available: [N]
- CI time budget: [X] minutes

Requirements:
- Recommend shard count
- Configure worker count per shard
- Handle test dependencies if any
- Optimize for both speed and cost
- Explain tradeoffs of different configurations
```

### Set Up Test Reporting

```
Configure comprehensive test reporting for Playwright in CI.

Requirements:
- HTML report for detailed analysis
- JSON report for programmatic access
- JUnit XML for CI integration
- Slack notification on failure
- Test metrics tracking
- Historical trend analysis

Provide:
1. playwright.config.ts reporter configuration
2. CI workflow steps for report handling
3. Slack notification script/action
```

---

## 7. Best Practices Review

### Review Test Quality

```
Review this Playwright test for best practices and suggest improvements.

Test:
```typescript
[paste test]
```

Review criteria:
- Selector stability and accessibility
- Test isolation
- Proper use of waits
- Assertion quality
- Error handling
- Readability and maintainability
- Performance considerations
- Edge case coverage

Provide specific improvement suggestions with code examples.
```

### Review Page Object

```
Review this Page Object class for best practices.

Page Object:
```typescript
[paste page object]
```

Review criteria:
- Locator strategies
- Method design (single responsibility)
- Return types (navigation methods)
- Reusability
- Error handling
- Documentation
- TypeScript usage

Rate each criterion and provide improvement suggestions.
```

### Architecture Review

```
Review my E2E test architecture and suggest improvements.

Current structure:
```
[paste directory tree]
```

Key files:
[describe main files and their purposes]

Pain points:
[list current issues]

Questions:
1. Is my structure scalable?
2. How should I organize tests for [X] features?
3. Where should shared utilities live?
4. How can I improve maintainability?
5. What am I missing?
```

---

## Prompt Engineering Tips

### Be Specific About Framework

Always specify:
- Framework: Playwright vs Cypress
- Language: TypeScript vs JavaScript
- Version: If using specific features

### Provide Context

Include:
- Existing code patterns in your project
- Available page objects/utilities
- Testing conventions your team follows
- Error messages with full stack traces

### Request Explanations

Add:
- "Explain why this approach is better"
- "What are the tradeoffs?"
- "What could go wrong?"

### Iterate on Output

Common follow-ups:
- "Add error handling for [scenario]"
- "Make this work with [edge case]"
- "Optimize this for [constraint]"
- "Add TypeScript types for [part]"

---

## Example Multi-Turn Conversation

### Initial Request

```
I need to create E2E tests for a shopping cart feature. The cart has:
- Add/remove items
- Update quantities
- Apply coupon codes
- Calculate totals with tax

We use Playwright with TypeScript and have existing Page Objects for ProductsPage and CheckoutPage.
```

### Follow-up 1

```
Good start! Now add tests for these edge cases:
- Cart with 0 items
- Applying invalid coupon
- Maximum quantity limit
- Removing last item
```

### Follow-up 2

```
The tests look good. Now help me:
1. Create a data factory for cart items
2. Add API mocks for the cart endpoints
3. Create a CartPage page object for the new tests
```

### Follow-up 3

```
One test is flaky - the "apply coupon" test fails ~20% of the time with "element not visible" error. Here's the trace...

[provide details]
```

---

## Quick Reference Prompts

| Task | Key Phrases |
|------|-------------|
| Page Object | "Create Page Object", "TypeScript", "getByRole/getByTestId" |
| Test Generation | "User story", "Acceptance criteria", "Edge cases" |
| Data Factory | "faker.js", "create/createMany", "overrides" |
| Debugging | "Flaky test", "Error message", "Stack trace" |
| Migration | "Convert Cypress to Playwright", "cy.intercept to page.route" |
| CI/CD | "GitHub Actions", "Sharding", "Report merging" |
| Review | "Best practices", "Improvement suggestions", "Anti-patterns" |
