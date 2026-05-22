# purpose: minimum viable filled architecture record for a docs Q&A RAG
# consumes: technical-docs corpus with 100M tokens, weekly updates
# produces: example downstream impl can follow directly
# depends-on: templates/rag-architecture.md.tmpl
# token-budget-impact: zero at runtime

# RAG Architecture Decision Record — Docs Q&A v1

Owner: alice
Date: 2026-05-22

## 1. Chunking
- Strategy: header
- Size: 1024 tokens
- Overlap: 200 tokens

## 2. Embeddings
- Model: text-embedding-3-large
- Dimensions: 3072

## 3. Vector DB
- Choice: qdrant

## 4. Retrieval
- Mode: hybrid
- Top-K pool: 20
- Reranker: cohere-rerank-3 → top-K final: 5

## 5. Context
- Budget tokens: 5000
- Ordering: relevance

## 6. Metrics & Gates
- MRR@10 target: 0.75
- Faithfulness target: 0.92
- Latency p95: 1500ms
- Cost per query: $0.012

## 7. Sign-off
- Owner: alice
- Date: 2026-05-22
- Revisit date: 2026-08-22
