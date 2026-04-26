# Reranking Models

## Summary

Two-stage retrieval: fast ANN retrieves top-50 candidates, then a reranker (cross-encoder or API service) rescores them to return top-5 for generation. Covered: Cohere Rerank, Jina Rerank, Voyage AI, LLM-based scoring (GPT-4o), local cross-encoders (sentence-transformers), and a production RerankerService with fallback to original ordering on timeout or error.

## Why

First-stage ANN retrieval optimizes for recall (the right answer is somewhere in the top-50); reranking optimizes precision (the right answer is in the top-5 passed to generation). Cross-encoders score query-document pairs jointly, capturing interactions the bi-encoder embedding step misses. This two-stage approach achieves better precision@5 than a single-stage ANN at top-5 at lower latency cost than running a cross-encoder over the full corpus.

## When To Use

- RAG pipelines where first-stage precision is low (top-5 does not contain the answer but top-50 does)
- Two-stage retrieval pattern: ANN (k=50-100) → rerank to top-5 for generation
- Domain-specific corpora where embedding similarity scores are poorly calibrated (legal, medical, code)
- Multilingual retrieval where query and document languages may differ
- Pipelines tolerating 100-400ms additional latency per query for precision gains

## When NOT To Use

- First-stage precision@5 is already above 0.85 — reranking adds latency and cost with diminishing returns
- Total latency SLA is &lt;100ms — even fast local cross-encoders add 20-50ms
- Chunk corpus is very short (&lt;200 chars per chunk) — cross-encoders underperform on very short texts
- Cost is the primary constraint and a small local model is not viable
- Queries are purely keyword-based — BM25 or hybrid search already handles these well

## Content

| File | What's inside |
|------|---------------|
| `content/01-api-services.xml` | Cohere, Jina, Voyage AI, and LLM-based reranking code examples |
| `content/02-local-and-production.xml` | Local cross-encoders, model selection guide, LangChain integration, and pitfalls |

## Templates

| File | Purpose |
|------|---------|
| `templates/reranker_service.py` | RerankerService with cross-encoder + Cohere dispatch, fallback, and FastAPI endpoint |
