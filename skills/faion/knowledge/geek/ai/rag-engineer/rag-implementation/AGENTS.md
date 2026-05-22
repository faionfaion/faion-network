---
slug: rag-implementation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Ships a production RAG pipeline: ingest, chunk, embed, Chroma-backed store, retrieve, query-enhance, answer-only-from-context with citations.
content_id: "99955bd1c5c37238"
complexity: deep
produces: code
est_tokens: 4500
tags: [rag, implementation, pipeline, chunking, production]
---
# RAG Implementation

## Summary

**One-sentence:** Ships a production RAG pipeline: ingest, chunk, embed, Chroma-backed store, retrieve, query-enhance, answer-only-from-context with citations.

**One-paragraph:** Complete production RAG pipeline: document loading (txt/md/pdf/directory), chunking (fixed-size, sentence, paragraph, semantic, Markdown-header), embedding, Chroma-backed vector storage, retrieval, query enhancement (expansion, HyDE, rewrite), and LLM generation with strict 'answer only from context' system prompt and validated citations.

**Ефективно для:** інженерів, які мають архітектурне рішення (rag-architecture) і потребують готового pipeline-коду на Chroma з ingestion + queryenhancement.

## Applies If (ALL must hold)

- Building a new RAG pipeline from scratch with Chroma + standard embedding models.
- Need to support multiple file types (txt, md, pdf, directory ingest).
- Want query enhancement (expansion / HyDE / rewrite) baked into the pipeline.
- Need cited answers with answer-only-from-context constraint.

## Skip If (ANY kills it)

- Already running production RAG on a different vector DB — use rag-architecture + vector-database-setup first.
- Need agentic / multi-hop retrieval — start with rag and add iterative loop on top.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Document corpus | txt/md/pdf paths | ingestion |
| Embedding model API key | env | infra |
| LLM API key | env | infra |
| Chroma persistence dir | path | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag` | RAG concept + rules. |
| `geek/ai/rag-engineer/chunking-basics` | Chunking strategy choice. |
| `geek/ai/rag-engineer/db-chroma` | Chroma client patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Write loader / chunker code | sonnet | Many file-type specifics. |
| Wire Chroma client | haiku | Standard SDK calls. |
| Design query-enhancement variants | sonnet | Quality trade-offs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-config.yaml` | Production RAG config skeleton. |
| `templates/rag-system-prompt.txt` | Answer-only-from-context system prompt. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-implementation.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag]]
- [[rag-architecture]]
- [[db-chroma]]
- [[chunking-basics]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether this Chroma-backed implementation fits the target store. Each leaf references a rule id from `01-core-rules.xml`.
