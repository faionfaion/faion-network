---
slug: django-pytest-parametrize
tier: free
group: dev
domain: python-developer
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a parametrize spec (validation matrices, permission grids, error-code tables) with descriptive IDs, valid-payload base, and group-by-category splits.
content_id: "47be71f59279d880"
complexity: light
produces: spec
est_tokens: 3200
tags: [django, pytest, parametrize, validation-matrix, permission-grid]
---

# Django pytest Parametrize

## Summary

**One-sentence:** Produces a parametrize spec naming the validation matrices, permission grids, and error-code tables — each with descriptive IDs, valid-payload base, and split-by-category to keep parameter lists below ~20 rows.

**Ефективно для:** Test suites where 12 near-identical tests differ only in (field, bad_value, expected_error), where pytest output reads `[0] [1] [2]` instead of `[email-invalid] [password-short]`.

**One-paragraph:** Codifies "when do we parametrize and how?" into one spec. Output names each parametrize block (test function + argnames + cases + IDs). Forbids: parameter lists &gt; 20 rows (split by category), model-instance parameters (use IDs + factories), generic auto-numeric IDs, mixed control-flow variations under one parametrize.

## Applies If (ALL must hold)

- Django ≥ 5.0 + pytest-django.
- The test under consideration has ≥ 3 near-identical bodies that differ only in data.
- Parameter cases are independent (no shared mutable state).
- Cases share setup, teardown, and assertion logic.
- Output drives test refactor or codegen.

## Skip If (ANY kills it)

- Cases need substantially different setup/teardown — separate test functions.
- &gt; 20 cases — split into category-named test functions.
- Cases differ in control flow, not just data.
- One-off test that isn't repeated anywhere — don't parametrize.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Group of near-identical tests | code refs | grep |
| Per-case (input, expected) data | bullets | spec / domain rules |
| Valid baseline payload (for matrix tests) | YAML | API contract |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-pytest-integration]]` | Endpoint matrix consumed by validation parametrize. |
| `[[django-pytest-fixtures]]` | api_client / authenticated_client used inside parametrize. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 4 testable rules: parametrize semantics, three-tuple matrix, refactor threshold, fixture switching via getfixturevalue | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the parametrize spec | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: huge parameter lists, model-instance params, generic IDs | ~700 |
| `content/06-decision-tree.xml` | essential | Per group of tests: refactor or keep? matrix shape? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `find_redundant_tests` | haiku | Mechanical grep. |
| `emit_parametrize_spec` | sonnet | Bounded transformation. |

## Templates

| File | Purpose |
|---|---|
| `templates/parametrize-spec.json` | Reference output. |
| `templates/test_validation_matrix.py` | Reference (field, value, error) matrix test. |
| `templates/test_role_grid.py` | Reference role/permission grid test. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-parametrize.py` | Validate the parametrize spec JSON. | After spec emission. |

## Related

- [[django-pytest-integration]] — endpoint matrix consumed here.
- [[django-pytest-fixtures]] — client fixtures used inside parametrize.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per redundant test group: ≥ 3 bodies, same shape, only data differs → parametrize. &gt; 20 cases → split by category. Parameters include model instances → replace with IDs + factory lookup inside the test.
