# purpose: Template fixture for django-service-layer: services.py
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
"""apps/orders/services.py -- module layout for the write side of one app.

Order inside the module: imports -> __all__ -> private helpers -> create ->
update -> delete -> orchestrations. Bodies for order_create and order_update
follow the sibling templates service_create.py and service_update.py; this
file shows what surrounds them. Names come from content/05-examples.xml.
"""
from __future__ import annotations

from django.db import transaction

from apps.orders.models import Order, OrderAuditLog
from apps.orders.tasks import notify_user_order_cancelled, notify_user_order_transferred
from core.exceptions import NotFoundError, PermissionDeniedError, ValidationError

# Public surface: one <entity>_<verb> function per write entry point. Views, Celery tasks,
# admin actions and management commands import from here and nowhere else.
__all__ = ["order_create", "order_update", "order_cancel", "order_transfer"]


def _get_owned_order(*, order_id: int, user) -> Order:
    """Shared lookup: locks the row inside the caller's atomic block; domain exceptions only."""
    try:
        order = Order.objects.select_for_update().get(pk=order_id)
    except Order.DoesNotExist:
        raise NotFoundError(f"order {order_id} not found")
    if order.user_id != user.id:
        raise PermissionDeniedError("not owner")
    return order


def _audit(*, order: Order, actor, action: str, detail: str = "") -> OrderAuditLog:
    """Audit rows go through full_clean like every other instance built in a service."""
    log = OrderAuditLog(order=order, actor=actor, action=action, detail=detail)
    log.full_clean()
    log.save()
    return log


# def order_create(*, user, items: list[dict], shipping_method_id: int) -> Order:
#     body: templates/service_create.py
#
# def order_update(*, order_id: int, user, shipping_method_id: int | None = None) -> Order:
#     body: templates/service_update.py


def order_cancel(*, order_id: int, user, reason: str) -> Order:
    """Status change + audit row: two model writes, so the atomic boundary lives here."""
    if not reason.strip():
        raise ValidationError("reason must be non-empty")
    with transaction.atomic():
        order = _get_owned_order(order_id=order_id, user=user)
        if order.status == Order.Status.SHIPPED:
            raise ValidationError("shipped order cannot be cancelled")
        order.status = Order.Status.CANCELLED
        order.full_clean()
        order.save(update_fields=["status", "updated_at"])
        _audit(order=order, actor=user, action="cancel", detail=reason)
        # Fires after commit, dropped on rollback: the worker never sees a row that was rolled back.
        transaction.on_commit(lambda: notify_user_order_cancelled.delay(order_id=order.id))
    return order


def order_transfer(*, order_id: int, from_user, to_user) -> Order:
    """Orchestration across ownership + audit under one outer atomic block."""
    if from_user.id == to_user.id:
        raise ValidationError("cannot transfer to the same user")
    with transaction.atomic():
        order = _get_owned_order(order_id=order_id, user=from_user)
        order.user = to_user
        order.full_clean()
        order.save(update_fields=["user", "updated_at"])
        # Any service called from here nests its own atomic() as a savepoint; this block remains the
        # rollback unit, so ownership change and audit row commit or fail together.
        _audit(order=order, actor=from_user, action="transfer", detail=str(to_user.id))
        transaction.on_commit(lambda: notify_user_order_transferred.delay(order_id=order.id, to_user_id=to_user.id))
    return order
