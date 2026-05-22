# purpose: skeleton Pydantic 2 model demonstrating safe rename with validation_alias for backwards-compat
# consumes: legacy Pydantic model where field names are generic
# produces: new model where internal names are semantically loaded but external JSON wire-format is preserved
# depends-on: pydantic >= 2.5
# token-budget-impact: ~250 tokens per rename when emitted in agent context

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Order(BaseModel):
    """Semantically renamed schema with backwards-compat aliases.

    External clients still POST `{"flag": true, "total": 1999, "label": "a"}`; the
    model accepts those keys via `validation_alias` and exposes the new names
    internally. For LLM-facing structured outputs the model will see the new
    names because Pydantic emits the canonical name in `model_json_schema()`.
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    customer_id: str = Field(description="Stable customer identifier (UUID).")
    is_paid: bool = Field(
        validation_alias="flag",
        description="True iff the order has been paid in full.",
    )
    total_cents: int = Field(
        validation_alias="total",
        ge=0,
        description="Order total in integer minor units (cents).",
    )
    priority: Literal["low", "medium", "high", "critical"] = Field(
        validation_alias="label",
        description="Triage priority; semantic vocabulary replaces legacy a|b|c|d.",
    )


def _smoke_test() -> None:
    legacy_payload = {"customer_id": "u-1", "flag": True, "total": 1999, "label": "high"}
    order = Order.model_validate(legacy_payload)
    assert order.is_paid is True
    assert order.total_cents == 1999
    assert order.priority == "high"
    schema = Order.model_json_schema()
    assert "is_paid" in schema["properties"]
    assert schema["additionalProperties"] is False


if __name__ == "__main__":
    _smoke_test()
