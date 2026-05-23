# purpose: State pattern template (Python).
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a behavioral-patterns artefact validating against scripts/validate-behavioral-patterns.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
"""
State pattern in Python with Context and abstract State base.

Use when: object behavior changes significantly per state, FSMs, lifecycle workflows.
Skip when: 2–3 simple states with minimal branching — use an enum + match instead.

This template models an order lifecycle: PENDING → CONFIRMED → SHIPPED → DELIVERED.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Abstract state
# ---------------------------------------------------------------------------
class OrderState(ABC):
    @property
    @abstractmethod
    def status(self) -> OrderStatus:
        ...

    @abstractmethod
    def confirm(self, order: Order) -> None:
        ...

    @abstractmethod
    def ship(self, order: Order) -> None:
        ...

    @abstractmethod
    def deliver(self, order: Order) -> None:
        ...

    @abstractmethod
    def cancel(self, order: Order) -> None:
        ...


# ---------------------------------------------------------------------------
# Concrete states
# ---------------------------------------------------------------------------
class PendingState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.PENDING

    def confirm(self, order: Order) -> None:
        print("Order confirmed.")
        order._state = ConfirmedState()

    def ship(self, order: Order) -> None:
        print("Cannot ship: order not confirmed.")

    def deliver(self, order: Order) -> None:
        print("Cannot deliver: order not confirmed.")

    def cancel(self, order: Order) -> None:
        print("Order cancelled.")
        order._state = CancelledState()


class ConfirmedState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.CONFIRMED

    def confirm(self, order: Order) -> None:
        print("Order is already confirmed.")

    def ship(self, order: Order) -> None:
        print("Order shipped.")
        order._state = ShippedState()

    def deliver(self, order: Order) -> None:
        print("Cannot deliver: order not shipped yet.")

    def cancel(self, order: Order) -> None:
        print("Order cancelled.")
        order._state = CancelledState()


class ShippedState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.SHIPPED

    def confirm(self, order: Order) -> None:
        print("Cannot confirm: order already shipped.")

    def ship(self, order: Order) -> None:
        print("Order is already shipped.")

    def deliver(self, order: Order) -> None:
        print("Order delivered.")
        order._state = DeliveredState()

    def cancel(self, order: Order) -> None:
        print("Cannot cancel: order already shipped.")


class DeliveredState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.DELIVERED

    def confirm(self, order: Order) -> None:
        print("Order already delivered.")

    def ship(self, order: Order) -> None:
        print("Order already delivered.")

    def deliver(self, order: Order) -> None:
        print("Order already delivered.")

    def cancel(self, order: Order) -> None:
        print("Cannot cancel: order already delivered.")


class CancelledState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.CANCELLED

    def confirm(self, order: Order) -> None:
        print("Cannot confirm: order is cancelled.")

    def ship(self, order: Order) -> None:
        print("Cannot ship: order is cancelled.")

    def deliver(self, order: Order) -> None:
        print("Cannot deliver: order is cancelled.")

    def cancel(self, order: Order) -> None:
        print("Order is already cancelled.")


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------
@dataclass
class Order:
    order_id: str
    _state: OrderState = field(default_factory=PendingState, init=False)

    @property
    def status(self) -> OrderStatus:
        return self._state.status

    def confirm(self) -> None:
        self._state.confirm(self)

    def ship(self) -> None:
        self._state.ship(self)

    def deliver(self) -> None:
        self._state.deliver(self)

    def cancel(self) -> None:
        self._state.cancel(self)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    order = Order(order_id="ORD-001")
    print(order.status)  # PENDING

    order.ship()         # Cannot ship: order not confirmed.
    order.confirm()      # Order confirmed.
    print(order.status)  # CONFIRMED

    order.ship()         # Order shipped.
    print(order.status)  # SHIPPED

    order.cancel()       # Cannot cancel: order already shipped.
    order.deliver()      # Order delivered.
    print(order.status)  # DELIVERED
