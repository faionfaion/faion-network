---
slug: python-pytest-mocking
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: pytest-mock: mocker fixture, autospec, spy, AsyncMock — auto-cleanup patches without try/finally.
content_id: "2b24d0d7cdeb405d"
complexity: medium
produces: code
est_tokens: 3700
tags: [pytest, mocking, testing, python, pytest-mock]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-pytest-mocking.py` | Check imports avoid unittest.mock directly, mocks specify autospec, ORM not patched. | Pre-commit. |

## Related

- [[python-pytest-setup]]
- [[python-pytest-fixtures]]
- [[python-pytest-async]]

## Decision tree

The tree at content/06-decision-tree.xml routes between mock, AsyncMock, spy, and 'do not mock'. Walk it before patching anything.
