"""
purpose: per-app constants.py — TextChoices enums + UPPER_SNAKE limits.
consumes: nothing (foundational module imported by models / services / views).
produces: importable enum classes and module-level limits.
depends-on: django >= 4.2 (TextChoices is 3.0+).
token-budget-impact: ~280 tokens when read by an agent.
"""

from __future__ import annotations

from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending Payment"
    PAID = "paid", "Paid"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class UserRole(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Administrator"
    MEMBER = "member", "Member"
    VIEWER = "viewer", "Viewer"


# Business limits — referenced by services, models, and tests.
# Reviewed quarterly per ops/limits-policy.md.
MAX_ORDERS_PER_USER: int = 100
DEFAULT_PAGE_SIZE: int = 25
MAX_PAGE_SIZE: int = 100
ORDER_CANCEL_WINDOW_HOURS: int = 24
RETRY_BACKOFF_SECONDS: tuple[int, ...] = (1, 5, 30, 120)
