---
slug: llamaindex-chat-engine
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LlamaIndex chat engines wrap a VectorStoreIndex with conversation memory and follow-up question handling.
content_id: "b40b522ab5bdefdf"
tags: [llamaindex, chat, memory, streaming, rag]
---
# LlamaIndex Chat Engine and Streaming

## Summary

**One-sentence:** LlamaIndex chat engines wrap a VectorStoreIndex with conversation memory and follow-up question handling.

**One-paragraph:** LlamaIndex chat engines wrap a VectorStoreIndex with conversation memory and follow-up question handling. Choose chat mode based on follow-up complexity: condense_plus_context for standard Q&A with history, react for tool-using agents. Bound memory with ChatMemoryBuffer(token_limit=3900) to prevent context overflow. Use streaming for responsive UX in production.

## Applies If (ALL must hold)

- Document Q&A with follow-up questions — users refer to previous answers ("what did you say about X?").
- Customer support bots grounded in a knowledge base — context mode injects relevant documents into each turn.
- Long-running research sessions where conversation history helps the agent track what has been covered.
- Production UX requiring streaming — users see words appear as the model generates, not a long wait.

## Skip If (ANY kills it)

- Single-turn Q&A with no follow-up — a query engine is simpler and cheaper (no history overhead).
- High-throughput batch querying — chat engines maintain per-session state; use query engines with async batching instead.
- The primary task is tool orchestration with complex state — LangGraph or a custom ReAct loop has better control primitives.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
