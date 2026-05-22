<!--
purpose: human-readable wrapper around the reasoning-first-architectures JSON spec
consumes: validated spec.json from the output contract
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~250 tokens
-->

# Reasoning-First Architectures Spec

## Drivers
- `task_complexity`: `<value>`
- `branching`: `<value>`
- `error_recovery_needed`: `<value>`
- `horizon`: `<value>`

## Decision
- `architecture`: `<value>`
- `max_turns`: `<value>`
- `thinking_budget_tokens`: `<value>`
- `replan_trigger`: `<value>`

## Audit
Rules consulted: `<r-list>` — see content/01-core-rules.xml.
