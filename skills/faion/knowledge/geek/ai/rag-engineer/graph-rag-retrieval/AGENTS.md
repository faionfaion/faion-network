---
slug: graph-rag-retrieval
tier: geek
group: ai
domain: rag-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: After the knowledge graph is built, retrieval requires classifying each query into one of four types (GLOBAL, ENTITY, RELATIONSHIP, LOCAL) and routing it to the appropriate retrieval strategy.
content_id: "2e24d7135c62a6a4"
tags: [graph-rag, query-routing, hybrid-retrieval, graph-traversal, rag]
---
# Graph RAG Retrieval: Query Routing and Hybrid Vector+Graph Retrieval

## Summary

**One-sentence:** After the knowledge graph is built, retrieval requires classifying each query into one of four types (GLOBAL, ENTITY, RELATIONSHIP, LOCAL) and routing it to the appropriate retrieval strategy.

**One-paragraph:** After the knowledge graph is built, retrieval requires classifying each query into one of four types (GLOBAL, ENTITY, RELATIONSHIP, LOCAL) and routing it to the appropriate retrieval strategy. Hybrid retrieval — vector search followed by graph neighbor expansion — outperforms both pure vector and pure graph approaches for most query distributions.

## Applies If (ALL must hold)

- A Graph RAG index already exists (graph-rag-indexing completed) and query traffic is mixed across global, entity, and local question types.
- Query latency budget allows LLM-based query classification (one fast model call per query).
- Hybrid retrieval — start here before committing to full graph-only retrieval.
- Entity relationship questions where vector similarity alone retrieves irrelevant chunks.

## Skip If (ANY kills it)

- No knowledge graph exists — run graph-rag-indexing first.
- All queries are purely local and chunk-answerable — skip routing, use vector search directly.
- Graph has more than 50k nodes and global queries are frequent — pre-compute summaries offline rather than routing to live traversal.
- Graph is densely connected and relationship queries require full path enumeration — cap hop depth to 3 or queries hit exponential path counts.

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
