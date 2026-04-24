# Qdrant Vector Database

Production-grade vector database with hybrid search and quantization support.

## Overview

Qdrant is recommended for production self-hosted deployments. Fast, scalable, supports hybrid search with sparse vectors.

**Performance:** 41 QPS @ 50M vectors | **Scale:** 100M+ vectors | **Hosting:** Self/Cloud

---

## Installation

```bash
# Docker (recommended)
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant

# Docker Compose
# docker-compose.yml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334

# Python client
pip install qdrant-client
```

---

## Collection Management

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct,
    Filter, FieldCondition, MatchValue,
    HnswConfigDiff, OptimizersConfigDiff
)

# Connect
client = QdrantClient(host="localhost", port=6333)
# or cloud: QdrantClient(url="...", api_key="...")

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,           # OpenAI embedding dimension
        distance=Distance.COSINE
    ),
    hnsw_config=HnswConfigDiff(
        m=16,                # Number of connections per element
        ef_construct=100,    # Search quality during construction
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000,  # Start indexing after N points
    ),
    on_disk_payload=True,    # Large payloads on disk
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

---

## Upserting Vectors

```python
# Single point
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, ...],  # 1536-dim embedding
            payload={
                "text": "Document content here",
                "source": "file.pdf",
                "page": 5,
                "category": "technical",
                "created_at": "2024-01-15"
            }
        )
    ]
)

# Batch upsert (recommended for large datasets)
batch_size = 100
points = []

for i, doc in enumerate(documents):
    points.append(PointStruct(
        id=i,
        vector=get_embedding(doc["text"]),
        payload={"text": doc["text"], "source": doc["source"]}
    ))

    if len(points) >= batch_size:
        client.upsert(
            collection_name="documents",
            points=points
        )
        points = []

# Upsert remaining
if points:
    client.upsert(collection_name="documents", points=points)

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
            payload={"title": "Sample"}
        )
    ]
)
```

---

## Searching

```python
# Basic similarity search
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    score_threshold=0.7,  # Minimum similarity
)

for result in results:
    print(f"ID: {result.id}, Score: {result.score}")
    print(f"Text: {result.payload['text'][:100]}...")

# Search with payload filter
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
                key="page",
                range=Range(gte=1, lte=10)
            )
        ]
    ),
    limit=10,
    with_payload=True,
    with_vectors=False,  # Don't return vectors (faster)
)

# Search with named vectors
results = client.search(
    collection_name="multimodal",
    query_vector=("text", text_query_embedding),
    limit=10,
)
```

---

## Hybrid Search (Vector + Keyword)

```python
from qdrant_client.models import SparseVectorParams, SparseIndexParams

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

# Upsert with sparse vectors (BM25)
from qdrant_client.models import SparseVector

client.upsert(
    collection_name="hybrid_docs",
    points=[
        PointStruct(
            id=1,
            vector=dense_embedding,
            sparse_vectors={
                "bm25": SparseVector(
                    indices=[100, 500, 1000],  # Token IDs
                    values=[0.5, 0.3, 0.2]     # BM25 weights
                )
            },
            payload={"text": "..."}
        )
    ]
)

# Hybrid search with fusion
from qdrant_client.models import Prefetch, FusionQuery, Fusion

results = client.query_points(
    collection_name="hybrid_docs",
    prefetch=[
        Prefetch(query=dense_query, using="", limit=20),
        Prefetch(query=sparse_query, using="bm25", limit=20),
    ],
    query=FusionQuery(fusion=Fusion.RRF),  # Reciprocal Rank Fusion
    limit=10,
)
```

---

## Payload Indexing

```python
from qdrant_client.models import PayloadSchemaType

# Create payload index for faster filtering
client.create_payload_index(
    collection_name="documents",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)

client.create_payload_index(
    collection_name="documents",
    field_name="created_at",
    field_schema=PayloadSchemaType.DATETIME
)

client.create_payload_index(
    collection_name="documents",
    field_name="page",
    field_schema=PayloadSchemaType.INTEGER
)

# Full-text index for keyword search
client.create_payload_index(
    collection_name="documents",
    field_name="text",
    field_schema=PayloadSchemaType.TEXT
)
```

---

## Quantization (Memory Optimization)

```python
from qdrant_client.models import (
    ScalarQuantization, ScalarQuantizationConfig,
    ProductQuantization, ProductQuantizationConfig,
    BinaryQuantization, BinaryQuantizationConfig
)

# Scalar quantization (4x memory reduction)
client.update_collection(
    collection_name="documents",
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type="int8",
            quantile=0.99,
            always_ram=True,
        )
    )
)

# Binary quantization (32x memory reduction, fastest)
client.update_collection(
    collection_name="documents",
    quantization_config=BinaryQuantization(
        binary=BinaryQuantizationConfig(always_ram=True)
    )
)

# Search with quantization rescoring
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    search_params=SearchParams(
        quantization=QuantizationSearchParams(
            rescore=True,      # Rescore with original vectors
            oversampling=2.0,  # Fetch 2x candidates before rescoring
        )
    )
)
```

---

## Backup and Snapshots

```python
# Create snapshot
snapshot_info = client.create_snapshot(
    collection_name="documents"
)

# List snapshots
snapshots = client.list_snapshots(
    collection_name="documents"
)

# Restore from snapshot
client.recover_snapshot(
    collection_name="documents",
    location=f"http://localhost:6333/collections/documents/snapshots/{snapshot_name}"
)
```

---

## Connection Optimization

```python
# Use gRPC for better performance
client = QdrantClient(
    host="localhost",
    port=6334,  # gRPC port
    prefer_grpc=True,
    timeout=30,
)
```

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## Sources

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://github.com/qdrant/qdrant-client)
- [Qdrant Cloud](https://qdrant.tech/documentation/cloud/)
- [Hybrid Search Guide](https://qdrant.tech/articles/hybrid-search/)
