---
slug: chunking-production-service
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ChunkingService is a production-grade orchestration layer over SemanticChunker, MarkdownChunker, CodeChunker, and the basics-tier RecursiveChunker.
content_id: "660340dd26bfba44"
tags: [chunking, production, orchestration, rag, chunking-service]
---
# Production Chunking Service with Strategy Routing

## Summary

**One-sentence:** ChunkingService is a production-grade orchestration layer over SemanticChunker, MarkdownChunker, CodeChunker, and the basics-tier RecursiveChunker.

**One-paragraph:** ChunkingService is a production-grade orchestration layer over SemanticChunker, MarkdownChunker, CodeChunker, and the basics-tier RecursiveChunker. It accepts a ChunkingConfig with strategy, chunk_size, overlap, and min_chunk_size; dispatches to the matching chunker; attaches caller-supplied metadata to every output chunk; and falls back to word-split on any exception.

## Applies If (ALL must hold)

- Production ingestion pipelines that process mixed content types (Markdown, code, HTML, prose) in a single run.
- Any pipeline where chunking strategy should be decided per-document rather than globally for the entire corpus.
- Batch ingestion jobs that require graceful degradation on parse errors without halting the run.
- Pipelines that attach document-level metadata (source path, page number, ingestion timestamp) to every chunk for traceability.

## Skip If (ANY kills it)

- Quick prototyping with a homogeneous corpus — use RecursiveChunker directly to avoid the orchestration layer overhead.
- When semantic chunking is the only strategy needed — SemanticChunker can be used directly without ChunkingService.
- Pipelines that need to audit which strategy was actually used per document — ChunkingService's fallback path does not currently expose a strategy_used field; add it before relying on this for audit trails.

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
