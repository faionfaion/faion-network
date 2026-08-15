# purpose: Working Django abstract BaseModel: int PK + UUIDField + created_at + updated_at.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Place at apps/core/models/base.py.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
"""
Django BaseModel scaffold.

Usage: copy to core/models.py, import in every domain model.
UUIDv7 upgrade: pip install uuid-utils, uncomment uuid7 section.
"""
import uuid
from django.db import models
from django.utils import timezone

# --- UUID: default is v4. For high-write tables, upgrade to v7: ---
# import uuid_utils
# def uuid7(): return uuid_utils.uuid7()
# Then set: uid = models.UUIDField(default=uuid7, ...)


class BaseModel(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,  # callable — NOT uuid.uuid4()
        editable=False,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.uid})"


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(BaseModel):
    """BaseModel + soft delete. Use only for non-PII data."""

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta(BaseModel.Meta):
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
