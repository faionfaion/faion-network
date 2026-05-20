---
slug: reranking-two-stage
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models.
content_id: "6009c66892a5f757"
tags: [reranking, rag, cross-encoder, retrieval, bi-encoder]
---
# Two-Stage Retrieval with Cross-Encoder Reranking

## Summary

**One-sentence:** Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models.

**One-paragraph:** Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models. While first-stage retrieval prioritizes speed (bi-encoders), reranking uses slower but more accurate cross-encoders to improve result quality. The two stages work together: fast vector search retrieves candidates, cross-encoder scores each (query, doc) pair jointly for high accuracy.

## Applies If (ALL must hold)

- Initial retrieval returns noisy results and top-k precision must improve.
- High-precision requirements (legal, medical, compliance) where the top result must be correct.
- After hybrid search to reconcile BM25 + vector rankings into a single ordered list.
- When latency budget exceeds 200ms per query and quality is the priority metric.
- Improving RAG answer accuracy when initial retrieval recall is adequate but ranking is poor.

## Skip If (ANY kills it)

- Latency-critical paths with <50ms budget — cross-encoders add 100-500ms per call.
- Candidate pool is already 5 or fewer results — overhead exceeds benefit.
- Simple keyword lookup tasks — BM25 alone outperforms reranking for exact-match queries.
- Corpus is multilingual and no suitable multilingual cross-encoder exists for the language mix.

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
