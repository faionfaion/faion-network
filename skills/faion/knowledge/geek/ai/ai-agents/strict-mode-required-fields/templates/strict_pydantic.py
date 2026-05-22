# purpose: reference Pydantic 2 invoice model with strict-mode-compatible schema
# consumes: Pydantic >= 2.5
# produces: model_json_schema() that passes OpenAI strict-mode compiler
# depends-on: pydantic >= 2.5; assert_strict_schema runs in CI
# token-budget-impact: ~450 tokens to render in agent context
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
