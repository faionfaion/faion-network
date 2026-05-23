# Chunking — Document Structure (Markdown / HTML)

## Summary

**One-sentence:** Splits Markdown by header hierarchy and HTML by sectioning elements, propagating parent header paths into every chunk to preserve navigational context for retrieval.

**One-paragraph:** MarkdownChunker splits at header boundaries (`#`, `##`, `###`) and prepends the parent `header_path` (joined by ` > `) into every chunk so queries that reference section context retrieve correctly. HTMLChunker uses BeautifulSoup to walk `<section>`, `<article>`, and `<div>` boundaries. Both attach min_chunk_size guards to drop near-empty chunks (single list items) that pollute nearest-neighbour scores.

**Ефективно для:** RAG engineer indexing docs site / wiki / API reference — closes the gap between flat character chunking (loses hierarchy) and the navigational anchors users actually query with.

## Applies If (ALL must hold)

- Corpus is Markdown documentation, wiki, README, or HTML with semantic sectioning elements.
- Retrieval queries reference section context ("what does the auth section say about tokens?").
- BeautifulSoup4 is available for the HTML path.
- min_chunk_size guard is configured (default 100 tokens) to filter near-empty chunks.

## Skip If (ANY kills it)

- Corpus is unstructured prose with no headers — load [[chunking-semantic]] or [[chunking-basics]].
- Source is code — load [[chunking-code-ast]].
- Flat HTML pages with no sectioning elements — HTMLChunker emits one giant chunk; pre-split with [[chunking-basics]] recursive.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Markdown / HTML files | text | docs repo / web crawl |
| beautifulsoup4 | python pkg | `pip install beautifulsoup4` |
| Max chunk size (token band) | int | matches embedding model |
| min_chunk_size guard | int | default 100 |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/chunking-basics` | Token measurement, metadata-at-creation, content-based IDs apply here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: header_path propagation, min_chunk_size guard, BeautifulSoup for HTML, oversized-block subdivision, version bump | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema with header_path field + section_id | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: lost header_path, no min guard, regex on HTML, no oversized subdivision | ~700 |
| `content/04-procedure.xml` | medium | 5 steps: detect → walk headers/sections → propagate path → subdivide oversize → emit | ~600 |
| `content/06-decision-tree.xml` | essential | Routes file type → Markdown or HTML chunker, and chooses subdivision threshold | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect-structure` | haiku | Header / DOM pattern detection. |
| `chunk-and-tag` | haiku | Mechanical walk + metadata attach. |

## Templates

| File | Purpose |
|------|---------|
| `templates/markdown_chunker.py` | MarkdownChunker reference with header_path propagation. |
| `templates/html_chunker.py` | HTMLChunker reference using BeautifulSoup4. |
| `templates/doc-chunk-schema.json` | JSON Schema for one document-structure chunk. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-document-structure.py` | Verify chunks match schema, header_path present, min_size respected. | After chunker run. |

## Related

- [[chunking-basics]] — base invariants.
- [[chunking-code-ast]] — code path.
- [[chunking-semantic]] — fallback when no structure present.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by file type (markdown vs html vs other) and by header-density (deep hierarchy vs flat). Use it to decide whether MarkdownChunker, HTMLChunker, or a fallback to chunking-basics applies.
