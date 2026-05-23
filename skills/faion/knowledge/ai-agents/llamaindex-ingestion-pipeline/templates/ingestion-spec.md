<!--
purpose: human-readable wrapper around the llamaindex-ingestion-pipeline decision-record JSON
consumes: validated decision-record.json
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~400 tokens
-->

# Decision: llamaindex-ingestion-pipeline — `<context>`

## Drivers
- `doc_count`: <value>
- `update_frequency`: <value>
- `embedding_budget_usd`: <value>

## Decision
- `loader`: <value>
- `metadata_extractors`: <value>
- `node_parser`: <value>
- `vector_store`: <value>
- `docstore`: <value>

## Rejected alternatives
| Option | Reason rejected |
|---|---|
| ... | ... |

## Audit
Rules consulted: `<r-list>`
