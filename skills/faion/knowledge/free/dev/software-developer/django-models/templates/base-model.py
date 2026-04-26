# core/models.py — Abstract BaseModel with UUID and timestamps
import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base providing integer PK, UUID external identifier, and timestamps.

    - id: integer PK for internal DB joins (never expose to clients)
    - uid: UUID for external API identifiers (stable, client-safe)
    - created_at / updated_at: auto-managed timestamps
    """

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
