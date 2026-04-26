# Agent Integration — GraphRAG

## When to use
- Questions require understanding relationships between entities across a large corpus ("How does policy X relate to regulation Y?")
- Multi-hop reasoning tasks: A → B → C chains that standard vector RAG breaks on (45% vs 73% accuracy)
- "What are the main themes in this corpus?" — global summarization that semantic search cannot answer
- Knowledge base contains structured relationships: org charts, legal hierarchies, medical ontologies, product taxonomies
- Users ask cross-document questions where the answer spans multiple sources connected by shared entities
- Research report analysis where entity co-occurrence and relationship strength matters

## When NOT to use
- Simple factual lookup ("What is the definition of X?") — standard vector RAG is 5-10x cheaper and faster
- Single-document Q&A — no graph structure to exploit
- Real-time user-facing chat where query latency under 500ms is required — global graph search runs map-reduce over all community summaries
- Corpora under ~500 documents — graph construction cost (5-10x tokens vs standard RAG) outweighs quality gain
- Frequently updated corpora — incremental graph updates require re-running entity resolution and community detection on affected subgraphs
- Teams without Neo4j/NetworkX operational experience — graph infrastructure adds meaningful ops burden

## Where it fails / limitations
- Entity extraction with LLMs hallucinates relationships not in the source text — always validate extraction against schema constraints
- Leiden community detection is non-deterministic — rebuilding the index with same data can produce different community structures
- Global search is expensive: map-reduce over all community summaries at 2000 tokens each compounds quickly (1000 communities = 2M tokens per query)
- Entity resolution merges distinct entities with similar names incorrectly without domain-specific disambiguation rules
- LightRAG's 10x token reduction comes at the cost of relationship granularity — not suitable for legal or medical precision
- Neo4j's Cypher learning curve blocks teams used to vector-only workflows; miswritten traversal queries silently return empty results

## Agentic workflow
Use a two-phase agentic workflow: an offline index-builder subagent runs entity extraction, relationship extraction, and Leiden clustering (can take hours for large corpora — run as a background task); an online query-router subagent classifies each user question as local (entity-specific) or global (theme/overview), routes to the corresponding retrieval strategy, assembles context, and calls the synthesis LLM. For real-time agent tool use, wrap local search as a tool that accepts entity names and returns subgraph context; global search is a separate tool returning community summaries. Always cache global search results — they change only when the corpus changes.

### Recommended subagents
- `graph-builder` — entity extraction + relationship extraction + graph construction + community detection (offline, batch)
- `query-classifier` — classifies question as local/global/hybrid, returns routing decision
- `local-searcher` — traverses entity subgraph, assembles 1-hop and 2-hop context
- `global-searcher` — selects relevant community summaries via map-reduce, assembles thematic context
- `synthesis-agent` — takes context from searcher, generates final answer with citations to source entities

### Prompt pattern
```
# Entity extraction prompt
Extract all entities and relationships from this text chunk.
Return as JSON:
{
  "entities": [{"name": str, "type": str, "description": str}],
  "relationships": [{"source": str, "target": str, "type": str, "description": str, "weight": float}]
}

Allowed entity types: {entity_types}
Allowed relationship types: {relationship_types}
Do not invent relationships not stated in the text.
```

```python
# Query routing decision
def route_query(question: str, llm) -> str:
    prompt = f"""Classify this question:
- LOCAL: asks about specific entities, people, places, or direct facts
- GLOBAL: asks about themes, patterns, summaries, or cross-cutting topics

Question: {question}
Return only: LOCAL or GLOBAL"""
    return llm(prompt).strip()
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `graphrag` | Microsoft GraphRAG: full pipeline, community detection | `pip install graphrag` / https://github.com/microsoft/graphrag |
| `neo4j-graphrag` | Neo4j GraphRAG Python library | `pip install neo4j-graphrag` / https://github.com/neo4j/neo4j-graphrag-python |
| `lightrag` | Lightweight GraphRAG with 10x token reduction | `pip install lightrag-hku` / https://github.com/HKUDS/LightRAG |
| `networkx` | In-memory graph for prototyping | `pip install networkx` / https://networkx.org/ |
| `neo4j` | Neo4j Python driver | `pip install neo4j` / https://neo4j.com/docs/python-manual/ |
| `graspologic` | Leiden algorithm + graph statistics | `pip install graspologic` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Neo4j AuraDB | SaaS | Yes | Managed Neo4j; Cypher API; GraphRAG-ready with vector index support |
| Weaviate | SaaS/OSS | Yes | Built-in knowledge graph + vector hybrid; less Cypher-centric |
| Amazon Neptune | SaaS | Partial | Gremlin/SPARQL; slower to integrate than Neo4j for Python agents |
| Memgraph | OSS | Yes | Cypher-compatible, high throughput; good for real-time graph updates |
| Diffbot | SaaS | Partial | Auto-builds knowledge graphs from web content; expensive but turnkey |
| Qdrant | OSS/SaaS | Yes | External graph integration; use alongside NetworkX for vector + graph |

## Templates & scripts
See `templates.md` for full GraphRAG pipeline configuration and Neo4j setup templates.

Minimal local search (Neo4j):
```python
from neo4j import GraphDatabase

def local_search(driver, entity_name: str, hops: int = 2) -> list[dict]:
    with driver.session() as session:
        result = session.run(
            """
            MATCH (e:Entity {name: $name})
            CALL apoc.path.subgraphNodes(e, {maxLevel: $hops}) YIELD node
            MATCH (node)-[r]-(neighbor)
            RETURN node.name, type(r), neighbor.name, r.description
            LIMIT 50
            """,
            name=entity_name, hops=hops,
        )
        return [dict(record) for record in result]
```

## Best practices
- Use traditional NER (SpaCy, GliNER) for entity extraction and LLMs only for relationship extraction — reduces cost by 60% with comparable entity recall
- Cache community summaries at index time; regenerate only when community membership changes (delta indexing)
- Cap graph traversal depth at 2 hops for agent tool calls — 3-hop queries return too much context for reliable synthesis
- Define explicit relationship type ontology before extraction — unconstrained relationship types produce thousands of unique types that defeat community detection
- Run entity resolution with embedding similarity (cosine > 0.9) before graph construction — duplicate entities fragment communities
- For LightRAG, tune `working_dir` chunking strategy to match your domain; default chunk size underperforms on long technical documents

## AI-agent gotchas
- Microsoft GraphRAG global search costs 2000+ tokens per community summary — agents running global search in a ReAct loop will exhaust token budgets in 3-5 iterations; use caching aggressively
- Entity extraction LLM calls are the primary cost driver during indexing — batch chunks (10-20 per call) to reduce API overhead by 5-8x
- Graph databases return empty results without error when entity names don't match exactly — agents interpret silence as "no relevant information" and hallucinate; normalize entity names before graph lookup
- Human-in-the-loop checkpoint: for high-stakes knowledge graph modifications (adding new relationships from unverified sources), require human review before writing to the graph — one hallucinated relationship can corrupt multi-hop reasoning for all subsequent queries

## References
- Microsoft GraphRAG paper: https://arxiv.org/abs/2404.16130
- Microsoft GraphRAG repo: https://github.com/microsoft/graphrag
- Neo4j GraphRAG Python: https://github.com/neo4j/neo4j-graphrag-python
- LightRAG: https://github.com/HKUDS/LightRAG
- LlamaIndex Property Graphs: https://docs.llamaindex.ai/en/stable/examples/property_graph/
- Weaviate GraphRAG: https://weaviate.io/blog/graph-rag
