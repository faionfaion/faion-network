# purpose: Service module skeleton with function signatures + docstrings
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# Service module skeleton for Django
# Copy and fill in: Feature, Model, app, verb, noun, params
# Conventions: lazy model imports, keyword-only args, domain exception, transaction.atomic

from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import transaction

if TYPE_CHECKING:
    from apps.<app>.models import <Model>
    from apps.users.models import User


class <Feature>Error(Exception):
    """Domain errors raised by <feature> service."""


@transaction.atomic
def <verb>_<noun>(
    user: "User",
    *,
    param: str,
) -> "<Model>":
    """One-line summary.

    Business logic:
    - bullet describing each rule

    Args:
        user: User performing the action.
        param: Description.

    Returns:
        The created/updated <Model> instance.

    Raises:
        <Feature>Error: When a business rule is violated.
    """
    from apps.<app>.models import <Model>

    try:
        obj = <Model>.objects.select_for_update().get(field=param)
    except <Model>.DoesNotExist:
        raise <Feature>Error(f"<Model> {param!r} not found")

    # mutate
    obj.field = ...
    obj.save(update_fields=["field", "updated_at"])
    return obj
