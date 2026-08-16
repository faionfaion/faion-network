# Event Sourcing — Event Versioning and GDPR

## Summary

**One-sentence:** Event versioning + upcasters — every published event has an event_version field; field changes bump version + register an upcaster; PII gets crypto-shredding.

**One-paragraph:** Once an event class is published (consumed by any downstream system) its contract is immutable. Any field rename, removal, or semantic change MUST bump `event_version` and register an upcaster that transforms old-shape events into new-shape on read. The event catalog MUST live in the repo and CI MUST fail when a published event class changes without the bump. PII MUST NOT appear in event payloads without a crypto-shredding plan (encrypt per-subject + drop key on erasure) OR externalization to a mutable side table. This methodology pins five rules: immutable contract, version + upcaster, committed event catalog, breaking-change CI gate, GDPR PII policy. Output: event-catalog entry + upcaster spec conforming to `02-output-contract.xml`.

**Ефективно для:**

- Long-lived ES systems where schema evolution is inevitable.
- GDPR / privacy compliance for European user data.
- Multi-consumer event streams where upstream changes affect many readers.
- Audit + compliance traceability via the event catalog.
- Snapshot invalidation discipline per `[[event-sourcing-snapshots]]`.

## Applies If (ALL must hold)

- ES is in place per `[[event-sourcing-fundamentals]]`.
- At least one event has been published (consumed somewhere).
- A schema-version field can be added to events.
- The repo can host a committed event catalog file.

## Skip If (ANY kills it)

- ES not yet adopted — apply the fundamentals first.
- Single-process ES with no external consumers — versioning still helps but is lower priority.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing event classes | source | repo |
| Downstream consumer list | docs | repo |
| GDPR data-mapping | spec | privacy officer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[event-sourcing-fundamentals]] | Events-immutable rule that versioning protects. |
| [[event-sourcing-snapshots]] | Snapshot invalidation triggered by schema bump. |
| [[event-sourcing-projections]] | Projections must handle both old + new versions via upcasters. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: immutable-after-publish, version-and-upcaster, committed-catalog, breaking-change-ci-gate, gdpr-pii-policy | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for catalog-entry + upcaster spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: silent-rename, no-upcaster, pii-in-payload, missing-ci-gate | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure for evolving an event | ~700 |
| `content/05-examples.xml` | essential | Worked upcaster v1→v2 example | ~600 |
| `content/06-decision-tree.xml` | essential | Routing tree on change type → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-change` | sonnet | Decide additive vs breaking. |
| `write-upcaster` | sonnet | Mapping logic. |
| `update-event-catalog` | haiku | Mechanical edit of catalog YAML. |

## Templates

| File | Purpose |
|------|---------|
| `templates/event-catalog.yml` | Versioned event catalog seed |
| `templates/Upcaster.py` | Upcaster registry + example transform |
| `templates/gdpr-policy.md.j2` | PII handling decision matrix |
| `templates/gdpr-policy.md` | PII handling decision matrix Generated from `templates/gdpr-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-versioning.py` | Validate catalog entry + upcaster spec | Pre-commit on catalog file |

## Related

- [[event-sourcing-fundamentals]]
- [[event-sourcing-aggregate]]
- [[event-sourcing-snapshots]]
- [[event-sourcing-projections]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (change type, PII presence, consumer count) to a rule from `01-core-rules.xml`. Use it whenever modifying an event class, adding PII, or planning a deprecation.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/event-catalog.yml`

```yaml
events:
  OrderPlaced:
    versions:
      - version: 1
        deprecated: true
        fields:
          - {name: order_id, type: UUID}
          - {name: customer_id, type: UUID}
          - {name: total_cents, type: int}
      - version: 2
        upcaster_from: 1
        upcaster_module: faion.events.upcasters.order_placed_v1_to_v2
        fields:
          - {name: order_id, type: UUID}
          - {name: buyer_id, type: UUID}
          - {name: total_cents, type: int}
    pii_handling: externalized_side_table
  PaymentCaptured:
    versions:
      - version: 1
        fields:
          - {name: order_id, type: UUID}
          - {name: amount_cents, type: int}
          - {name: card_token_id, type: UUID}    # opaque ID — PII lives in mutable side table
    pii_handling: externalized_side_table
ci_gate_enabled: true
```

### `templates/Upcaster.py`

```python
from __future__ import annotations

from typing import Callable

Upcaster = Callable[[dict], dict]

_REGISTRY: dict[tuple[str, int], Upcaster] = {}


def register(event_name: str, from_version: int):
    def decorator(fn: Upcaster) -> Upcaster:
        _REGISTRY[(event_name, from_version)] = fn
        return fn
    return decorator


def upcast(event_name: str, payload: dict, target_version: int) -> dict:
    while payload.get("event_version", 1) < target_version:
        current = payload.get("event_version", 1)
        fn = _REGISTRY.get((event_name, current))
        if fn is None:
            raise RuntimeError(
                f"no upcaster registered for {event_name} v{current} -> v{current + 1}"
            )
        payload = fn(payload)
        payload["event_version"] = current + 1
    return payload


@register("OrderPlaced", from_version=1)
def order_placed_v1_to_v2(v1: dict) -> dict:
    return {
        "order_id": v1["order_id"],
        "buyer_id": v1["customer_id"],
        "total_cents": v1["total_cents"],
    }
```
