---
slug: python-pytest-parametrize
tier: free
group: dev
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: pytest.mark.parametrize: input matrices, per-case ids, stacked decorators, pytest.param for marks, indirect via fixtures.
content_id: "8446275e77fd8ff0"
complexity: light
produces: code
est_tokens: 3400
tags: [pytest, parametrize, testing, python, matrix-testing]
---
# pytest Parametrize

## Summary

**One-sentence:** pytest.mark.parametrize: input matrices, per-case ids, stacked decorators, pytest.param for marks, indirect via fixtures.

**One-paragraph:** @pytest.mark.parametrize eliminates repeated test functions by running a single test body against multiple (input, expected) pairs. Use pytest.param() for per-case marks and ids; stack decorators for cartesian products; use indirect=True to feed params through fixtures.

**Ефективно для:** інженера, який покриває валідатори / permission matrices / branching logic — закриває петлю між N майже-однаковими тестами і одним parametrized.

## Applies If (ALL must hold)

- Validation functions with many valid/invalid input cases.
- Business logic with multiple branches that need individual coverage.
- Permission matrices (role × method × expected status).
- Boundary value testing (min, max, off-by-one).

## Skip If (ANY kills it)

- Single-case test — parametrize adds noise.
- Cases share little setup but have wildly different behaviour — write separate tests.
- Cases need fixture variants only — use fixture parametrisation instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pytest installed | package | uv add --dev pytest |
| Test body with repeated structure | Python | tests/ |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-pytest-setup` | pytest config baseline. |
| `free/dev/python-developer/python-pytest-fixtures` | indirect parametrisation goes through fixtures. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: one body per parametrized matrix, ids for readability, pytest.param for per-case marks, stack for cartesian product, indirect to feed fixtures. | ~900 |
| `content/02-output-contract.xml` | essential | Shape: @pytest.mark.parametrize('a,b,expected', [pytest.param(..., id=..., marks=...), ...]) def test_x(a, b, expected). Forbidden: parametrize without ids when failure messages matter; cartesian explosion >100 cases. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: no ids, cartesian explosion, wildly different behaviour cases together, parametrize across unrelated assertions. | ~700 |
| `content/04-procedure.xml` | medium | Steps: identify repeated body → extract (input, expected) tuples → add ids → stack if matrix → use pytest.param for marks/skip. | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: ≥3 cases same body? → parametrize. Cases need different fixtures? → fixture params. Need per-case skip? → pytest.param. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `convert-to-parametrize` | sonnet | Identify common body across tests and lift parameters. |
| `add-ids` | haiku | Generate readable ids from case data. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test_parametrize.py` | Skeleton: simple parametrize, stacked decorators (cartesian), pytest.param with id+marks, indirect=True. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-pytest-parametrize.py` | Check parametrize calls have ids when 4+ cases; detect cartesian explosions. | Pre-commit. |

## Related

- [[python-pytest-setup]]
- [[python-pytest-fixtures]]

## Decision tree

The tree at content/06-decision-tree.xml decides parametrize vs separate tests, cartesian stack vs single, and pytest.param vs raw tuple. Walk it any time you write the second test with the same body.
