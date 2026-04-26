# Testing Patterns

Proven structural and data patterns for writing maintainable, reliable tests — applicable across Python, TypeScript, and Go. Covers test structure (AAA/GWT), data creation (Builder/Object Mother), test doubles, architecture strategy (pyramid), UI patterns (POM), isolation, and property-based testing.

## Why

Tests without a consistent structure are hard to debug, slow down CI when the wrong layer is over-tested, and drift toward false positives. These patterns solve the recurring problems: unclear failure points, tightly-coupled test data, shared mutable state, and brittle selectors.

## When To Use

- Establishing or reviewing a test strategy for a new project
- Refactoring tangled tests that are hard to maintain
- Adding test coverage to a module with complex data setup
- Building E2E test suites that need to survive UI churn
- Choosing between test double types (mock vs stub vs fake)

## When NOT To Use

- Trivial one-off scripts with no business logic
- Pure data-transformation functions with no branches — just use direct assertions

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | AAA and Given-When-Then patterns with Python/JS/Go examples |
| `content/02-data.xml` | Test Data Builder (fluent API), Object Mother, combined pattern |
| `content/03-doubles.xml` | Five test double types, decision table, mock-vs-stub distinction |
| `content/04-architecture.xml` | Test Pyramid (70/20/10), Testing Trophy, ice cream cone antipattern, flaky test prevention |
| `content/05-advanced.xml` | Page Object Model structure and antipatterns, property-based testing, isolation strategies |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity-builder.ts` | TypeScript fluent builder for domain entities |
| `templates/object-mother.ts` | TypeScript Object Mother returning builders |
| `templates/login-page.ts` | Playwright Page Object Model (BasePage + LoginPage + DashboardPage) |
| `templates/playwright-fixtures.ts` | Playwright custom fixture extension with pre-authenticated page |
