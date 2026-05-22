---
slug: reranking-two-stage
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Designs the two-stage retrieve→rerank flow: fast ANN top-50 then cross-encoder rerank to top-5.
content_id: "6009c66892a5f757"
complexity: medium
produces: decision-record
est_tokens: 2800
tags: [reranking, rag, cross-encoder, retrieval, bi-encoder]
---
# Two-Stage Retrieval with Cross-Encoder Reranking

## Summary

**One-sentence:** Designs the two-stage retrieve→rerank flow: fast ANN top-50 then cross-encoder rerank to top-5.

**One-paragraph:** Reranking is a second-stage retrieval technique that refines initial search results using more sophisticated models. The first stage uses a bi-encoder ANN for fast recall (top-50 candidates), the second stage uses a cross-encoder for precision (rerank to top-5). The split trades recall (bi-encoder) and precision (cross-encoder) without paying full cross-encoder cost on the entire corpus.

**Ефективно для:** інженерів, які пишуть design доку про two-stage RAG retrieval до того, як обирати конкретну модель і код.

## Applies If (ALL must hold)

- RAG pipeline where precision@5 needs to improve over bi-encoder-only.
- Latency budget allows 100-300ms second stage.
- Test set shows MRR is bounded by ranking, not by missing recall.

## Skip If (ANY kills it)

- Recall@50 < 0.5 — fix recall first (chunking, embedding, hybrid) before rerank.
- Latency budget < 200ms total — no room for second stage.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Bi-encoder ANN retrieval | service | vector-database-setup |
| Latency budget | ms | product |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/vector-database-setup` | First-stage retrieval is bi-encoder ANN. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Benchmark recall and precision | haiku | Mechanical eval. |
| Draft design record | sonnet | Trade-off framing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/two-stage-design.md` | Design record skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reranking-two-stage.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[reranking-models]]
- [[reranking-pipeline-integration]]
- [[rag-architecture]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides single-stage vs two-stage based on recall and latency budget. Each leaf references a rule id from `01-core-rules.xml`.
