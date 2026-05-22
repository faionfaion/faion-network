<!--
purpose: human-readable wrapper around the prompt-cache-prefix-order JSON spec
consumes: validated spec.json from the output contract
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~250 tokens
-->

# Prompt Cache Prefix Order Spec

## Drivers
- `stable_prefix_tokens`: `<value>`
- `calls_per_day`: `<value>`
- `system_prompt_changes_per_day`: `<value>`

## Decision
- `section_order`: `<value>`
- `breakpoint_position_tokens`: `<value>`
- `stable_token_count`: `<value>`
- `cache_hit_target`: `<value>`

## Audit
Rules consulted: `<r-list>` — see content/01-core-rules.xml.
