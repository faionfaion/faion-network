"""PostgreSQL event store skeleton with optimistic concurrency, serialize, and deserialize."""
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class ConcurrencyError(Exception):
    pass


class UnknownEventType(Exception):
    pass


# Registry: populated by decorating event classes with @register_event
EVENT_REGISTRY: Dict[str, Type] = {}


def register_event(cls):
    EVENT_REGISTRY[cls.__name__] = cls
    return cls


class EventStore(ABC):
    @abstractmethod
    async def append(self, stream_id: str, events: List, expected_version: int) -> None: ...

    @abstractmethod
    async def read_stream(self, stream_id: str, from_version: int = 0) -> List: ...


class PostgresEventStore(EventStore):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def append(self, stream_id: str, events: List, expected_version: int) -> None:
        result = await self._session.execute(
            text("SELECT COALESCE(MAX(version), 0) FROM events WHERE stream_id = :s"),
            {"s": stream_id},
        )
        current = result.scalar()
        if current != expected_version:
            raise ConcurrencyError(f"Expected version {expected_version}, got {current}")

        for i, event in enumerate(events):
            version = expected_version + i + 1
            await self._session.execute(
                text("""
                    INSERT INTO events
                        (event_id, stream_id, version, event_type, event_data, metadata, occurred_at)
                    VALUES
                        (:eid, :sid, :ver, :etype, :edata, :meta, :occ)
                """),
                {
                    "eid": str(event.event_id), "sid": stream_id, "ver": version,
                    "etype": type(event).__name__,
                    "edata": json.dumps(self._serialize(event)),
                    "meta": json.dumps(getattr(event, "metadata", {})),
                    "occ": event.occurred_at,
                },
            )
        await self._session.commit()

    async def read_stream(self, stream_id: str, from_version: int = 0) -> List:
        result = await self._session.execute(
            text("""
                SELECT event_type, event_data, metadata, occurred_at
                FROM events
                WHERE stream_id = :s AND version > :v
                ORDER BY version ASC
            """),
            {"s": stream_id, "v": from_version},
        )
        return [
            self._deserialize(row.event_type, json.loads(row.event_data),
                              json.loads(row.metadata), row.occurred_at)
            for row in result
        ]

    def _serialize(self, event) -> dict:
        return {k: str(v) for k, v in event.__dict__.items()
                if k not in ("event_id", "occurred_at", "metadata")}

    def _deserialize(self, event_type: str, data: dict, metadata: dict, occurred_at) -> Any:
        cls = EVENT_REGISTRY.get(event_type)
        if not cls:
            raise UnknownEventType(event_type)
        return cls(**data, metadata=metadata, occurred_at=occurred_at)
