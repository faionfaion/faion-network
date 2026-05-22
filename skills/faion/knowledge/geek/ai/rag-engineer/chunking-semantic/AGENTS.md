---
slug: chunking-semantic
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Splits text where cosine similarity between adjacent sentence embeddings drops below a threshold, so chunks capture coherent concepts instead of arbitrary token windows.
content_id: "2e1ca82bbd75475a"
complexity: deep
produces: code
est_tokens: 3800
tags: [chunking, semantic-chunking, embeddings, rag, nlp]
---
# Chunking — Semantic (Embedding Similarity)

## Summary

**One-sentence:** Splits text where cosine similarity between adjacent sentence embeddings drops below a threshold, so chunks capture coherent concepts instead of arbitrary token windows.

**One-paragraph:** SemanticChunker embeds every sentence, computes pairwise cosine similarity for adjacent pairs, and places a boundary where similarity drops below `similarity_threshold` (default 0.75). Size guards subsplit chunks exceeding max_chunk_size and merge those below min_chunk_size. Empty / 1-sentence documents return a single chunk without calling the embedding function. Uses the same embedding model as retrieval so chunk boundaries align with the query-time similarity signal.

**Ефективно для:** RAG engineer running legal / medical / scientific RAG where mid-concept splits ruin answer quality — closes the gap between structure-blind fixed-size chunking and the conceptual flow of prose.

## Applies If (ALL must hold)

- High-stakes retrieval domain (legal / medical / scientific) where mid-concept splits degrade answers.
- Prose-heavy corpus without reliable headers or code structure.
- Embedding API budget allows one call per sentence at index time.
- Sentence tokenizer is reliable for the corpus language (NLTK punkt, spaCy).

## Skip If (ANY kills it)

- Quick prototyping with ≤10k docs — [[chunking-basics]] recursive is sufficient.
- Corpus language lacks reliable sentence tokenization — semantic boundaries become noise.
- Structured documents (Markdown / HTML / code) — load the structure-specific chunker; structure is a stronger signal than similarity.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Embedding function | callable str -> list[float] | matches retrieval model |
| Sentence tokenizer | nltk punkt / spaCy | language-appropriate |
| similarity_threshold | float (0..1) | default 0.75 |
| max_chunk_size / min_chunk_size | tokens | size guards |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/chunking-basics` | Token measurement + metadata invariants. |
| `geek/ai/rag-engineer/embedding-generation` | Embedding function semantics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: same model as retrieval, threshold band, size guards, empty-doc short-circuit, version | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema with similarity_threshold + embedding_model fields | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: model drift, no size guard, oversized sentences, mismatched tokenizer | ~700 |
| `content/04-procedure.xml` | deep | 6-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus profile + budget | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sentence-tokenize` | haiku | Mechanical text split. |
| `embed-sentences` | embedding-model | Direct embed call. |
| `threshold-tuning` | sonnet | Judgement on threshold across a sample. |

## Templates

| File | Purpose |
|------|---------|
| `templates/semantic_chunker.py` | SemanticChunker reference with size guards and empty-doc handling. |
| `templates/semantic-chunk-schema.json` | JSON Schema for one semantic chunk. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-semantic.py` | Verify schema; flag chunks below min or above max; check embedding_model field present. | After chunker run. |

## Related

- [[chunking-basics]] · [[chunking-document-structure]] · [[chunking-code-ast]] · [[chunking-production-service]] · [[embedding-generation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether semantic chunking is justified (high-stakes domain + budget + reliable tokenizer) or whether the cheaper recursive splitter from chunking-basics suffices.
