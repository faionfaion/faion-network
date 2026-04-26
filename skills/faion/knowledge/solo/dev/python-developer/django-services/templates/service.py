"""
Canonical Django service template.

Usage:
    from apps.orders.services import order_create

    order = order_create(user=request.user, data=validated_data)

Rules:
- Functions named entity_action (order_create, order_cancel)
- Keyword-only arguments after the first positional
- @transaction.atomic on write operations
- Raise domain exceptions, never HTTP exceptions
- Inside atomic block: use task.delay_on_commit() instead of task.delay()
"""
from django.db import transaction

from apps.orders.models import Order
from apps.orders.exceptions import OrderAlreadyCancelledError


@transaction.atomic
def order_create(*, user, product_id: int, quantity: int) -> Order:
    """
    Create a new order for the given user.

    Raises:
        ProductNotFoundError: if product_id does not exist
    """
    from apps.products.selectors import product_get  # late import avoids circular dep

    product = product_get(id=product_id)

    order = Order.objects.create(
        user=user,
        product=product,
        quantity=quantity,
        status=Order.Status.PENDING,
    )

    # Use delay_on_commit so task only runs after DB commit
    from apps.notifications.tasks import notify_order_created
    notify_order_created.delay_on_commit(order_id=order.id)

    return order


@transaction.atomic
def order_cancel(*, order: Order, reason: str = "") -> Order:
    """
    Cancel an existing order.

    Raises:
        OrderAlreadyCancelledError: if order is already cancelled
    """
    if order.status == Order.Status.CANCELLED:
        raise OrderAlreadyCancelledError(f"Order {order.id} is already cancelled.")

    order.status = Order.Status.CANCELLED
    order.cancel_reason = reason
    order.save(update_fields=["status", "cancel_reason", "updated_at"])

    return order
