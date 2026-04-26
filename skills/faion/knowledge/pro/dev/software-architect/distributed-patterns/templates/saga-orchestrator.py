"""
Saga Orchestrator skeleton with compensating transaction registry.

Pattern: central coordinator sends commands to services and awaits replies.
Each step has a corresponding compensating transaction registered up front.

Usage:
    saga = OrderSaga(order_id="ord_123", payload={...})
    await saga.execute()

All compensating transactions must be idempotent — they may be called
more than once due to at-least-once delivery semantics.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Awaitable

logger = logging.getLogger(__name__)


class SagaStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


@dataclass
class SagaStep:
    name: str
    action: Callable[..., Awaitable[Any]]
    compensation: Callable[..., Awaitable[None]]
    result: Any = None


class SagaOrchestrator:
    """
    Generic saga orchestrator.

    - Executes steps in order; on any failure, compensates completed steps
      in reverse order.
    - correlation_id is attached to every command and event for deduplication.
    """

    def __init__(self, saga_id: str | None = None):
        self.saga_id = saga_id or str(uuid.uuid4())
        self.steps: list[SagaStep] = []
        self.completed_steps: list[SagaStep] = []
        self.status = SagaStatus.PENDING

    def add_step(
        self,
        name: str,
        action: Callable[..., Awaitable[Any]],
        compensation: Callable[..., Awaitable[None]],
    ) -> None:
        """Register a step with its compensating transaction."""
        self.steps.append(SagaStep(name=name, action=action, compensation=compensation))

    async def execute(self) -> dict:
        """
        Execute all steps in order. On failure, compensate in reverse order.
        Returns the final saga result or raises on unrecoverable failure.
        """
        self.status = SagaStatus.RUNNING
        logger.info("saga_start", extra={"saga_id": self.saga_id})

        for step in self.steps:
            try:
                logger.info(
                    "saga_step_start",
                    extra={"saga_id": self.saga_id, "step": step.name},
                )
                step.result = await step.action()
                self.completed_steps.append(step)
                logger.info(
                    "saga_step_complete",
                    extra={"saga_id": self.saga_id, "step": step.name},
                )
            except Exception as exc:
                logger.error(
                    "saga_step_failed",
                    extra={"saga_id": self.saga_id, "step": step.name, "error": str(exc)},
                )
                await self._compensate()
                self.status = SagaStatus.FAILED
                raise SagaFailedError(
                    f"Saga {self.saga_id} failed at step '{step.name}'"
                ) from exc

        self.status = SagaStatus.COMPLETED
        logger.info("saga_complete", extra={"saga_id": self.saga_id})
        return {"saga_id": self.saga_id, "status": self.status}

    async def _compensate(self) -> None:
        """Execute compensating transactions in reverse order."""
        self.status = SagaStatus.COMPENSATING
        for step in reversed(self.completed_steps):
            try:
                logger.info(
                    "saga_compensation_start",
                    extra={"saga_id": self.saga_id, "step": step.name},
                )
                await step.compensation()
                logger.info(
                    "saga_compensation_complete",
                    extra={"saga_id": self.saga_id, "step": step.name},
                )
            except Exception as exc:
                # Log and continue compensating remaining steps.
                # A failed compensation is a stuck saga — requires manual intervention.
                logger.critical(
                    "saga_compensation_failed",
                    extra={
                        "saga_id": self.saga_id,
                        "step": step.name,
                        "error": str(exc),
                        "action": "manual_intervention_required",
                    },
                )


class SagaFailedError(Exception):
    pass


# --- Concrete example: Order placement saga ---

async def create_order(order_id: str, payload: dict) -> dict:
    """Step 1: create order record in Order Service."""
    # await order_service_client.post("/orders", json={...})
    logger.info("order_created", extra={"order_id": order_id})
    return {"order_id": order_id}


async def cancel_order(order_id: str) -> None:
    """Compensation for step 1: idempotent — safe to call multiple times."""
    # await order_service_client.post(f"/orders/{order_id}/cancel")
    logger.info("order_cancelled", extra={"order_id": order_id})


async def charge_payment(order_id: str, amount_cents: int, idempotency_key: str) -> dict:
    """Step 2: charge payment in Payment Service. Idempotency key prevents double-charge."""
    # await payment_service_client.post("/payments", json={...}, headers={"Idempotency-Key": idempotency_key})
    return {"payment_id": f"pay_{order_id}"}


async def refund_payment(payment_id: str) -> None:
    """Compensation for step 2."""
    # await payment_service_client.post(f"/payments/{payment_id}/refund")
    logger.info("payment_refunded", extra={"payment_id": payment_id})


async def place_order(order_id: str, payload: dict) -> dict:
    """Orchestrate the full order placement saga."""
    idempotency_key = f"{order_id}-charge"
    payment_id = None

    saga = SagaOrchestrator(saga_id=f"order-{order_id}")

    saga.add_step(
        name="create_order",
        action=lambda: create_order(order_id, payload),
        compensation=lambda: cancel_order(order_id),
    )
    saga.add_step(
        name="charge_payment",
        action=lambda: charge_payment(order_id, payload["amount_cents"], idempotency_key),
        compensation=lambda: refund_payment(payment_id or f"pay_{order_id}"),
    )

    return await saga.execute()
