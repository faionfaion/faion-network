# purpose: service partial-update skeleton — kwarg-only, atomic, full_clean, domain exceptions
# consumes: Model + payload of fields to update
# produces: updated Model instance; raises domain exceptions on missing / forbidden state
# depends-on: Django ORM, core.exceptions
# token-budget-impact: ~150 tokens

from django.db import transaction

from apps.<x>.models import <Entity>
from core.exceptions import NotFoundError, PermissionDeniedError


def <entity>_update(
    *,
    <entity>_id: int,
    user,
    name: str | None = None,
    is_active: bool | None = None,
) -> <Entity>:
    """Update fields on an existing <Entity> the user owns."""
    with transaction.atomic():
        try:
            entity = <Entity>.objects.select_for_update().get(pk=<entity>_id)
        except <Entity>.DoesNotExist:
            raise NotFoundError(f"<entity> {<entity>_id} not found")

        if entity.user_id != user.id:
            raise PermissionDeniedError("not owner")

        if name is not None:
            entity.name = name
        if is_active is not None:
            entity.is_active = is_active

        entity.full_clean()
        entity.save()

        return entity
