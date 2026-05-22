<!--
purpose: human-readable wrapper around the schema-version-pinning JSON spec
consumes: validated spec.json from the output contract
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~250 tokens
-->

# Schema Version Pinning Spec

## Drivers
- `schema_change_rate_per_quarter`: `<value>`
- `agent_deploys`: `<value>`
- `recorded_calls_count`: `<value>`

## Decision
- `pin_range`: `<value>`
- `migration_script_path`: `<value>`
- `deprecation_window_days`: `<value>`

## Audit
Rules consulted: `<r-list>` — see content/01-core-rules.xml.
