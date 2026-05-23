<!--
purpose: side-by-side rename rubric for a single Pydantic / JSON Schema review pass
consumes: pydantic model file or JSON Schema dump
produces: markdown table + JSON report matching 02-output-contract schema
depends-on: Pydantic >= 2.5 OR raw JSON Schema; an eval set with >= 5 rows
token-budget-impact: ~600 tokens to render; output JSON ~150 tokens per rename
-->

# Semantic Field Rename Rubric — `<model_path>`

Schema version: `<old>` → `<new>` (bump on every non-empty rename set).

## Renames

| Field path | Old name | New name | Reason code | Rationale |
|---|---|---|---|---|
| `Order.flag` | `flag` | `is_paid` | `missing-direction` | Boolean without `is_/has_` prefix; True/False ambiguous to model and downstream code. |
| `Order.total` | `total` | `total_cents` | `missing-unit` | Float dollars drifted between cents and dollars in production traces. |
| `Story.text` | `text` | `body_markdown` | `generic-placeholder` | Generic `text` does not encode the format constraint; model emitted plain text instead of Markdown. |

Reason codes (closed enum): `generic-placeholder`, `missing-unit`, `missing-direction`, `redundant-suffix`, `non-english`, `cardinality-mismatch`, `cryptic-enum`.

## Kept (passed audit)

- `Order.customer_id` — already specific; UUID encoded by type.
- `Order.created_at_iso` — format already in name.

## A/B accuracy check

- Eval set: `evals/<feature>/gold.jsonl`, rows: `<N>`.
- Baseline (old names): `<baseline_accuracy>` (0.0..1.0).
- After rename: `<renamed_accuracy>`.
- Delta: `<delta_points>` absolute points.

## Migration notes

- External API contract: preserved via `validation_alias` on the renamed fields if any downstream system sends the old key.
- `ConfigDict(extra="forbid")` retained.
- `schema_version` bumped from `<old>` to `<new>` in `pyproject.toml` / `__init__.py`.
