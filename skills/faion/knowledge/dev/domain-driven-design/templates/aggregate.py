"""
purpose: Aggregate root template with internal invariant enforcement.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (domain-driven-design)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price_cents: int


@dataclass
class Order:
    id: UUID = field(default_factory=uuid4)
    lines: List[OrderLine] = field(default_factory=list)
    placed: bool = False

    def add_line(self, line: OrderLine) -> None:
        if self.placed:
            raise ValueError("cannot modify a placed order")
        self.lines.append(line)

    def place(self) -> None:
        if not self.lines:
            raise ValueError("cannot place an empty order")
        self.placed = True
