---
name: faion-llamaindex-indexes-queries
user-invocable: false
description: "LlamaIndex: indexes, query engines, retrievers, response synthesis"
---

# LlamaIndex: Indexes & Query Engines

**Index Types, Query Engines, Retrievers, and Response Synthesis**

Part of the LlamaIndex skill series. See also:
- [llamaindex-basics.md](llamaindex-basics.md) - Installation, data connectors, node parsers
- [llamaindex-agents-eval.md](llamaindex-agents-eval.md) - Agents, evaluation, production patterns

---

## Quick Reference

| Component | Purpose |
|-----------|---------|
| **Index Types** | VectorStore, Keyword, KnowledgeGraph, Tree, Summary |
| **Query Engines** | Process queries and synthesize responses |
| **Retrievers** | Fetch relevant nodes from indices |
| **Response Synthesizers** | Generate final answers from retrieved context |

---

## Index Types

### VectorStoreIndex (Primary)

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# In-memory (development)
index = VectorStoreIndex.from_documents(documents)

# Persistent with Qdrant
client = QdrantClient(path="./qdrant_data")  # Local
# client = QdrantClient(url="http://localhost:6333")  # Server

vector_store = QdrantVectorStore(
    client=client,
    collection_name="my_collection",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

# Load existing index
index = VectorStoreIndex.from_vector_store(vector_store)
```

### Supported Vector Stores

| Store | Use Case | Code |
|-------|----------|------|
| **Qdrant** | Production, filtering | `llama-index-vector-stores-qdrant` |
| **Pinecone** | Managed, serverless | `llama-index-vector-stores-pinecone` |
| **Weaviate** | Hybrid search | `llama-index-vector-stores-weaviate` |
| **Chroma** | Local development | `llama-index-vector-stores-chroma` |
| **pgvector** | PostgreSQL native | `llama-index-vector-stores-postgres` |
| **Milvus** | Large scale | `llama-index-vector-stores-milvus` |
| **FAISS** | In-memory speed | `llama-index-vector-stores-faiss` |

### KeywordTableIndex (BM25)

```python
from llama_index.core import KeywordTableIndex

index = KeywordTableIndex.from_documents(
    documents,
    max_keywords_per_chunk=10,
)

# Good for exact keyword matching
query_engine = index.as_query_engine()
```

### KnowledgeGraphIndex

```python
from llama_index.core import KnowledgeGraphIndex
from llama_index.graph_stores.neo4j import Neo4jGraphStore

# With Neo4j
graph_store = Neo4jGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
)

index = KnowledgeGraphIndex.from_documents(
    documents,
    graph_store=graph_store,
    max_triplets_per_chunk=10,
    include_embeddings=True,
)

# Query with graph traversal
query_engine = index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize",
)
```

### TreeIndex (Summarization)

```python
from llama_index.core import TreeIndex

# Builds hierarchical summaries
index = TreeIndex.from_documents(
    documents,
    num_children=10,  # Children per node
)

# Good for summarization tasks
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
)
```

### SummaryIndex (Full Context)

```python
from llama_index.core import SummaryIndex

# Passes ALL nodes to LLM
index = SummaryIndex.from_documents(documents)

# Best for small documents, comprehensive answers
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
)
```

### ComposableGraph (Multi-Index)

```python
from llama_index.core import ComposableGraph, ListIndex

# Create multiple indices
index1 = VectorStoreIndex.from_documents(docs_tech)
index2 = VectorStoreIndex.from_documents(docs_finance)

# Compose into graph
graph = ComposableGraph.from_indices(
    ListIndex,
    [index1, index2],
    index_summaries=[
        "Technical documentation",
        "Financial reports",
    ],
)

# Router chooses relevant index
query_engine = graph.as_query_engine()
```

---

## Query Engines

### Basic Query Engine

```python
# From index
query_engine = index.as_query_engine(
    similarity_top_k=5,          # Number of chunks to retrieve
    response_mode="compact",      # Response synthesis mode
    streaming=False,              # Enable streaming
)

response = query_engine.query("What is RAG?")

print(response.response)           # Answer
print(response.source_nodes)       # Retrieved chunks
print(response.metadata)           # Query metadata
```

### Response Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **refine** | Iteratively refine answer | Long context, accuracy |
| **compact** | Compress chunks, single LLM call | Fast, good default |
| **tree_summarize** | Hierarchical summarization | Large retrievals |
| **simple_summarize** | Concatenate and summarize | Small context |
| **no_text** | Return only source nodes | Custom processing |
| **accumulate** | Separate answer per node | Multi-source answers |
| **compact_accumulate** | Compact + accumulate | Balanced |

```python
# Refine mode (most accurate)
query_engine = index.as_query_engine(
    response_mode="refine",
    similarity_top_k=10,
)

# Tree summarize (large context)
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
    similarity_top_k=20,
)
```

### SubQuestionQueryEngine

```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# Create tools from indices
tools = [
    QueryEngineTool(
        query_engine=tech_index.as_query_engine(),
        metadata=ToolMetadata(
            name="tech_docs",
            description="Technical documentation for the product",
        ),
    ),
    QueryEngineTool(
        query_engine=finance_index.as_query_engine(),
        metadata=ToolMetadata(
            name="financial_reports",
            description="Financial reports and metrics",
        ),
    ),
]

# Decomposes complex questions
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=tools,
    use_async=True,
)

response = query_engine.query(
    "Compare the technical roadmap with financial projections for Q1"
)
```

### RouterQueryEngine

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=tools,
)

# LLM routes to appropriate index
response = query_engine.query("What are our revenue numbers?")
```

### SQL + Vector Hybrid

```python
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

# SQL database
sql_database = SQLDatabase(engine, include_tables=["users", "orders"])

sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["users", "orders"],
)

# Combine with vector search
from llama_index.core.query_engine import SQLAutoVectorQueryEngine

query_engine = SQLAutoVectorQueryEngine(
    sql_query_engine=sql_query_engine,
    vector_query_engine=vector_index.as_query_engine(),
)

# Automatically routes text vs structured queries
response = query_engine.query(
    "How many orders do customers with 'gold' status have?"
)
```

---

## Retrievers

### VectorIndexRetriever

```python
from llama_index.core.retrievers import VectorIndexRetriever

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

nodes = retriever.retrieve("What is machine learning?")

for node in nodes:
    print(f"Score: {node.score}")
    print(f"Text: {node.text[:200]}...")
    print(f"Metadata: {node.metadata}")
```

### Hybrid Retriever (BM25 + Vector)

```python
from llama_index.core.retrievers import BM25Retriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# BM25 retriever
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=10,
)

# Vector retriever
vector_retriever = index.as_retriever(similarity_top_k=10)

# Fusion with reciprocal rank
retriever = QueryFusionRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    retriever_weights=[0.4, 0.6],
    num_queries=1,  # Generate additional query variants
    mode="reciprocal_rerank",
)

nodes = retriever.retrieve("machine learning applications")
```

### Auto-Merging Retriever

```python
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.node_parser import HierarchicalNodeParser

# Create hierarchical nodes
parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]
)
nodes = parser.get_nodes_from_documents(documents)

# Build index with storage for relationships
from llama_index.core.storage.docstore import SimpleDocumentStore
docstore = SimpleDocumentStore()
docstore.add_documents(nodes)

storage_context = StorageContext.from_defaults(docstore=docstore)
index = VectorStoreIndex(nodes, storage_context=storage_context)

# Auto-merging retriever
retriever = AutoMergingRetriever(
    index.as_retriever(similarity_top_k=12),
    storage_context=storage_context,
    simple_ratio_thresh=0.5,  # Merge if >50% children retrieved
)

# Returns parent nodes when enough children match
nodes = retriever.retrieve("detailed explanation of RAG")
```

### Reranking

```python
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.postprocessor.cohere_rerank import CohereRerank

# Cross-encoder reranking (local)
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2",
    top_n=5,
)

# Cohere reranking (API)
reranker = CohereRerank(
    api_key="...",
    top_n=5,
)

# Apply to query engine
query_engine = index.as_query_engine(
    similarity_top_k=20,  # Retrieve more
    node_postprocessors=[reranker],  # Rerank to top 5
)
```

---

## Response Synthesis

### Custom Prompts

```python
from llama_index.core import PromptTemplate

# Custom QA prompt
qa_prompt = PromptTemplate(
    """You are a helpful assistant. Use the following context to answer the question.

Context:
{context_str}

Question: {query_str}

Answer in a clear, concise manner. If you don't know, say "I don't know."
"""
)

query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
)

# Custom refine prompt
refine_prompt = PromptTemplate(
    """Given the original answer and new context, refine the answer.

Original answer: {existing_answer}
New context: {context_msg}

Refined answer:"""
)

query_engine = index.as_query_engine(
    refine_template=refine_prompt,
    response_mode="refine",
)
```

### Response Synthesizer

```python
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import ResponseMode

synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT,
    use_async=True,
)

# Manual synthesis
from llama_index.core.query_engine import RetrieverQueryEngine

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=synthesizer,
)
```

### Structured Output

```python
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser

class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float

output_parser = PydanticOutputParser(output_cls=AnalysisResult)

query_engine = index.as_query_engine(
    output_parser=output_parser,
)

response = query_engine.query("Analyze the document")
result: AnalysisResult = response.response
```

---

## Related Files

- [llamaindex-basics.md](llamaindex-basics.md) - Installation, data connectors, node parsers
- [llamaindex-agents-eval.md](llamaindex-agents-eval.md) - Agents, evaluation, production patterns
- [vector-databases.md](vector-databases.md) - Vector database operations
- [embeddings.md](embeddings.md) - Embedding models

---

*LlamaIndex Indexes & Query Engines v1.0*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement llamaindex-indexes-queries pattern | haiku | Straightforward implementation |
| Review llamaindex-indexes-queries implementation | sonnet | Requires code analysis |
| Optimize llamaindex-indexes-queries design | opus | Complex trade-offs |

