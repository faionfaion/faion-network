---
slug: rag-implementation
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Complete production RAG pipeline: document loading (txt/md/pdf/directory), chunking (fixed-size, sentence, paragraph, semantic, Markdown-header), embedding, Chroma-backed vector storage, retrieval, query enhancement (expansion, HyDE, rewrite), and LLM generation with strict "answer only from context" system prompt.
content_id: "99955bd1c5c37238"
tags: [rag, implementation, pipeline, chunking, production]
---
# RAG Implementation

## Summary

**One-sentence:** Complete production RAG pipeline: document loading (txt/md/pdf/directory), chunking (fixed-size, sentence, paragraph, semantic, Markdown-header), embedding, Chroma-backed vector storage, retrieval, query enhancement (expansion, HyDE, rewrite), and LLM generation with strict "answer only from context" system prompt.

**One-paragraph:** Complete production RAG pipeline: document loading (txt/md/pdf/directory), chunking (fixed-size, sentence, paragraph, semantic, Markdown-header), embedding, Chroma-backed vector storage, retrieval, query enhancement (expansion, HyDE, rewrite), and LLM generation with strict "answer only from context" system prompt. Implemented as single RAGPipeline class with separate ingest and query paths.

## Applies If (ALL must hold)

- Building a question-answering system over proprietary documents (PDFs, Markdown, text).
- LLM needs to answer questions about data post-dating its training cutoff.
- Reducing hallucinations by grounding generation in retrieved facts.
- Products requiring citations or source attribution alongside answers.
- Knowledge-base chatbots where answers must come only from a controlled corpus.

## Skip If (ANY kills it)

- Corpus changes faster than re-ingestion can keep up — design a streaming update strategy first.
- Purely conversational queries with no factual grounding need — RAG adds latency and cost with no benefit.
- Entire knowledge base fits in context window — just include it directly.
- Structured data questions (revenue figures, counts) — SQL + function-calling beats RAG for tabular data.

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
