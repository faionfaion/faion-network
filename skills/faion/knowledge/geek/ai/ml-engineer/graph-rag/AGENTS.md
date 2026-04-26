# GraphRAG

## Summary

GraphRAG combines knowledge graph construction with vector retrieval to answer multi-hop and global questions. It extracts entity-relationship graphs from documents, runs community detection (Leiden algorithm), and builds hierarchical summaries — enabling local (entity-subgraph) and global (theme-overview) search strategies that standard vector RAG cannot perform.

## Why

Standard RAG uses semantic similarity over flat chunks; it breaks on "How does entity A relate to B through C?" and cannot answer "What are the main themes across the entire corpus?" GraphRAG solves both by maintaining structured graph state. Multi-hop accuracy improves from ~45% to ~73%; global sensemaking goes from impossible to a first-class operation.

## When To Use

- Questions require multi-hop entity reasoning (A relates to B, B relates to C)
- Need global "theme overview" answers across a large corpus
- Knowledge base has structured relationships: org charts, legal hierarchies, medical ontologies
- Users ask cross-document questions where the answer spans sources connected by shared entities
- Entity co-occurrence and relationship strength matter for answers

## When NOT To Use

- Simple factual lookup — standard vector RAG is 5-10x cheaper and faster
- Single-document Q&A — no graph structure to exploit
- Real-time queries under 500ms required — global search runs map-reduce over all community summaries
- Corpus under ~500 documents — graph construction cost (5-10x tokens vs standard RAG) outweighs gain
- Frequently updated corpora — incremental graph updates require re-running entity resolution and community detection
- Teams without Neo4j/NetworkX operational experience

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | Knowledge graph construction: entity extraction, relationship extraction, entity resolution, community detection |
| `content/02-retrieval.xml` | Retrieval strategies: local search, global search, hybrid search; query classification; context assembly |
| `content/03-implementation.xml` | Implementation checklist phases, validation checkpoints, cost considerations, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/graphrag-settings.yaml` | Microsoft GraphRAG `settings.yaml` with key parameters |
| `templates/neo4j-schema.cypher` | Neo4j constraints, vector index, fulltext index, traversal index setup |
| `templates/entity-schema.py` | Generic entity/relationship schema + domain-specific variants |
| `templates/cypher-queries.cypher` | Traversal patterns: 1-hop, 2-hop, weighted, path finding, hybrid vector+graph |
| `templates/prompt-entity-extraction.txt` | Schema-guided entity extraction prompt with gleaning support |
| `templates/prompt-query-classification.txt` | Query classification prompt: LOCAL / GLOBAL / HYBRID |
