---
slug: hybrid-search
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a hybrid-search config (BM25 + vector + RRF fusion, optional cross-encoder rerank, query-adaptive alpha) for a RAG retriever with measured precision uplift.
content_id: "e5ee49fb4ced3c60"
complexity: medium
produces: config
est_tokens: 3600
tags: [hybrid-search, rag, vector-search, bm25, fusion]
---
# Hybrid Search — BM25 + Vector with RRF

## Summary

**One-sentence:** Picks BM25 + dense fusion (RRF k=60 default, linear with tuned alpha as fallback), assigns query-adaptive alpha by query shape, and decides whether a cross-encoder reranker is justified.

**One-paragraph:** Pure vector misses exact terms (product codes, error strings, names); pure BM25 misses paraphrases. Hybrid + RRF captures both at ~20% extra latency. The methodology output is a retrieval config: which fusion (RRF vs linear), which alpha schedule, native endpoint vs two-call, and whether to add cross-encoder rerank (Cohere / bge-reranker-v2-m3). Benchmark target: precision@10 ≥ 0.85.

**Ефективно для:**

- RAG над технічною документацією — error codes + concepts змішані; обидва retrieverʼа потрібні.
- Enterprise search — користувачі чергують точні запити (SKU, account number) з природньою мовою.
- Заміна старого BM25 на семантику без втрати exact match — додаєш vector, фʼюзиш через RRF.
- Legal / compliance — exact statute number + контекст; ні vector, ні BM25 сам не вистачає.

## Applies If (ALL must hold)

- Corpus ≥ 1k documents.
- Queries mix natural language and exact terms (codes, names, statute numbers).
- Vector-only precision@10 &lt; 0.75 measured on a held-out query set.

## Skip If (ANY kills it)

- Conversational-only queries — pure vector is enough, hybrid adds latency for no precision gain.
- Latency SLO &lt; 20 ms — hybrid + fusion costs 40-100 ms.
- Single-store stack (Elasticsearch native kNN + BM25) already covers it natively.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Corpus + embedding index | vector DB | `vector-database-setup` |
| Held-out query set with relevance labels | JSONL | eval team |
| Latency SLO | float ms | `slo-doc` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `vector-databases` | Determines which native hybrid endpoint is available. |
| `chunking-strategies` | Chunk size drives BM25 quality. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: rrf-default, native-over-manual, query-adaptive-alpha, rerank-top100, precision-floor | 1000 |
| `content/02-output-contract.xml` | essential | Schema for hybrid-search-config.json | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: unnormalised-linear, top-10-rerank, fixed-alpha, two-call-when-native-exists | 800 |
| `content/04-procedure.xml` | essential | 5 steps: baseline → fusion choice → alpha schedule → optional rerank → bench | 600 |
| `content/06-decision-tree.xml` | essential | Fusion + rerank decision tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick_fusion_method` | haiku | Mostly deterministic. |
| `tune_alpha_schedule` | sonnet | Reasoning over query type distribution. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hybrid_search_qdrant.py` | Qdrant native FusionQuery example |
| `templates/_smoke-test.py` | Minimum benchmark runner |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hybrid-search.py` | Validate hybrid-search-config.json | Pre-deploy gate |

## Related

- [[vector-databases]] — native hybrid endpoint inventory
- [[chunking-strategies]] — BM25 quality depends on chunking
- [[model-evaluation]] — eval harness that measures precision@10

## Decision tree

See `content/06-decision-tree.xml`. Branches on vector DB capability (native vs manual), corpus size, and rerank latency budget.
