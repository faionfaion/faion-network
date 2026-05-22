"""
purpose: BaseModel + TimestampMixin + SoftDeleteMixin + managers reference for Django 5.x.
consumes: a Django 5.x project with PostgreSQL.
produces: importable abstract base classes for concrete models.
depends-on: django >= 5.0; psycopg / mysqlclient depending on engine.
token-budget-impact: ~520 tokens when read by an agent.
"""

from __future__ import annotations

import uuid

from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone


class TimestampMixin(models.Model):
    """Adds created_at and updated_at to any model."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UidMixin(models.Model):
    """Adds a public-facing UUID `uid` while keeping integer `id` as the PK."""

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """Overrides delete() at the QuerySet level — without this, bulk deletes hard-delete."""

    def delete(self):  # type: ignore[override]
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    """Default manager: only live rows. Pair with `all_objects = models.Manager()` on the model."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # required: gives admin / loaddata access to every row

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):  # type: ignore[override]
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self) -> None:
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])


class BaseModel(TimestampMixin, UidMixin):
    class Meta:
        abstract = True


class SoftDeletableModel(TimestampMixin, UidMixin, SoftDeleteMixin):
    class Meta:
        abstract = True


# Example concrete model showing the partial-unique pattern required by r3.
# class Customer(SoftDeletableModel):
#     email = models.EmailField()
#
#     class Meta:
#         constraints = [
#             UniqueConstraint(
#                 fields=["email"],
#                 condition=Q(deleted_at__isnull=True),
#                 name="unique_active_customer_email",
#             ),
#         ]
