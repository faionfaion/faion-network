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
