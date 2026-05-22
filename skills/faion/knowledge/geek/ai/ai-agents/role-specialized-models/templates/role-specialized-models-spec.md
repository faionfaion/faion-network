<!--
purpose: human-readable wrapper around the role-specialized-models JSON spec
consumes: validated spec.json from the output contract
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~250 tokens
-->

# Role-Specialized Models Spec

## Drivers
- `role_count`: `<value>`
- `monthly_cost_target`: `<value>`
- `quality_floor`: `<value>`

## Decision
- `role_map`: `<value>`
- `fallback_chain`: `<value>`
- `eval_schedule_cron`: `<value>`

## Audit
Rules consulted: `<r-list>` — see content/01-core-rules.xml.
