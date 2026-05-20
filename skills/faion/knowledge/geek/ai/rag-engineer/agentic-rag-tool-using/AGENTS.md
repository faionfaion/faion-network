---
slug: agentic-rag-tool-using
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Instead of always calling the vector store, a tool-using agentic RAG lets the LLM select from a registry of retrieval tools on each step: vector_search (semantic), keyword_search (exact match), sql_query (structured data), web_search (external).
content_id: "91860cbd38c40a02"
tags: [rag, agentic, tool-use, function-calling, multi-modal-retrieval]
---
# Agentic RAG — Tool-Using Agent

## Summary

**One-sentence:** Instead of always calling the vector store, a tool-using agentic RAG lets the LLM select from a registry of retrieval tools on each step: vector_search (semantic), keyword_search (exact match), sql_query (structured data), web_search (external).

**One-paragraph:** Instead of always calling the vector store, a tool-using agentic RAG lets the LLM select from a registry of retrieval tools on each step: vector_search (semantic), keyword_search (exact match), sql_query (structured data), web_search (external). The agent loops up to a max_calls budget, then synthesizes a final answer from the accumulated multi-source context.

## Applies If (ALL must hold)

- Questions require combining structured data (SQL/tables) with unstructured document retrieval.
- The corpus has known coverage gaps that require web search as a fallback.
- Different query types in the same application benefit from different retrieval strategies (semantic vs exact vs structured).
- Auditable retrieval decisions are required — each tool call and its result is logged.

## Skip If (ANY kills it)

- Single-corpus applications where all information lives in one vector store — tool selection overhead adds latency with no benefit.
- When web_search is in the registry but the application has strict data governance preventing external lookups.
- When the LLM model does not support structured function calling — tool selection degrades to unreliable free-text parsing.

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

- parent skill: `geek/ai/rag-engineer/`
