---
slug: python-pytest-setup
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: pytest config + plugin set + coverage gate + parallel CI + agentic TDD loop.
content_id: "aabf85df9e38e31e"
complexity: medium
produces: config
est_tokens: 4000
tags: [pytest, configuration, ci, coverage, python]
---
# pytest Project Setup

## Summary

**One-sentence:** pytest config + plugin set + coverage gate + parallel CI + agentic TDD loop.

**One-paragraph:** Wire pytest into a Python project: install the essential plugin set (pytest-cov, pytest-xdist, pytest-mock, pytest-asyncio when async), configure pyproject.toml [tool.pytest.ini_options] with strict markers and coverage gates, structure tests/ to mirror src/, add parallel execution for CI, and follow the agentic TDD loop for feature development.

**Ефективно для:** інженера, який ставить pytest на новий проєкт — закриває петлю між пустим репо і робочим test gate з coverage + xdist + strict-markers + правильною структурою.

## Applies If (ALL must hold)

- New Python project — wire pytest as the only test runner.
- Migrating from unittest.TestCase — keep tests running, add new tests pytest-style.
- Adding coverage gates and parallel CI to an existing repo.
- Standardising plugin set across multiple repos.

## Skip If (ANY kills it)

- Project already has a working pytest gate — load python-pytest-fixtures or python-pytest-parametrize instead.
- Pure script with no tests planned.
- Notebook-only project (use nbval).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pyproject.toml | TOML | repo root |
| src/ + tests/ layout | directory | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-modern-2026` | Defines target Python version and uv tooling. |
| `free/dev/python-developer/python-code-quality` | Pre-commit gate where pytest plugs in. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: pytest as only runner, strict-markers, tests mirror src layout, coverage gate ≥80%, pytest-xdist for CI, agentic TDD loop. | ~1100 |
| `content/02-output-contract.xml` | essential | Shape: pyproject [tool.pytest.ini_options] + [tool.coverage.*] + tests/ mirroring src/. Forbidden: setup.cfg config, no --strict-markers, tests outside tests/. | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: no strict-markers, tests next to src, coverage threshold = 0, xdist with shared state, unittest.TestCase for new code. | ~800 |
| `content/04-procedure.xml` | medium | Steps: install plugins → write pyproject config → set up tests/ structure → write first failing test → add coverage gate → add CI matrix. | ~800 |
| `content/06-decision-tree.xml` | essential | Tree: new project? → full setup. Migrating unittest? → keep running, add pytest. Adding to existing? → reuse config. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-pytest-config` | haiku | Template fill. |
| `wire-coverage-ci` | sonnet | Tuning thresholds and exclusions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml.fragment` | Complete pytest config: ini_options, coverage, markers. |
| `templates/tests-structure.txt` | Reference tree showing tests/ mirroring src/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-pytest-setup.py` | Check strict-markers, coverage threshold > 0, no setup.cfg test config. | Pre-commit. |

## Related

- [[python-pytest-fixtures]]
- [[python-pytest-mocking]]
- [[python-pytest-parametrize]]
- [[python-pytest-async]]
- [[python-code-quality]]

## Decision tree

The tree at content/06-decision-tree.xml triages new vs migration vs extension and picks the plugin set + coverage strategy. Walk it before editing pyproject's [tool.pytest.ini_options].
