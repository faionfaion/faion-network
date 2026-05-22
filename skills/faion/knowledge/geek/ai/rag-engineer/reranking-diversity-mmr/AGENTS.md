---
slug: reranking-diversity-mmr
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Maximal Marginal Relevance (MMR) reranking selects documents that are both relevant to the query and dissimilar to already-selected documents.
content_id: "881e7fb271a64eb8"
tags: [reranking, mmr, diversity, rag, retrieval]
---
# Diversity-Aware Reranking with Maximal Marginal Relevance (MMR)

## Summary

**One-sentence:** Maximal Marginal Relevance (MMR) reranking selects documents that are both relevant to the query and dissimilar to already-selected documents.

**One-paragraph:** Maximal Marginal Relevance (MMR) reranking selects documents that are both relevant to the query and dissimilar to already-selected documents. Unlike pure relevance reranking, MMR prevents returning multiple nearly identical passages that waste the LLM context window without adding new information.

## Applies If (ALL must hold)

- Corpora where documents cluster around a few popular topics and top-k results are near-duplicates of each other.
- Long-context RAG where the LLM receives 5-10 passages and redundancy wastes context budget.
- Question-answering over documents that repeat the same fact multiple times (e.g., legal contracts, news archives).
- When user complaints indicate the LLM gives repetitive answers that seem to all say the same thing.

## Skip If (ANY kills it)

- When query asks for a single precise fact — diversity hurts precision in this case; use pure relevance reranking.
- When the corpus is already highly diverse and there is no redundancy problem — MMR adds cost without benefit.
- When document embeddings were discarded after indexing — MMR requires embeddings at rerank time (recomputation doubles cost).
- Latency-critical paths — MMR requires an embedding call for every candidate document in addition to the relevance scoring step.

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
