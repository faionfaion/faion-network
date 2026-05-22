<!--
purpose: Markdown skeleton for an authored Multi-Agent Orchestration decision record.
consumes: subtask list + baseline metrics + eval result + cost budget + owner
produces: filled-in record matching the JSON schema sibling file
depends-on: content/02-output-contract.xml
token-budget-impact: 0 — template
-->

# Multi-Agent Orchestration Decision — `<artefact_id>`

- **Owner:** `<single named handle / email / role>`
- **Topology pick:** `single | hierarchical | collaborative | conversational`

## Subtasks

- `<distinct subtask 1>`
- `<distinct subtask 2>`

## Hand-off protocol

| Field | Value |
|---|---|
| task_id | `<id schema>` |
| scoped_context | `<what subset of context is passed>` |
| success_criteria | `<measurable definition>` |
| escalation | `<who/what handles failure>` |

## Judge–actor (only if used)

| Metric | Value |
|---|---|
| quality_lift_pp | `<>= 2 required>` |
| cost_multiplier | `<within budget>` |

## Rollback trigger

| Metric | Threshold |
|---|---|
| latency_threshold_ms | `<>` |
| cost_threshold_multiplier | `<>` |
| quality_threshold_pp | `<>` |

## Rationale

`<≥2 sentences citing measured baseline; explain why single-agent default is being overridden>`
