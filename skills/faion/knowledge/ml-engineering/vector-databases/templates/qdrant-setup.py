# purpose: Qdrant collection setup with HNSW + scalar quantization + payload index
# consumes: collection name, dim, metric, tenant filter field
# produces: code (drop-in setup module)
# depends-on: qdrant-client >= 1.10
# token-budget-impact: ~200 tokens if loaded into LLM context
"""Qdrant collection setup: HNSW + scalar quantization + payload index."""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, HnswConfigDiff,
    ScalarQuantizationConfig, ScalarType, QuantizationConfig
)

client = QdrantClient("localhost", port=6333)

client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    hnsw_config=HnswConfigDiff(m=16, ef_construct=200),
    quantization_config=QuantizationConfig(
        scalar=ScalarQuantizationConfig(type=ScalarType.INT8, always_ram=True)
    ),
)

# Create payload index BEFORE bulk upsert — not after
client.create_payload_index(
    collection_name="docs",
    field_name="tenant_id",
    field_schema="keyword",
)

client.create_payload_index(
    collection_name="docs",
    field_name="source_file",
    field_schema="keyword",
)
