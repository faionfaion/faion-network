"""
Module Public API Template

Other modules must ONLY import from this file.
Internal classes (models, repositories, services) are private.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Protocol


# ============================================================
# Enums
# ============================================================

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ============================================================
# DTOs — immutable, no business logic
# ============================================================

@dataclass(frozen=True)
class OrderDTO:
    id: str
    user_id: str
    status: OrderStatus
    total_amount: float
    created_at: datetime


@dataclass(frozen=True)
class CreateOrderRequest:
    user_id: str
    items: list[dict]  # [{"product_id": str, "quantity": int}]
    shipping_address_id: Optional[str] = None


# ============================================================
# Service Protocol (public interface)
# ============================================================

class OrderService(Protocol):
    """
    Public interface for Orders module.
    Inject this type; never import the concrete implementation.
    """

    def create_order(self, request: CreateOrderRequest) -> OrderDTO: ...
    def get_order(self, order_id: str) -> Optional[OrderDTO]: ...
    def cancel_order(self, order_id: str, reason: str) -> OrderDTO: ...
    def complete_order(self, order_id: str) -> OrderDTO: ...


# ============================================================
# Module-specific exceptions
# ============================================================

class OrderError(Exception):
    """Base exception for Orders module."""

class OrderNotFoundError(OrderError):
    def __init__(self, order_id: str):
        self.order_id = order_id
        super().__init__(f"Order not found: {order_id}")

class InsufficientStockError(OrderError):
    def __init__(self, product_id: str, requested: int, available: int):
        super().__init__(
            f"Insufficient stock for {product_id}: "
            f"requested {requested}, available {available}"
        )
