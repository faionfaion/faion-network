"""
purpose: Aggregate base class with _apply dispatch + version tracking + pending events.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (event-sourcing-basics)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List, Type
from uuid import UUID, uuid4


@dataclass
class Aggregate:
    id: UUID = field(default_factory=uuid4)
    version: int = 0
    _pending: List[object] = field(default_factory=list)

    def apply_new(self, event: object) -> None:
        self._apply(event)
        self.version += 1
        self._pending.append(event)

    def _apply(self, event: object) -> None:
        # convention: dispatch to apply_<EventClassName>
        name = type(event).__name__
        snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        method = getattr(self, f"apply_{snake}", None)
        if method is None:
            raise NotImplementedError(f"no apply_{snake} on {type(self).__name__}")
        method(event)

    def flush_pending(self) -> List[object]:
        events, self._pending = self._pending, []
        return events

    @classmethod
    def load_from_events(cls, events: list[object]) -> "Aggregate":
        agg = cls()
        for ev in events:
            agg._apply(ev)
            agg.version += 1
        return agg
