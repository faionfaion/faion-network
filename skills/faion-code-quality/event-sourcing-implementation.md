---
id: event-sourcing-implementation
name: "Event Sourcing - Implementation"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Event Sourcing - Implementation

## Event Store

```python
# infrastructure/event_store/event_store.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.events.base import Event


class EventStore(ABC):
    """Abstract event store interface."""

    @abstractmethod
    async def append(
        self,
        stream_id: str,
        events: List[Event],
        expected_version: int,
    ) -> None:
        """Append events to stream with optimistic concurrency."""
        pass

    @abstractmethod
    async def read_stream(
        self,
        stream_id: str,
        from_version: int = 0,
    ) -> List[Event]:
        """Read all events from a stream."""
        pass

    @abstractmethod
    async def read_all(
        self,
        from_position: int = 0,
        batch_size: int = 100,
    ) -> List[Event]:
        """Read all events across all streams."""
        pass


# infrastructure/event_store/postgres_event_store.py
import json
from typing import List
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresEventStore(EventStore):
    """PostgreSQL implementation of event store."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._serializers: dict = {}

    def register_serializer(self, event_type: type, serializer) -> None:
        self._serializers[event_type] = serializer

    async def append(
        self,
        stream_id: str,
        events: List[Event],
        expected_version: int,
    ) -> None:
        """Append events with optimistic concurrency check."""

        # Check current version
        result = await self._session.execute(
            text("""
                SELECT COALESCE(MAX(version), 0) as version
                FROM events WHERE stream_id = :stream_id
            """),
            {"stream_id": stream_id},
        )
        current_version = result.scalar()

        if current_version != expected_version:
            raise ConcurrencyError(
                f"Expected version {expected_version}, got {current_version}"
            )

        # Insert events
        for i, event in enumerate(events):
            version = expected_version + i + 1
            await self._session.execute(
                text("""
                    INSERT INTO events (
                        event_id, stream_id, version, event_type,
                        event_data, metadata, occurred_at
                    ) VALUES (
                        :event_id, :stream_id, :version, :event_type,
                        :event_data, :metadata, :occurred_at
                    )
                """),
                {
                    "event_id": str(event.event_id),
                    "stream_id": stream_id,
                    "version": version,
                    "event_type": type(event).__name__,
                    "event_data": json.dumps(self._serialize(event)),
                    "metadata": json.dumps(event.metadata),
                    "occurred_at": event.occurred_at,
                },
            )

        await self._session.commit()

    async def read_stream(
        self,
        stream_id: str,
        from_version: int = 0,
    ) -> List[Event]:
        """Read events from stream."""
        result = await self._session.execute(
            text("""
                SELECT event_type, event_data, metadata, occurred_at
                FROM events
                WHERE stream_id = :stream_id AND version > :from_version
                ORDER BY version ASC
            """),
            {"stream_id": stream_id, "from_version": from_version},
        )

        events = []
        for row in result:
            event = self._deserialize(
                event_type=row.event_type,
                data=json.loads(row.event_data),
                metadata=json.loads(row.metadata),
                occurred_at=row.occurred_at,
            )
            events.append(event)

        return events

    def _serialize(self, event: Event) -> dict:
        """Serialize event to dict."""
        serializer = self._serializers.get(type(event))
        if serializer:
            return serializer.serialize(event)

        # Default: use dataclass fields
        return {
            k: str(v) if isinstance(v, UUID) else v
            for k, v in event.__dict__.items()
            if k not in ('event_id', 'occurred_at', 'metadata')
        }

    def _deserialize(
        self,
        event_type: str,
        data: dict,
        metadata: dict,
        occurred_at: datetime,
    ) -> Event:
        """Deserialize event from stored data."""
        # Get event class from registry
        event_class = EVENT_REGISTRY.get(event_type)
        if not event_class:
            raise UnknownEventType(event_type)

        return event_class(**data, metadata=metadata, occurred_at=occurred_at)
```

## Database Schema

```sql
-- Event store table
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_id UUID NOT NULL UNIQUE,
    stream_id VARCHAR(255) NOT NULL,
    version INTEGER NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    occurred_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT events_stream_version_unique UNIQUE (stream_id, version)
);

CREATE INDEX events_stream_id_idx ON events(stream_id);
CREATE INDEX events_event_type_idx ON events(event_type);
CREATE INDEX events_occurred_at_idx ON events(occurred_at);
```

## Snapshots

```python
# infrastructure/event_store/snapshot_store.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json


@dataclass
class Snapshot:
    stream_id: str
    version: int
    state: dict
    created_at: datetime


class SnapshotStore:
    """Store for aggregate snapshots."""

    def __init__(self, session):
        self._session = session

    async def save(self, snapshot: Snapshot) -> None:
        await self._session.execute(
            text("""
                INSERT INTO snapshots (stream_id, version, state, created_at)
                VALUES (:stream_id, :version, :state, :created_at)
                ON CONFLICT (stream_id) DO UPDATE SET
                    version = :version,
                    state = :state,
                    created_at = :created_at
            """),
            {
                "stream_id": snapshot.stream_id,
                "version": snapshot.version,
                "state": json.dumps(snapshot.state),
                "created_at": snapshot.created_at,
            },
        )

    async def get(self, stream_id: str) -> Optional[Snapshot]:
        result = await self._session.execute(
            text("SELECT * FROM snapshots WHERE stream_id = :stream_id"),
            {"stream_id": stream_id},
        )
        row = result.fetchone()
        if row:
            return Snapshot(
                stream_id=row.stream_id,
                version=row.version,
                state=json.loads(row.state),
                created_at=row.created_at,
            )
        return None


# Repository with snapshot support
class EventSourcedOrderRepository:
    SNAPSHOT_FREQUENCY = 50  # Snapshot every 50 events

    def __init__(
        self,
        event_store: EventStore,
        snapshot_store: SnapshotStore,
    ):
        self._event_store = event_store
        self._snapshot_store = snapshot_store

    async def get(self, order_id: UUID) -> Optional[Order]:
        stream_id = f"order-{order_id}"

        # Try to load from snapshot
        snapshot = await self._snapshot_store.get(stream_id)

        if snapshot:
            # Load events after snapshot
            events = await self._event_store.read_stream(
                stream_id, from_version=snapshot.version
            )
            order = Order(**snapshot.state)
            order.version = snapshot.version
        else:
            # Load all events
            events = await self._event_store.read_stream(stream_id)
            order = Order(id=order_id)

        # Apply events
        for event in events:
            order._apply(event, is_new=False)

        return order if order.version > 0 else None

    async def save(self, order: Order) -> None:
        stream_id = f"order-{order.id}"
        events = order.collect_pending_events()

        if not events:
            return

        expected_version = order.version - len(events)

        await self._event_store.append(stream_id, events, expected_version)

        # Create snapshot if needed
        if order.version % self.SNAPSHOT_FREQUENCY == 0:
            await self._snapshot_store.save(Snapshot(
                stream_id=stream_id,
                version=order.version,
                state=self._serialize_order(order),
                created_at=datetime.utcnow(),
            ))

    def _serialize_order(self, order: Order) -> dict:
        """Serialize order state for snapshot."""
        return {
            "id": str(order.id),
            "customer_id": str(order.customer_id),
            "status": order.status.value,
            "items": [
                {
                    "product_id": str(item.product_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                }
                for item in order.items
            ],
            "shipping_address": order.shipping_address,
            "tracking_number": order.tracking_number,
        }
```

## Snapshot Schema

```sql
-- Snapshot store table
CREATE TABLE snapshots (
    stream_id VARCHAR(255) PRIMARY KEY,
    version INTEGER NOT NULL,
    state JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL
);
```

## Projections

```python
# projections/order_details_projection.py
from typing import Dict
from uuid import UUID


class OrderDetailsProjection:
    """Read model for order details."""

    def __init__(self, session):
        self._session = session

    async def handle_order_created(self, event: OrderCreated) -> None:
        await self._session.execute(
            text("""
                INSERT INTO order_details (
                    order_id, customer_id, status, created_at
                ) VALUES (
                    :order_id, :customer_id, :status, :created_at
                )
            """),
            {
                "order_id": str(event.order_id),
                "customer_id": str(event.customer_id),
                "status": "draft",
                "created_at": event.occurred_at,
            },
        )

    async def handle_order_item_added(self, event: OrderItemAdded) -> None:
        await self._session.execute(
            text("""
                INSERT INTO order_items (
                    order_id, product_id, product_name, quantity, unit_price
                ) VALUES (
                    :order_id, :product_id, :product_name, :quantity, :unit_price
                )
            """),
            {
                "order_id": str(event.order_id),
                "product_id": str(event.product_id),
                "product_name": event.product_name,
                "quantity": event.quantity,
                "unit_price": event.unit_price,
            },
        )

    async def handle_order_placed(self, event: OrderPlaced) -> None:
        await self._session.execute(
            text("""
                UPDATE order_details
                SET status = 'placed', placed_at = :placed_at
                WHERE order_id = :order_id
            """),
            {
                "order_id": str(event.order_id),
                "placed_at": event.occurred_at,
            },
        )
```

## Projection Schema

```sql
-- Order details projection
CREATE TABLE order_details (
    order_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    placed_at TIMESTAMP,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP
);

CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id UUID NOT NULL REFERENCES order_details(order_id),
    product_id UUID NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);
```

## Event Handlers

```python
# event_handlers.py
from typing import Dict, List, Callable


class EventBus:
    """Simple event bus for projections."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: Event) -> None:
        event_type = type(event).__name__
        handlers = self._handlers.get(event_type, [])

        for handler in handlers:
            await handler(event)


# Setup projections
event_bus = EventBus()

order_details = OrderDetailsProjection(session)
event_bus.subscribe("OrderCreated", order_details.handle_order_created)
event_bus.subscribe("OrderItemAdded", order_details.handle_order_item_added)
event_bus.subscribe("OrderPlaced", order_details.handle_order_placed)
```

## Command Handler

```python
# commands/place_order_handler.py
from uuid import UUID


class PlaceOrderHandler:
    """Command handler for placing orders."""

    def __init__(
        self,
        repository: EventSourcedOrderRepository,
        event_bus: EventBus,
    ):
        self._repository = repository
        self._event_bus = event_bus

    async def handle(
        self,
        order_id: UUID,
        shipping_address: dict,
    ) -> None:
        # Load aggregate
        order = await self._repository.get(order_id)

        if not order:
            raise OrderNotFound(order_id)

        # Execute command
        order.place(shipping_address)

        # Save events
        await self._repository.save(order)

        # Publish events to projections
        for event in order.collect_pending_events():
            await self._event_bus.publish(event)
```

## Testing

```python
# tests/test_event_sourcing.py
import pytest
from uuid import uuid4
from decimal import Decimal


@pytest.mark.asyncio
async def test_order_lifecycle():
    order_id = uuid4()
    customer_id = uuid4()

    # Create order
    order = Order.create(order_id, customer_id)
    assert order.status == OrderStatus.DRAFT

    # Add items
    order.add_item(
        product_id=uuid4(),
        product_name="Product 1",
        quantity=2,
        unit_price=Decimal("10.00"),
    )

    # Place order
    order.place({"street": "123 Main St"})
    assert order.status == OrderStatus.PLACED

    # Verify events
    events = order.collect_pending_events()
    assert len(events) == 3
    assert isinstance(events[0], OrderCreated)
    assert isinstance(events[1], OrderItemAdded)
    assert isinstance(events[2], OrderPlaced)


@pytest.mark.asyncio
async def test_event_replay():
    order_id = uuid4()
    customer_id = uuid4()
    product_id = uuid4()

    # Create events
    events = [
        OrderCreated(order_id=order_id, customer_id=customer_id),
        OrderItemAdded(
            order_id=order_id,
            product_id=product_id,
            product_name="Product",
            quantity=1,
            unit_price=Decimal("10.00"),
        ),
        OrderPlaced(
            order_id=order_id,
            shipping_address={"street": "123 Main St"},
            total_amount=Decimal("10.00"),
        ),
    ]

    # Reconstruct from events
    order = Order.from_events(order_id, events)

    assert order.status == OrderStatus.PLACED
    assert len(order.items) == 1
    assert order.total == Decimal("10.00")
```

## See Also

- [event-sourcing-basics.md](event-sourcing-basics.md) - Event sourcing concepts and patterns
- [cqrs-pattern.md](cqrs-pattern.md) - CQRS pattern (often used with event sourcing)
- [domain-driven-design.md](domain-driven-design.md) - DDD patterns
