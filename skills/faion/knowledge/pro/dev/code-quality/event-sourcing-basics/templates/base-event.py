"""
purpose: Immutable BaseEvent + payload pattern.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (event-sourcing-basics)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID, uuid4


@dataclass(frozen=True)
class BaseEvent:
    event_id: UUID = field(default_factory=uuid4)
    aggregate_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 0
    payload: Dict[str, Any] = field(default_factory=dict)
