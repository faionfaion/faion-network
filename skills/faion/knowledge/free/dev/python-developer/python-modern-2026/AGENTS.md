---
slug: python-modern-2026
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Python 3.12/3.13/3.14 features + uv/ruff/hatchling/pyright tooling. PEP 695 generics, t-strings (3.14), free-threaded mode.
content_id: "348d315e419eae89"
complexity: medium
produces: config
est_tokens: 3500
tags: [python-3.12, python-3.13, uv, ruff, pyright]
---
# Modern Python 2026

## Summary

**One-sentence:** Python 3.12/3.13/3.14 features + uv/ruff/hatchling/pyright tooling. PEP 695 generics, t-strings (3.14), free-threaded mode.

**One-paragraph:** Python 3.12/3.13/3.14 feature guide and tooling stack (uv, ruff, hatchling, pyright). Covers PEP 695 generics, PEP 701 f-strings, free-threaded mode (3.13t/3.14), t-strings (3.14 only), deferred annotations, and uv-based project bootstrap. Pin one Python version per repo via .python-version; keep requires-python, ruff target-version, and mypy python_version in sync.

**Ефективно для:** розробника, який бутстрапить новий проєкт або вирішує, на яку версію 3.12+ переходити — закриває петлю між фічами мови, інструментарієм uv/ruff і компат-таблицею.

## Applies If (ALL must hold)

- Bootstrapping a new Python project (uv init, pyproject.toml, ruff + mypy + pytest).
- Migrating 3.10/3.11 code to 3.12+: built-in generics, PEP 695 type parameters, modern f-strings.
- Choosing between 3.13t free-threaded vs 3.13 GIL for a workload.
- Adopting t-strings (3.14) for safe template literals.

## Skip If (ANY kills it)

- Stuck on 3.10/3.11 due to platform constraints (legacy CI, old AWS Lambda).
- Pure data-science notebooks where conda manages the env.
- Library that must support 3.9 — load python-basics instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| uv 0.4+ installed | binary | curl -LsSf https://astral.sh/uv/install.sh |
| pyproject.toml or empty dir | TOML | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-basics` | Foundational syntax and idioms this builds on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pin one Python via .python-version, sync target-versions, PEP 695 type params, free-threaded only for CPU + pure-Python, uv as the one package manager. | ~900 |
| `content/02-output-contract.xml` | essential | Shape: pyproject.toml [project] requires-python + .python-version + uv.lock + [tool.ruff] target-version + [tool.mypy] python_version. Forbidden: pip + poetry + uv coexisting. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: target-version drift, free-threaded for C-ext heavy stack, multiple package managers, t-strings on 3.13. | ~700 |
| `content/04-procedure.xml` | medium | Steps: uv init → pin Python → sync target-versions → adopt PEP 695 generics → decide free-threaded. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: pure Python + CPU-bound? → consider 3.13t. C-ext heavy? → stay GIL. Need t-strings? → 3.14+. Else: 3.13 default. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bootstrap-project` | haiku | uv init template fill. |
| `audit-version-drift` | sonnet | Cross-check requires-python ↔ ruff target ↔ mypy python_version. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Complete pyproject for 3.13: [project], [tool.uv], [tool.ruff], [tool.mypy], [tool.pytest.ini_options]. |
| `templates/.python-version` | Single Python version pin file. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-modern-2026.py` | Validate target-version sync across requires-python, ruff target-version, mypy python_version, .python-version. | Pre-commit. |

## Related

- [[python-basics]]
- [[python-code-quality]]
- [[python-poetry-setup]]

## Decision tree

The tree at content/06-decision-tree.xml decides Python version (3.12 / 3.13 / 3.13t / 3.14), package manager (uv only), and PEP-695 vs legacy generics. Walk it whenever a new repo is created or a version bump is considered.
