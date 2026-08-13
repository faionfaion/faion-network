# Graph RAG Retrieval: Query Routing and Hybrid Vector+Graph Retrieval

## Summary

**One-sentence:** Routes Graph-RAG queries into GLOBAL/ENTITY/RELATIONSHIP/LOCAL strategies and combines vector candidates with graph neighbor expansion.

**One-paragraph:** After the knowledge graph is built (graph-rag-indexing), retrieval requires classifying each query into one of four types and routing it to the matching retrieval strategy. Hybrid retrieval — vector search followed by graph neighbor expansion — outperforms both pure vector and pure graph approaches for most query distributions because it anchors candidates on semantic similarity, then expands using graph structure.

**Ефективно для:** інженерів RAG, які підтримують knowledge-graph індекс і хочуть, щоб маршрутизатор сам обрав між summary, neighbor lookup, path-traversal і vector search замість одного fallback пайплайна.

## Applies If (ALL must hold)

- A Graph-RAG index already exists (graph-rag-indexing completed) and query traffic is mixed across global / entity / local question types.
- Query latency budget allows one fast LLM call for query classification.
- The team is ready to start with hybrid retrieval before committing to pure-graph traversal.
- Entity-relationship questions exist where vector similarity alone retrieves irrelevant chunks.

## Skip If (ANY kills it)

- No knowledge graph exists — run graph-rag-indexing first.
- All queries are purely local and chunk-answerable — skip routing, use vector search directly.
- Graph has &gt;50k nodes and global queries are frequent — pre-compute summaries offline rather than route to live traversal.
- Graph is densely connected and relationship queries require full path enumeration — cap hop depth or hit exponential path counts.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Knowledge graph G | NetworkX Graph | output of graph-rag-indexing |
| Vector store (entity + chunk indexes) | Qdrant/Weaviate/Chroma | embedding-generation pipeline |
| Hierarchical summaries dict | JSON {global, entities, communities} | offline summarisation step |
| Query string | text | user input |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/graph-rag-indexing` | Produces the graph + summaries consumed here. |
| `geek/ai/rag-engineer/hybrid-search-basics` | Defines RRF/alpha fusion used for the vector leg. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: classify-before-retrieve, route-by-type, hybrid-first, cap-expansion, fall-back-on-failure | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the retrieval result + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | Step-by-step routing + hybrid expansion procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree picking GLOBAL/ENTITY/RELATIONSHIP/LOCAL branch | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Classify query type | haiku | One-call categorisation, temp=0; latency-critical. |
| Extract entities from query | sonnet | NER quality matters for ENTITY/RELATIONSHIP paths. |
| Synthesise final answer over assembled context | sonnet | Grounded generation, citations preserved. |
| Fallback path debugging | opus | Multi-strategy reasoning when classification is ambiguous. |

## Templates

| File | Purpose |
|------|---------|
| `templates/classify-query-prompt.txt` | Few-shot classifier prompt with the four canonical types. |
| `templates/router.py.tmpl` | Skeleton router function dispatching on QueryType. |
| `templates/_smoke-test.py` | Minimum runnable example: classify → route → assemble context. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graph-rag-retrieval.py` | Validates a retrieval result against the 02-output-contract schema. | Pre-commit; CI on every retrieval-result fixture. |

## Related

- [[graph-rag-indexing]]
- [[graph-rag-production]]
- [[hybrid-search-basics]]
- [[reranking-two-stage]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` selects the retrieval path: root question — "Which canonical query type does this question match?". Each branch names a concrete observable (entity count, contains-relation-word, asks-for-themes) and concludes by referencing the rule that owns the chosen path. Branches without a clear type-match fall through to LOCAL via `r5`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/classify-query-prompt.txt`

```text
Classify the following query into exactly one of four canonical Graph-RAG types.
Return ONLY the uppercase token, no commentary.

Types:
- GLOBAL: about main themes, overall trends, dataset-wide patterns ("what topics dominate this corpus")
- ENTITY: about a specific named entity ("what does Alice do")
- RELATIONSHIP: about a connection between two entities ("how is Alice connected to Acme Corp")
- LOCAL: factoid answerable from a single chunk ("what is the capital of France")

Few-shot examples:
Q: "Summarise the main themes in this dataset."           A: GLOBAL
Q: "Tell me about Alice."                                  A: ENTITY
Q: "How does Alice relate to Acme Corp?"                   A: RELATIONSHIP
Q: "What is the boiling point of water?"                   A: LOCAL

Query: {query}
Answer:
```

### `templates/router.py.tmpl`

```python
from enum import Enum
from typing import Dict, List
import networkx as nx


class QueryType(str, Enum):
    GLOBAL = "GLOBAL"
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    LOCAL = "LOCAL"


def route(
    query: str,
    query_type: QueryType,
    G: nx.Graph,
    summaries: Dict,
    vector_store,
) -> Dict:
    candidates: List[Dict] = []
    fallback_used = False
    path = ""

    if query_type == QueryType.GLOBAL:
        path = "summary"
        candidates = [{"chunk_id": "__global__", "score": 1.0, "source": "summary"}]
        assembled = summaries.get("global", "")
        return _result(query, query_type, path, candidates, assembled, fallback_used)

    if query_type == QueryType.RELATIONSHIP:
        entities = _extract_entities(query)
        if len(entities) >= 2 and entities[0] in G and entities[1] in G:
            try:
                p = nx.shortest_path(G, entities[0], entities[1])
                if len(p) - 1 > 3:
                    p = p[:4]
                candidates = [{"chunk_id": n, "score": 1.0, "source": "shortest-path"} for n in p]
                assembled = " -> ".join(p)
                return _result(query, query_type, "shortest-path", candidates, assembled, fallback_used)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                pass
        fallback_used = True

    if query_type == QueryType.ENTITY:
        entity = _extract_single_entity(query)
        if entity and entity in G:
            neighbors = list(G.neighbors(entity))[:3]
            candidates = [{"chunk_id": n, "score": 0.9, "source": "graph-neighbor"} for n in neighbors]
            for n in [entity, *neighbors]:
                for r in vector_store.search(n, k=2):
                    candidates.append({"chunk_id": r["id"], "score": float(r["score"]), "source": "vector"})
            seen, deduped = set(), []
            for c in candidates:
                if c["chunk_id"] in seen:
                    continue
                seen.add(c["chunk_id"])
                deduped.append(c)
            return _result(query, query_type, "hybrid", deduped, _assemble(deduped), fallback_used)
        fallback_used = True

    # LOCAL or fallback
    results = vector_store.search(query, k=5)
    candidates = [{"chunk_id": r["id"], "score": float(r["score"]), "source": "vector"} for r in results]
    return _result(query, QueryType.LOCAL, "vector-search", candidates, _assemble(candidates), fallback_used)


def _result(q, qt, path, cands, ctx, fb):
    return {
        "query": q,
        "query_type": qt.value if isinstance(qt, QueryType) else qt,
        "retrieval_path": path,
        "candidates": cands,
        "assembled_context": ctx,
        "fallback_used": fb,
    }


def _extract_entities(q: str) -> List[str]:
    # Replace with real NER (spaCy / Claude). Placeholder splits on common conjunctions.
    return [w.strip() for w in q.replace("?", "").split(" and ") if w.strip()]


def _extract_single_entity(q: str) -> str:
    parts = _extract_entities(q)
    return parts[0] if parts else ""


def _assemble(cands: List[Dict]) -> str:
    return "\n".join(f"[{c['source']}] {c['chunk_id']} (score={c['score']:.2f})" for c in cands)
```

### `templates/_smoke-test.py`

```python
from dataclasses import dataclass
import networkx as nx
from router import route, QueryType  # rename router.py.tmpl -> router.py to run


@dataclass
class FakeStore:
    def search(self, q, k):
        return [{"id": f"chunk-{i}-{q[:6]}", "score": 0.5 - 0.05 * i} for i in range(k)]


G = nx.Graph()
G.add_edges_from([("Alice", "Acme"), ("Acme", "Globex"), ("Bob", "Acme")])
summaries = {"global": "The corpus describes founders, companies, and acquisitions."}

if __name__ == "__main__":
    res = route("How is Alice connected to Globex?", QueryType.RELATIONSHIP, G, summaries, FakeStore())
    assert res["query_type"] == "RELATIONSHIP"
    assert res["retrieval_path"] in ("shortest-path", "vector-search")
    print(res)
```
