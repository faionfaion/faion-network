"""hybrid_search_qdrant.py.
purpose: Qdrant native FusionQuery example
consumes: query string + sparse + dense vectors
produces: top-k document IDs + scores
depends-on: qdrant-client >= 1.10
token-budget-impact: +220t.
"""
from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Fusion, FusionQuery, Prefetch


def hybrid_search(
    client: QdrantClient,
    collection: str,
    dense_vec: list[float],
    sparse_vec: dict[int, float],
    limit: int = 10,
) -> list[dict]:
    """Run native Qdrant RRF hybrid search; one network call, server-side fusion."""
    result = client.query_points(
        collection_name=collection,
        prefetch=[
            Prefetch(query=dense_vec, using="dense", limit=100),
            Prefetch(query=sparse_vec, using="sparse", limit=100),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=limit,
        with_payload=True,
    )
    return [{"id": p.id, "score": p.score, "payload": p.payload} for p in result.points]


def get_alpha(query: str) -> float:
    """Query-adaptive alpha when using linear (non-RRF) fusion."""
    if '"' in query:
        return 0.2
    if any(c.isdigit() for c in query):
        return 0.3
    if len(query.split()) <= 3:
        return 0.5
    return 0.7
