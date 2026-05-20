---
slug: llamaindex-ingestion-pipeline
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LlamaIndex IngestionPipeline chains document loaders, metadata extractors, and node parsers into a single reusable pipeline.
content_id: "d8528dadb1b8a6b5"
tags: [llamaindex, ingestion, chunking, vector-store, rag]
---
# LlamaIndex Ingestion Pipeline

## Summary

**One-sentence:** LlamaIndex IngestionPipeline chains document loaders, metadata extractors, and node parsers into a single reusable pipeline.

**One-paragraph:** LlamaIndex IngestionPipeline chains document loaders, metadata extractors, and node parsers into a single reusable pipeline. Connect to a persistent vector store (Chroma or Pinecone) via StorageContext to avoid re-embedding on restart. Tune chunking strategy — SentenceSplitter for speed, SemanticSplitterNodeParser for coherence — based on query patterns.

## Applies If (ALL must hold)

- Building a production RAG system that must survive restarts without re-embedding the corpus.
- Corpus requires metadata enrichment (auto-extracted titles, summaries, keywords) for filtered retrieval.
- Multiple document types from different sources — IngestionPipeline unifies loading, parsing, and embedding in one call.
- Long documents where chunk boundary choice materially affects answer quality — compare SentenceSplitter vs SemanticSplitter.

## Skip If (ANY kills it)

- Prototype with fewer than 100 documents — VectorStoreIndex.from_documents() inline is simpler and sufficient.
- Fully dynamic data with real-time updates — LlamaIndex indexes are append-friendly but not designed for continuous stream ingestion; use a dedicated streaming pipeline.
- Cost is the hard constraint on a small corpus — metadata extractors (TitleExtractor, SummaryExtractor) fire LLM calls per document; disable them if the corpus is large and metadata is not needed.

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

- parent skill: `geek/ai/ai-agents/`
