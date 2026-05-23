<!-- purpose: ADR template for ES vs state-stored decision -->
<!-- consumes: outputs from procedure steps 1-4 -->
<!-- produces: ADR file in decisions/ folder -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens when loaded as reference -->

# ADR-NNN — Event Sourcing for <Aggregate>

## Context

Aggregate: <Aggregate>
Date: <YYYY-MM-DD>
Decision-maker: <name>

Audit need: <yes/no — why>
Schema stability: <yes/no — last 6 months data>
Naming discipline: <yes/no — team trained on past-tense events>

## Decision

`use_event_sourcing` / `use_state_stored` / `defer`

## Rationale

<2-4 sentences citing rules from event-sourcing-fundamentals/01-core-rules.xml>

## Consequences

- Event log size estimate: <events/day, retention months>
- Projections planned: <list>
- Snapshot policy: <every N events / off>
- Versioning approach: <see event-sourcing-versioning>

## Status

`accepted` / `proposed` / `superseded by ADR-MMM`
