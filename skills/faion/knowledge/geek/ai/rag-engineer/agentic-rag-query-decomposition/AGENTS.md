---
slug: agentic-rag-query-decomposition
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A planning agent decomposes a complex query into 2–4 atomic sub-queries that can each be answered with a single retrieval call.
content_id: "532be04b3a0ede2b"
tags: [rag, agentic, query-decomposition, multi-hop, planning]
---
# Agentic RAG — Query Decomposition

## Summary

**One-sentence:** A planning agent decomposes a complex query into 2–4 atomic sub-queries that can each be answered with a single retrieval call.

**One-paragraph:** A planning agent decomposes a complex query into 2–4 atomic sub-queries that can each be answered with a single retrieval call. Independent sub-queries run in parallel; results are merged and passed to the generator. This pattern maps directly to the "plan" node in a LangGraph agentic RAG workflow.

## Applies If (ALL must hold)

- The user query contains multiple distinct information needs (comparison, multi-part, "and also" structure).
- Multi-hop QA: the answer requires combining facts from disjoint documents.
- Research synthesis where the question has a known structure (e.g., compare A vs B across dimensions C, D, E).
- Legal compliance or fact-checking where exhaustive coverage of multiple sub-topics is required.

## Skip If (ANY kills it)

- Simple factual lookups — decomposition adds an extra LLM call with no benefit.
- Queries with a single clear information need — decompose into one sub-query is a no-op and wastes a round-trip.
- When the sub-queries are not known upfront but emerge from retrieved context — use iterative retrieval instead.

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
