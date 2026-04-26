# Rerank Before Reasoning (Two-Stage Retrieval)

## Summary

When an agent retrieves context for a strong-model reasoning step, never feed the raw vector-search top-K straight into the LLM. Insert a small cross-encoder reranker between the embedding model and the reasoner: retrieve 50-200 candidates with cheap embeddings, rerank with a small cross-encoder (Cohere Rerank, BGE-reranker, Voyage rerank-2), keep top 5-10, then call the expensive model. The two-stage pattern preserves recall from a wide first pass while delivering the precision the reasoner depends on.

## Why

Embedding-only retrieval ranks chunks by surface similarity — which is too coarse for hard queries with negation, multi-hop intent, or domain jargon. A cross-encoder takes the (query, chunk) pair as joint input and produces a calibrated relevance score, lifting retrieval precision @10 by 10-20 percentage points on enterprise benchmarks (Pinecone, ZeroEntropy, Cohere). The economics are favourable: rerankers cost a fraction of a cent per 100 candidates and add 50-150 ms of latency, while a single Opus call on bad context can cost orders of magnitude more and still return wrong. The bottleneck of an Agentic RAG pipeline is almost always retrieval precision, not reasoning.

## When To Use

- Any RAG agent or knowledge-base lookup where retrieval feeds a strong reasoner.
- Corpora with at least 1k chunks where ANN top-K returns plausible-but-wrong neighbours.
- Tool-use agents that look up documentation, code, or policy and then act on it.
- Domains with negation, abbreviations, or domain-specific jargon (medical, legal, finance) where embedding-only similarity misranks.

## When NOT To Use

- Tiny corpora (under ~100 documents) — retrieve everything, skip reranking.
- Latency budgets under 200 ms where the rerank round-trip dominates.
- Pipelines that already pin the reasoner to a small model — reranker latency costs more than the precision is worth.
- High-cardinality structured lookups (SQL-style) where deterministic filters do the work better and cheaper.

## Content

| File | What's inside |
|------|---------------|
| `content/01-two-stage-pipeline.xml` | The retrieve-then-rerank pipeline, candidate window, and the precision/latency trade. |
| `content/02-reranker-choice.xml` | How to pick a reranker (Cohere, BGE, Voyage), evaluation harness, and refresh cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rerank_pipeline.py` | End-to-end retrieve+rerank wrapper around an embedding store and a cross-encoder. |
