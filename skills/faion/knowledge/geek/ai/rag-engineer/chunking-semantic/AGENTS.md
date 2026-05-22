---
slug: chunking-semantic
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: SemanticChunker splits text by computing embeddings for every sentence, then placing chunk boundaries where cosine similarity between adjacent sentences drops below a threshold.
content_id: "2e1ca82bbd75475a"
tags: [chunking, semantic-chunking, embeddings, rag, nlp]
---
# Semantic Chunking via Embedding Similarity

## Summary

**One-sentence:** SemanticChunker splits text by computing embeddings for every sentence, then placing chunk boundaries where cosine similarity between adjacent sentences drops below a threshold.

**One-paragraph:** SemanticChunker splits text by computing embeddings for every sentence, then placing chunk boundaries where cosine similarity between adjacent sentences drops below a threshold. Unlike fixed-size splitting, chunks capture coherent concepts rather than arbitrary byte windows.

## Applies If (ALL must hold)

- High-stakes retrieval domains (legal, medical, scientific) where splitting mid-concept degrades answer quality.
- Prose-heavy corpora (news, blog posts, academic papers) where structural markers (headers, code blocks) are absent or inconsistent.
- After baseline RecursiveChunker benchmarks show retrieval precision below acceptable threshold and document structure is absent.
- Any corpus where you already call the embedding API at index time and can absorb one embedding call per sentence.

## Skip If (ANY kills it)

- Quick prototyping — RecursiveChunker from chunking-basics is faster to wire up and sufficient for 10k docs or fewer.
- Constrained embedding budget — semantic chunking calls the embedding API once per sentence during indexing, not once per chunk; a 10k-doc corpus adds significant API cost.
- Corpora entirely in languages without NLTK punkt support — sentence tokenization silently degrades, producing sentence boundaries at wrong positions.
- Structured documents (Markdown, HTML, code) — use chunking-document-structure or chunking-code-ast instead; structure is a stronger signal than similarity.

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
