# Agentic RAG — Tool-Using Agent

## Summary

**One-sentence:** Routes each RAG sub-query through an LLM-selected tool from a registry (vector_search, keyword_search, sql_query, web_search) and synthesises one answer from accumulated multi-source context.

**One-paragraph:** Instead of always calling the vector store, a tool-using agentic RAG lets the LLM select from a registry of retrieval tools on each step. The agent loops up to a `max_calls` budget, logs every selection decision, then asks a heavier model to synthesise a final answer from the accumulated multi-source context. Built on LangGraph / LlamaIndex `FunctionCallingAgent` primitives.

**Ефективно для:** RAG engineer who needs to fuse SQL + documents + web search behind one query — closes the gap between structured and unstructured retrieval in a single auditable loop.

## Applies If (ALL must hold)

- Questions require combining structured data (SQL/tables) with unstructured document retrieval.
- Corpus has known coverage gaps that require web_search as a fallback.
- Different query types in the same application benefit from different retrieval strategies (semantic vs exact vs structured).
- Auditable retrieval decisions are required — each tool call and its result is logged for offline debugging.

## Skip If (ANY kills it)

- Single-corpus apps where all info lives in one vector store — tool-selection overhead adds latency with no benefit.
- Data governance forbids external lookups but `web_search` is in the registry without an allow-list — security regression.
- LLM lacks reliable structured function calling — tool selection degrades to free-text parsing.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool registry definition | Python dict / JSON | author-supplied callables |
| Tool descriptions for the selector | text | derived from registry |
| Vector store handle | client object | `db-qdrant` / `db-chroma` |
| SQL connection (optional) | SQLAlchemy engine | application DB |
| Web search API key (optional) | env var | provider credentials |
| Model for selection | sonnet/haiku/gpt-4o-mini | application config |
| Model for synthesis | opus/sonnet/gpt-4o | application config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/rag-architecture` | Pipeline shape this agent slots into. |
| `geek/ai/llm-integration/function-calling` | Underlying mechanism the selector relies on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: max_calls cap + log, specific tool descriptions, cheap routing model, result caching, allow-list for web_search | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agent's emitted trace + final answer, with valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: full-results-in-selector, unrestricted web_search, ambiguous tool names, routing with heavy model | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: define registry → write tool descriptions → run loop with cap → cache → synthesise → log | ~900 |
| `content/05-examples.xml` | medium | Worked example: ToolUsingRAG class with 4 tools answering a hybrid query | ~600 |
| `content/06-decision-tree.xml` | essential | Branch on registry-size + governance + function-calling support | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tool-selection` | haiku | Classification task — which tool — does not need deep reasoning. |
| `intermediate-summarisation` | haiku | One-line summary per tool result for selector context. |
| `final-synthesis` | opus | Multi-source synthesis under faithfulness constraints. |
| `trace-audit` | sonnet | Reviewer pass over the selection log for compliance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool_using_rag.py` | Reference implementation of ToolUsingRAG with 4-tool registry, max_calls cap, result cache, and JSON trace emit. |
| `templates/output-schema.json` | JSON Schema for the agent's `{answer, trace, calls_used}` output. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-tool-using.py` | Validate emitted JSON trace against output schema, check call cap respected, no web_search outside allow-list. | After each agent run, before answer ships. |

## Related

- [[rag-architecture]] — outer RAG pipeline this loop plugs into.
- [[agentic-rag-iterative-retrieval]] — sibling pattern for single-store iterative refinement.
- [[agentic-rag-query-decomposition]] — pre-step splits one user question into sub-queries.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether tool-using RAG is the right pattern at all (≥2 retrieval modalities + auditable + reliable function calling) versus collapsing to a single-store iterative agent. Branches gate `web_search` behind an explicit allow-list before any production rollout.
