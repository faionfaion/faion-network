# purpose: Service-layer module skeleton with @transaction.atomic.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Copy when creating apps/<app>/services/<topic>.py.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
"""Service stub template for Django service-layer functions.

`@transaction.atomic` is not decoration. Two things in this skeleton only work
inside a transaction, and both fail SILENTLY outside one:

* `select_for_update()` raises on PostgreSQL outside a transaction and is a
  no-op on SQLite, so the lock the comment promises does not exist.
* `transaction.on_commit()` fires IMMEDIATELY when there is no transaction to
  commit, so the Celery task is dispatched before the row is saved and the
  worker reads a row that is not there yet. That is the exact incident the
  sibling `django-celery` methodology's `on-commit-dispatch` rule cites.

The first version of this file advertised "@transaction.atomic" in its purpose
line and did not contain it. Verified on Django 6.1.
"""
from django.core.exceptions import ValidationError
from django.db import transaction

# Replace with the real imports for the app this service belongs to:
#   from apps.<app>.models import Entity
#   from apps.<app>.tasks import side_effect_task


@transaction.atomic
def do_something(
    entity: "Entity",
    param: str,
    *,
    optional_flag: bool = True,
) -> "Entity":
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
    # 1. Load and lock. Holds a row lock until the surrounding transaction
    #    commits, so two concurrent calls serialise instead of both passing
    #    the precondition check below.
    obj = Entity.objects.select_for_update().get(pk=entity.pk)

    # 2. Guard preconditions — after the lock, never before it.
    if getattr(obj, "already_done", False):
        raise ValidationError("Already processed")

    # 3. Apply changes — always list every modified field.
    obj.some_field = param
    obj.save(update_fields=["some_field", "updated_at"])

    # 4. Side effects after commit. Inside @atomic this runs once the row is
    #    durable; a rollback cancels it.
    if optional_flag:
        transaction.on_commit(lambda: side_effect_task.delay(obj.pk))

    return obj
