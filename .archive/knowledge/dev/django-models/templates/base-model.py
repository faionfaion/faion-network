# purpose: Working Django abstract BaseModel with id + uid + created_at + updated_at.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Place at apps/core/models/base.py.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
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
