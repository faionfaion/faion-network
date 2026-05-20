---
slug: graph-rag-production
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Moving Graph RAG to production requires selecting the right graph database backend (Neo4j for scale, FalkorDB for speed, Kuzu for embedded), deciding between LlamaIndex KnowledgeGraphIndex and Microsoft graphrag CLI, managing indexing costs ($4-20/million tokens), and handling the known failure modes that affect agents operating on live graph indexes.
content_id: "e27da99be3678b99"
tags: [graph-rag, production, llamaindex, neo4j, microsoft-graphrag]
---
# Graph RAG Production: LlamaIndex, Graph Databases, and Deployment Gotchas

## Summary

**One-sentence:** Moving Graph RAG to production requires selecting the right graph database backend (Neo4j for scale, FalkorDB for speed, Kuzu for embedded), deciding between LlamaIndex KnowledgeGraphIndex and Microsoft graphrag CLI, managing indexing costs ($4-20/million tokens), and handling the known failure modes that affect agents operating on live graph indexes.

**One-paragraph:** Moving Graph RAG to production requires selecting the right graph database backend (Neo4j for scale, FalkorDB for speed, Kuzu for embedded), deciding between LlamaIndex KnowledgeGraphIndex and Microsoft graphrag CLI, managing indexing costs ($4-20/million tokens), and handling the known failure modes that affect agents operating on live graph indexes.

## Applies If (ALL must hold)

- Graph RAG indexing and retrieval are working in development (NetworkX) and the corpus exceeds memory capacity or requires concurrent access.
- Choosing between LlamaIndex KnowledgeGraphIndex and Microsoft graphrag CLI for the production pipeline.
- Selecting a graph database backend for a new deployment environment.
- Debugging agent failures involving graph traversal errors, stale summaries, or community ID instability.

## Skip If (ANY kills it)

- Still in exploration phase — use NetworkX in-memory until the approach is validated on a sample corpus.
- Corpus fits in memory and is accessed by a single process — NetworkX is simpler and faster.
- No budget for Neo4j or managed graph DB — evaluate Kuzu (embedded, zero server cost) first.

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
