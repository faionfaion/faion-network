---
slug: graph-rag
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GraphRAG combines knowledge graph construction with vector retrieval to answer multi-hop and global questions.
content_id: "4dffbca6150f8053"
tags: [graph-rag, knowledge-graph, entity-extraction, neo4j, multi-hop]
---
# GraphRAG

## Summary

**One-sentence:** GraphRAG combines knowledge graph construction with vector retrieval to answer multi-hop and global questions.

**One-paragraph:** GraphRAG combines knowledge graph construction with vector retrieval to answer multi-hop and global questions. It extracts entity-relationship graphs from documents, runs community detection (Leiden algorithm), and builds hierarchical summaries — enabling local (entity-subgraph) and global (theme-overview) search strategies that standard vector RAG cannot perform.

## Applies If (ALL must hold)

- Questions require multi-hop entity reasoning (A relates to B, B relates to C)
- Need global "theme overview" answers across a large corpus
- Knowledge base has structured relationships: org charts, legal hierarchies, medical ontologies
- Users ask cross-document questions where the answer spans sources connected by shared entities
- Entity co-occurrence and relationship strength matter for answers

## Skip If (ANY kills it)

- Simple factual lookup — standard vector RAG is 5-10x cheaper and faster
- Single-document Q&A — no graph structure to exploit
- Real-time queries under 500ms required — global search runs map-reduce over all community summaries
- Corpus under ~500 documents — graph construction cost (5-10x tokens vs standard RAG) outweighs gain
- Frequently updated corpora — incremental graph updates require re-running entity resolution and community detection
- Teams without Neo4j/NetworkX operational experience

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

- parent skill: `geek/ai/ml-engineer/`
