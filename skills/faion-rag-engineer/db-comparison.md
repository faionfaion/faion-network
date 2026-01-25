# Vector Database Comparison

Comparison of popular vector databases and selection guide.

---

## Database Comparison

| Database | Best For | Hosting | Scale | Performance | Filtering |
|----------|----------|---------|-------|-------------|-----------|
| **Qdrant** | Production RAG | Self/Cloud | 100M+ | 41 QPS @ 50M | Payload filters |
| **Weaviate** | Knowledge graphs | Self/Cloud | 10M+ | GraphQL native | Hybrid search |
| **pgvector** | Existing Postgres | Self-hosted | 10M | Good w/ indexes | SQL WHERE |
| **Chroma** | Prototyping | In-memory | 1M | Fast, simple | Metadata |
| **Pinecone** | Managed scale | Cloud only | 1B+ | Serverless | Metadata |
| **Milvus** | Large scale | Self/Cloud | 1B+ | GPU support | Attribute |

---

## Selection Guide

```
Rapid prototyping       --> Chroma
Existing PostgreSQL     --> pgvector
Production self-hosted  --> Qdrant (recommended)
Knowledge graphs        --> Weaviate
Fully managed           --> Pinecone
Massive scale (1B+)     --> Milvus or Pinecone
```

---

## pgvector (PostgreSQL Extension)

### Installation

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR(255),
    page INTEGER,
    category VARCHAR(100),
    embedding vector(1536),  -- OpenAI dimension
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create HNSW index (recommended)
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Or IVFFlat index (faster build, less accurate)
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- sqrt(n) for n rows
```

### Python Usage

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect and register vector type
conn = psycopg2.connect("postgresql://user:pass@localhost/db")
register_vector(conn)

cur = conn.cursor()

# Insert
cur.execute("""
    INSERT INTO documents (content, source, embedding)
    VALUES (%s, %s, %s)
""", ("Document text...", "file.pdf", embedding))

# Batch insert
from psycopg2.extras import execute_values

data = [(doc["text"], doc["source"], doc["embedding"]) for doc in documents]
execute_values(cur, """
    INSERT INTO documents (content, source, embedding)
    VALUES %s
""", data)

conn.commit()
```

### Searching

```python
# Cosine similarity (closer to 1 is better)
cur.execute("""
    SELECT id, content, source,
           1 - (embedding <=> %s) AS similarity
    FROM documents
    WHERE category = %s
    ORDER BY embedding <=> %s
    LIMIT %s
""", (query_embedding, "technical", query_embedding, 10))

results = cur.fetchall()

# L2 distance (smaller is better)
cur.execute("""
    SELECT id, content, embedding <-> %s AS distance
    FROM documents
    ORDER BY embedding <-> %s
    LIMIT 10
""", (query_embedding, query_embedding))

# Inner product (larger is better, for normalized vectors)
cur.execute("""
    SELECT id, content, embedding <#> %s AS neg_inner_product
    FROM documents
    ORDER BY embedding <#> %s
    LIMIT 10
""", (query_embedding, query_embedding))
```

### Performance Tuning

```sql
-- Set probes for IVFFlat (accuracy vs speed tradeoff)
SET ivfflat.probes = 10;  -- Default: 1

-- Set ef_search for HNSW
SET hnsw.ef_search = 100;  -- Default: 40

-- Partial index for filtered queries
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WHERE category = 'technical';

-- Vacuum and analyze after bulk inserts
VACUUM ANALYZE documents;

-- Check index usage
EXPLAIN ANALYZE
SELECT * FROM documents
ORDER BY embedding <=> '[...]'::vector
LIMIT 10;
```

### Django Integration

```python
# models.py
from django.db import models
from pgvector.django import VectorField, HnswIndex

class Document(models.Model):
    content = models.TextField()
    source = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    embedding = VectorField(dimensions=1536)

    class Meta:
        indexes = [
            HnswIndex(
                name="document_embedding_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]

# queries.py
from pgvector.django import CosineDistance

# Search
similar = Document.objects.annotate(
    distance=CosineDistance("embedding", query_embedding)
).filter(
    category="technical"
).order_by("distance")[:10]
```

---

## Pinecone (Managed)

### Setup

```bash
pip install pinecone-client
```

### Usage

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
            "metadata": {
                "text": "Document content...",
                "source": "file.pdf",
                "category": "technical"
            }
        }
    ],
    namespace="production"  # Optional namespace
)

# Batch upsert
vectors = [
    {"id": f"doc{i}", "values": emb, "metadata": meta}
    for i, (emb, meta) in enumerate(zip(embeddings, metadatas))
]

# Upsert in batches of 100
for i in range(0, len(vectors), 100):
    batch = vectors[i:i+100]
    index.upsert(vectors=batch, namespace="production")
```

### Querying

```python
# Basic query
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True,
    namespace="production"
)

for match in results["matches"]:
    print(f"ID: {match['id']}, Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")

# Filtered query
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "category": {"$eq": "technical"},
        "$and": [
            {"page": {"$gte": 1}},
            {"page": {"$lte": 10}}
        ]
    },
    include_metadata=True,
)

# Hybrid search with sparse-dense
results = index.query(
    vector=dense_embedding,
    sparse_vector={
        "indices": [100, 200, 300],
        "values": [0.5, 0.3, 0.2]
    },
    top_k=10,
)
```

### Index Management

```python
# Describe index
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
print(f"Namespaces: {stats['namespaces']}")

# Delete vectors
index.delete(ids=["doc1", "doc2"], namespace="production")
index.delete(filter={"source": "old.pdf"}, namespace="production")
index.delete(delete_all=True, namespace="old_namespace")

# List indexes
indexes = pc.list_indexes()
```

---

## Indexing Strategies

### HNSW (Hierarchical Navigable Small World)

Best for: Most use cases, balanced speed/accuracy

```
Parameters:
- M: Number of connections per element (default: 16)
  - Higher = better recall, more memory
  - Recommended: 12-48

- ef_construction: Search quality during build (default: 100)
  - Higher = better index quality, slower build
  - Recommended: 100-500

- ef_search: Search quality at query time (default: 40)
  - Higher = better recall, slower search
  - Recommended: 50-200
```

### IVF (Inverted File Index)

Best for: Large datasets, faster build time

```
Parameters:
- nlist: Number of clusters (default: sqrt(n))
  - Higher = more clusters, better accuracy
  - Recommended: sqrt(n) to 4*sqrt(n)

- nprobe: Clusters to search (default: 1)
  - Higher = better recall, slower search
  - Recommended: nlist/10 to nlist/4
```

### Quantization Comparison

| Method | Memory Reduction | Speed Impact | Accuracy Loss |
|--------|------------------|--------------|---------------|
| None | 1x | Baseline | None |
| Scalar (int8) | 4x | Faster | 1-2% |
| Product (PQ) | 8-32x | Faster | 3-5% |
| Binary | 32x | Fastest | 5-10% |

---

## Sources

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [Vector Database Comparison](https://benchmark.vectorview.ai/vectordbs.html)
