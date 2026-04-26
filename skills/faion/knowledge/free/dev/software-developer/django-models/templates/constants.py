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
