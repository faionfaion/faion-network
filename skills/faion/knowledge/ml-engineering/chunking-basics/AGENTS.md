# Chunking Basics

## Summary

**One-sentence:** Pick a chunk-size + overlap + splitter strategy for a RAG corpus by content type, measured in tiktoken tokens not words, with metadata attached at creation time.

**One-paragraph:** Chunking splits documents into smaller pieces for embedding and retrieval. Strategy must match content type — Markdown by headers, code by AST, prose by sentence or recursive splitter. Default starting point is chunk_size=500 tokens with 50-token overlap; legal/technical needs 1000–1500, QA needs 200–400. Token counts are measured with tiktoken; word counts diverge by ~30%. Source, page, chunk_index, strategy metadata is attached at creation time — retrofit requires full re-index. Content-based IDs (md5 of source+index) prevent collisions on re-ingest.

**Ефективно для:** RAG engineer preparing a new corpus — closes the loop between document → embedding-ready chunks before the first index build, avoiding a costly re-chunk later.

## Applies If (ALL must hold)

- Preparing documents for a RAG pipeline or semantic search system.
- Documents are longer than 200 tokens each.
- Retrieval queries map to chunks (not full documents).
- A representative query set is available for benchmarking the chosen strategy.

## Skip If (ANY kills it)

- Source documents are already structured records (key/value rows) — no chunking needed.
- Content is code — load [[chunking-code-ast]] instead, regex/sentence splitters destroy function boundaries.
- Documents are ultra-short (<200 tokens) — chunking adds overhead with no retrieval gain.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Document corpus | text / markdown / pdf-extracted | upstream ingestion |
| Tokenizer | tiktoken encoding name | match the target embedding model |
| Representative query set (≥5) | text list | retrieval benchmark |
| Pre-cleaning pipeline | code | strip headers/footers/boilerplate |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/embedding-models` | Defines the tokenizer / max-input that constrains chunk_size. |
| `geek/ai/rag-engineer/rag-architecture` | Outer pipeline this chunker plugs into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: tiktoken measurement, default 500/50, content-type routing, metadata at creation, content-based IDs, version on strategy change | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for a chunk: id, text, token_count, source, page, chunk_index, strategy, version | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: mid-sentence splits, no overlap, one-size-fits-all, too small (<200), too large (>2000) | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: detect type → pick splitter → measure → tag metadata → benchmark | ~700 |
| `content/06-decision-tree.xml` | essential | Routes content-type → splitter and chunk-size band | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect-content-type` | haiku | Classification on file extension + header signal. |
| `apply-splitter` | haiku | Mechanical execution once strategy chosen. |
| `benchmark-retrieval` | sonnet | Multi-query retrieval-quality judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/recursive_chunker.py` | RecursiveChunker reference with token-accurate measurement and overlap. |
| `templates/chunk-schema.json` | JSON Schema for one chunk record emitted by the pipeline. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-basics.py` | Validate emitted chunk list against the schema; flag chunks outside the size band; verify deterministic IDs. | After chunker run, before the embedding step. |

## Related

- [[chunking-code-ast]] — code-specific path.
- [[chunking-document-structure]] — Markdown/HTML structure-aware splitter.
- [[chunking-semantic]] — embedding-similarity boundary detection.
- [[chunking-production-service]] — wraps chunkers into a production service.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by content type (code / markdown / html / prose) and corpus profile (legal/technical vs QA vs general) to the splitter + size band. Use it before writing any pipeline code so the chunker choice is explicit and auditable.
