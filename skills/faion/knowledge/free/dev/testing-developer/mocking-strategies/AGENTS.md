# Mocking Strategies

Test doubles taxonomy and language-specific mocking: when to mock, mock boundaries, partial vs full mocking, and over-mocking detection.

## Summary

Covers the five test-double types (Dummy/Stub/Spy/Mock/Fake), decision framework for what to mock (mock at boundaries, not internals), Python `unittest.mock` / `pytest-mock`, JavaScript `vi.mock` / Jest, Go interface-based mocking, time mocking, and external API levels. Includes an over-mock linter script.

## Why

Over-mocking is a silent suite killer: tests pass but production breaks because the mocked contract drifts from reality. Under-mocking makes tests slow and non-deterministic. The boundary-based decision tree and the `autospec` / `over-mock-lint.py` tools prevent both failure modes.

## When To Use

- Deciding whether to mock a dependency or use a real one
- Writing Python mocks with `unittest.mock` / `pytest-mock`
- Writing JavaScript mocks with Vitest `vi.mock` or Jest
- Writing Go mocks via interface substitution or `mockery`
- Diagnosing "mock swallows typo" bugs (MagicMock, wrong patch target)
- Auditing a test suite for over-mocking

## When NOT To Use

- E2E tests where no mocking is desired → use `e2e-testing`
- Database isolation (use real DB with rollback) → use `test-fixtures`
- Fixture design decisions → use `test-fixtures`

## Content

| File | What it covers |
|------|---------------|
| `content/01-taxonomy.xml` | Five test-double types with definitions and when to use each |
| `content/02-boundaries.xml` | Mock at boundaries diagram, partial vs full mocking, time mocking, external API levels, decision tree |
| `content/03-language-tooling.xml` | Python unittest.mock/pytest-mock, JavaScript vi.mock/Jest, Go interface mocks; common mistakes (patch location, MagicMock typos, missing autospec) |

## Templates

| File | Purpose |
|------|---------|
| `templates/over-mock-lint.py` | Script to detect over-mocked test files in a Python project |
