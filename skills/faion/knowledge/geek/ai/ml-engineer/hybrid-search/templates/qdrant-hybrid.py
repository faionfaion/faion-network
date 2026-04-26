"""
Qdrant native hybrid search using sparse + dense prefetch with RRF fusion.
Requires: qdrant-client >= 1.9, sparse vectors indexed as "sparse" named vector.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Prefetch, FusionQuery, Fusion


def hybrid_search(
    client: QdrantClient,
    query: str,
    sparse_vector,    # SPLADE or BM25 sparse vector for the query
    dense_vector,     # Embedding vector for the query
    collection: str = "docs",
    top_k: int = 10,
    prefetch_k: int = 100,  # Always prefetch more than top_k
):
    """
    Run hybrid search: parallel sparse + dense retrieval, fused via RRF.
    Returns list of ScoredPoint.
    """
    return client.query_points(
        collection_name=collection,
        prefetch=[
            Prefetch(query=sparse_vector, using="sparse", limit=prefetch_k),
            Prefetch(query=dense_vector, using="dense", limit=prefetch_k),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=top_k,
    )


# Weaviate equivalent (alpha-based):
# results = collection.query.hybrid(
#     query=query_text,
#     alpha=0.7,  # 0=BM25, 1=vector
#     limit=10,
# )
