---
slug: graph-rag-indexing
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Standard vector RAG retrieves chunks by semantic similarity and fails on global questions, entity relationships, and multi-hop reasoning.
content_id: "bfa4359d64814741"
tags: [graph-rag, knowledge-graph, entity-extraction, community-detection, neo4j]
---
# Graph RAG Indexing: Entity Extraction, Graph Construction, and Hierarchical Summarization

## Summary

**One-sentence:** Standard vector RAG retrieves chunks by semantic similarity and fails on global questions, entity relationships, and multi-hop reasoning.

**One-paragraph:** Standard vector RAG retrieves chunks by semantic similarity and fails on global questions, entity relationships, and multi-hop reasoning. Graph RAG fixes this by building a knowledge graph from documents — entities become nodes, relationships become edges — then running community detection and hierarchical summarization so global queries can be answered from pre-computed summaries instead of brute-force chunk retrieval.

## Applies If (ALL must hold)

- Corpus-wide thematic summarization: "What are the main topics across all 10,000 documents?"
- Entity relationship questions that a single chunk cannot answer (org charts, citation networks, drug interactions).
- Domain corpora with dense cross-references: legal case law, medical literature, research paper networks.
- Multi-hop reasoning required: "How are entity A and entity B connected through intermediaries?"
- Existing vector RAG answers global questions with low confidence or hallucinated relationships.

## Skip If (ANY kills it)

- Corpora where questions are local and chunk-answerable — vector RAG is 10-100x cheaper and faster.
- Corpora with fewer than 1,000 documents — graph overhead exceeds quality gain.
- Real-time indexing required — entity/relationship extraction costs one LLM call per chunk and takes seconds each.
- No graph database or networkx/Neo4j infra in deployment — infrastructure cost is non-trivial.
- Team has no graph query skills (Cypher) — maintainability cost is high.

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
