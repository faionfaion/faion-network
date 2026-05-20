---
slug: nosql-neo4j-patterns
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Neo4j stores data as nodes (entities) and relationships (typed, directed edges with properties).
content_id: "f501f286b21ec172"
tags: [neo4j, graph-database, cypher, recommendations, social-graph]
---
# Neo4j Graph Database Patterns

## Summary

**One-sentence:** Neo4j stores data as nodes (entities) and relationships (typed, directed edges with properties).

**One-paragraph:** Neo4j stores data as nodes (entities) and relationships (typed, directed edges with properties). Use graph databases when the query value is in the connections — social networks, recommendation engines, fraud detection, knowledge graphs. Shape queries with LIMIT and hop-depth caps; deep traversals (>5 hops) without cost shaping cause exponential blowup. Use EXPLAIN/PROFILE before deploying any traversal query.

## Applies If (ALL must hold)

- Social network features: friends, followers, mutual connections, degrees of separation.
- Collaborative filtering: "users who bought X also bought Y" recommendation engines.
- Fraud detection: connected accounts, shared identifiers, ring patterns across transactions.
- Knowledge graphs, ontologies, and entity resolution where relationships carry semantic meaning.
- Path-finding problems: shortest path, all paths, route optimization over a graph topology.

## Skip If (ANY kills it)

- Tabular or document-centric data where entities are not connected — MongoDB or PostgreSQL is simpler.
- High-volume write workloads (millions of writes/second) — Neo4j's write throughput is lower than Cassandra or DynamoDB for simple key-value patterns.
- Analytical aggregations over large datasets — graph databases are optimized for traversal, not GROUP BY + aggregation at scale; use a warehouse.
- When traversal depth exceeds 5 hops on a dense graph — query cost grows superlinearly; apply algorithmic pruning or switch to a specialized graph analytics engine (GraphX, Kuzu).

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

- parent skill: `pro/dev/backend-systems/`
