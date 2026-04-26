"""
Canonical Django selector template.

Selectors = read-only queries. Never write DB inside a selector.
Use select_related / prefetch_related to prevent N+1.
Raise domain exceptions for not-found; do not return None.
"""
from django.db.models import QuerySet, Prefetch

from apps.orders.models import Order
from apps.orders.exceptions import OrderNotFoundError
from apps.products.models import Product


def order_get(*, id: int) -> Order:
    """
    Fetch a single Order by primary key.

    Raises:
        OrderNotFoundError: if the order does not exist
    """
    try:
        return Order.objects.select_related("user", "product").get(pk=id)
    except Order.DoesNotExist:
        raise OrderNotFoundError(f"Order {id} not found.")


def order_list(*, user_id: int | None = None, status: str | None = None) -> QuerySet[Order]:
    """
    Return a filtered, annotated queryset of orders.
    Callers paginate; do not call .all() without filters in production.
    """
    qs = Order.objects.select_related("user", "product").order_by("-created_at")

    if user_id is not None:
        qs = qs.filter(user_id=user_id)
    if status is not None:
        qs = qs.filter(status=status)

    return qs


def order_list_with_items(*, user_id: int) -> QuerySet[Order]:
    """
    Fetch orders with line items pre-fetched to avoid N+1 in template loops.
    """
    return (
        Order.objects.filter(user_id=user_id)
        .prefetch_related(
            Prefetch("items", queryset=Product.objects.only("id", "name", "price"))
        )
        .order_by("-created_at")
    )
