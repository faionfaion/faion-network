# Agent Integration — Graph RAG and Advanced Retrieval

## When to use
- Queries require multi-hop reasoning: "How are entity A and entity B connected through intermediaries?"
- Corpus-wide thematic summarization: "What are the main topics across all 10,000 documents?"
- Entity relationship questions that a single chunk cannot answer (org charts, citation networks, drug interactions)
- Domain corpora with dense cross-references: legal case law, medical literature, research paper networks
- Existing vector RAG answers global questions with low confidence or hallucinated relationships

## When NOT to use
- Corpora where questions are local and chunk-answerable — vector RAG is 10-100× cheaper and faster
- Corpora <1,000 documents — graph overhead exceeds quality gain
- Real-time indexing required — entity/relationship extraction takes seconds per chunk (LLM call per chunk)
- No access to a graph database or networkx/Neo4j infra in the deployment environment
- Team has no graph query skills (Cypher) — maintainability cost is high

## Where it fails / limitations
- Entity extraction quality is LLM-dependent; hallucinated entities pollute the graph permanently
- Community detection (Louvain) is non-deterministic; re-running on the same corpus can produce different communities
- LlamaIndex KnowledgeGraphIndex is tightly coupled to the OpenAI API format — migrating to Anthropic requires custom LLM adapter
- Graph traversal for relationship queries can hit exponential path-count on densely connected graphs (cap hop depth to 3)
- Microsoft graphrag CLI is expensive to run at scale: ~$4-20 per 1M tokens for indexing (LLM extraction per chunk)
- Hierarchical summaries stale quickly when documents are updated — re-summarization must be triggered on any corpus change

## Agentic workflow
Graph RAG is a two-agent workflow: an **indexing agent** extracts entities and relationships from each chunk via structured LLM output, builds the graph (NetworkX or Neo4j), runs community detection, and generates hierarchical summaries; a **retrieval agent** classifies incoming queries (GLOBAL/ENTITY/RELATIONSHIP/LOCAL), routes to the appropriate retrieval path, and assembles context for the generation step. The indexing agent should checkpoint progress every 100 chunks and be resumable — full re-index of a large corpus is costly. Human review is recommended before promoting a new graph index to production.

### Recommended subagents
- `faion-sdd-executor-agent` — plan and execute the Graph RAG indexing pipeline as a multi-task SDD feature

### Prompt pattern
```xml
<task>Extract entities and relationships from the text below.</task>
<output_format>
{
  "entities": [{"name": str, "type": "PERSON|ORG|CONCEPT|EVENT|LOCATION", "description": str}],
  "relationships": [{"source": str, "target": str, "type": str, "description": str}]
}
</output_format>
<constraints>
- Only extract entities explicitly mentioned, not implied
- Relationship type must be a verb phrase (e.g., "works_at", "cites", "contradicts")
- Max 15 entities, max 20 relationships per chunk
</constraints>
<text>{{chunk_text}}</text>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `graphrag` | Microsoft GraphRAG CLI: index + query pipeline | `pip install graphrag` · https://github.com/microsoft/graphrag |
| `networkx` | In-memory graph construction, community detection, path finding | `pip install networkx` |
| `neo4j` (Python driver) | Production graph database client | `pip install neo4j` · https://neo4j.com/docs/python-manual/ |
| `llama-index-graph-stores-neo4j` | LlamaIndex Neo4j integration | `pip install llama-index-graph-stores-neo4j` |
| `graspologic` | Graph statistics, hierarchical community detection | `pip install graspologic` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Neo4j AuraDB | SaaS | Yes (Bolt/HTTP/Python SDK) | Managed graph DB; free tier to 200k nodes; Cypher query language |
| Neo4j (self-hosted) | OSS | Yes (Docker) | Production option; docker pull neo4j |
| Microsoft GraphRAG | OSS | Yes (CLI + Python API) | Full pipeline (index + local/global query); works with OpenAI + Azure |
| FalkorDB | OSS | Yes (Redis-compatible) | Graph DB with vector support; faster than Neo4j for small graphs |
| Kuzu | OSS | Yes (Python embedded) | Embedded graph DB (like SQLite for graphs); no server needed |
| Amazon Neptune | SaaS | Yes (REST/Gremlin/SPARQL) | Managed; expensive but integrates with AWS stack |

## Templates & scripts
See `templates.md` for entity extraction, Neo4jGraphBuilder, community detection, hierarchical_summarization, and hybrid_graph_vector_retrieval templates.

Inline — resumable chunk-level extraction with progress file:
```python
import json, hashlib
from pathlib import Path

def extract_graph_resumable(chunks: list[dict], progress_file: str, extract_fn) -> dict:
    progress_path = Path(progress_file)
    done = set(json.loads(progress_path.read_text())["done"]) if progress_path.exists() else set()
    graph = {"entities": [], "relationships": []}

    for chunk in chunks:
        cid = hashlib.md5(chunk["text"].encode()).hexdigest()
        if cid in done:
            continue
        result = extract_fn(chunk["text"])
        graph["entities"].extend(result.get("entities", []))
        graph["relationships"].extend(result.get("relationships", []))
        done.add(cid)
        progress_path.write_text(json.dumps({"done": list(done)}))

    return graph
```

## Best practices
- Run entity extraction with temperature=0 and structured JSON output (response_format) to minimize hallucinated entities
- Deduplicate entities by normalized name (lowercase, strip punctuation) before building the graph — "OpenAI" and "openai" must merge
- Cap community summarization to communities with ≥5 nodes; singleton communities produce useless summaries
- Use a versioned graph namespace (e.g., collection prefix + date) so a re-index does not corrupt an in-use production graph
- For global queries, prefer pre-computed hierarchical summaries over live graph traversal — traversal at query time is too slow for >50k nodes
- Hybrid retrieval (vector + graph expansion) outperforms pure graph for most queries; start hybrid before committing to full graph-only

## AI-agent gotchas
- LLM entity extraction has recall ~70-85%; agents must not assume all entities in a corpus are in the graph
- `nx.shortest_path` raises `NetworkXNoPath` when entities are in disconnected subgraphs; wrap every path query in try/except
- Community detection output order is not stable across runs — do not use community IDs as persistent identifiers; use content hashes of node sets instead
- Microsoft graphrag CLI rewrites config files on first run; agents running it in CI must checkpoint the generated config to avoid re-indexing from scratch
- LlamaIndex KnowledgeGraphIndex stores triplets but not full graph structure; `max_triplets_per_chunk=10` silently truncates dense chunks — verify extraction coverage

## References
- https://arxiv.org/abs/2404.16130 (GraphRAG paper — Microsoft)
- https://github.com/microsoft/graphrag
- https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/
- https://neo4j.com/developer/rag/
- https://networkx.org/documentation/stable/
