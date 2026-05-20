---
slug: llamaindex-hybrid-retrieval
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use QueryFusionRetriever to combine vector and keyword retrievers with reciprocal rank fusion, then apply a cross-encoder reranker to shrink the candidate set.
content_id: "8f945959918a21d4"
tags: [llamaindex, retrieval, reranking, rag, hybrid-search]
---
# LlamaIndex Hybrid Retrieval and Reranking

## Summary

**One-sentence:** Use QueryFusionRetriever to combine vector and keyword retrievers with reciprocal rank fusion, then apply a cross-encoder reranker to shrink the candidate set.

**One-paragraph:** Use QueryFusionRetriever to combine vector and keyword retrievers with reciprocal rank fusion, then apply a cross-encoder reranker to shrink the candidate set. For hierarchical corpora, wire AutoMergingRetriever to promote parent nodes when enough children match. Apply SimilarityPostprocessor before the cross-encoder to pre-filter low-relevance candidates.

## Applies If (ALL must hold)

- Corpora mixing technical terms (exact-match) and natural language questions (semantic) — hybrid retrieval is the default.
- Top-k precision matters more than recall — add SentenceTransformerRerank after retrieval.
- Long documents split into fine-grained chunks where individual chunks lack context — use HierarchicalNodeParser + AutoMergingRetriever.
- Multi-hop or multi-perspective queries where a single query may miss relevant phrasing — QueryFusionRetriever with num_queries=2-3.

## Skip If (ANY kills it)

- Small corpora (<500 nodes) — vector search alone is sufficient and cheaper.
- Latency budget under 200 ms — cross-encoder reranking adds 100-500 ms on CPU; skip or use Cohere Rerank API.
- Index was not built with HierarchicalNodeParser — AutoMergingRetriever fails silently without parent nodes.
- Cost is the primary constraint — QueryFusionRetriever with num_queries=4 fires 4 LLM calls per user query; set num_queries=2 or disable query expansion entirely.

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
