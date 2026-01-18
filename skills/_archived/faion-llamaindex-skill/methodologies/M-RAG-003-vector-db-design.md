# M-RAG-003: Vector Database Design

## Overview

Vector databases store and index embeddings for efficient similarity search. Design considerations include schema, indexing strategies, partitioning, and metadata filtering. The right design enables fast, accurate retrieval at scale.

**When to use:** Building production RAG systems, semantic search, or any application requiring similarity matching.

## Core Concepts

### 1. Vector Database Comparison

| Database | Type | Best For | Hosting |
|----------|------|----------|---------|
| **Pinecone** | Managed | Ease of use | Cloud only |
| **Weaviate** | Open source | Flexibility | Self-host/Cloud |
| **Qdrant** | Open source | Performance | Self-host/Cloud |
| **Milvus** | Open source | Scale | Self-host/Cloud |
| **Chroma** | Embedded | Prototyping | Local |
| **pgvector** | Extension | Existing PG | Self-host/Cloud |
| **Redis Stack** | Extension | Existing Redis | Self-host/Cloud |

### 2. Index Types

| Index | Speed | Accuracy | Memory | Best For |
|-------|-------|----------|--------|----------|
| **Flat/Brute** | Slow | 100% | Low | Small datasets |
| **HNSW** | Fast | 98%+ | High | Production |
| **IVF** | Medium | 95%+ | Medium | Large datasets |
| **PQ** | Very Fast | 90%+ | Very Low | Memory constrained |
| **IVF-PQ** | Fast | 92%+ | Low | Billion scale |

### 3. Distance Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Cosine** | 1 - cos(A,B) | Normalized embeddings |
| **Euclidean** | L2 distance | Absolute positions |
| **Dot Product** | A . B | When magnitude matters |
| **Manhattan** | L1 distance | Sparse vectors |

## Best Practices

### 1. Design Effective Schema

```python
# Qdrant collection schema example
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PayloadSchemaType
)

def create_collection(client: QdrantClient, name: str):
    """Create optimized collection schema."""

    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(
            size=1536,  # Match embedding model
            distance=Distance.COSINE
        ),
        # Enable payload indexing for filtering
        payload_schema={
            "source": PayloadSchemaType.KEYWORD,
            "category": PayloadSchemaType.KEYWORD,
            "created_at": PayloadSchemaType.DATETIME,
            "word_count": PayloadSchemaType.INTEGER,
        },
        # HNSW index configuration
        hnsw_config={
            "m": 16,  # Connections per node
            "ef_construct": 100,  # Build quality
        },
        # Quantization for memory efficiency
        quantization_config={
            "scalar": {
                "type": "int8",
                "quantile": 0.99,
                "always_ram": True
            }
        }
    )
```

### 2. Partition Large Collections

```python
class PartitionedVectorStore:
    """Partition vectors by tenant or category."""

    def __init__(self, client):
        self.client = client

    def get_collection_name(self, tenant_id: str) -> str:
        """Get tenant-specific collection."""
        return f"documents_{tenant_id}"

    def create_tenant_collection(self, tenant_id: str):
        """Create isolated collection per tenant."""
        name = self.get_collection_name(tenant_id)
        create_collection(self.client, name)

    def insert(self, tenant_id: str, vectors: list, metadata: list):
        """Insert into tenant's collection."""
        collection = self.get_collection_name(tenant_id)
        self.client.upsert(
            collection_name=collection,
            points=self._prepare_points(vectors, metadata)
        )

    def search(self, tenant_id: str, query_vector: list, limit: int = 10):
        """Search within tenant's collection only."""
        collection = self.get_collection_name(tenant_id)
        return self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=limit
        )
```

### 3. Optimize for Query Patterns

```python
# Configure based on query patterns
index_configs = {
    "high_throughput": {
        # Many concurrent queries, moderate accuracy
        "hnsw_m": 8,
        "hnsw_ef_construct": 64,
        "hnsw_ef_search": 32
    },
    "high_accuracy": {
        # Maximum recall, slower
        "hnsw_m": 32,
        "hnsw_ef_construct": 200,
        "hnsw_ef_search": 128
    },
    "balanced": {
        # Good balance
        "hnsw_m": 16,
        "hnsw_ef_construct": 100,
        "hnsw_ef_search": 64
    },
    "memory_optimized": {
        # Lower memory, use quantization
        "hnsw_m": 12,
        "hnsw_ef_construct": 100,
        "quantization": "int8"
    }
}
```

## Common Patterns

### Pattern 1: Pinecone Setup

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key="your-api-key")

# Create index
pc.create_index(
    name="documents",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Connect to index
index = pc.Index("documents")

# Upsert vectors
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": embedding,
            "metadata": {"source": "wiki", "category": "science"}
        }
    ],
    namespace="default"  # Optional namespace for partitioning
)

# Query with filtering
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": {"$eq": "science"}},
    include_metadata=True
)
```

### Pattern 2: Weaviate Schema

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_weaviate_cloud(
    cluster_url="https://your-instance.weaviate.network",
    auth_credentials=weaviate.auth.AuthApiKey("your-key")
)

# Create collection with schema
client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.none(),  # We provide vectors
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="category", data_type=DataType.TEXT),
        Property(name="created_at", data_type=DataType.DATE),
    ],
    vector_index_config=Configure.VectorIndex.hnsw(
        distance_metric="cosine",
        ef_construction=128,
        max_connections=16,
        ef=64
    )
)

# Insert
collection = client.collections.get("Document")
collection.data.insert(
    properties={
        "content": "Document text...",
        "source": "file.pdf",
        "category": "technical"
    },
    vector=embedding
)

# Query with filters
results = collection.query.near_vector(
    near_vector=query_embedding,
    limit=10,
    filters=Filter.by_property("category").equal("technical")
)
```

### Pattern 3: Qdrant with Filtering

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct, Filter, FieldCondition, MatchValue, Range
)

client = QdrantClient(url="http://localhost:6333")

# Upsert with rich metadata
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=embedding,
            payload={
                "content": "Document text...",
                "source": "manual.pdf",
                "category": "technical",
                "pages": 50,
                "created_at": "2024-01-15T10:30:00Z"
            }
        )
    ]
)

# Complex filtered search
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="category",
                match=MatchValue(value="technical")
            ),
            FieldCondition(
                key="pages",
                range=Range(gte=10, lte=100)
            )
        ],
        must_not=[
            FieldCondition(
                key="source",
                match=MatchValue(value="deprecated.pdf")
            )
        ]
    ),
    limit=10,
    with_payload=True
)
```

### Pattern 4: pgvector Integration

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect
conn = psycopg2.connect("postgresql://user:pass@localhost/db")
register_vector(conn)

# Create table with vector column
cur = conn.cursor()
cur.execute("""
    CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        source VARCHAR(255),
        category VARCHAR(100),
        created_at TIMESTAMP DEFAULT NOW(),
        embedding vector(1536)
    );

    -- Create HNSW index
    CREATE INDEX ON documents
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

    -- Create filter indexes
    CREATE INDEX ON documents (category);
    CREATE INDEX ON documents (created_at);
""")

# Insert
cur.execute("""
    INSERT INTO documents (content, source, category, embedding)
    VALUES (%s, %s, %s, %s)
""", ("Document text", "file.pdf", "technical", embedding))

# Query with filter
cur.execute("""
    SELECT id, content, source, 1 - (embedding <=> %s) as similarity
    FROM documents
    WHERE category = %s
    ORDER BY embedding <=> %s
    LIMIT 10
""", (query_embedding, "technical", query_embedding))

results = cur.fetchall()
```

### Pattern 5: Hybrid Search Setup

```python
class HybridVectorStore:
    """Combine vector search with keyword search."""

    def __init__(self, qdrant_client, es_client):
        self.vector_db = qdrant_client
        self.keyword_db = es_client

    def index(self, doc_id: str, text: str, embedding: list, metadata: dict):
        """Index in both stores."""

        # Vector store
        self.vector_db.upsert(
            collection_name="documents",
            points=[{
                "id": doc_id,
                "vector": embedding,
                "payload": metadata
            }]
        )

        # Keyword store
        self.keyword_db.index(
            index="documents",
            id=doc_id,
            body={"content": text, **metadata}
        )

    def hybrid_search(
        self,
        query_text: str,
        query_embedding: list,
        vector_weight: float = 0.7,
        limit: int = 10
    ) -> list:
        """Combine vector and keyword results."""

        # Vector search
        vector_results = self.vector_db.search(
            collection_name="documents",
            query_vector=query_embedding,
            limit=limit * 2
        )

        # Keyword search
        keyword_results = self.keyword_db.search(
            index="documents",
            body={"query": {"match": {"content": query_text}}},
            size=limit * 2
        )

        # Combine and rerank using RRF
        combined = reciprocal_rank_fusion(
            [vector_results, keyword_results],
            weights=[vector_weight, 1 - vector_weight]
        )

        return combined[:limit]
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No metadata indexing | Slow filtered queries | Index filterable fields |
| Wrong distance metric | Poor results | Match to embedding model |
| Single huge collection | Slow, no isolation | Partition by tenant/category |
| Ignoring ef_search | Accuracy issues | Tune per query |
| No quantization | High memory cost | Use int8/binary when ok |
| Flat index at scale | Very slow | Use HNSW/IVF |

## Capacity Planning

```python
def estimate_requirements(
    num_vectors: int,
    dimensions: int,
    index_type: str = "hnsw"
) -> dict:
    """Estimate storage and memory requirements."""

    bytes_per_vector = dimensions * 4  # float32
    vector_storage = num_vectors * bytes_per_vector

    # HNSW index overhead (roughly 1.5x for m=16)
    index_overhead = 1.5 if index_type == "hnsw" else 1.1
    total_memory = vector_storage * index_overhead

    # With quantization
    quantized_memory = num_vectors * dimensions  # int8 = 1 byte

    return {
        "vectors": num_vectors,
        "vector_storage_gb": vector_storage / 1e9,
        "index_memory_gb": total_memory / 1e9,
        "quantized_memory_gb": quantized_memory * 1.5 / 1e9,
        "recommended_ram_gb": (total_memory * 1.2) / 1e9  # 20% headroom
    }

# Example: 10M documents, 1536 dimensions
reqs = estimate_requirements(10_000_000, 1536)
# vector_storage_gb: 57.2 GB
# index_memory_gb: 85.8 GB
# quantized_memory_gb: 22.9 GB
```

## Tools & References

### Related Skills
- faion-vector-db-skill
- faion-embeddings-skill

### Related Agents
- faion-rag-agent

### External Resources
- [Pinecone Docs](https://docs.pinecone.io/)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [pgvector](https://github.com/pgvector/pgvector)

## Checklist

- [ ] Selected appropriate vector database
- [ ] Designed collection schema
- [ ] Configured proper index type (HNSW, IVF)
- [ ] Set distance metric matching embeddings
- [ ] Indexed filterable metadata fields
- [ ] Implemented partitioning if multi-tenant
- [ ] Configured quantization for memory
- [ ] Tuned ef_search for accuracy/speed
- [ ] Estimated capacity requirements
- [ ] Set up monitoring and backups

---

*Methodology: M-RAG-003 | Category: RAG/Vector DB*
*Related: faion-rag-agent, faion-vector-db-skill*
