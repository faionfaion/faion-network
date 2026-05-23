"""
purpose: Frozen + slotted dataclass skeleton with __post_init__ validation.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Money:
    amount_cents: int
    currency: str = "EUR"

    def __post_init__(self) -> None:
        if self.amount_cents < 0:
            raise ValueError("Money cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("ISO 4217 currency code expected")
