"""
Canonical Celery task skeleton.

Rules:
- Accept primitive arguments only (IDs, strings — never model instances)
- Implement idempotency guard at the top of the function body
- Set both soft_time_limit and time_limit
- Use autoretry_for with retry_backoff for transient errors
- Use bind=True only when self.retry or self.request is needed
- Call via task.delay_on_commit() inside @transaction.atomic views
"""
import logging

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

logger = logging.getLogger(__name__)


@shared_task(
    name="orders.process_order",   # explicit name, not auto-generated
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,            # 1s, 2s, 4s, 8s, 16s …
    retry_backoff_max=600,         # cap at 10 minutes
    max_retries=5,
    acks_late=True,                # re-queue on worker crash
    soft_time_limit=55,
    time_limit=60,
)
def process_order(self, order_id: int) -> dict:
    """
    Process a pending order.

    Idempotent: returns immediately if the order is already processed.
    """
    from apps.orders.models import Order  # late import keeps module-level clean

    # --- Idempotency guard ---
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.warning("process_order: order %s not found, skipping.", order_id)
        return {"status": "skipped", "reason": "order_not_found"}

    if order.status != Order.Status.PENDING:
        return {"status": "skipped", "reason": f"already_{order.status}"}

    # --- Business logic ---
    try:
        # ... actual processing ...
        Order.objects.filter(pk=order_id, status=Order.Status.PENDING).update(
            status=Order.Status.PROCESSED
        )
    except SoftTimeLimitExceeded:
        logger.error("process_order: soft time limit exceeded for order %s", order_id)
        raise

    return {"status": "processed", "order_id": order_id}
