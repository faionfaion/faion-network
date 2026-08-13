# Strict-Mode Schemas: Required-Everything + No Additional Properties

## Summary

**One-sentence:** Strict-mode structured outputs compile the schema into a finite-state grammar that rejects optional fields and unknown properties.

**One-paragraph:** Produces a Pydantic 2 model (and the JSON Schema it emits) that satisfies the OpenAI Responses / Chat-Completions `strict: true` compiler: every property declared on every object is listed in `required`, every object sets `additionalProperties: false`, and optional semantics are encoded by `T | None = None` (nullable type, still required). Applies identically to Anthropic tool-use input schemas, Azure OpenAI strict mode, and Gemini `responseSchema` with strict enforcement.

**Ефективно для:** будь-якого Pydantic / JSON-Schema коду, що йде в OpenAI Responses API з `response_format={type: "json_schema", strict: true}` або Anthropic tool-use, і ламається з помилкою `400 additionalProperties must be false when strict is true`.

## Applies If (ALL must hold)

- A structured-output call uses strict mode: OpenAI `response_format={type: "json_schema", strict: true}`, Anthropic tool-use, Azure parse API, or Gemini `responseSchema` with strict.
- Schema is generated from Pydantic 2 (or hand-rolled JSON Schema) and owned by the team.
- The team can tolerate the model emitting `null` for fields that are conceptually optional.
- A CI step can be added to assert the emitted schema against `assert_strict_schema()`.

## Skip If (ANY kills it)

- Local Outlines / XGrammar pipelines that support standard JSON-Schema optional fields natively — required-everything wastes tokens for no grammar gain.
- Loose JSON mode (`response_format={type: "json_object"}`) — there is no grammar; strict-mode rules do not apply.
- Schemas intentionally accept arbitrary additional properties (metadata bags) — strict mode is the wrong tool; split into typed sub-object + audit field.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Pydantic model file | `*.py` | `models/`, `schemas/` |
| Schema dump | JSON Schema produced by `Model.model_json_schema()` | one-liner CLI |
| Strict-mode target | `openai` / `anthropic` / `azure` / `gemini` | runtime config |
| Failure log (if any) | `400` body from the provider | provider error response |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/structured-output-mode-picker` | Confirms strict mode is the right pick for this call. |
| `geek/ai/ai-agents/semantic-field-naming` | Rename before adding strict constraints; the two are paired. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: required-everything, additionalProperties:false, nullable-not-optional, CI assertion, ConfigDict(extra="forbid") | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the strict-mode audit report: model path, violations, fix patches | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: empty-string sentinel, missing required, missing additionalProperties, nullable int-money, metadata-bag-in-strict | ~700 |
| `content/04-procedure.xml` | medium | Migrate Pydantic to strict: scan → add `extra="forbid"` → convert Optional[X] to `X | None` → assert → ship | ~800 |
| `content/06-decision-tree.xml` | essential | Picks the encoding (nullable / split-bag / drop-strict) per field shape | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scan model for strict-mode violations | sonnet | Mechanical AST walk. |
| Convert legacy Optional[X] → X | None | sonnet | Refactor mechanic. |
| Decide whether a metadata bag should stay or split | opus | Modeling judgement. |
| Generate the `assert_strict_schema` CI test | sonnet | Boilerplate code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/strict_pydantic.py` | Reference Pydantic 2 model with `ConfigDict(extra="forbid")`, nullable fields, and an `assert_strict_schema()` helper that walks the emitted schema. |
| `templates/strict.schema.json` | Equivalent hand-rolled JSON Schema that passes the OpenAI strict-mode compiler. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strict-mode-required-fields.py` | Validates the strict-mode audit report against the `02-output-contract.xml` schema. | After running the audit pass, before opening the migration PR. |

## Related

- [[semantic-field-naming]] — pair rename + strict encoding in the same PR.
- [[structured-output-mode-picker]] — decides whether strict mode is even the right pick.
- [[refusal-field-strict-schema]] — companion rule for refusal handling under strict mode.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the encoding from the field's logical role: hard-required scalar → keep as `T`; sometimes-absent scalar → `T | None = None` (nullable, still required); arbitrary metadata bag → split into typed sub-object + separate audit field; field that can never be present (deprecation) → remove from schema entirely. Use it whenever the question is "how do I express optional under strict mode without violating the FSM-grammar invariant".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/strict_pydantic.py`

```python
"""Pydantic template for OpenAI/Azure strict-mode structured outputs.

Key rules wired in:
  - `model_config = ConfigDict(extra="forbid")` -> additionalProperties: false
  - Every property is in `required` (Pydantic emits this automatically when
    every field is declared, including `T | None` ones with a default).
  - Optionality is encoded as `T | None`, not as a missing field.

Smoke check before shipping:

    from json import dumps
    print(dumps(Invoice.model_json_schema(), indent=2))
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sku: str
    quantity: int
    unit_price_usd: str = Field(
        pattern=r"^\d+\.\d{2}$",
        description="USD price as decimal string e.g. '19.99'.",
    )


class Invoice(BaseModel):
    """Strict-mode-compatible invoice extraction shape."""

    model_config = ConfigDict(extra="forbid")
    invoice_id: str
    issue_date: str = Field(
        description="ISO-8601 YYYY-MM-DD. If only month/year shown, use day=01.",
    )
    currency: Literal["USD", "EUR", "GBP"]
    items: list[LineItem]
    notes: str | None = Field(default=None, description="Free-form note or null.")


def assert_strict_schema(model: type[BaseModel]) -> None:
    """Walk the emitted schema and assert it satisfies strict-mode rules."""
    schema = model.model_json_schema()

    def _check(node: dict) -> None:
        if node.get("type") == "object" and "properties" in node:
            assert node.get("additionalProperties") is False, (
                f"missing additionalProperties:false in {node.get('title')}"
            )
            props = set(node["properties"].keys())
            req = set(node.get("required", []))
            assert props == req, (
                f"required != properties in {node.get('title')}: "
                f"missing={props - req}"
            )
        for value in node.values():
            if isinstance(value, dict):
                _check(value)

    _check(schema)
    for defn in schema.get("$defs", {}).values():
        _check(defn)
```

### `templates/strict.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$comment": "purpose: hand-rolled JSON Schema that passes the OpenAI strict-mode compiler\nconsumes: nothing (this IS the schema artifact)\nproduces: strict-mode-submittable response_format JSON\ndepends-on: openai >= 1.50, Azure 2024-08+ parse API, Anthropic tool-use 2026-03+\ntoken-budget-impact: ~250 tokens to render verbatim in agent context",
  "title": "Invoice",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "invoice_id",
    "issue_date",
    "currency",
    "items",
    "notes"
  ],
  "properties": {
    "invoice_id": {
      "type": "string"
    },
    "issue_date": {
      "type": "string",
      "description": "ISO-8601 YYYY-MM-DD."
    },
    "currency": {
      "type": "string",
      "enum": [
        "USD",
        "EUR",
        "GBP"
      ]
    },
    "items": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/LineItem"
      }
    },
    "notes": {
      "type": [
        "string",
        "null"
      ],
      "description": "Free-form note or null."
    }
  },
  "$defs": {
    "LineItem": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "sku",
        "quantity",
        "unit_price_usd"
      ],
      "properties": {
        "sku": {
          "type": "string"
        },
        "quantity": {
          "type": "integer"
        },
        "unit_price_usd": {
          "type": "string",
          "pattern": "^\\d+\\.\\d{2}$"
        }
      }
    }
  }
}
```
