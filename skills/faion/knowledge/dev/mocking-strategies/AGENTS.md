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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/fake-repository.py`

```python
"""
Fake in-memory repository implementing a UserRepository ABC.
Use in unit tests instead of a database.
Reset state between tests via fake_repo.clear() or a fresh fixture.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from uuid import uuid4


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: "User") -> "User": ...

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional["User"]: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional["User"]: ...


class FakeUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: Dict[str, "User"] = {}
        self.email_index: Dict[str, str] = {}

    def save(self, user: "User") -> "User":
        if not getattr(user, "id", None):
            user.id = str(uuid4())
        self.users[user.id] = user
        self.email_index[user.email] = user.id
        return user

    def find_by_id(self, user_id: str) -> Optional["User"]:
        return self.users.get(user_id)

    def find_by_email(self, email: str) -> Optional["User"]:
        uid = self.email_index.get(email)
        return self.users.get(uid) if uid else None

    def clear(self) -> None:
        self.users.clear()
        self.email_index.clear()
```

### `templates/over-mock-lint.py`

```python
"""
Over-mock detector: flags test functions with too many assert_called* calls.
Input:  tests/ directory (recursive scan of test_*.py files)
Output: stdout listing offenders; exits 1 if any found
Usage:  python over-mock-lint.py [threshold]
"""
import ast
import pathlib
import sys

THRESHOLD = int(sys.argv[1]) if len(sys.argv) > 1 else 4
issues = 0

for path in pathlib.Path("tests").rglob("test_*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            asserts = sum(
                1
                for child in ast.walk(node)
                if isinstance(child, ast.Attribute)
                and child.attr.startswith("assert_called")
            )
            if asserts > THRESHOLD:
                print(
                    f"{path}:{node.lineno} {node.name} "
                    f"has {asserts} call assertions (threshold {THRESHOLD})"
                )
                issues += 1

sys.exit(1 if issues else 0)
```

### `templates/prompt-choose-double.txt`

```text
Goal: write tests for <module>.<function>.

Step 1: List every external collaborator of <function> (databases, HTTP clients, email services,
clocks, random sources). Classify each as:
  pure        — no side effects, no external state
  stub        — needs to return canned data
  fake        — needs a working in-memory implementation
  mock        — the call itself is part of the contract (must be verified)
  integration — should hit the real service (do NOT mock)

Step 2: For each non-pure collaborator, propose the smallest double:
  prefer fake > stub > mock.

Step 3: Emit a pytest test file using the chosen doubles.
  - Use pytest-mock `mocker` fixture, NOT raw @patch decorators.
  - Do NOT mock the function under test.
  - Do NOT mock dataclasses or Pydantic models.
  - Do NOT verify internal helper calls — only contract-level interactions.
  - Each test asserts on observable behavior (return value, raised exception, side effect).
```
