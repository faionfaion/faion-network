"""Service stub template for Django service-layer functions."""
from django.db import transaction


def do_something(
    entity: Entity,
    param: str,
    *,
    optional_flag: bool = True,
) -> Entity:
    """
    One-line description of what this service does.

    Args:
        entity: The primary domain object being acted on
        param: Description of the parameter
        optional_flag: Description of the optional flag

    Returns:
        The modified Entity instance

    Raises:
        Entity.DoesNotExist: If entity is not found
        ValidationError: If precondition is violated
    """
    # 1. Load and lock if mutating
    obj = Entity.objects.select_for_update().get(pk=entity.pk)

    # 2. Guard preconditions
    # if obj.already_done:
    #     raise ValidationError("Already processed")

    # 3. Apply changes — always list all modified fields
    obj.some_field = param
    obj.save(update_fields=["some_field", "updated_at"])

    # 4. Enqueue side effects after commit
    if optional_flag:
        transaction.on_commit(lambda: side_effect_task.delay(obj.pk))

    return obj
