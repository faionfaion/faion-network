# purpose: numeric field with units, range, rounding rule
# consumes: invoice raw input
# produces: validated numeric field with explicit description
# depends-on: pydantic v2
# token-budget-impact: ~80 tokens of description
"""Numeric-with-units template — total in cents, integer."""

from pydantic import BaseModel, Field


class Total(BaseModel):
    total_cents: int = Field(
        ge=0,
        description=(
            "Total in CENTS as integer. $19.99 -> 1999. "
            "Never include currency symbol or decimals. Includes tax."
        ),
    )
