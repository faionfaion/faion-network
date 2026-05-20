---
slug: rerank-before-reasoning
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When an agent retrieves context for a strong-model reasoning step, never feed the raw vector-search top-K straight into the LLM.
content_id: "14b0e739510c984f"
tags: [rag, retrieval, reranker, cross-encoder, embedding]
---
# Rerank Before Reasoning (Two-Stage Retrieval)

## Summary

**One-sentence:** When an agent retrieves context for a strong-model reasoning step, never feed the raw vector-search top-K straight into the LLM.

**One-paragraph:** When an agent retrieves context for a strong-model reasoning step, never feed the raw vector-search top-K straight into the LLM. Insert a small cross-encoder reranker between the embedding model and the reasoner: retrieve 50-200 candidates with cheap embeddings, rerank with a small cross-encoder (Cohere Rerank, BGE-reranker, Voyage rerank-2), keep top 5-10, then call the expensive model. The two-stage pattern preserves recall from a wide first pass while delivering the precision the reasoner depends on.

## Applies If (ALL must hold)

- Any RAG agent or knowledge-base lookup where retrieval feeds a strong reasoner.
- Corpora with at least 1k chunks where ANN top-K returns plausible-but-wrong neighbours.
- Tool-use agents that look up documentation, code, or policy and then act on it.
- Domains with negation, abbreviations, or domain-specific jargon (medical, legal, finance) where embedding-only similarity misranks.

## Skip If (ANY kills it)

- Tiny corpora (under ~100 documents) — retrieve everything, skip reranking.
- Latency budgets under 200 ms where the rerank round-trip dominates.
- Pipelines that already pin the reasoner to a small model — reranker latency costs more than the precision is worth.
- High-cardinality structured lookups (SQL-style) where deterministic filters do the work better and cheaper.

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

- parent skill: `geek/ai/ai-agents/`
