---
slug: chunking-production-service
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Production orchestration layer that routes documents to per-type chunkers (Markdown/HTML/code/recursive), propagates document-level metadata, and falls back to word-split on exception with a logged warning.
content_id: "660340dd26bfba44"
complexity: deep
produces: code
est_tokens: 3800
tags: [chunking, production, orchestration, rag, service]
---
# Chunking — Production Service

## Summary

**One-sentence:** Production orchestration layer that routes documents to per-type chunkers (Markdown/HTML/code/recursive), propagates document-level metadata, and falls back to word-split on exception with a logged warning.

**One-paragraph:** ChunkingService takes a `ChunkingConfig(strategy, chunk_size, overlap, min_chunk_size, embedding_func?)` and a per-document `metadata` dict. It dispatches to MarkdownChunker, HTMLChunker, CodeChunker, SemanticChunker, or RecursiveChunker; attaches document-level metadata to every output chunk; and on any exception logs the failure then returns a word-split fallback with `strategy_used="fallback"`. Fail-fast on missing embedding_func for SEMANTIC strategy at construction time, not at chunk time.

**Ефективно для:** RAG engineer running batch ingest over mixed content types — closes the gap between per-document chunker wiring and a single service call the pipeline layer can rely on.

## Applies If (ALL must hold)

- Pipeline processes mixed content types (markdown, code, html, prose) in one run.
- Per-document metadata (source path, ingestion timestamp, tenant) must be on every chunk.
- Batch jobs require graceful degradation rather than total failure on parse errors.
- Operators need to distinguish fallback chunks from primary chunks for monitoring.

## Skip If (ANY kills it)

- Quick prototyping with one homogeneous content type — instantiate the chunker directly.
- Single-strategy pipelines (only semantic, or only recursive).
- No need for fallback or strategy-tagged audit trail.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| ChunkingConfig | dataclass | application config |
| Sub-chunker implementations | classes | [[chunking-basics]], [[chunking-document-structure]], [[chunking-code-ast]], [[chunking-semantic]] |
| Per-document metadata | dict | upstream ingestion |
| Structured logger | logging.Logger | application bootstrap |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/chunking-basics` | Default recursive chunker + token measurement. |
| `geek/ai/rag-engineer/chunking-document-structure` | Markdown / HTML path. |
| `geek/ai/rag-engineer/chunking-code-ast` | Code path. |
| `geek/ai/rag-engineer/chunking-semantic` | Optional semantic path. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fail-fast config validation, dispatch by strategy enum, metadata propagation, logged fallback, strategy_used in output | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema unioning per-strategy chunk shapes + service envelope | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: silent fallback, missing embedding_func discovered mid-batch, metadata loss, no strategy_used field | ~700 |
| `content/04-procedure.xml` | deep | 6-step procedure: validate config → dispatch → chunk → tag metadata → catch exceptions → log + fallback | ~700 |
| `content/05-examples.xml` | medium | ChunkingService class with all dispatch + fallback paths | ~600 |
| `content/06-decision-tree.xml` | essential | Routes content type and config to strategy or fallback | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `config-validation` | haiku | Schema check, no judgement. |
| `dispatch` | haiku | Mechanical. |
| `incident-review` | sonnet | Inspect fallback log entries for re-ingest decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunking_service.py` | ChunkingService reference with dispatch + fallback + metadata propagation. |
| `templates/chunking-service-schema.json` | JSON Schema for the service output envelope. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-production-service.py` | Verify service output envelope, check fallback chunks have a warning, metadata present on every chunk. | After each ingest batch. |

## Related

- [[chunking-basics]] · [[chunking-document-structure]] · [[chunking-code-ast]] · [[chunking-semantic]] — dispatch targets.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes based on `config.strategy` (explicit) vs auto-detect (content-type sniff). Fallback is only reachable through the exception handler, never as a default.
