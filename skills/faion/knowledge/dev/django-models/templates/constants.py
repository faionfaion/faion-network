# purpose: TextChoices skeleton for status / role / kind enums.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Place at apps/<app>/constants.py.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
# apps/users/constants.py — TextChoices enums and module-level constants
from django.db import models


class UserType(models.TextChoices):
    REGULAR = "regular", "Regular"
    PREMIUM = "premium", "Premium"
    ADMIN = "admin", "Administrator"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


# Pagination and limits
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MAX_ITEMS_PER_USER = 100
