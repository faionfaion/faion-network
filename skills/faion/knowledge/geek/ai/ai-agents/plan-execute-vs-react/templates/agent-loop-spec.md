<!--
purpose: human-readable wrapper around the agent-loop-spec JSON
consumes: validated spec.json from the output contract
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~250 tokens
-->

# Agent Loop Spec — `<task-name>`

## Drivers

- `known_substeps`: `<value>`
- `horizon`: `<value>`
- `adaptability_needed`: `<value>`
- `audit_required`: `<value>`
- `mixed_predictability`: `<value>`

## Decision

- `loop_type`: `<plan-execute | react | hybrid>`
- `max_turns`: `<n>`
- `plan_model`: `<opus | sonnet>`
- `execute_model`: `<opus | sonnet | haiku>`
- `replan_on_failure`: `<true | false>`

## Audit

Rules consulted: `<r-list>` — see content/01-core-rules.xml.
