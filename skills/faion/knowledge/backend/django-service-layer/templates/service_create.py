# purpose: HackSoft-style service create skeleton — kwarg-only, atomic, full_clean, on_commit
# consumes: Models + Celery tasks + domain exceptions module
# produces: a service function callable from views / Celery / admin / management commands
# depends-on: Django ORM, core.exceptions
# token-budget-impact: ~180 tokens

from django.db import transaction

from apps.<x>.models import <Entity>
from core.exceptions import ValidationError


def <entity>_create(
    *,
    user,
    name: str,
    items: list[dict] | None = None,
) -> <Entity>:
    """Create a new <Entity> and dispatch side-effects after commit."""
    if not name:
        raise ValidationError("name must be non-empty")

    with transaction.atomic():
        entity = <Entity>(user=user, name=name)
        entity.full_clean()  # runs Model.clean() + field validators
        entity.save()

        if items:
            <Entity>Item.objects.bulk_create(
                [<Entity>Item(<entity>=entity, **i) for i in items]
            )

        transaction.on_commit(
            lambda: notify_user_<entity>_created.delay(<entity>_id=entity.id)
        )

    return entity
