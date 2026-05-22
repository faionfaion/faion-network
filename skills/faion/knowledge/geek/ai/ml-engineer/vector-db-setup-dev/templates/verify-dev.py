# purpose: smoke test for dev Qdrant — create + insert + search
# consumes: nothing (uses local Qdrant from docker-compose)
# produces: code (exits 0 on smoke pass; 1 on fail)
# depends-on: qdrant-client matched to server major.minor
# token-budget-impact: 0
"""Smoke test for dev vector DB setup."""
from __future__ import annotations

import sys
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


def smoke(host: str = "localhost", port: int = 6333) -> int:
    client = QdrantClient(host=host, port=port)
    coll = f"smoke_{uuid.uuid4().hex[:8]}"
    client.create_collection(collection_name=coll,
                             vectors_config=VectorParams(size=4, distance=Distance.COSINE))
    client.upsert(
        collection_name=coll,
        points=[PointStruct(id=i, vector=[float(i), 0.0, 0.0, 0.0]) for i in range(10)],
    )
    hits = client.search(collection_name=coll, query_vector=[1.0, 0.0, 0.0, 0.0], limit=5)
    client.delete_collection(coll)
    if not hits:
        sys.stderr.write("FAIL: search returned no results\n")
        return 1
    sys.stdout.write(f"OK: smoke returned {len(hits)} hits\n")
    return 0


if __name__ == "__main__":
    sys.exit(smoke())
