# Event Sourcing — Basics

## Summary

**One-sentence:** Produces an event-sourced aggregate skeleton: ordered immutable events as the source of truth, in-memory state as a cache derived by replay, _apply dispatch, version tracking, and pending-events flush.

**One-paragraph:** Event Sourcing persists an aggregate's state as an ordered immutable sequence of domain events. Current state is derived by replaying events (or from a snapshot). Once written, an event is never modified — it is the source of truth; in-memory state is a cache. This yields a free audit trail, time-travel queries, projection rebuilding, and natural integration with event-driven architectures.

**Ефективно для:**

- Аудит-trail обовʼязковий (фінанси, healthcare, compliance).
- Складний domain з temporal queries ('state at 3pm yesterday').
- Event-driven downstream — log сам по собі message bus.
- Pair з CQRS для незалежних read projections.

## Applies If (ALL must hold)

- Complete audit trail required (financial, healthcare, compliance, legal).
- Complex domain with temporal queries.
- Event-driven architecture where downstream services consume history.
- System requires state reconstruction after data corruption or logic bug.

## Skip If (ANY kills it)

- Simple CRUD where history is irrelevant.
- Strong cross-aggregate consistency requirement — replay is eventual.
- Team unfamiliar with the pattern.
- High-frequency tiny writes (telemetry) — use a time-series DB.
- Unplanned schema evolution — changing an event's fields breaks replay.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Aggregate definition + commands | model doc | domain expert |
| Event list (verbs in past tense) | list | domain expert |
| Persistence target (Postgres / EventStore / Kafka) | infra | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[domain-driven-design]] | Aggregate root + invariants from DDD drive the event names and state transitions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-event-list` | sonnet | Per-aggregate enumeration of state-change events. |
| `scaffold-aggregate-base` | sonnet | _apply dispatch + version tracking + pending events list. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/base-event.py` | Immutable BaseEvent + payload pattern. |
| `templates/aggregate-base.py` | Aggregate base class with _apply dispatch + version tracking + pending events. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-basics.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[event-sourcing-implementation]]
- [[cqrs-pattern]]
- [[domain-driven-design]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates event sourcing on audit-trail requirement, schema-evolution discipline, and team familiarity.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/base-event.py`

```python
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
```

### `templates/aggregate-base.py`

```python
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
```
