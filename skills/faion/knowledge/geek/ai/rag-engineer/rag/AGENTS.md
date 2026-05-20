---
slug: rag
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A Retrieval-Augmented Generation pipeline ingests documents (load → chunk → embed → store), retrieves relevant chunks for a query (embed → vector search → rerank), and generates a grounded answer with source citations.
content_id: "3328b6fffebf5dd2"
tags: [rag, retrieval, generation, vector-search, llm]
---
# RAG Pipeline

## Summary

**One-sentence:** A Retrieval-Augmented Generation pipeline ingests documents (load → chunk → embed → store), retrieves relevant chunks for a query (embed → vector search → rerank), and generates a grounded answer with source citations.

**One-paragraph:** A Retrieval-Augmented Generation pipeline ingests documents (load → chunk → embed → store), retrieves relevant chunks for a query (embed → vector search → rerank), and generates a grounded answer with source citations. Key invariants: chunk quality bounds retrieval quality; hybrid search is the default; reranking is required for production accuracy; evaluate with MRR > 0.7 and faithfulness > 0.9 before launch.

## Applies If (ALL must hold)

- Agent needs to answer questions grounded in a private or frequently-updated document corpus.
- Reducing hallucinations on domain-specific topics not in the model's training data.
- Building a knowledge assistant over PDFs, docs, wikis, or code repositories.
- Source corpus is too large to fit in a single context window.
- Citation / source attribution is required for compliance or user trust.

## Skip If (ANY kills it)

- Document set is tiny (less than 50 chunks) and fits in context — just stuff the full context.
- Questions are purely general knowledge — RAG adds retrieval latency with no accuracy gain.
- Real-time data (stock prices, live APIs) — RAG retrieves static indexed content; use live tool calls.
- Query volume is very low and latency is critical — embed + retrieve round-trip adds 200–600ms.

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
