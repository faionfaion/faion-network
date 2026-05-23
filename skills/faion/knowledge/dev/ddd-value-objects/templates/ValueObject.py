# purpose: Python value object with frozen dataclass + constructor validation
# consumes: amount + currency primitives
# produces: immutable Money type with value-equality + add/subtract
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded as reference

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        if self.amount < 0:
            raise ValueError("Money amount must be >= 0")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Money currency must be ISO 4217 (3 chars)")
        object.__setattr__(self, "currency", self.currency.upper())

    def add(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"currency mismatch {self.currency} vs {other.currency}")
