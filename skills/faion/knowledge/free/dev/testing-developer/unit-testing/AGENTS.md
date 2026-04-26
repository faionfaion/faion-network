# Unit Testing

Core unit test principles: FIRST, AAA pattern, naming conventions, coverage strategies, and anti-patterns.

## Summary

Covers the FIRST properties (Fast/Isolated/Repeatable/Self-validating/Timely), Arrange-Act-Assert structure, test naming conventions (method-scenario-expected, should-when, given-when-then), coverage strategies (line vs branch vs mutation), test categories, and the most damaging anti-patterns (testing implementation, not behavior).

## Why

Unit tests are the foundation of every test pyramid. Without consistent structure and naming, suites become maintenance burdens: tests that pass for wrong reasons, fail for infrastructure reasons, or describe nothing useful in their names. FIRST + AAA enforces a minimal discipline that scales.

## When To Use

- Writing the first unit tests for a function, method, or class
- Reviewing unit test quality (FIRST compliance, AAA structure, naming)
- Choosing a coverage strategy for a new module
- Identifying test anti-patterns: testing internals, slow unit tests, non-isolated fixtures
- Onboarding new developers to the project test style

## When NOT To Use

- pytest-specific features (fixtures, parametrize) → use `testing-pytest`
- Mocking strategy decisions → use `mocking-strategies`
- E2E tests → use `e2e-testing`
- Test fixture design → use `test-fixtures`

## Content

| File | What it covers |
|------|---------------|
| `content/01-principles.xml` | FIRST properties, AAA pattern, test naming conventions, self-documenting test structure |
| `content/02-coverage.xml` | Line vs branch vs mutation coverage, coverage targets by module type, when coverage misleads |
| `content/03-antipatterns.xml` | Testing implementation details, flaky assertions, excessive mocking, slow unit tests, non-isolated state |
