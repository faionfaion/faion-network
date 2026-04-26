"""Event-sourced aggregate base class with _apply dispatch, version tracking, and pending events."""
import re
from dataclasses import dataclass, field
from typing import List, Type
from uuid import UUID


def _to_snake(name: str) -> str:
    """Convert CamelCase event class name to snake_case handler name."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


@dataclass
class EventSourcedAggregate:
    """Base for event-sourced aggregates.

    Subclass and implement:
    - _on_<event_name_snake_case>(self, event) for each event type
    - create() classmethod factory
    - from_events() classmethod for replay
    - Command methods that call self._apply(SomeEvent(...))
    """

    id: UUID = field(default=None)
    version: int = 0
    _pending_events: List = field(default_factory=list, repr=False)

    @classmethod
    def from_events(cls, aggregate_id: UUID, events: List) -> "EventSourcedAggregate":
        instance = cls(id=aggregate_id)
        for event in events:
            instance._apply(event, is_new=False)
        return instance

    def _apply(self, event, is_new: bool = True) -> None:
        handler_name = f"_on_{_to_snake(type(event).__name__)}"
        handler = getattr(self, handler_name, None)
        if handler:
            handler(event)
        self.version += 1
        if is_new:
            self._pending_events.append(event)

    def collect_pending_events(self) -> List:
        events = self._pending_events.copy()
        self._pending_events.clear()
        return events
