# Testing (Multi-Language)

## Summary

Comprehensive testing patterns for pytest (Python), Jest/Vitest (JavaScript/TypeScript), Go's testing package, Playwright (E2E), and Cypress. Every test follows Arrange-Act-Assert. Tests are isolated, idempotent, and can run in any order. Coverage threshold: 80% branches minimum.

## Why

Untested code accumulates hidden regressions. A consistent naming convention (test_{what}_{when}_{expected}) and fixture pattern (factory or builder, not inline literals) makes tests readable and cheap to maintain as models grow. The test pyramid prevents slow E2E tests from dominating CI feedback loops.

## When To Use

- Unit testing pure functions and services with mocks for external dependencies.
- Configuring pytest, Jest, or Vitest for a new project.
- Setting up fixture factories, parametrization, and async test support.
- Implementing TDD with red-green-refactor cycles.
- Adding E2E tests with Playwright or Cypress.

## When NOT To Use

- Integration tests with real databases (see integration-testing methodology instead).
- Load and performance testing (use k6, Locust, or go test -bench=).
- Visual regression testing (use Percy or Chromatic).

## Content

| File | What's inside |
|------|---------------|
| `content/01-pytest-patterns.xml` | pytest configuration, naming conventions, fixtures (scopes, factories), parametrize, mocking, async, markers. |
| `content/02-jest-vitest-patterns.xml` | Jest/Vitest config, matchers, function/module mocks, async patterns, snapshot testing. |
| `content/03-go-patterns.xml` | Go table-driven tests, subtests, mocking via interfaces, benchmarks, fuzzing. |
| `content/04-e2e-patterns.xml` | Playwright setup, page object pattern, fixtures, API testing via request; Cypress basics. |
| `content/05-structure-and-tdd.xml` | AAA and Given-When-Then patterns, test isolation rules, TDD red-green-refactor cycle. |

## Templates

none
