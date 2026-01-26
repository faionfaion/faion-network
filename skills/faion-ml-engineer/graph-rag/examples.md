# GraphRAG Code Examples

## 1. Microsoft GraphRAG (Official)

### Installation

```bash
pip install graphrag
```

### Basic Indexing

```python
import asyncio
from graphrag.index import run_pipeline
from graphrag.config import GraphRagConfig

async def index_documents():
    config = GraphRagConfig.from_file("settings.yaml")

    await run_pipeline(
        config=config,
        input_dir="./input",
        output_dir="./output",
    )

asyncio.run(index_documents())
```

### Querying

```python
from graphrag.query import LocalSearch, GlobalSearch
from graphrag.config import GraphRagConfig

config = GraphRagConfig.from_file("settings.yaml")

# Local search (entity-focused)
local_search = LocalSearch(config)
local_result = await local_search.search(
    query="What is the relationship between Company A and Company B?"
)

# Global search (theme-focused)
global_search = GlobalSearch(config)
global_result = await global_search.search(
    query="What are the main themes in this dataset?"
)
```

## 2. Neo4j GraphRAG Python

### Installation

```bash
pip install neo4j-graphrag
```

### Graph Construction

```python
from neo4j import GraphDatabase
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline

# Connect to Neo4j
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

# Initialize LLM and embeddings
llm = OpenAILLM(model="gpt-4o", api_key="...")
embeddings = OpenAIEmbeddings(api_key="...")

# Define schema
entities = ["Person", "Organization", "Location", "Product"]
relations = ["WORKS_FOR", "LOCATED_IN", "PRODUCES", "KNOWS"]

# Build pipeline
pipeline = SimpleKGPipeline(
    driver=driver,
    llm=llm,
    embeddings=embeddings,
    entities=entities,
    relations=relations,
)

# Process documents
await pipeline.run_async(
    text="John works at Acme Corp in New York. Acme produces widgets."
)
```

### Hybrid Retrieval with Graph Traversal

```python
from neo4j_graphrag.retrievers import HybridCypherRetriever
from neo4j_graphrag.generation import GraphRAG

# Create retriever with graph traversal
retriever = HybridCypherRetriever(
    driver=driver,
    vector_index_name="entity_embeddings",
    fulltext_index_name="entity_fulltext",
    retrieval_query="""
    MATCH (node)-[r:RELATED_TO|WORKS_FOR|PRODUCES*1..2]-(related)
    RETURN node.name AS name,
           node.description AS description,
           collect(DISTINCT related.name) AS related_entities,
           collect(DISTINCT type(r)) AS relationships
    """,
)

# Create GraphRAG pipeline
rag = GraphRAG(
    retriever=retriever,
    llm=llm,
)

# Query
response = await rag.search(
    query="What products does the company John works for produce?",
    retriever_config={"top_k": 10}
)
```

### Vector + Graph Hybrid

```python
from neo4j_graphrag.retrievers import VectorCypherRetriever

retriever = VectorCypherRetriever(
    driver=driver,
    index_name="entity_embeddings",
    embedder=embeddings,
    retrieval_query="""
    // Start from vector-matched nodes
    WITH node, score

    // Traverse relationships
    OPTIONAL MATCH (node)-[r]->(related)
    WHERE type(r) IN ['WORKS_FOR', 'LOCATED_IN', 'PRODUCES']

    // Return enriched context
    RETURN node.name AS entity,
           node.description AS description,
           score AS relevance,
           collect({
               type: type(r),
               target: related.name,
               properties: properties(r)
           }) AS relationships
    ORDER BY score DESC
    LIMIT 10
    """,
)
```

## 3. LlamaIndex Property Graphs

### Installation

```bash
pip install llama-index llama-index-graph-stores-neo4j
```

### Graph Construction

```python
from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Initialize graph store
graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
)

# Create index with automatic extraction
index = PropertyGraphIndex.from_documents(
    documents,
    llm=OpenAI(model="gpt-4o"),
    embed_model=OpenAIEmbedding(),
    property_graph_store=graph_store,
    show_progress=True,
)
```

### Custom Entity Extraction

```python
from llama_index.core.indices.property_graph import (
    SchemaLLMPathExtractor,
    ImplicitPathExtractor,
)

# Define schema
entities = ["Person", "Organization", "Product", "Technology"]
relations = ["WORKS_AT", "USES", "DEVELOPS", "ACQUIRED"]

# Schema-guided extraction
schema_extractor = SchemaLLMPathExtractor(
    llm=OpenAI(model="gpt-4o"),
    possible_entities=entities,
    possible_relations=relations,
    strict=False,  # Allow entities outside schema
)

# Implicit extraction (co-occurrence based)
implicit_extractor = ImplicitPathExtractor()

# Build with multiple extractors
index = PropertyGraphIndex.from_documents(
    documents,
    kg_extractors=[schema_extractor, implicit_extractor],
    property_graph_store=graph_store,
)
```

### Querying

```python
from llama_index.core.indices.property_graph import (
    LLMSynonymRetriever,
    VectorContextRetriever,
)

# Synonym-based retrieval
synonym_retriever = LLMSynonymRetriever(
    index.property_graph_store,
    llm=OpenAI(model="gpt-4o"),
    include_text=True,
)

# Vector-based retrieval
vector_retriever = VectorContextRetriever(
    index.property_graph_store,
    embed_model=OpenAIEmbedding(),
    include_text=True,
)

# Combined query engine
query_engine = index.as_query_engine(
    sub_retrievers=[synonym_retriever, vector_retriever],
    llm=OpenAI(model="gpt-4o"),
)

response = query_engine.query(
    "What technologies does Company X use?"
)
```

## 4. LangChain with Neo4j

### Installation

```bash
pip install langchain langchain-openai langchain-community neo4j
```

### Graph Construction

```python
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document

# Connect to Neo4j
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password",
)

# Initialize transformer
llm = ChatOpenAI(model="gpt-4o", temperature=0)
transformer = LLMGraphTransformer(llm=llm)

# Extract graph from documents
documents = [
    Document(page_content="Elon Musk is CEO of Tesla. Tesla produces electric cars.")
]
graph_documents = transformer.convert_to_graph_documents(documents)

# Store in Neo4j
graph.add_graph_documents(graph_documents)
```

### Graph QA Chain

```python
from langchain_community.chains import GraphCypherQAChain

# Create QA chain
chain = GraphCypherQAChain.from_llm(
    llm=ChatOpenAI(model="gpt-4o"),
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True,  # Required for Cypher execution
)

# Query
response = chain.invoke({"query": "Who is the CEO of Tesla?"})
```

### Hybrid Vector + Graph

```python
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings

# Create vector index in Neo4j
vector_store = Neo4jVector.from_existing_graph(
    embedding=OpenAIEmbeddings(),
    url="bolt://localhost:7687",
    username="neo4j",
    password="password",
    index_name="entity_index",
    node_label="Entity",
    text_node_properties=["name", "description"],
    embedding_node_property="embedding",
)

# Hybrid retrieval
from langchain.retrievers import EnsembleRetriever

# Vector retriever
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Graph retriever (custom)
from langchain_core.retrievers import BaseRetriever

class GraphRetriever(BaseRetriever):
    graph: Neo4jGraph

    def _get_relevant_documents(self, query: str):
        # Extract entities from query
        # Traverse graph for context
        cypher = """
        MATCH (e:Entity)-[r*1..2]-(related)
        WHERE e.name CONTAINS $query
        RETURN e, r, related
        LIMIT 20
        """
        results = self.graph.query(cypher, {"query": query})
        # Convert to documents
        ...

# Combine retrievers
ensemble = EnsembleRetriever(
    retrievers=[vector_retriever, graph_retriever],
    weights=[0.5, 0.5],
)
```

## 5. Custom Implementation (NetworkX)

### Lightweight Graph Construction

```python
import networkx as nx
from openai import OpenAI
import json

client = OpenAI()

def extract_entities_and_relations(text: str, schema: dict) -> dict:
    """Extract entities and relationships using LLM."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """Extract entities and relationships from text.
                Return JSON: {"entities": [...], "relationships": [...]}"""
            },
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)

def build_graph(documents: list[str]) -> nx.DiGraph:
    """Build knowledge graph from documents."""
    G = nx.DiGraph()

    for doc in documents:
        extracted = extract_entities_and_relations(doc, schema={})

        # Add entities as nodes
        for entity in extracted["entities"]:
            G.add_node(
                entity["name"],
                type=entity["type"],
                description=entity.get("description", ""),
            )

        # Add relationships as edges
        for rel in extracted["relationships"]:
            G.add_edge(
                rel["source"],
                rel["target"],
                type=rel["type"],
                weight=rel.get("weight", 1.0),
            )

    return G
```

### Community Detection

```python
import community as community_louvain  # pip install python-louvain
# Or use: from graspologic.partition import hierarchical_louvain

def detect_communities(G: nx.Graph) -> dict:
    """Detect communities using Louvain algorithm."""
    # Convert to undirected for community detection
    G_undirected = G.to_undirected()

    # Detect communities
    partition = community_louvain.best_partition(G_undirected)

    # Group nodes by community
    communities = {}
    for node, comm_id in partition.items():
        if comm_id not in communities:
            communities[comm_id] = []
        communities[comm_id].append(node)

    return communities

def summarize_community(G: nx.Graph, nodes: list[str]) -> str:
    """Generate summary for a community."""
    # Gather community information
    subgraph = G.subgraph(nodes)

    entities = [G.nodes[n] for n in nodes]
    edges = [(u, v, G.edges[u, v]) for u, v in subgraph.edges()]

    # Generate summary with LLM
    prompt = f"""Summarize this community of entities:

    Entities: {entities}
    Relationships: {edges}

    Provide a 2-3 sentence summary of what this community represents."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
```

### Graph Retrieval

```python
def local_search(G: nx.DiGraph, query_entities: list[str], hops: int = 2) -> list:
    """Retrieve subgraph around query entities."""
    relevant_nodes = set(query_entities)

    # Expand by N hops
    for _ in range(hops):
        new_nodes = set()
        for node in relevant_nodes:
            if node in G:
                new_nodes.update(G.predecessors(node))
                new_nodes.update(G.successors(node))
        relevant_nodes.update(new_nodes)

    # Extract subgraph context
    subgraph = G.subgraph(relevant_nodes)

    context = []
    for node in subgraph.nodes():
        node_data = G.nodes[node]
        neighbors = list(G.neighbors(node))
        context.append({
            "entity": node,
            "type": node_data.get("type"),
            "description": node_data.get("description"),
            "relationships": [
                {"target": n, "type": G.edges[node, n].get("type")}
                for n in neighbors if (node, n) in G.edges
            ]
        })

    return context

def global_search(community_summaries: dict, query: str) -> str:
    """Search using community summaries (map-reduce)."""
    # Map: Get relevant summaries
    partial_responses = []

    for comm_id, summary in community_summaries.items():
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Answer the question based on this community summary. "
                               "If not relevant, say 'Not relevant'."
                },
                {
                    "role": "user",
                    "content": f"Summary: {summary}\n\nQuestion: {query}"
                }
            ],
        )
        answer = response.choices[0].message.content
        if "not relevant" not in answer.lower():
            partial_responses.append(answer)

    # Reduce: Combine partial responses
    combined_prompt = f"""Combine these partial answers into a comprehensive response:

    Question: {query}

    Partial answers:
    {chr(10).join(f'- {r}' for r in partial_responses)}
    """

    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": combined_prompt}],
    )

    return final_response.choices[0].message.content
```

## 6. LightRAG (Cost-Efficient)

### Installation

```bash
pip install lightrag-hku
```

### Usage

```python
from lightrag import LightRAG, QueryParam

# Initialize
rag = LightRAG(
    working_dir="./lightrag_data",
    llm_model_func=your_llm_func,  # Custom LLM function
    embedding_func=your_embedding_func,
)

# Insert documents
with open("document.txt", "r") as f:
    rag.insert(f.read())

# Query modes
# Naive (standard RAG)
result = rag.query("What is X?", param=QueryParam(mode="naive"))

# Local (entity-focused)
result = rag.query("What is X?", param=QueryParam(mode="local"))

# Global (theme-focused)
result = rag.query("What are main themes?", param=QueryParam(mode="global"))

# Hybrid (combined)
result = rag.query("Tell me about X", param=QueryParam(mode="hybrid"))
```

## 7. Weaviate with Knowledge Graphs

```python
import weaviate
from weaviate.classes.config import Property, DataType

client = weaviate.connect_to_local()

# Create collection with references (graph edges)
client.collections.create(
    name="Entity",
    properties=[
        Property(name="name", data_type=DataType.TEXT),
        Property(name="type", data_type=DataType.TEXT),
        Property(name="description", data_type=DataType.TEXT),
    ],
    references=[
        {"name": "relatedTo", "target_collection": "Entity"},
        {"name": "worksFor", "target_collection": "Entity"},
    ],
)

# Add entity with relationships
entity = client.collections.get("Entity")

# Add nodes
tesla_id = entity.data.insert(
    properties={"name": "Tesla", "type": "Organization"}
)
elon_id = entity.data.insert(
    properties={"name": "Elon Musk", "type": "Person"}
)

# Add edge
entity.data.reference_add(
    from_uuid=elon_id,
    from_property="worksFor",
    to=tesla_id,
)

# Hybrid query with graph traversal
response = entity.query.hybrid(
    query="Tesla CEO",
    limit=5,
    return_references=["worksFor", "relatedTo"],
)
```
