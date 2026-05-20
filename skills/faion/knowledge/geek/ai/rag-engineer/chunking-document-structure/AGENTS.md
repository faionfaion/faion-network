---
slug: chunking-document-structure
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: MarkdownChunker splits documents at header boundaries while propagating parent headers into child chunks as a header_path.
content_id: "5e0219f312b80392"
tags: [chunking, markdown, html, document-structure, rag]
---
# Document Structure Chunking (Markdown and HTML)

## Summary

**One-sentence:** MarkdownChunker splits documents at header boundaries while propagating parent headers into child chunks as a header_path.

**One-paragraph:** MarkdownChunker splits documents at header boundaries while propagating parent headers into child chunks as a header_path. HTMLChunker uses BeautifulSoup to split by section/article/div elements. Both strategies preserve navigational context inside every chunk, improving embedding quality and retrieval traceability.

## Applies If (ALL must hold)

- Processing Markdown documentation sites, wikis, or README files where header hierarchy must be preserved.
- Indexing HTML pages that use semantic sectioning elements (section, article).
- Any corpus where retrieval queries reference section context ("what does the authentication section say about tokens?").
- Documentation RAG pipelines for LLM tool/API references, where a function's section parent provides critical context.

## Skip If (ANY kills it)

- Flat HTML pages with no sectioning elements — HTMLChunker produces one giant chunk because there are no div/section/article boundaries.
- Code files — use chunking-code-ast; MarkdownChunker can produce very small chunks on single-line code blocks that embed poorly.
- Unstructured prose (news, essays) without headers — use chunking-semantic or RecursiveChunker instead.
- MarkdownChunker without min_chunk_size guard on documentation with many shallow headers — single-line list items produce near-zero vectors that pollute nearest-neighbor results.

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
