# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Django BaseModel + SoftDeleteModel scaffold.
Location: core/models.py
"""
import uuid
from django.db import models
from django.utils import timezone


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
    """For non-PII data only. Do NOT use for models containing user PII."""

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
