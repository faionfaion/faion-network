---
slug: rag
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A framework for augmenting LLMs with real-time access to external knowledge: embed query → retrieve top-k chunks from vector store → rerank to top-5 → inject context into prompt → generate with citations.
content_id: "3328b6fffebf5dd2"
tags: [rag, retrieval, embeddings, chunking, reranking]
---
# RAG (Retrieval-Augmented Generation)

## Summary

**One-sentence:** A framework for augmenting LLMs with real-time access to external knowledge: embed query → retrieve top-k chunks from vector store → rerank to top-5 → inject context into prompt → generate with citations.

**One-paragraph:** A framework for augmenting LLMs with real-time access to external knowledge: embed query → retrieve top-k chunks from vector store → rerank to top-5 → inject context into prompt → generate with citations. Always rerank (retrieve top-20, reduce to top-5); always include a "no information" path when retrieval fails; always include source metadata in chunks for citations.

## Applies If (ALL must hold)

- The application needs to answer questions about documents not in the model's training data
- Knowledge is updated frequently (daily/weekly) and retraining is impractical
- Users need source citations to verify claims
- The knowledge base is too large to fit in a single context window (more than a few hundred pages)
- Multi-tenant system where each tenant has a separate knowledge base
- Cost constraint: RAG is substantially cheaper than fine-tuning for factual recall tasks

## Skip If (ANY kills it)

- Knowledge is behavioral (writing style, persona, domain jargon) rather than factual — use fine-tuning
- The corpus is fewer than 50 documents that can all fit in a single long-context prompt — skip retrieval entirely
- Latency budget is under 200ms — retrieval + reranking adds 100-500ms overhead
- The task is pure reasoning on data already in the prompt — adding retrieval introduces noise

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
