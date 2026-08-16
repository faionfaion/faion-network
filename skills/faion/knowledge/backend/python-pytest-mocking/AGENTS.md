# pytest Mocking

## Summary

**One-sentence:** pytest-mock: mocker fixture, autospec, spy, AsyncMock — auto-cleanup patches without try/finally.

**One-paragraph:** Use pytest-mock's mocker fixture instead of unittest.mock directly. The mocker fixture auto-cleans patches after each test, supports autospec for signature validation, provides AsyncMock for async callables, and exposes a spy() helper that calls through to the real implementation while recording calls.

**Ефективно для:** інженера, який ізолює юніт від мережі/диску/часу — закриває петлю між повторним boilerplate patch/start/stop і чистими mocker-фікстурами.

## Applies If (ALL must hold)

- Isolating a unit from external dependencies: HTTP APIs, email services, databases, file systems.
- Testing error paths that are hard to trigger naturally: network timeouts, disk full, auth failures.
- Validating call signatures with autospec.
- Spying on real implementations while recording call arguments.

## Skip If (ANY kills it)

- Pure functions with no external dependencies — call them directly.
- Integration tests where the real service is the point.
- Mocking the ORM (anti-pattern; use real DB fixtures with rollback).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pytest-mock installed | package | uv add --dev pytest-mock |
| Unit under test with external deps | Python | src/ |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-pytest-setup` | pytest config baseline. |
| `free/dev/python-developer/python-pytest-fixtures` | mocker is itself a fixture; understanding fixtures is required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: mocker over unittest.mock, patch the use site, autospec for signature, AsyncMock for async, spy when behaviour matters, never mock the ORM. | ~1000 |
| `content/02-output-contract.xml` | essential | Shape: mocker.patch('module.use_site.name'), autospec=True or new=AsyncMock; assert_called_once_with on the mock. Forbidden: from unittest.mock import patch; mock without autospec. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: patch-define-site, MagicMock for async, no autospec, over-mocking the ORM, asserting on the wrong attribute. | ~800 |
| `content/04-procedure.xml` | medium | Steps: identify boundary → pick patch target (use site) → use mocker with autospec or AsyncMock → assert calls → spy when real impl is desired. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: external I/O? → mock. Async? → AsyncMock. Want real behaviour + records? → spy. ORM? → don't mock. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-boundary` | sonnet | Pick the use-site for patching. |
| `scaffold-mocks` | haiku | Template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test_with_mocks.py` | Test skeleton: mocker.patch + autospec + AsyncMock + spy examples. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-pytest-mocking.py` | Check imports avoid unittest.mock directly, mocks specify autospec, ORM not patched. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[python-pytest-setup]]
- [[python-pytest-fixtures]]
- [[python-pytest-async]]

## Decision tree

The tree at content/06-decision-tree.xml routes between mock, AsyncMock, spy, and 'do not mock'. Walk it before patching anything.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/test_with_mocks.py`

```python
"""

from unittest.mock import AsyncMock


def test_mocker_patches_use_site(mocker):
    mock_send = mocker.patch(
        "apps.orders.services.send_mail", autospec=True
    )
    from apps.orders.services import confirm_order

    confirm_order(order_id=1)
    mock_send.assert_called_once()


async def test_async_callable_uses_asyncmock(mocker):
    mock_fetch = mocker.patch(
        "apps.users.services.fetch_profile",
        new=AsyncMock(return_value={"id": 1}),
    )
    from apps.users.services import load_user

    result = await load_user(1)
    assert result == {"id": 1}
    mock_fetch.assert_awaited_once_with(1)
```
