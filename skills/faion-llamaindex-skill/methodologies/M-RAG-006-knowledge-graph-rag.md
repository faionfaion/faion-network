# M-RAG-006: Knowledge Graph RAG

## Overview

Knowledge Graph RAG enhances retrieval by combining vector similarity with graph-based relationships. Entities and their connections provide structured context that pure vector search misses. Ideal for complex domains with rich entity relationships.

**When to use:** Domains with structured relationships (legal, medical, technical docs), multi-hop reasoning, or when entity relationships are critical for answers.

## Core Concepts

### 1. Graph RAG Architecture

```
Documents → Entity Extraction → Knowledge Graph
                                     ↓
Query → Vector Search → Graph Traversal → Combined Context → LLM
            ↓                   ↓
        Chunks              Relationships
```

### 2. Graph Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Nodes** | Entities | Person, Company, Product |
| **Edges** | Relationships | WORKS_AT, DEVELOPS, RELATED_TO |
| **Properties** | Attributes | name, date, score |
| **Embeddings** | Vector representations | Entity/relationship vectors |

### 3. Benefits Over Pure Vector RAG

| Aspect | Vector RAG | Graph RAG |
|--------|-----------|-----------|
| Multi-hop reasoning | Limited | Strong |
| Relationship queries | Poor | Excellent |
| Entity disambiguation | Weak | Strong |
| Explainability | Low | High |
| Structured data | Poor | Native |

## Best Practices

### 1. Extract Entities and Relationships

```python
def extract_knowledge_graph(text: str, llm) -> dict:
    """Extract entities and relationships from text."""

    prompt = f"""
    Extract entities and relationships from this text.

    Text: {text}

    Return as JSON:
    {{
        "entities": [
            {{"name": "...", "type": "...", "description": "..."}}
        ],
        "relationships": [
            {{"source": "...", "target": "...", "type": "...", "description": "..."}}
        ]
    }}

    Entity types: Person, Organization, Product, Technology, Concept, Location, Event
    Relationship types: WORKS_AT, DEVELOPS, USES, RELATES_TO, PART_OF, CREATED_BY
    """

    result = llm.invoke(prompt)
    return json.loads(result)

# Process documents
def build_knowledge_graph(documents: list, llm) -> tuple:
    """Build knowledge graph from documents."""

    all_entities = []
    all_relationships = []

    for doc in documents:
        kg = extract_knowledge_graph(doc.text, llm)

        for entity in kg["entities"]:
            entity["source_doc"] = doc.id
            all_entities.append(entity)

        for rel in kg["relationships"]:
            rel["source_doc"] = doc.id
            all_relationships.append(rel)

    # Deduplicate entities
    unique_entities = deduplicate_entities(all_entities)

    return unique_entities, all_relationships
```

### 2. Store in Graph Database

```python
from neo4j import GraphDatabase

class KnowledgeGraphStore:
    def __init__(self, uri: str, auth: tuple):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def add_entity(self, entity: dict):
        """Add entity node to graph."""

        query = """
        MERGE (e:{type} {{name: $name}})
        SET e.description = $description,
            e.embedding = $embedding,
            e.source_doc = $source_doc
        RETURN e
        """.format(type=entity["type"])

        with self.driver.session() as session:
            session.run(query, **entity)

    def add_relationship(self, rel: dict):
        """Add relationship edge to graph."""

        query = """
        MATCH (source {{name: $source}})
        MATCH (target {{name: $target}})
        MERGE (source)-[r:{rel_type}]->(target)
        SET r.description = $description,
            r.source_doc = $source_doc
        RETURN r
        """.format(rel_type=rel["type"])

        with self.driver.session() as session:
            session.run(query, **rel)

    def search_entities(self, query_embedding: list, k: int = 10) -> list:
        """Find similar entities using vector index."""

        query = """
        CALL db.index.vector.queryNodes('entity_embeddings', $k, $embedding)
        YIELD node, score
        RETURN node.name AS name, node.type AS type,
               node.description AS description, score
        """

        with self.driver.session() as session:
            result = session.run(query, embedding=query_embedding, k=k)
            return [dict(r) for r in result]
```

### 3. Combine Graph and Vector Retrieval

```python
class GraphRAG:
    def __init__(self, vector_store, graph_store, llm):
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.llm = llm

    def retrieve(self, query: str, k: int = 5) -> dict:
        """Hybrid retrieval: vector + graph."""

        # Extract entities from query
        query_entities = self._extract_query_entities(query)

        # Vector retrieval
        query_embedding = embed(query)
        vector_results = self.vector_store.search(query_embedding, limit=k)

        # Graph retrieval
        graph_context = []
        for entity in query_entities:
            # Find entity in graph
            entity_node = self.graph_store.find_entity(entity)

            if entity_node:
                # Get relationships
                relationships = self.graph_store.get_relationships(entity_node)
                graph_context.append({
                    "entity": entity_node,
                    "relationships": relationships
                })

        # Combine contexts
        return {
            "text_chunks": vector_results,
            "graph_context": graph_context,
            "entities": query_entities
        }

    def generate(self, query: str, context: dict) -> str:
        """Generate answer using combined context."""

        # Format graph context
        graph_text = self._format_graph_context(context["graph_context"])

        # Format vector context
        vector_text = "\n\n".join([c.text for c in context["text_chunks"]])

        prompt = f"""
        Answer the question using both the text excerpts and knowledge graph.

        Question: {query}

        Knowledge Graph:
        {graph_text}

        Text Excerpts:
        {vector_text}

        Provide a comprehensive answer using both sources.
        """

        return self.llm.invoke(prompt)
```

## Common Patterns

### Pattern 1: Microsoft GraphRAG

```python
from graphrag.index import build_index
from graphrag.query import local_search, global_search

# Build index from documents
# This extracts entities, relationships, and creates communities
build_index(
    input_dir="./documents",
    output_dir="./graphrag_index",
    config={
        "llm": {
            "model": "gpt-4o-mini",
            "type": "openai"
        },
        "embeddings": {
            "model": "text-embedding-3-small"
        }
    }
)

# Local search: specific questions
local_result = local_search(
    query="What are the key features of product X?",
    index_dir="./graphrag_index"
)

# Global search: broad themes
global_result = global_search(
    query="What are the main themes in these documents?",
    index_dir="./graphrag_index"
)
```

### Pattern 2: LlamaIndex Knowledge Graph

```python
from llama_index.core import KnowledgeGraphIndex, StorageContext
from llama_index.graph_stores.neo4j import Neo4jGraphStore

# Configure graph store
graph_store = Neo4jGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
    database="neo4j"
)

storage_context = StorageContext.from_defaults(graph_store=graph_store)

# Build knowledge graph index
kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=10,
    include_embeddings=True
)

# Query with graph
query_engine = kg_index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize",
    embedding_mode="hybrid"
)

response = query_engine.query("What technologies does Company X use?")
```

### Pattern 3: Multi-hop Reasoning

```python
class MultiHopGraphRAG:
    """Answer questions requiring traversal through multiple relationships."""

    def __init__(self, graph_store, llm):
        self.graph = graph_store
        self.llm = llm

    def answer(self, query: str, max_hops: int = 3) -> str:
        """Multi-hop reasoning through knowledge graph."""

        # Decompose query into sub-questions
        sub_questions = self._decompose_query(query)

        # Answer each sub-question with graph traversal
        intermediate_answers = []

        for sq in sub_questions:
            # Find starting entities
            entities = self._extract_entities(sq)

            # Traverse graph
            paths = []
            for entity in entities:
                path = self._traverse(entity, sq, max_hops)
                paths.extend(path)

            # Generate sub-answer
            sub_answer = self._answer_with_paths(sq, paths)
            intermediate_answers.append(sub_answer)

        # Synthesize final answer
        return self._synthesize(query, intermediate_answers)

    def _traverse(self, start_entity: str, question: str, max_hops: int) -> list:
        """Traverse graph to find relevant paths."""

        query = """
        MATCH path = (start {name: $entity})-[*1..$max_hops]-(end)
        WHERE end.description CONTAINS $keyword
        RETURN path
        LIMIT 10
        """

        keywords = self._extract_keywords(question)

        paths = []
        for kw in keywords:
            result = self.graph.run(query, entity=start_entity, max_hops=max_hops, keyword=kw)
            paths.extend(result)

        return paths
```

### Pattern 4: Entity Resolution

```python
class EntityResolver:
    """Resolve entity mentions to canonical entities."""

    def __init__(self, graph_store, embedding_model):
        self.graph = graph_store
        self.embedder = embedding_model

    def resolve(self, mention: str, context: str = "") -> dict:
        """Resolve mention to canonical entity."""

        # Get embedding of mention in context
        mention_embedding = self.embedder.embed(f"{context} {mention}")

        # Find candidate entities
        candidates = self.graph.search_entities(
            embedding=mention_embedding,
            k=10
        )

        if not candidates:
            return {"resolved": False, "entity": None}

        # Score candidates
        best_match = None
        best_score = 0

        for candidate in candidates:
            # Combine embedding similarity with name similarity
            name_sim = self._name_similarity(mention, candidate["name"])
            embed_sim = candidate["score"]
            combined = 0.4 * name_sim + 0.6 * embed_sim

            if combined > best_score:
                best_score = combined
                best_match = candidate

        if best_score > 0.7:
            return {"resolved": True, "entity": best_match, "confidence": best_score}

        return {"resolved": False, "entity": None}

    def _name_similarity(self, a: str, b: str) -> float:
        """Calculate name similarity."""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
```

### Pattern 5: Community Detection for Global Queries

```python
from networkx.algorithms import community

class CommunityRAG:
    """Use graph communities for global/theme queries."""

    def __init__(self, graph, llm):
        self.graph = graph
        self.llm = llm
        self.communities = None

    def build_communities(self):
        """Detect communities in knowledge graph."""

        # Export to networkx
        nx_graph = self.graph.to_networkx()

        # Detect communities
        communities = community.louvain_communities(nx_graph)

        # Summarize each community
        self.communities = []
        for i, comm in enumerate(communities):
            nodes = list(comm)
            subgraph = nx_graph.subgraph(nodes)

            summary = self._summarize_community(subgraph)
            self.communities.append({
                "id": i,
                "nodes": nodes,
                "summary": summary,
                "size": len(nodes)
            })

    def _summarize_community(self, subgraph) -> str:
        """Generate summary of community."""

        # Get node descriptions
        descriptions = [
            subgraph.nodes[n].get("description", n)
            for n in subgraph.nodes()
        ]

        prompt = f"""
        Summarize the main theme of this group of related concepts:

        {chr(10).join(descriptions[:20])}

        Provide a 2-3 sentence summary of what connects these concepts.
        """

        return self.llm.invoke(prompt)

    def global_query(self, query: str) -> str:
        """Answer broad questions using community summaries."""

        # Find relevant communities
        relevant = []
        query_embedding = embed(query)

        for comm in self.communities:
            comm_embedding = embed(comm["summary"])
            similarity = cosine_similarity(query_embedding, comm_embedding)

            if similarity > 0.5:
                relevant.append(comm)

        # Generate answer from community summaries
        summaries = "\n\n".join([c["summary"] for c in relevant])

        return self.llm.invoke(f"""
        Based on these topic summaries, answer: {query}

        Summaries:
        {summaries}
        """)
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Over-extraction | Noisy graph | Set thresholds for entity confidence |
| Ignoring coreference | Duplicate entities | Entity resolution pipeline |
| Too many hops | Irrelevant paths | Limit max_hops, use semantic filtering |
| Skipping embeddings | Can't do similarity search | Embed entities and relationships |
| No community structure | Poor global queries | Build community hierarchy |

## Tools & References

### Related Skills
- faion-llamaindex-skill
- faion-vector-db-skill

### Related Agents
- faion-rag-agent

### External Resources
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [LlamaIndex Knowledge Graphs](https://docs.llamaindex.ai/en/stable/module_guides/indexing/knowledge_graph/)
- [Neo4j Vector Search](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
- [NetworkX](https://networkx.org/)

## Checklist

- [ ] Defined entity types for domain
- [ ] Defined relationship types
- [ ] Implemented entity extraction
- [ ] Set up graph database (Neo4j, etc.)
- [ ] Added entity embeddings
- [ ] Implemented entity resolution
- [ ] Combined vector + graph retrieval
- [ ] Added multi-hop reasoning
- [ ] Built community structure
- [ ] Tested on relationship queries

---

*Methodology: M-RAG-006 | Category: RAG/Vector DB*
*Related: faion-rag-agent, faion-llamaindex-skill*
