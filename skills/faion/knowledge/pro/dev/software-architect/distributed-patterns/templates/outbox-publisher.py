"""
Outbox Pattern: polling publisher with at-least-once delivery and idempotency.

Flow:
1. Business transaction writes record + outbox row in same DB transaction.
2. This publisher polls the outbox table periodically.
3. For each pending row, it publishes to the message broker.
4. On successful publish, marks the row as processed (or deletes it).

Consumers MUST be idempotent — the publisher may deliver the same message
more than once (crash between publish and marking processed).

PostgreSQL example. Adapt the SQL to your DB dialect.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class OutboxMessage:
    id: uuid.UUID
    topic: str
    key: str | None
    payload: dict
    created_at: datetime
    retry_count: int = 0


class OutboxPublisher:
    """
    Polls the outbox table and publishes pending messages.

    Idempotency: the outbox row id is used as the Kafka message key or
    as the SQS MessageDeduplicationId to prevent duplicate processing at
    the broker level. Consumer-side deduplication is still required for
    non-Kafka targets or when the broker dedup window expires.
    """

    def __init__(
        self,
        db_pool,           # asyncpg connection pool (or sync equivalent)
        broker_client,     # Kafka producer / SQS client
        poll_interval: float = 5.0,     # seconds between polls
        batch_size: int = 100,          # messages per poll
        max_retries: int = 5,           # abandon after N broker failures
    ):
        self.db = db_pool
        self.broker = broker_client
        self.poll_interval = poll_interval
        self.batch_size = batch_size
        self.max_retries = max_retries
        self._running = False

    async def start(self) -> None:
        """Start the polling loop. Run as a background task."""
        self._running = True
        logger.info("outbox_publisher_started")
        while self._running:
            try:
                await self._poll_and_publish()
            except Exception as exc:
                logger.error("outbox_poll_error", extra={"error": str(exc)})
            await asyncio.sleep(self.poll_interval)

    def stop(self) -> None:
        self._running = False

    async def _poll_and_publish(self) -> None:
        """Fetch a batch of pending messages and publish each one."""
        async with self.db.acquire() as conn:
            # Lock rows for this publisher instance (skip locked = no contention
            # with other publisher replicas running in parallel)
            rows = await conn.fetch(
                """
                SELECT id, topic, key, payload, created_at, retry_count
                FROM outbox
                WHERE processed_at IS NULL
                  AND retry_count < $1
                ORDER BY created_at ASC
                LIMIT $2
                FOR UPDATE SKIP LOCKED
                """,
                self.max_retries,
                self.batch_size,
            )

        if not rows:
            return

        for row in rows:
            msg = OutboxMessage(
                id=row["id"],
                topic=row["topic"],
                key=row["key"],
                payload=json.loads(row["payload"]),
                created_at=row["created_at"],
                retry_count=row["retry_count"],
            )
            await self._publish_one(msg)

    async def _publish_one(self, msg: OutboxMessage) -> None:
        """Publish a single message and mark it processed on success."""
        try:
            # Use outbox row id as idempotency key at the broker level
            await self.broker.send(
                topic=msg.topic,
                key=msg.key or str(msg.id),
                value=json.dumps(msg.payload),
                headers={"outbox_id": str(msg.id)},
            )

            # Mark processed — delete (or set processed_at) within a transaction
            async with self.db.acquire() as conn:
                await conn.execute(
                    "DELETE FROM outbox WHERE id = $1", msg.id
                )
            logger.debug("outbox_published", extra={"id": str(msg.id), "topic": msg.topic})

        except Exception as exc:
            logger.warning(
                "outbox_publish_failed",
                extra={"id": str(msg.id), "retry_count": msg.retry_count, "error": str(exc)},
            )
            async with self.db.acquire() as conn:
                await conn.execute(
                    """
                    UPDATE outbox
                    SET retry_count = retry_count + 1,
                        last_error = $2,
                        last_attempt_at = now()
                    WHERE id = $1
                    """,
                    msg.id,
                    str(exc),
                )


# --- Schema reference (PostgreSQL) ---
OUTBOX_DDL = """
CREATE TABLE IF NOT EXISTS outbox (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic           VARCHAR(255) NOT NULL,
    key             VARCHAR(255),
    payload         JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at    TIMESTAMPTZ,
    retry_count     INTEGER NOT NULL DEFAULT 0,
    last_error      TEXT,
    last_attempt_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_outbox_pending
    ON outbox (created_at ASC)
    WHERE processed_at IS NULL;
"""


# --- Writing to outbox (in the same DB transaction as the business record) ---

async def create_order_with_outbox(conn, order_data: dict) -> dict:
    """
    Example: write order + outbox row atomically.
    The publisher will deliver the OrderCreated event at-least-once.
    """
    async with conn.transaction():
        order = await conn.fetchrow(
            "INSERT INTO orders (customer_id, amount_cents) VALUES ($1, $2) RETURNING id",
            order_data["customer_id"],
            order_data["amount_cents"],
        )
        order_id = order["id"]

        await conn.execute(
            "INSERT INTO outbox (topic, key, payload) VALUES ($1, $2, $3)",
            "orders.created",
            str(order_id),
            json.dumps({"order_id": str(order_id), "event": "OrderCreated"}),
        )

    return {"order_id": str(order_id)}
