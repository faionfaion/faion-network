# purpose: Pydantic invoice schema with regex-patterned price and big-int ID fields
# consumes: nothing (used as a model spec for SO calls)
# produces: structured Invoice/LineItem instances after model_validate_json
# depends-on: pydantic v2, decimal stdlib
# token-budget-impact: schema serialization ~250 tokens
"""Invoice schema with pattern-constrained decimals and big-int identifiers.

Money and large IDs are strings with regex patterns — strict-mode and grammar
backends enforce the pattern at sampling time, so the model cannot drift on
decimal count or digit length. Receiving side parses to Decimal/int.
"""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    """One line on an invoice."""

    sku: str = Field(pattern=r"^[A-Z0-9-]{2,40}$", description="Uppercase SKU.")
    description: str
    quantity: int = Field(ge=1, le=10_000)
    unit_price_usd: str = Field(
        pattern=r"^\d+\.\d{2}$",
        description="USD unit price as decimal string. Two decimals required. Example: '19.99'.",
    )

    def line_total(self) -> Decimal:
        return Decimal(self.unit_price_usd) * self.quantity


class Invoice(BaseModel):
    """Top-level invoice document."""

    model_config = {"extra": "forbid"}

    invoice_id: str = Field(
        pattern=r"^\d{1,32}$",
        description="Numeric ID up to 32 digits. Stored as string to avoid float overflow.",
    )
    currency: Literal["USD"] = "USD"
    issue_date: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="ISO-8601 date. If only month/year are visible, use day=01.",
    )
    items: list[LineItem]
    total_usd: str = Field(
        pattern=r"^\d+\.\d{2}$",
        description="Grand total in USD as decimal string. Must equal sum of line totals.",
    )

    def expected_total(self) -> Decimal:
        return sum((item.line_total() for item in self.items), Decimal("0.00"))
