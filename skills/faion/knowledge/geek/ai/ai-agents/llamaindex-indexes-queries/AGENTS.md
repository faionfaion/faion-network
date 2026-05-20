---
slug: llamaindex-indexes-queries
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LlamaIndex offers multiple index types (VectorStore, Keyword, KnowledgeGraph, Tree, Summary) to optimize for different query patterns and data shapes.
content_id: "37dedcd42f3fc8d9"
tags: [llamaindex, query-engines, retrievers, vector-stores, hybrid-search]
---
# LlamaIndex: Indexes & Query Engines

## Summary

**One-sentence:** LlamaIndex offers multiple index types (VectorStore, Keyword, KnowledgeGraph, Tree, Summary) to optimize for different query patterns and data shapes.

**One-paragraph:** LlamaIndex offers multiple index types (VectorStore, Keyword, KnowledgeGraph, Tree, Summary) to optimize for different query patterns and data shapes. Query engines wrap retrievers and response synthesizers to handle the full pipeline from user question to final answer. This guide covers index selection, query engine configuration, hybrid retrieval, reranking, and structured output generation.

## Applies If (ALL must hold)

- Building a RAG pipeline that requires multiple index types over the same corpus (vector - keyword - graph).
- Queries span heterogeneous data sources: SQL tables - unstructured documents - knowledge graphs.
- Need hierarchical summarization (TreeIndex, SummaryIndex) over large document sets.
- Building an agent with knowledge retrieval tools backed by LlamaIndex query engines.
- Complex multi-hop questions that benefit from SubQuestionQueryEngine decomposition.
- Need structured output (Pydantic) from document queries with schema enforcement.

## Skip If (ANY kills it)

- Simple single-document Q&A — direct prompt - context is faster and cheaper.
- High-throughput production APIs where LlamaIndex's Python overhead matters — use a dedicated vector DB SDK directly.
- When you only need BM25 keyword search — Elasticsearch or Typesense is lighter.
- If the codebase already uses LangChain RAG heavily — mixing both frameworks adds cognitive overhead without clear gain.
- Real-time streaming over very large retrievals — latency compounds with each response synthesis pass.

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
