# purpose: TextChoices skeleton for status / role / kind enums.
# consumes: the enum fields named in the models spec.
# produces: apps/<app>/constants.py — the single source for choices and limits.
# depends-on: content/01-core-rules.xml rule r3-text-choices-enums.
# token-budget-impact: zero — local-only template; build time is the only cost.
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
