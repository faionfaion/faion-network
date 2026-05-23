<!--
purpose: human-readable wrapper around the decision-record JSON; commits next to it
consumes: validated decision-record.json from scripts/validate-langchain-memory.py
produces: rendered markdown for code review
depends-on: 02-output-contract.xml schema
token-budget-impact: ~400 tokens (review surface only, not loaded by agent)
-->

# Decision: LangChain Memory — `<slug-or-context>`

**Memory type:** `<buffer|summary|vector|entity>`
**Store backend:** `<redis|postgres|chroma|pinecone>`
**TTL:** `<seconds>`
**Session ID strategy:** `<uuid|hashed-user-id|thread-id>`

## Drivers

- `expected_turns`: `<n>`
- `recall_pattern`: `<recency|semantic|mixed>`
- `entity_focus`: `<true|false>`

## Why not the alternatives

| Memory type | Reason rejected |
|---|---|
| buffer  | ... |
| summary | ... |
| vector  | ... |
| entity  | ... |

(Drop the row that won.)

## Wiring

```python
# Pasted from templates/wiring-snippet.py with the chosen backend filled in.
```

## Audit

Rules consulted: `<r1, r13, r14, ...>`
