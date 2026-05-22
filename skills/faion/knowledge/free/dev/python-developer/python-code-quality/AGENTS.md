---
slug: python-code-quality
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Ruff + mypy + pytest-cov + bandit + pre-commit toolchain for Python 2026.
content_id: "27c7e1be1a30850c"
complexity: medium
produces: config
est_tokens: 3900
tags: [code-quality, linting, type-checking, ruff, mypy]
---
# Python Code Quality

## Summary

**One-sentence:** Ruff + mypy + pytest-cov + bandit + pre-commit toolchain for Python 2026.

**One-paragraph:** Modern Python code-quality toolchain centred on Ruff (lint + format in one tool, 10–100x faster than Black + isort + flake8), mypy/pyright for type checking, pytest-cov for coverage gates, bandit for security scanning, and pre-commit hooks as the canonical gate. Replaces the legacy Black + isort + flake8 + autoflake + pyupgrade stack with a single config.

**Ефективно для:** розробника, який ставить lint/format/type/cov-гейт на новому репо або мігрує застарілий стек на Ruff — закриває петлю між якістю і швидкістю CI.

## Applies If (ALL must hold)

- Setting up the lint + format + type-check + security gate on a new Python repo.
- Migrating a legacy repo off flake8 + black + isort + autoflake + pyupgrade to Ruff.
- Adding mypy/pyright strict mode incrementally to a partially typed codebase.
- Wiring pre-commit hooks to fail fast on style and type violations.

## Skip If (ANY kills it)

- One-off scripts that will never be merged.
- Pure data-science notebooks where format is enforced by nbqa separately.
- Vendored third-party code under a vendor/ directory.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pyproject.toml | TOML | repo root |
| Existing test suite or scaffolding | Python | tests/ |
| pre-commit installed | package | uv add --dev pre-commit |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-modern-2026` | Toolchain baseline (uv, ruff, target Python version). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: Ruff replaces Black+isort+flake8, mypy/pyright strict at boundary, pytest-cov gate, bandit on every commit, pre-commit canonical gate, sync target-version across tools. | ~1000 |
| `content/02-output-contract.xml` | essential | Output: pyproject [tool.ruff] + [tool.mypy] + [tool.pytest.ini_options] + .pre-commit-config.yaml. Forbidden: separate black/isort configs, mypy ignore-missing-imports global, --no-verify in CI. | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: black+ruff coexisting, --no-verify shortcut, ignore-missing-imports global, coverage threshold = 0, bandit skipped. | ~800 |
| `content/04-procedure.xml` | medium | Steps: drop legacy tools → add Ruff config → add mypy strict → add coverage gate → add bandit → wire pre-commit → wire CI. | ~800 |
| `content/06-decision-tree.xml` | essential | Tree: greenfield → full Ruff + mypy strict; legacy → migrate per directory; library → strict + py.typed; app → strict at boundaries. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Template fill. |
| `migrate-legacy-stack` | sonnet | Per-rule mapping black/isort/flake8 → Ruff with judgement on noqa survivors. |
| `audit-quality-gates` | opus | Cross-cutting: detect skip-patterns, gate bypasses, drift. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml.fragment` | Full [tool.ruff] + [tool.mypy] + [tool.pytest.ini_options] config. |
| `templates/.pre-commit-config.yaml` | Pre-commit hooks: ruff, ruff-format, mypy, pytest, bandit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-code-quality.py` | Verify Ruff config presence, mypy strict, pre-commit hooks installed, coverage threshold > 0. | Pre-commit and weekly drift scan. |

## Related

- [[python-modern-2026]]
- [[python-basics]]
- [[python-type-hints]]

## Decision tree

The tree at content/06-decision-tree.xml decides Ruff-only vs Ruff+legacy, mypy strict vs gradual, and library vs application gating. Walk it before editing any [tool.*] block in pyproject.
