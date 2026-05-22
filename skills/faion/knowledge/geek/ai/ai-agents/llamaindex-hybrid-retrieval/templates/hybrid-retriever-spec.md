<!--
purpose: human-readable wrapper around the llamaindex-hybrid-retrieval decision-record JSON
consumes: validated decision-record.json
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~400 tokens
-->

# Decision: llamaindex-hybrid-retrieval — `<context>`

## Drivers
- `corpus_heterogeneity`: <value>
- `latency_target_ms`: <value>
- `rerank_budget_usd`: <value>

## Decision
- `retrievers`: <value>
- `fusion_top_k`: <value>
- `rerank_model`: <value>
- `rerank_top_n`: <value>
- `similarity_cutoff`: <value>

## Rejected alternatives
| Option | Reason rejected |
|---|---|
| ... | ... |

## Audit
Rules consulted: `<r-list>`
