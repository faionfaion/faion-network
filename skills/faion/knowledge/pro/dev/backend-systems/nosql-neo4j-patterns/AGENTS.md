---
slug: nosql-neo4j-patterns
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Graph modelling for Neo4j: labelled nodes + typed directed relationships with properties, bounded Cypher traversals with EXPLAIN/PROFILE, property indexes on every filtered property.
content_id: "418da840dacc1b3c"
complexity: deep
produces: spec
est_tokens: 4400
tags: [neo4j, graph-database, cypher, recommendations, social-graph]
---
# Neo4j Graph Database Patterns

## Summary

**One-sentence:** Graph modelling for Neo4j: labelled nodes + typed directed relationships with properties, bounded Cypher traversals with EXPLAIN/PROFILE, property indexes on every filtered property.

**One-paragraph:** Neo4j stores data as nodes (entities) and relationships (typed, directed edges with properties). Domain modelling promotes connections to first-class citizens; traversal queries MUST cap hop depth via *..N and a LIMIT; every property used in a WHERE clause needs a property index or uniqueness constraint. Output is a graph schema bundle: labels + relationship types + property indexes + sample Cypher with EXPLAIN/PROFILE results.

**Ефективно для:**

- Recommendation engines walking purchase / viewing graphs.
- Social-graph traversals (friends-of-friends).
- Fraud / anti-money-laundering link analysis.
- Knowledge graphs with mixed entity types and rich relationship properties.

## Applies If (ALL must hold)

- Workload uses Neo4j (Community or Enterprise) or another labelled-property graph DB.
- Domain has rich relationships where edges carry meaning beyond foreign keys.
- Traversal queries hop ≥2 levels and benefit from native pointer chasing.
- Team can model relationships first-class and update Cypher when domain changes.

## Skip If (ANY kills it)

- Domain is fundamentally tabular and JOIN-heavy — Postgres + recursive CTE is simpler.
- Workload is OLAP / analytical aggregations — columnar store wins.
- Cardinality of traversals is unknown / unbounded with no clear depth cap.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model | ER / mind map | team |
| Traversal queries | Cypher | team — every query with expected hop depth |
| Cluster size / RAM budget | yaml | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-graph` | sonnet | Picking labels + relationship types + property location needs judgement. |
| `review-cypher` | sonnet | Cypher review with PROFILE benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.cypher` | Neo4j schema skeleton (labels, indexes, constraints) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nosql-neo4j-patterns.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[nosql-mongodb-patterns]]
- [[nosql-cassandra-patterns]]
- [[nosql-redis-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
