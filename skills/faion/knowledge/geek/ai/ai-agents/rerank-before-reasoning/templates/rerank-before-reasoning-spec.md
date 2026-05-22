<!--
purpose: human-readable wrapper around the rerank-before-reasoning JSON spec
consumes: validated spec.json from the output contract
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~250 tokens
-->

# Rerank Before Reasoning Spec

## Drivers
- `top_1_miss_rate`: `<value>`
- `latency_budget_ms`: `<value>`
- `context_budget_tokens`: `<value>`

## Decision
- `reranker_model`: `<value>`
- `k_retrieved`: `<value>`
- `k_final`: `<value>`
- `timeout_ms`: `<value>`
- `fallback_mode`: `<value>`

## Audit
Rules consulted: `<r-list>` — see content/01-core-rules.xml.
