"""MessagePublisher and MessageConsumer using aio_pika (RabbitMQ)."""
import json
import logging
from typing import Callable, Dict

import aio_pika

log = logging.getLogger(__name__)


class MessagePublisher:
    """Publish events to RabbitMQ exchange."""

    def __init__(self, channel: aio_pika.Channel, exchange_name: str = "events"):
        self._channel = channel
        self._exchange_name = exchange_name

    async def publish(self, routing_key: str, payload: dict) -> None:
        exchange = await self._channel.get_exchange(self._exchange_name)
        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
        )
        await exchange.publish(message, routing_key=routing_key)


class MessageConsumer:
    """Consume events from a durable RabbitMQ queue."""

    def __init__(self, channel: aio_pika.Channel):
        self._channel = channel
        self._handlers: Dict[str, Callable] = {}

    def register(self, event_type: str, handler: Callable) -> None:
        self._handlers[event_type] = handler

    async def start(self, queue_name: str) -> None:
        queue = await self._channel.declare_queue(queue_name, durable=True)
        async with queue.iterator() as messages:
            async for message in messages:
                async with message.process():
                    data = json.loads(message.body)
                    event_type = data.get("type", "")
                    handler = self._handlers.get(event_type)
                    if handler:
                        try:
                            await handler(data)
                        except Exception:
                            log.exception("Handler failed for event_type=%s", event_type)
                            # message.process() context manager nacks on exception
                            raise
