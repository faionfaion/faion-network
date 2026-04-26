# Mocking Strategies

## Summary

Test doubles (stubs, mocks, spies, fakes) isolate code under test from external dependencies. Use the
smallest double that validates the required behavior: fake for repository abstractions, stub for state
return values, mock only when the call itself is part of the contract, spy to wrap real objects.

## Why

Tests that reach real databases, HTTP services, clocks, or random sources are slow, flaky, and
environment-dependent. Test doubles replace these collaborators with deterministic stand-ins.
Choosing the wrong double (e.g., mocking everything) produces tests that pass even when the
production code is broken — mutation testing reveals this. Mock only at architectural seams.

## When To Use

- Isolating unit tests from databases, HTTP services, filesystems, clocks, or randomness
- Testing error handling and edge cases by controlling what a dependency returns
- Verifying that a specific interaction (e.g., email sent on order placement) occurred
- Replacing slow I/O with instant in-memory fakes for the service layer
- Writing characterization tests around legacy code by stubbing its dependencies

## When NOT To Use

- Integration tests that should hit a real DB/queue/cache — use Testcontainers instead
- Pure functions — they need no mocks; mocking their inputs reveals a design smell
- Tests of the boundary itself (the HTTP client, the SQL layer) — test against real or VCR-recorded backend
- End-to-end tests — should exercise real services in a controlled environment
- When a 30-line `FakeRepository` is cheaper to maintain than setting up mocks per test

## Content

| File | What's inside |
|------|---------------|
| `content/01-test-doubles.xml` | Five double types (dummy/stub/mock/spy/fake) with Python and TypeScript examples |
| `content/02-patching.xml` | `@patch`, `patch.object`, `patch.dict`, `AsyncMock`, common pitfalls |
| `content/03-antipatterns.xml` | Over-mocking, wrong-layer patching, non-spec mocks, async confusion |

## Templates

| File | Purpose |
|------|---------|
| `templates/fake-repository.py` | In-memory fake repository implementing an ABC interface |
| `templates/over-mock-lint.py` | Script: flags test functions with too many `assert_called` (over-mocking detector) |
| `templates/prompt-choose-double.txt` | Two-step prompt: classify collaborators then generate test using the right double |
