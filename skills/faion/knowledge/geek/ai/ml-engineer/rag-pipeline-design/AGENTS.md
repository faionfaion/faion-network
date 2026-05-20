---
slug: rag-pipeline-design
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production RAG pipelines ground LLM responses in domain-specific data through a retrieval layer (embedding + vector search + reranking) followed by synthesis.
content_id: "dd5c690bb2f48cc0"
tags: [rag, pipeline, architecture, hybrid-search, production]
---
# RAG Pipeline Design

## Summary

**One-sentence:** Production RAG pipelines ground LLM responses in domain-specific data through a retrieval layer (embedding + vector search + reranking) followed by synthesis.

**One-paragraph:** Production RAG pipelines ground LLM responses in domain-specific data through a retrieval layer (embedding + vector search + reranking) followed by synthesis. Use hybrid search (vector + BM25) as the default; it improves recall@10 by 15-25% over pure vector search. Choose the architecture tier — Naive, Advanced, Modular, or Agentic — based on query complexity and data source heterogeneity.

## Applies If (ALL must hold)

- LLM needs access to private, domain-specific, or frequently updated knowledge not in training data
- Application requires citations: users need to verify sources for trust
- Knowledge base exceeds the model's context window (>200K tokens of documents)
- Multiple heterogeneous data sources (PDFs, SQL DB, APIs) need unified semantic search
- Answer accuracy on domain queries is below acceptable threshold with prompt engineering alone

## Skip If (ANY kills it)

- Knowledge is fully covered by the model's training and does not change — prompt engineering suffices
- Retrieval latency >500ms is unacceptable and caching cannot compensate (e.g., real-time trading)
- Corpus is fewer than 50 documents — just include them all in the context window (simpler, often more accurate)
- Team lacks infra to maintain a vector database and embedding pipeline — use a managed RAG service (LlamaCloud, Azure AI Search)
- Queries are always the same — pre-generate answers and cache them instead of building a full pipeline

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

- parent skill: `geek/ai/ml-engineer/`
