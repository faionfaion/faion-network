"""Idempotent consumer template for at-least-once event delivery.

Backing store: Postgres processed_events table with PK on (event_id, consumer).
Usage: subclass IdempotentConsumer and implement handle_event().
"""
import asyncio
import hashlib
import json
import logging

log = logging.getLogger("consumer")


class RetryableError(Exception):
    """Raise to nack and redeliver the message."""


class PoisonError(Exception):
    """Raise to send to DLQ and ack (do not redeliver)."""


class IdempotentConsumer:
    def __init__(self, db, consumer_name: str):
        self.db = db
        self.consumer = consumer_name

    async def process(self, raw: bytes, headers: dict) -> bool:
        """Process a raw message. Returns True if acked, raises RetryableError to nack."""
        evt = json.loads(raw)
        eid = evt.get("id") or evt.get("event_id") or hashlib.sha256(raw).hexdigest()

        async with self.db.transaction() as tx:
            inserted = await tx.execute(
                "INSERT INTO processed_events(event_id, consumer) "
                "VALUES($1,$2) ON CONFLICT DO NOTHING RETURNING event_id",
                eid,
                self.consumer,
            )
            if not inserted:
                log.info("dedup skip event_id=%s consumer=%s", eid, self.consumer)
                return True  # ack: already handled

            try:
                await self.handle_event(evt, headers, tx)
            except RetryableError:
                raise  # broker will redeliver; dedup row rolls back with tx
            except PoisonError as e:
                log.error("poison event_id=%s: %s", eid, e)
                await self._send_to_dlq(evt, headers, str(e))
                return True  # ack: poison goes to DLQ, do not redeliver

        return True

    async def handle_event(self, evt: dict, headers: dict, tx) -> None:
        """Override in subclass to implement event handling logic."""
        raise NotImplementedError

    async def _send_to_dlq(self, evt: dict, headers: dict, reason: str) -> None:
        """Override to publish failed events to a dead-letter queue."""
        log.error("DLQ: event=%s reason=%s", evt.get("id"), reason)
