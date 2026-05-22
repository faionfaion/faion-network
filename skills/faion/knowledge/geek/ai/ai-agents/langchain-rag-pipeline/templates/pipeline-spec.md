<!--
purpose: human-readable wrapper around the langchain-rag-pipeline decision-record JSON
consumes: validated decision-record.json
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~400 tokens
-->

# Decision: langchain-rag-pipeline — `<context>`

## Drivers
- `doc_count`: <value>
- `avg_doc_chars`: <value>
- `query_pattern`: <value>
- `latency_budget_ms`: <value>

## Decision
- `loader`: <value>
- `splitter`: <value>
- `chunk_size`: <value>
- `embedding_model`: <value>
- `vectorstore`: <value>
- `retriever_k`: <value>
- `prompt_template`: <value>

## Rejected alternatives
| Option | Reason rejected |
|---|---|
| ... | ... |

## Audit
Rules consulted: `<r-list>`
