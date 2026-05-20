---
slug: agentic-rag
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Agentic RAG embeds autonomous agents into the retrieval pipeline to enable multi-hop retrieval, query routing, self-correction, and iterative refinement.
content_id: "cdb282feeb7d1121"
tags: [rag, retrieval, agents, langgraph, multi-hop, corrective-rag]
---
# Agentic RAG (RAG 2.0)

## Summary

**One-sentence:** Agentic RAG embeds autonomous agents into the retrieval pipeline to enable multi-hop retrieval, query routing, self-correction, and iterative refinement.

**One-paragraph:** Agentic RAG embeds autonomous agents into the retrieval pipeline to enable multi-hop retrieval, query routing, self-correction, and iterative refinement. Unlike traditional single-shot RAG, agents plan decompositions, grade retrieved documents, rewrite failed queries, and verify answers before returning — trading latency for higher accuracy on complex queries.

## Applies If (ALL must hold)

- Queries require multi-hop reasoning across documents
- Single-shot retrieval consistently fails for complex or ambiguous questions
- Knowledge base spans multiple heterogeneous sources (internal docs, web, APIs)
- Self-correction is essential: domain where one retrieval miss produces costly wrong answers (legal, medical, financial)
- Complex pipelines already have observability tooling (traces, per-turn cost logging)

## Skip If (ANY kills it)

- Simple factual Q&A with a single knowledge base and high recall — standard RAG is faster and cheaper
- Latency budget under 2 seconds — agentic loops add 2-10x more turns than static RAG
- The orchestration infrastructure does not exist yet — build standard RAG first, then layer agentic behavior
- Cost constraints are tight — multi-hop retrieval multiplies token usage; each agent turn = one LLM call
- No observability tooling — debugging agentic loop failures without traces is impractical

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
