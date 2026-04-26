# Vector Database Code Examples

Comprehensive code examples for each major vector database, covering setup, indexing, querying, and advanced operations.

---

## Table of Contents

- [Qdrant](#qdrant)
- [Weaviate](#weaviate)
- [Milvus](#milvus)
- [Pinecone](#pinecone)
- [pgvector](#pgvector)
- [Chroma](#chroma)
- [Cross-Database Patterns](#cross-database-patterns)

---

## Qdrant

### Installation

```bash
# Docker
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant:latest

# Python client
pip install qdrant-client
```

### Connection

```python
from qdrant_client import QdrantClient

# Local connection
client = QdrantClient(host="localhost", port=6333)

# Cloud connection
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="your-api-key",
)

# With gRPC (faster)
client = QdrantClient(
    host="localhost",
    port=6334,
    prefer_grpc=True,
)
```

### Collection Management

```python
from qdrant_client.models import (
    VectorParams, Distance,
    HnswConfigDiff, OptimizersConfigDiff,
    ScalarQuantization, ScalarQuantizationConfig
)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,  # OpenAI text-embedding-3-small
        distance=Distance.COSINE,
    ),
    hnsw_config=HnswConfigDiff(
        m=16,
        ef_construct=100,
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000,
    ),
    on_disk_payload=True,  # Large payloads on disk
)

# Create with quantization
client.create_collection(
    collection_name="documents_quantized",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE,
    ),
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type="int8",
            quantile=0.99,
            always_ram=True,
        )
    ),
)

# Named vectors (multiple embeddings per point)
client.create_collection(
    collection_name="multimodal",
    vectors_config={
        "text": VectorParams(size=1536, distance=Distance.COSINE),
        "image": VectorParams(size=512, distance=Distance.COSINE),
    }
)

# Get collection info
info = client.get_collection("documents")
print(f"Points: {info.points_count}")
print(f"Indexed: {info.indexed_vectors_count}")
```

### Payload Indexing

```python
from qdrant_client.models import PayloadSchemaType, TextIndexParams, TokenizerType

# Keyword index (exact match)
client.create_payload_index(
    collection_name="documents",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD,
)

# Integer index (range queries)
client.create_payload_index(
    collection_name="documents",
    field_name="page",
    field_schema=PayloadSchemaType.INTEGER,
)

# DateTime index
client.create_payload_index(
    collection_name="documents",
    field_name="created_at",
    field_schema=PayloadSchemaType.DATETIME,
)

# Full-text index
client.create_payload_index(
    collection_name="documents",
    field_name="content",
    field_schema=TextIndexParams(
        type="text",
        tokenizer=TokenizerType.WORD,
        min_token_len=2,
        max_token_len=15,
        lowercase=True,
    ),
)
```

### Inserting Data

```python
from qdrant_client.models import PointStruct
import uuid

# Single point
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=str(uuid.uuid4()),
            vector=[0.1, 0.2, ...],  # 1536-dim embedding
            payload={
                "text": "Document content here",
                "source": "file.pdf",
                "page": 5,
                "category": "technical",
                "created_at": "2025-01-15T10:30:00Z",
            }
        )
    ]
)

# Batch upsert (recommended)
def batch_upsert(documents: list[dict], batch_size: int = 100):
    points = []

    for doc in documents:
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=doc["embedding"],
            payload={
                "text": doc["text"],
                "source": doc["source"],
                "metadata": doc.get("metadata", {}),
            }
        ))

        if len(points) >= batch_size:
            client.upsert(
                collection_name="documents",
                points=points,
                wait=False,  # Don't wait for indexing
            )
            points = []

    # Final batch
    if points:
        client.upsert(
            collection_name="documents",
            points=points,
            wait=True,  # Wait for final batch
        )

# Named vectors
client.upsert(
    collection_name="multimodal",
    points=[
        PointStruct(
            id=1,
            vector={
                "text": text_embedding,
                "image": image_embedding,
            },
            payload={"title": "Sample document"}
        )
    ]
)
```

### Basic Search

```python
from qdrant_client.models import SearchParams, QuantizationSearchParams

# Simple search
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    score_threshold=0.7,
)

for result in results:
    print(f"ID: {result.id}")
    print(f"Score: {result.score:.4f}")
    print(f"Text: {result.payload['text'][:100]}...")

# Search with quantization rescoring
results = client.search(
    collection_name="documents_quantized",
    query_vector=query_embedding,
    limit=10,
    search_params=SearchParams(
        quantization=QuantizationSearchParams(
            rescore=True,
            oversampling=2.0,
        )
    ),
)

# Search with named vectors
results = client.search(
    collection_name="multimodal",
    query_vector=("text", text_query_embedding),
    limit=10,
)
```

### Filtered Search

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range, MatchAny

# Single filter
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="category",
                match=MatchValue(value="technical"),
            )
        ]
    ),
    limit=10,
)

# Multiple filters (AND)
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="technical")),
            FieldCondition(key="page", range=Range(gte=1, lte=10)),
        ]
    ),
    limit=10,
)

# OR filters
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        should=[
            FieldCondition(key="category", match=MatchValue(value="technical")),
            FieldCondition(key="category", match=MatchValue(value="tutorial")),
        ]
    ),
    limit=10,
)

# NOT filter
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must_not=[
            FieldCondition(key="source", match=MatchValue(value="deprecated.pdf")),
        ]
    ),
    limit=10,
)

# Match any (IN)
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="category",
                match=MatchAny(any=["technical", "tutorial", "guide"]),
            )
        ]
    ),
    limit=10,
)

# Full-text filter
from qdrant_client.models import MatchText

results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="content",
                match=MatchText(text="machine learning"),
            )
        ]
    ),
    limit=10,
)
```

### Hybrid Search

```python
from qdrant_client.models import (
    SparseVectorParams, SparseIndexParams, SparseVector,
    Prefetch, FusionQuery, Fusion
)

# Create collection with sparse vectors
client.create_collection(
    collection_name="hybrid_docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    sparse_vectors_config={
        "bm25": SparseVectorParams(
            index=SparseIndexParams(on_disk=False)
        )
    }
)

# Upsert with sparse vectors
client.upsert(
    collection_name="hybrid_docs",
    points=[
        PointStruct(
            id=1,
            vector=dense_embedding,
            sparse_vectors={
                "bm25": SparseVector(
                    indices=[100, 500, 1000, 2500],  # Token IDs
                    values=[0.5, 0.3, 0.2, 0.1],      # BM25 weights
                )
            },
            payload={"text": "Document content..."}
        )
    ]
)

# Hybrid search with RRF fusion
results = client.query_points(
    collection_name="hybrid_docs",
    prefetch=[
        Prefetch(query=dense_query, using="", limit=20),
        Prefetch(query=sparse_query, using="bm25", limit=20),
    ],
    query=FusionQuery(fusion=Fusion.RRF),
    limit=10,
)
```

### Scroll (Pagination)

```python
# Scroll through all points
offset = None
all_points = []

while True:
    points, offset = client.scroll(
        collection_name="documents",
        limit=100,
        offset=offset,
        with_payload=True,
        with_vectors=False,
    )

    if not points:
        break

    all_points.extend(points)

    if offset is None:
        break

# Scroll with filter
points, _ = client.scroll(
    collection_name="documents",
    scroll_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="technical"))]
    ),
    limit=100,
)
```

### Delete Operations

```python
# Delete by ID
client.delete(
    collection_name="documents",
    points_selector=[1, 2, 3],
)

# Delete by filter
client.delete(
    collection_name="documents",
    points_selector=Filter(
        must=[
            FieldCondition(key="source", match=MatchValue(value="old_file.pdf"))
        ]
    ),
)
```

---

## Weaviate

### Installation

```bash
# Docker
docker run -p 8080:8080 -p 50051:50051 \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -v weaviate_data:/var/lib/weaviate \
  semitechnologies/weaviate:latest

# Python client
pip install weaviate-client
```

### Connection

```python
import weaviate
from weaviate.classes.init import Auth

# Local connection (v4 client)
client = weaviate.connect_to_local()

# Cloud connection
client = weaviate.connect_to_weaviate_cloud(
    cluster_url="https://your-cluster.weaviate.cloud",
    auth_credentials=Auth.api_key("your-api-key"),
)

# Custom connection
client = weaviate.connect_to_custom(
    http_host="localhost",
    http_port=8080,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False,
)
```

### Schema Design

```python
from weaviate.classes.config import Configure, Property, DataType, VectorDistances

# Create collection with schema
documents = client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.none(),  # Bring your own vectors
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="page", data_type=DataType.INT),
        Property(name="category", data_type=DataType.TEXT, skip_vectorization=True),
        Property(name="created_at", data_type=DataType.DATE),
    ],
    vector_index_config=Configure.VectorIndex.hnsw(
        ef=100,
        max_connections=16,
        distance_metric=VectorDistances.COSINE,
    ),
)

# Collection with auto-vectorization
documents_auto = client.collections.create(
    name="DocumentAuto",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-small",
    ),
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
    ],
)

# Get existing collection
documents = client.collections.get("Document")
```

### Cross-References (Knowledge Graph)

```python
# Create Author class
client.collections.create(
    name="Author",
    vectorizer_config=Configure.Vectorizer.none(),
    properties=[
        Property(name="name", data_type=DataType.TEXT),
        Property(name="email", data_type=DataType.TEXT),
    ],
)

# Add reference to Document
from weaviate.classes.config import ReferenceProperty

documents = client.collections.get("Document")
documents.config.add_reference(
    ReferenceProperty(
        name="hasAuthor",
        target_collection="Author",
    )
)
```

### Inserting Data

```python
import uuid

documents = client.collections.get("Document")

# Single insert
doc_uuid = documents.data.insert(
    properties={
        "text": "Document content...",
        "source": "file.pdf",
        "page": 1,
        "category": "technical",
    },
    vector=embedding_vector,
)

# Insert with specific UUID
documents.data.insert(
    uuid=uuid.uuid4(),
    properties={"text": "Content...", "source": "file.pdf"},
    vector=embedding_vector,
)

# Batch insert
with documents.batch.dynamic() as batch:
    for doc in documents_list:
        batch.add_object(
            properties={
                "text": doc["text"],
                "source": doc["source"],
                "page": doc["page"],
            },
            vector=doc["embedding"],
        )

# Insert with reference
authors = client.collections.get("Author")
author_uuid = authors.data.insert(
    properties={"name": "John Doe", "email": "john@example.com"},
)

documents.data.insert(
    properties={"text": "Content...", "source": "file.pdf"},
    vector=embedding_vector,
    references={"hasAuthor": author_uuid},
)
```

### Vector Search

```python
from weaviate.classes.query import MetadataQuery

documents = client.collections.get("Document")

# Basic vector search
response = documents.query.near_vector(
    near_vector=query_embedding,
    limit=10,
    return_metadata=MetadataQuery(certainty=True, distance=True),
)

for obj in response.objects:
    print(f"UUID: {obj.uuid}")
    print(f"Certainty: {obj.metadata.certainty:.4f}")
    print(f"Text: {obj.properties['text'][:100]}")

# Search by object (find similar)
response = documents.query.near_object(
    near_object=existing_uuid,
    limit=10,
)
```

### Filtered Search

```python
from weaviate.classes.query import Filter

documents = client.collections.get("Document")

# Single filter
response = documents.query.near_vector(
    near_vector=query_embedding,
    filters=Filter.by_property("category").equal("technical"),
    limit=10,
)

# Multiple filters (AND)
response = documents.query.near_vector(
    near_vector=query_embedding,
    filters=(
        Filter.by_property("category").equal("technical") &
        Filter.by_property("page").greater_than(0)
    ),
    limit=10,
)

# OR filters
response = documents.query.near_vector(
    near_vector=query_embedding,
    filters=(
        Filter.by_property("category").equal("technical") |
        Filter.by_property("category").equal("tutorial")
    ),
    limit=10,
)

# Range filter
response = documents.query.near_vector(
    near_vector=query_embedding,
    filters=Filter.by_property("page").greater_or_equal(1).less_or_equal(10),
    limit=10,
)

# Contains (array)
response = documents.query.near_vector(
    near_vector=query_embedding,
    filters=Filter.by_property("tags").contains_any(["python", "ml"]),
    limit=10,
)
```

### Hybrid Search

```python
documents = client.collections.get("Document")

# Hybrid search (BM25 + vector)
response = documents.query.hybrid(
    query="machine learning tutorial",
    vector=query_embedding,
    alpha=0.7,  # 0=pure BM25, 1=pure vector
    limit=10,
    return_metadata=MetadataQuery(score=True, explain_score=True),
)

for obj in response.objects:
    print(f"Score: {obj.metadata.score:.4f}")
    print(f"Text: {obj.properties['text'][:100]}")

# Hybrid with filters
response = documents.query.hybrid(
    query="machine learning",
    vector=query_embedding,
    alpha=0.7,
    filters=Filter.by_property("category").equal("technical"),
    limit=10,
)
```

### BM25 (Keyword) Search

```python
documents = client.collections.get("Document")

# Pure keyword search
response = documents.query.bm25(
    query="machine learning python",
    limit=10,
)

# With filters
response = documents.query.bm25(
    query="neural network",
    filters=Filter.by_property("category").equal("technical"),
    limit=10,
)
```

### GraphQL Queries (Advanced)

```python
# Raw GraphQL for complex queries
result = client.graphql_raw_query("""
{
  Get {
    Document(
      nearVector: {vector: [...], certainty: 0.7}
      where: {
        operator: And
        operands: [
          {path: ["category"], operator: Equal, valueText: "technical"}
          {path: ["page"], operator: GreaterThan, valueInt: 0}
        ]
      }
      limit: 10
    ) {
      text
      source
      page
      _additional {
        certainty
        distance
      }
    }
  }
}
""")

# Aggregate queries
result = client.graphql_raw_query("""
{
  Aggregate {
    Document {
      meta {
        count
      }
      category {
        count
        topOccurrences(limit: 5) {
          value
          occurs
        }
      }
    }
  }
}
""")
```

---

## Milvus

### Installation

```bash
# Docker Compose (standalone)
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start

# Python client
pip install pymilvus
```

### Connection

```python
from pymilvus import MilvusClient, connections

# Simple client
client = MilvusClient("milvus_demo.db")  # Local file

# Connect to server
client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus",
)

# Legacy connection
connections.connect(
    alias="default",
    host="localhost",
    port="19530",
)
```

### Collection Management

```python
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection

# Simple creation
client.create_collection(
    collection_name="documents",
    dimension=1536,
    metric_type="COSINE",
)

# Detailed schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="page", dtype=DataType.INT64),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
]

schema = CollectionSchema(fields=fields, description="Document collection")

collection = Collection(name="documents", schema=schema)
```

### Index Creation

```python
from pymilvus import Collection

collection = Collection("documents")

# HNSW index (recommended)
index_params = {
    "metric_type": "COSINE",
    "index_type": "HNSW",
    "params": {"M": 16, "efConstruction": 200},
}

collection.create_index(
    field_name="embedding",
    index_params=index_params,
)

# Load collection to memory
collection.load()

# IVF_FLAT index (alternative)
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024},
}
```

### Inserting Data

```python
# Simple insert
data = [
    {"text": "Document 1", "source": "file1.pdf", "embedding": embedding1},
    {"text": "Document 2", "source": "file2.pdf", "embedding": embedding2},
]

client.insert(collection_name="documents", data=data)

# Batch insert with Collection API
from pymilvus import Collection

collection = Collection("documents")

entities = [
    [text1, text2, text3],          # text field
    [source1, source2, source3],    # source field
    [1, 2, 3],                       # page field
    ["tech", "tech", "guide"],      # category field
    [emb1, emb2, emb3],             # embedding field
]

collection.insert(entities)
collection.flush()
```

### Vector Search

```python
# Simple search
results = client.search(
    collection_name="documents",
    data=[query_embedding],
    limit=10,
    output_fields=["text", "source", "page"],
)

for hits in results:
    for hit in hits:
        print(f"ID: {hit['id']}")
        print(f"Distance: {hit['distance']:.4f}")
        print(f"Text: {hit['entity']['text'][:100]}")

# Search with Collection API
collection = Collection("documents")
collection.load()

search_params = {
    "metric_type": "COSINE",
    "params": {"ef": 100},
}

results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param=search_params,
    limit=10,
    output_fields=["text", "source"],
)
```

### Filtered Search

```python
# Search with filter expression
results = client.search(
    collection_name="documents",
    data=[query_embedding],
    filter='category == "technical" and page > 0',
    limit=10,
    output_fields=["text", "source", "page"],
)

# Complex filters
filter_expr = '''
    category in ["technical", "tutorial"]
    and page >= 1
    and page <= 10
'''

results = client.search(
    collection_name="documents",
    data=[query_embedding],
    filter=filter_expr,
    limit=10,
)

# Text contains (requires text index)
filter_expr = 'text like "%machine learning%"'
```

### Hybrid Search

```python
from pymilvus import AnnSearchRequest, WeightedRanker, Collection

collection = Collection("hybrid_docs")

# Dense search request
dense_req = AnnSearchRequest(
    data=[dense_embedding],
    anns_field="dense_embedding",
    param={"metric_type": "COSINE", "params": {"ef": 100}},
    limit=20,
)

# Sparse search request
sparse_req = AnnSearchRequest(
    data=[sparse_embedding],
    anns_field="sparse_embedding",
    param={"metric_type": "IP"},
    limit=20,
)

# Hybrid search with weighted ranking
results = collection.hybrid_search(
    reqs=[dense_req, sparse_req],
    ranker=WeightedRanker(0.7, 0.3),  # 70% dense, 30% sparse
    limit=10,
    output_fields=["text", "source"],
)
```

---

## Pinecone

### Installation

```bash
pip install pinecone-client
```

### Setup

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key="your-api-key")

# Create serverless index
pc.create_index(
    name="documents",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
    ),
)

# Connect to index
index = pc.Index("documents")

# List indexes
for idx in pc.list_indexes():
    print(idx.name)
```

### Inserting Data

```python
# Single upsert
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": embedding,
            "metadata": {
                "text": "Document content...",
                "source": "file.pdf",
                "category": "technical",
                "page": 1,
            }
        }
    ],
    namespace="production",
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

# Upsert from DataFrame
import pandas as pd

df = pd.DataFrame({
    "id": ids,
    "values": embeddings,
    "metadata": metadatas,
})

index.upsert_from_dataframe(df, namespace="production", batch_size=100)
```

### Vector Search

```python
# Basic query
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True,
    namespace="production",
)

for match in results["matches"]:
    print(f"ID: {match['id']}")
    print(f"Score: {match['score']:.4f}")
    print(f"Metadata: {match['metadata']}")

# Query by ID
results = index.query(
    id="doc1",
    top_k=10,
    include_metadata=True,
)
```

### Filtered Search

```python
# Simple filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": {"$eq": "technical"}},
    include_metadata=True,
)

# Complex filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "$and": [
            {"category": {"$in": ["technical", "tutorial"]}},
            {"page": {"$gte": 1}},
            {"page": {"$lte": 10}},
        ]
    },
)

# NOT filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": {"$ne": "deprecated"}},
)
```

### Hybrid Search

```python
# Sparse-dense hybrid
results = index.query(
    vector=dense_embedding,
    sparse_vector={
        "indices": [100, 200, 300, 400],
        "values": [0.5, 0.3, 0.15, 0.05],
    },
    top_k=10,
    include_metadata=True,
)
```

### Index Management

```python
# Describe index
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
print(f"Namespaces: {stats['namespaces']}")

# Delete by IDs
index.delete(ids=["doc1", "doc2"], namespace="production")

# Delete by filter
index.delete(
    filter={"source": {"$eq": "old_file.pdf"}},
    namespace="production",
)

# Delete all in namespace
index.delete(delete_all=True, namespace="old_data")

# Delete entire index
pc.delete_index("documents")
```

---

## pgvector

### Installation

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;
```

```bash
pip install pgvector psycopg2-binary
```

### Table Setup

```sql
-- Create table with vector column
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR(255),
    page INTEGER,
    category VARCHAR(100),
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- HNSW index (recommended for production)
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Partial index for filtered queries
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WHERE category = 'technical';
```

### Python Usage

```python
import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np

# Connect and register
conn = psycopg2.connect("postgresql://user:pass@localhost/db")
register_vector(conn)
cur = conn.cursor()

# Insert single
cur.execute("""
    INSERT INTO documents (content, source, category, embedding)
    VALUES (%s, %s, %s, %s)
    RETURNING id
""", ("Document text...", "file.pdf", "technical", embedding))

doc_id = cur.fetchone()[0]
conn.commit()

# Batch insert
from psycopg2.extras import execute_values

data = [
    (doc["text"], doc["source"], doc["category"], doc["embedding"])
    for doc in documents
]

execute_values(cur, """
    INSERT INTO documents (content, source, category, embedding)
    VALUES %s
""", data)
conn.commit()
```

### Vector Search

```python
# Cosine similarity search
cur.execute("""
    SELECT id, content, source,
           1 - (embedding <=> %s) AS similarity
    FROM documents
    ORDER BY embedding <=> %s
    LIMIT %s
""", (query_embedding, query_embedding, 10))

results = cur.fetchall()

# L2 distance search
cur.execute("""
    SELECT id, content, embedding <-> %s AS distance
    FROM documents
    ORDER BY embedding <-> %s
    LIMIT 10
""", (query_embedding, query_embedding))

# Inner product (for normalized vectors)
cur.execute("""
    SELECT id, content, (embedding <#> %s) * -1 AS inner_product
    FROM documents
    ORDER BY embedding <#> %s
    LIMIT 10
""", (query_embedding, query_embedding))
```

### Filtered Search

```python
# With category filter
cur.execute("""
    SELECT id, content, 1 - (embedding <=> %s) AS similarity
    FROM documents
    WHERE category = %s
    ORDER BY embedding <=> %s
    LIMIT %s
""", (query_embedding, "technical", query_embedding, 10))

# Multiple filters
cur.execute("""
    SELECT id, content, 1 - (embedding <=> %s) AS similarity
    FROM documents
    WHERE category IN %s
      AND page BETWEEN %s AND %s
      AND created_at >= %s
    ORDER BY embedding <=> %s
    LIMIT %s
""", (
    query_embedding,
    ("technical", "tutorial"),
    1, 10,
    "2025-01-01",
    query_embedding,
    10
))
```

### Performance Tuning

```sql
-- Set ef_search for HNSW (higher = better recall, slower)
SET hnsw.ef_search = 100;

-- Check index usage
EXPLAIN ANALYZE
SELECT * FROM documents
ORDER BY embedding <=> '[...]'::vector
LIMIT 10;

-- Vacuum after bulk operations
VACUUM ANALYZE documents;
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            HnswIndex(
                name="document_embedding_idx",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]

# queries.py
from pgvector.django import CosineDistance, L2Distance

# Search
similar = Document.objects.annotate(
    distance=CosineDistance("embedding", query_embedding)
).filter(
    category="technical"
).order_by("distance")[:10]

# With score
for doc in similar:
    print(f"ID: {doc.id}, Distance: {doc.distance:.4f}")
```

---

## Chroma

### Installation

```bash
pip install chromadb
```

### Basic Usage

```python
import chromadb

# In-memory (default)
client = chromadb.Client()

# Persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"},  # cosine, l2, ip
)

# Get existing
collection = client.get_collection("documents")
```

### Adding Documents

```python
# Add with embeddings
collection.add(
    ids=["doc1", "doc2", "doc3"],
    embeddings=[emb1, emb2, emb3],
    metadatas=[
        {"source": "file1.pdf", "page": 1, "category": "technical"},
        {"source": "file2.pdf", "page": 2, "category": "tutorial"},
        {"source": "file3.pdf", "page": 3, "category": "guide"},
    ],
    documents=["Text 1", "Text 2", "Text 3"],  # Optional raw text
)

# Batch add
collection.add(
    ids=[f"doc{i}" for i in range(len(documents))],
    embeddings=[doc["embedding"] for doc in documents],
    metadatas=[doc["metadata"] for doc in documents],
    documents=[doc["text"] for doc in documents],
)
```

### Querying

```python
# Basic query
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    include=["documents", "metadatas", "distances"],
)

print(results["ids"])
print(results["distances"])
print(results["documents"])

# Query with filter
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={"category": {"$eq": "technical"}},
)

# Document content filter
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where_document={"$contains": "machine learning"},
)

# Complex filter
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={
        "$and": [
            {"category": {"$in": ["technical", "tutorial"]}},
            {"page": {"$gte": 1}},
        ]
    },
)
```

### Update and Delete

```python
# Update
collection.update(
    ids=["doc1"],
    embeddings=[new_embedding],
    metadatas=[{"source": "updated.pdf", "page": 1}],
)

# Upsert (update or insert)
collection.upsert(
    ids=["doc1", "doc4"],
    embeddings=[emb1, emb4],
    metadatas=[meta1, meta4],
)

# Delete by ID
collection.delete(ids=["doc1", "doc2"])

# Delete by filter
collection.delete(where={"source": {"$eq": "old_file.pdf"}})
```

### LangChain Integration

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create from documents
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="langchain_docs",
)

# Load existing
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="langchain_docs",
)

# Search
results = vectorstore.similarity_search_with_score(
    query="search query",
    k=10,
    filter={"category": "technical"},
)

# As retriever
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 10, "fetch_k": 20},
)
```

---

## Cross-Database Patterns

### Unified Search Interface

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    """Unified interface for vector databases."""

    @abstractmethod
    def upsert(self, vectors: List[Dict[str, Any]]) -> None:
        """Upsert vectors with metadata."""
        pass

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        filters: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        """Delete vectors by ID."""
        pass


class QdrantStore(VectorStore):
    def __init__(self, client, collection_name: str):
        self.client = client
        self.collection_name = collection_name

    def upsert(self, vectors: List[Dict[str, Any]]) -> None:
        from qdrant_client.models import PointStruct

        points = [
            PointStruct(
                id=v["id"],
                vector=v["vector"],
                payload=v.get("metadata", {}),
            )
            for v in vectors
        ]
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        filters: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        query_filter = self._build_filter(filters) if filters else None

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
        )

        return [
            {"id": r.id, "score": r.score, "metadata": r.payload}
            for r in results
        ]

    def _build_filter(self, filters: Dict[str, Any]):
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        conditions = [
            FieldCondition(key=k, match=MatchValue(value=v))
            for k, v in filters.items()
        ]
        return Filter(must=conditions)


class PineconeStore(VectorStore):
    def __init__(self, index, namespace: str = ""):
        self.index = index
        self.namespace = namespace

    def upsert(self, vectors: List[Dict[str, Any]]) -> None:
        pinecone_vectors = [
            {
                "id": v["id"],
                "values": v["vector"],
                "metadata": v.get("metadata", {}),
            }
            for v in vectors
        ]

        for i in range(0, len(pinecone_vectors), 100):
            batch = pinecone_vectors[i:i+100]
            self.index.upsert(vectors=batch, namespace=self.namespace)

    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        filters: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        filter_dict = {k: {"$eq": v} for k, v in (filters or {}).items()}

        results = self.index.query(
            vector=query_vector,
            top_k=limit,
            filter=filter_dict if filter_dict else None,
            include_metadata=True,
            namespace=self.namespace,
        )

        return [
            {"id": m["id"], "score": m["score"], "metadata": m.get("metadata", {})}
            for m in results["matches"]
        ]
```

### Hybrid Search with Reranking

```python
from sentence_transformers import CrossEncoder

class HybridSearcher:
    """Hybrid search with cross-encoder reranking."""

    def __init__(self, vector_store: VectorStore, reranker_model: str = None):
        self.vector_store = vector_store
        self.reranker = CrossEncoder(
            reranker_model or "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def search(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 10,
        oversample: int = 3,
        filters: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        # Step 1: Get candidates
        candidates = self.vector_store.search(
            query_vector=query_embedding,
            limit=k * oversample,
            filters=filters,
        )

        # Step 2: Rerank with cross-encoder
        pairs = [(query, c["metadata"].get("text", "")) for c in candidates]
        scores = self.reranker.predict(pairs)

        # Step 3: Combine scores
        for i, score in enumerate(scores):
            candidates[i]["rerank_score"] = float(score)
            candidates[i]["combined_score"] = (
                candidates[i]["score"] * 0.3 + score * 0.7
            )

        # Step 4: Sort and return top k
        candidates.sort(key=lambda x: x["combined_score"], reverse=True)
        return candidates[:k]
```

### MMR (Maximum Marginal Relevance)

```python
import numpy as np
from typing import List

def mmr_search(
    query_embedding: np.ndarray,
    candidate_embeddings: List[np.ndarray],
    candidates: List[Dict],
    k: int = 10,
    lambda_mult: float = 0.5,
) -> List[Dict]:
    """
    Select diverse results using MMR.

    Args:
        query_embedding: Query vector
        candidate_embeddings: Candidate vectors
        candidates: Candidate metadata
        k: Number of results to return
        lambda_mult: Diversity factor (0=max diversity, 1=max relevance)
    """
    query_embedding = np.array(query_embedding)
    candidate_embeddings = [np.array(e) for e in candidate_embeddings]

    selected = []
    remaining = list(range(len(candidates)))

    while len(selected) < k and remaining:
        mmr_scores = []

        for idx in remaining:
            # Similarity to query
            query_sim = np.dot(query_embedding, candidate_embeddings[idx])

            # Max similarity to already selected
            if selected:
                selected_sims = [
                    np.dot(candidate_embeddings[idx], candidate_embeddings[s])
                    for s in selected
                ]
                max_selected_sim = max(selected_sims)
            else:
                max_selected_sim = 0

            # MMR score
            mmr = lambda_mult * query_sim - (1 - lambda_mult) * max_selected_sim
            mmr_scores.append((idx, mmr))

        # Select best
        best_idx = max(mmr_scores, key=lambda x: x[1])[0]
        selected.append(best_idx)
        remaining.remove(best_idx)

    return [candidates[i] for i in selected]
```

---

*Code Examples v2.0*
*Part of vector-databases skill*
