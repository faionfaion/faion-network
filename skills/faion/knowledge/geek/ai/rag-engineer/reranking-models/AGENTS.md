---
slug: reranking-models
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Two-stage retrieval: fast ANN retrieves top-50 candidates, then a reranker (cross-encoder or API service) rescores them to return top-5 for generation.
content_id: "eaef26648b495581"
tags: [rag, reranking, cross-encoder, retrieval, vector-search]
---
# Reranking Models

## Summary

**One-sentence:** Two-stage retrieval: fast ANN retrieves top-50 candidates, then a reranker (cross-encoder or API service) rescores them to return top-5 for generation.

**One-paragraph:** Two-stage retrieval: fast ANN retrieves top-50 candidates, then a reranker (cross-encoder or API service) rescores them to return top-5 for generation. Covered: Cohere Rerank, Jina Rerank, Voyage AI, LLM-based scoring (GPT-4o), local cross-encoders (sentence-transformers), and a production RerankerService with fallback to original ordering on timeout or error.

## Applies If (ALL must hold)

- RAG pipelines where first-stage precision is low (top-5 does not contain the answer but top-50 does)
- Two-stage retrieval pattern: ANN (k=50-100) → rerank to top-5 for generation
- Domain-specific corpora where embedding similarity scores are poorly calibrated (legal, medical, code)
- Multilingual retrieval where query and document languages may differ
- Pipelines tolerating 100-400ms additional latency per query for precision gains

## Skip If (ANY kills it)

- First-stage precision@5 is already above 0.85 — reranking adds latency and cost with diminishing returns
- Total latency SLA is <100ms — even fast local cross-encoders add 20-50ms
- Chunk corpus is very short (<200 chars per chunk) — cross-encoders underperform on very short texts
- Cost is the primary constraint and a small local model is not viable
- Queries are purely keyword-based — BM25 or hybrid search already handles these well

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
