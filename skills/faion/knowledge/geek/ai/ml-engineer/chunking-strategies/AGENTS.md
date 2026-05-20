---
slug: chunking-strategies
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Chunking splits documents into semantically meaningful pieces for embedding and retrieval.
content_id: "017c45a13b6b1ab9"
tags: [chunking, rag, embeddings, retrieval, ingestion]
---
# Chunking Strategies for RAG

## Summary

**One-sentence:** Chunking splits documents into semantically meaningful pieces for embedding and retrieval.

**One-paragraph:** Chunking splits documents into semantically meaningful pieces for embedding and retrieval. The right strategy improves retrieval precision by 30-40%. Decision rule: if short (<1000 tokens) → no chunking; if code → code-aware (AST); if structured (MD/HTML) → structure-based; if context-critical (legal/medical) → semantic; default → recursive with 15% overlap.

## Applies If (ALL must hold)

- Building or improving a RAG ingestion pipeline where retrieval recall or precision is suboptimal
- Corpus contains mixed document types (code, markdown, PDFs, legal text) that need different splitting logic
- Current chunking causes hallucinations because LLM receives incomplete context at chunk boundaries
- Scaling to a large corpus where embedding cost per chunk matters
- Migrating from document-level embedding to chunk-level retrieval

## Skip If (ANY kills it)

- Documents are short (<500 tokens each) — embed at document level, no chunking needed
- Prototype with <100 documents — use RecursiveCharacterTextSplitter defaults; optimize later
- Cost is the primary constraint and documents are uniform — fixed-size is fastest and cheapest
- Late chunking (Jina embeddings) is available and documents fit in the model's context window — late chunking outperforms all others for contextual coherence

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
