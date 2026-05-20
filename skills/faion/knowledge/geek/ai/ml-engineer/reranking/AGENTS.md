---
slug: reranking
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models.
content_id: "817be12585bc88ee"
tags: [reranking, rag, cross-encoder, retrieval, information-retrieval]
---
# Reranking for RAG Systems

## Summary

**One-sentence:** Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models.

**One-paragraph:** Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models. While first-stage retrieval prioritizes speed (bi-encoders), reranking uses slower but more accurate cross-encoders to improve result quality. Cross-encoder reranking improves RAG accuracy by 20-35% while adding 200-500ms latency per query.

## Applies If (ALL must hold)

- Sufficient candidate pool — retrieve 3-10x more candidates than final top-k
- Reasonable first-stage recall — reranker cannot recover missing documents
- Latency budget — allow 100-500ms additional processing time
- Quality-sensitive application — improvement justifies added complexity
- RAG pipeline where initial vector retrieval produces noisy or inconsistent top results
- First-stage retrieval uses a fast bi-encoder and you have a latency budget of 200ms+ beyond it
- Hybrid search (BM25 + dense) needs a single score for final ranking
- Domain-critical applications: legal, medical, enterprise knowledge bases where precision matters
- Corpus size greater than 10K documents where bi-encoder recall starts to degrade
- Multi-hop reasoning — quality matters more than speed

## Skip If (ANY kills it)

- Real-time autocomplete or sub-100ms latency requirements — cross-encoder overhead is prohibitive
- Fewer than 10 candidate documents retrieved — marginal improvement does not justify cost
- Simple keyword-match use cases with deterministic answer lookup
- High-volume low-value queries where API cost exceeds quality benefit
- Latency budget less than 100ms — reranking adds 100-500ms

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
