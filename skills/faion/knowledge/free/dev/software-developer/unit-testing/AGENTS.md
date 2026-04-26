# Unit Testing

## Summary

A methodology for writing isolated, deterministic tests that verify a single behavior per test using the Arrange-Act-Assert pattern. Each test names its scenario explicitly (`test_<behavior>_when_<context>`), uses fixtures or fakes for setup, and mocks only at process boundaries (network, disk, clock).

## Why

Tests written without this discipline rot quickly: naming collisions, shared mutable state, and deep mocking make suites brittle — tests pass even when production behavior breaks. The AAA pattern separates concerns, the naming convention makes failures self-documenting, and the mock-at-boundary rule ensures fakes exercise real contracts rather than verify their own setup.

## When To Use

- New code with branching logic, math, parsing, validation, or state transitions.
- Refactoring legacy code — safety net before changing internals.
- Bug fixes — write the failing test first, then fix.
- Boundary cases: empty inputs, min/max, off-by-one, unicode, time zones.
- TDD workflow: spec → failing test → impl → green → refactor.

## When NOT To Use

- Pure plumbing (controller → service → repo) — integration test is more honest.
- UI rendering — visual regression or snapshot tests catch more; unit tests on JSX are brittle.
- Network protocols, DB-specific queries, cache eviction — needs real dependency.
- Code ≤5 lines that is trivially correct (`return a + b`).
- High-churn experimental / spike code — tests rot faster than the code; defer.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | AAA pattern, naming convention, isolation rules, fixture guidance |
| `content/02-examples.xml` | Python pytest examples: AAA, parametrize, exceptions, fixtures, async, test doubles |
| `content/03-antipatterns.xml` | Antipatterns: implementation-detail tests, over-mocking, shared state, flaky tests |

## Templates

| File | Purpose |
|------|---------|
| `templates/pytest-runner.sh` | Fast feedback loop script: pytest with markers, deduplication, duration report |
| `templates/pyproject-markers.toml` | pytest markers config: slow, integration, e2e, strict-markers |
