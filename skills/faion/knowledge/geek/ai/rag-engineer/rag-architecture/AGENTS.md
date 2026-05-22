---
slug: rag-architecture
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Retrieval Augmented Generation (RAG) combines information retrieval with LLM generation to produce accurate, grounded responses.
content_id: "b44ab943fe698c41"
tags: [rag, architecture, design-patterns, vector-db, system-design]
---
# RAG Architecture

## Summary

**One-sentence:** Retrieval Augmented Generation (RAG) combines information retrieval with LLM generation to produce accurate, grounded responses.

**One-paragraph:** Retrieval Augmented Generation (RAG) combines information retrieval with LLM generation to produce accurate, grounded responses. This guide covers architecture patterns and design decisions: indexing pipeline (documents → chunking → embedding → vector store), query pipeline (query → embedding → retrieval → context → LLM → response), chunking strategies (fixed-size, sentence-based, paragraph-based, semantic, header-based), retrieval strategies (basic, hybrid, reranking, query enhancement), context management, vector database selection, quality metrics, best practices, and common pitfalls.

## Applies If (ALL must hold)

- Question answering over custom documents, deciding between chunking strategies and vector database selection.
- Chatbots with domain-specific knowledge where architecture patterns (agentic, graph, multi-index) determine quality.
- Evaluating whether RAG is the right approach vs. fine-tuning or long-context LLM.
- Diagnosing production RAG quality problems (low faithfulness, hallucinations, slow retrieval).
- Designing multi-index or agentic RAG variants that go beyond a single vector store.

## Skip If (ANY kills it)

- Data is static and small enough to fit in a single LLM context window — skip RAG, use long-context prompting.
- Questions require real-time web data — use tool-calling with search APIs instead.
- Fine-tuning already achieved acceptable accuracy on a stable, closed corpus.
- Team has no infrastructure for a vector database — consider pgvector extension on existing Postgres before introducing a new service.

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
