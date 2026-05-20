---
slug: chunking-basics
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Chunking is the process of splitting documents into smaller pieces for embedding and retrieval.
content_id: "cdbfc89bc6287501"
tags: [chunking, rag, document-processing, embeddings, retrieval]
---
# Chunking Basics

## Summary

**One-sentence:** Chunking is the process of splitting documents into smaller pieces for embedding and retrieval.

**One-paragraph:** Chunking is the process of splitting documents into smaller pieces for embedding and retrieval. The chunking strategy significantly impacts RAG performance - too large chunks dilute relevance, too small chunks lose context.

## Applies If (ALL must hold)

- Preparing documents for RAG pipelines
- Building semantic search systems
- Processing long documents for LLMs
- Creating knowledge bases

## Skip If (ANY kills it)

- Source documents are already structured records - no chunking needed
- Content is code - use AST-based splitting rather than sentence/paragraph splitters
- Documents are ultra-short (less than 200 tokens each) - chunking adds overhead
- Legal or medical content requiring sentence-level precision - semantic chunking required

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
