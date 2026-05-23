# GraphRAG

## Summary

**One-sentence:** Produces a GraphRAG pipeline spec: entity extraction → knowledge graph → community detection → hierarchical summaries → query-routing for multi-hop and global questions.

**One-paragraph:** Produces a GraphRAG pipeline spec. GraphRAG combines knowledge-graph construction with vector retrieval to answer multi-hop and global questions standard vector RAG cannot. Pipeline: extract entity-relationship graphs from documents, run community detection (Leiden algorithm), build hierarchical summaries — enabling local (entity-subgraph) and global (theme-overview) search strategies. Use only when (multi-hop questions are common) AND (entity vocabulary is closed enough to extract reliably).

**Ефективно для:** Дата-інженер для multi-hop QA — fixed spec з extraction prompt, Neo4j schema, query routing.

## Applies If (ALL must hold)

- Question pattern includes multi-hop ('what links X to Y through Z') or global ('summarise themes across N docs').
- Domain has clear entity types (people, orgs, products, concepts) and relation types.
- Corpus stable enough to justify the graph build cost (≥10k docs reused ≥3 months).
- Vector RAG baseline tried and failed on multi-hop / global queries.
- Have or can stand up a graph store (Neo4j, ArangoDB, or graph extension to PG).

## Skip If (ANY kills it)

- Pure semantic search on documents — vector RAG suffices.
- Corpus changes daily — graph maintenance cost dominates.
- Entity vocabulary open-ended / fuzzy — extraction will be noisy.
- Single-hop questions dominate the workload — graph adds latency without benefit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source corpus | directory or db dump | data team |
| Entity / relation schema | yaml | domain SME + ML |
| Graph store | service URL + creds | infra |
| Sample multi-hop questions | jsonl | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Confirms GraphRAG vs vector RAG choice. |
| `geek/ai/ml-engineer/llm-observability-stack` | Traces extraction + query latency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: schema-design → extract → graph-build → community-detect → summarise → wire-query-router. | ~800 |
| `content/05-examples.xml` | medium | Worked example: legal-document corpus → entity graph → Leiden communities → global QA. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by question pattern + corpus stability. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-schema` | opus | Cross-cutting: entity types + relation types from domain SME. |
| `run-extraction` | sonnet | Per-document entity + relation extraction with stable prompt. |
| `query-routing` | sonnet | Classify incoming question as local / global / multi-hop. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity-schema.py` | Pydantic models for Entity + Relation. |
| `templates/neo4j-schema.cypher` | Constraints + indexes for the entity graph. |
| `templates/cypher-queries.cypher` | Library of multi-hop / community-traversal queries. |
| `templates/graphrag-settings.yaml` | Pipeline config: model, chunk_size, community params. |
| `templates/prompt-entity-extraction.txt` | Stable extraction prompt with schema. |
| `templates/prompt-query-classification.txt` | Local / global / multi-hop classifier. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graph-rag.py` | Validate pipeline spec (schema, extraction prompt, community params, routing). | Pre-merge of every GraphRAG pipeline PR. |

## Related

- [[llm-decision-framework]] — parent decision; GraphRAG branch elaborated here.
- [[llm-observability-stack]] — traces extraction + retrieval.
- [[llamaindex]] — alternative implementation with PropertyGraphIndex.

## Decision tree

Decision tree at `content/06-decision-tree.xml` decides if GraphRAG is justified given (multi-hop %, corpus stability, entity-vocab closedness). Use BEFORE building the graph.
