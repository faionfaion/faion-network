"""rabbitmq-client.py — RabbitMQ producer + consumer with DLQ wiring.

Features:
  - Persistent delivery (delivery_mode=2)
  - Durable queues with dead-letter exchange
  - prefetch_count=10 for fair dispatch
  - Manual ack after successful processing
  - basic_nack(requeue=False) on failure → routes to DLQ

Usage:
    client = RabbitMQClient()
    client.declare_queue(QueueConfig(name="orders", durable=True,
                                     dead_letter_exchange="", dead_letter_routing_key="orders.dlq"))
    client.publish("orders", {"order_id": "123"})
    client.consume("orders", lambda msg: process(msg))
"""
import json
from dataclasses import dataclass, field
from typing import Callable, Optional

import pika


@dataclass
class QueueConfig:
    name: str
    durable: bool = True
    dead_letter_exchange: Optional[str] = None
    dead_letter_routing_key: Optional[str] = None
    message_ttl: Optional[int] = None  # milliseconds


class RabbitMQClient:
    def __init__(self, host: str = "localhost", port: int = 5672):
        params = pika.ConnectionParameters(
            host=host, port=port, heartbeat=600, blocked_connection_timeout=300
        )
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.basic_qos(prefetch_count=10)

    def declare_queue(self, config: QueueConfig) -> None:
        args: dict = {}
        if config.dead_letter_exchange is not None:
            args["x-dead-letter-exchange"] = config.dead_letter_exchange
        if config.dead_letter_routing_key:
            args["x-dead-letter-routing-key"] = config.dead_letter_routing_key
        if config.message_ttl:
            args["x-message-ttl"] = config.message_ttl

        self._channel.queue_declare(
            queue=config.name,
            durable=config.durable,
            arguments=args or None,
        )

    def publish(self, queue: str, message: dict) -> None:
        self._channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type="application/json",
            ),
        )

    def consume(self, queue: str, callback: Callable[[dict], None]) -> None:
        def _wrapper(ch, method, properties, body):
            try:
                msg = json.loads(body)
                callback(msg)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception:
                # nack without requeue → routes to DLQ
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                raise

        self._channel.basic_consume(queue=queue, on_message_callback=_wrapper, auto_ack=False)
        self._channel.start_consuming()
