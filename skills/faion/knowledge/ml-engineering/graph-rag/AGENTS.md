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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/entity-schema.py`

```python
"""

# Generic entity/relationship schema for GraphRAG pipelines

GENERIC_SCHEMA = {
    "entities": [
        {"name": "Person", "properties": ["name", "title", "affiliation"]},
        {"name": "Organization", "properties": ["name", "type", "industry", "location"]},
        {"name": "Location", "properties": ["name", "type", "country"]},
        {"name": "Product", "properties": ["name", "type", "manufacturer"]},
        {"name": "Technology", "properties": ["name", "type", "version"]},
        {"name": "Event", "properties": ["name", "date", "location"]},
        {"name": "Concept", "properties": ["name", "domain"]},
    ],
    "relationships": [
        {"name": "WORKS_FOR", "source": "Person", "target": "Organization"},
        {"name": "LOCATED_IN", "source": ["Person", "Organization"], "target": "Location"},
        {"name": "PRODUCES", "source": "Organization", "target": "Product"},
        {"name": "USES", "source": ["Person", "Organization"], "target": "Technology"},
        {"name": "ACQUIRED", "source": "Organization", "target": "Organization"},
        {"name": "RELATED_TO", "source": "*", "target": "*", "properties": ["type", "strength"]},
    ],
}

# Domain-specific: Technical documentation
TECH_DOCS_SCHEMA = {
    "entities": [
        {"name": "API", "properties": ["name", "version", "type"]},
        {"name": "Function", "properties": ["name", "signature", "module"]},
        {"name": "Class", "properties": ["name", "module", "parent_class"]},
        {"name": "Module", "properties": ["name", "package", "version"]},
        {"name": "ErrorType", "properties": ["name", "code", "severity"]},
    ],
    "relationships": [
        {"name": "CONTAINS", "source": "Module", "target": ["Function", "Class"]},
        {"name": "CALLS", "source": "Function", "target": "Function"},
        {"name": "INHERITS", "source": "Class", "target": "Class"},
        {"name": "RAISES", "source": "Function", "target": "ErrorType"},
        {"name": "DEPENDS_ON", "source": "Module", "target": "Module"},
    ],
}
```

### `templates/neo4j-schema.cypher`

```cypher
// Neo4j GraphRAG schema setup
// Run once during initial setup

// Entity uniqueness constraints
CREATE CONSTRAINT entity_name IF NOT EXISTS
FOR (e:Entity) REQUIRE e.name IS UNIQUE;

// Vector index for semantic search
CREATE VECTOR INDEX entity_embeddings IF NOT EXISTS
FOR (e:Entity) ON e.embedding
OPTIONS {indexConfig: {
  `vector.dimensions`: 1536,
  `vector.similarity_function`: 'cosine'
}};

// Fulltext index for hybrid search
CREATE FULLTEXT INDEX entity_fulltext IF NOT EXISTS
FOR (e:Entity) ON EACH [e.name, e.description];

// Traversal performance indexes
CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type);
CREATE INDEX relationship_type IF NOT EXISTS FOR ()-[r:RELATED_TO]-() ON (r.type);
```

### `templates/cypher-queries.cypher`

```cypher
// GraphRAG Cypher traversal patterns

// 1-hop neighborhood
MATCH (n:Entity {name: $entity_name})-[r]-(neighbor)
RETURN n, r, neighbor LIMIT 50;

// 2-hop with relationship type filter
MATCH path = (n:Entity {name: $entity_name})-[r*1..2]-(related)
WHERE ALL(rel IN relationships(path) WHERE type(rel) IN $relationship_types)
RETURN path LIMIT 100;

// Weighted traversal — strong edges only
MATCH (n:Entity {name: $entity_name})-[r]-(neighbor)
WHERE r.weight > 0.5
RETURN n, r, neighbor ORDER BY r.weight DESC LIMIT 20;

// Shortest path between two entities
MATCH path = shortestPath(
  (a:Entity {name: $source})-[*1..5]-(b:Entity {name: $target})
)
RETURN path;

// Hybrid: vector search + 2-hop graph expansion
CALL db.index.vector.queryNodes('entity_embeddings', 10, $query_embedding)
YIELD node, score
WHERE score > 0.7
MATCH (node)-[r*1..2]-(related)
RETURN node, score,
       collect(DISTINCT {
         entity: related.name,
         relationship: type(r),
         properties: properties(r)
       }) AS context
ORDER BY score DESC;
```

### `templates/graphrag-settings.yaml`

```yaml
# Microsoft GraphRAG settings.yaml — key parameters
# Full reference: https://microsoft.github.io/graphrag/config/

encoding_model: cl100k_base
llm:
  api_key: ${OPENAI_API_KEY}
  type: openai_chat
  model: gpt-4o
  model_supports_json: true
  max_tokens: 4096
  temperature: 0
  concurrent_requests: 25
  tokens_per_minute: 150000

parallelization:
  stagger: 0.3
  num_threads: 50

embeddings:
  llm:
    api_key: ${OPENAI_API_KEY}
    type: openai_embedding
    model: text-embedding-3-small

chunks:
  size: 1200
  overlap: 100
  group_by_columns: [id]

entity_extraction:
  prompt: prompts/entity_extraction.txt
  entity_types: [organization, person, geo, event, product, technology]
  max_gleanings: 1

community_reports:
  max_length: 2000
  max_input_length: 8000

cluster_graph:
  max_cluster_size: 10

local_search:
  top_k_entities: 10
  top_k_relationships: 10
  max_tokens: 12000

global_search:
  max_tokens: 12000
  map_max_tokens: 1000
  reduce_max_tokens: 2000
  concurrency: 32
```

### `templates/prompt-entity-extraction.txt`

```text
-->

You are a knowledge graph extraction expert. Extract entities from the text following the schema below.

SCHEMA:
{schema_json}

TEXT:
{text}

INSTRUCTIONS:
1. Extract only entities matching schema types
2. Capture all properties defined in the schema
3. Use exact entity type names from the schema
4. If a property is not mentioned, omit it (do not use null)
5. Resolve coreferences (he, she, it, they) to actual entity names
6. Do not invent entities not stated in the text

OUTPUT FORMAT (JSON only):
{
  "entities": [
    {
      "name": "string",
      "type": "schema entity type",
      "description": "brief description from context",
      "properties": { "property_name": "value" }
    }
  ]
}

GLEANING (if entities were missed):
After your first extraction, review the text again for any entities not yet captured.
Implicit entities (referenced but not named) count.
If nothing missed, return: {"entities": []}
```

### `templates/prompt-query-classification.txt`

```text
-->

Classify the query to select the best GraphRAG retrieval strategy.

QUERY: {query}

CLASSIFICATION CATEGORIES:

LOCAL — specific entity or relationship question
Examples: "What is X?", "Who founded Y?", "How are A and B related?"

GLOBAL — broad theme or summary question
Examples: "What are the main themes?", "Summarize key topics", "What patterns exist across..."

HYBRID — requires both specific facts and broader context
Examples: "How does X compare to similar entities?", "What role does Y play in the broader context?"

OUTPUT (JSON only):
{
  "classification": "LOCAL" | "GLOBAL" | "HYBRID",
  "confidence": 0.0-1.0,
  "reasoning": "one sentence",
  "suggested_traversal_depth": 1-3,
  "suggested_community_level": 0
}
```
