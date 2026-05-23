# Mocking Strategies (test doubles)

## Summary

**One-sentence:** Produces a test-double decision (dummy/stub/spy/mock/fake) and patch-target choice that validates the required behavior without over-specifying interaction, using AsyncMock for async and patching where the name is looked up.

**One-paragraph:** Choose the smallest double that validates the required behavior: `dummy` for unused params, `stub` for state-returning collaborators, `spy` for wrapping real objects, `mock` only when the call itself is part of the contract, `fake` for full working replacements (in-memory repository, file system). Patch where the name is looked up (`module_a.function_b` if module_a imports it), not where it is defined. Use `AsyncMock` for `async def` functions. Keep mock setup in fixtures; assertions in tests. More than 5 lines of inline mock setup is a smell.

**Ефективно для:** unit tests with collaborators, tests that broke because mocks tightly coupled to implementation, fast-test design where real dependencies are expensive, fixing AsyncMock-vs-Mock confusion.

## Applies If (ALL must hold)

- Code under test has at least one collaborator (HTTP client, DB, file system, time).
- Tests should run in milliseconds (no real I/O).
- Team accepts the dummy/stub/spy/mock/fake taxonomy.
- Test framework supports either pytest mock / unittest.mock / sinon / vitest.

## Skip If (ANY kills it)

- Integration tests where real collaborators are intentional (see `[[integration-testing]]`).
- Code with no collaborators (pure function).
- E2E tests where you mock at network boundary (use MSW / page.route).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Code under test | filename | repo |
| Collaborator list | bullet list | code |
| Language test framework | string | tech stack |
| Sync vs async | boolean | function signature |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[integration-testing]]` | Boundary between when to mock and when to use real. |
| `[[e2e-testing]]` | Network-level mocking via MSW/page.route. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: smallest-double, patch where looked up, AsyncMock for async, fixtures for setup, fakes for repositories | ~600 |
| `content/02-output-contract.xml` | essential | Schema for a double-choice record + valid/invalid examples | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: over-mocking, patch wrong target, Mock for async, inline setup bloat | ~600 |
| `content/05-examples.xml` | light | Two worked examples: stub + fake | ~500 |
| `content/06-decision-tree.xml` | essential | Root: "Is the call's existence part of the contract?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pick double type | sonnet | Pattern-match on intent. |
| Patch-target resolution | sonnet | Imports analysis. |
| Refactor over-mocked test | opus | Multi-step reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fake-repository.py` | Drop-in in-memory fake repository implementing the same interface. |
| `templates/over-mock-lint.py` | Lint script flagging tests with >5 lines of mock setup. |
| `templates/prompt-choose-double.txt` | Prompt for sub-agent picking a double type. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mocking-strategies.py` | Validates a choice record and flags Mock used for async def + wrong patch target. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[integration-testing]]` — when to keep dependencies real
- `[[e2e-testing]]` — network-boundary mocking with MSW

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters by: contract requires the call, state suffices, real impl too expensive — and routes to the right double.
