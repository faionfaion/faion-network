<!--
purpose: human-readable wrapper around the llamaindex-sql-query decision-record JSON
consumes: validated decision-record.json
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~400 tokens
-->

# Decision: llamaindex-sql-query — `<context>`

## Drivers
- `table_count`: <value>
- `schema_size_chars`: <value>
- `read_only_required`: <value>

## Decision
- `dsn`: <value>
- `include_tables`: <value>
- `use_object_index`: <value>
- `max_returned_rows`: <value>
- `read_only`: <value>

## Rejected alternatives
| Option | Reason rejected |
|---|---|
| ... | ... |

## Audit
Rules consulted: `<r-list>`
