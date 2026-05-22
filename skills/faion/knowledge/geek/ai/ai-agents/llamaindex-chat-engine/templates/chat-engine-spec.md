<!--
purpose: human-readable wrapper around the llamaindex-chat-engine decision-record JSON
consumes: validated decision-record.json
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~400 tokens
-->

# Decision: llamaindex-chat-engine — `<context>`

## Drivers
- `follow_up_complexity`: <value>
- `tool_use`: <value>
- `latency_target_ms`: <value>

## Decision
- `chat_mode`: <value>
- `token_limit`: <value>
- `streaming`: <value>
- `context_prompt`: <value>

## Rejected alternatives
| Option | Reason rejected |
|---|---|
| ... | ... |

## Audit
Rules consulted: `<r-list>`
