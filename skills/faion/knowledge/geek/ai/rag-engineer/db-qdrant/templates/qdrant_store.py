# purpose: minimal Qdrant wrapper with collection + payload indexes + batch upsert + filtered search
# consumes: qdrant URL, collection name, distance metric, HNSW params, payload index fields
# produces: search response dict per templates/qdrant-schema.json
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: small
"""
QdrantStore — minimal Qdrant wrapper: create collection, batch upsert, filtered search.

Usage:
    store = QdrantStore("documents", vector_size=1536)
    store.upsert([{"id": 1, "embedding": [...], "payload": {"text": "...", "source": "a.pdf"}}])
    results = store.search(query_embedding, top_k=10, must_match={"category": "technical"})
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    HnswConfigDiff,
    MatchValue,
    OptimizersConfigDiff,
    PointStruct,
    VectorParams,
)


@dataclass
class SearchResult:
    id: int | str
    score: float
    payload: Dict[str, Any]


class QdrantStore:
    def __init__(
        self,
        collection_name: str,
        vector_size: int = 1536,
        host: str = "localhost",
        port: int = 6333,
        batch_size: int = 100,
    ) -> None:
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.client = QdrantClient(host=host, port=port)
        self._ensure_collection(vector_size)

    def _ensure_collection(self, vector_size: int) -> None:
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                hnsw_config=HnswConfigDiff(m=16, ef_construct=100),
                optimizers_config=OptimizersConfigDiff(indexing_threshold=20000),
                on_disk_payload=True,
            )

    def upsert(self, documents: List[Dict[str, Any]]) -> None:
        """documents: list of {id, embedding, payload}."""
        batch: List[PointStruct] = []
        for doc in documents:
            batch.append(PointStruct(
                id=doc["id"],
                vector=doc["embedding"],
                payload=doc.get("payload", {}),
            ))
            if len(batch) >= self.batch_size:
                self.client.upsert(collection_name=self.collection_name, points=batch)
                batch = []
        if batch:
            self.client.upsert(collection_name=self.collection_name, points=batch)

    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        score_threshold: float = 0.0,
        must_match: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        search_filter = None
        if must_match:
            search_filter = Filter(must=[
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in must_match.items()
            ])
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
            query_filter=search_filter,
            with_payload=True,
            with_vectors=False,
        )
        return [SearchResult(id=r.id, score=r.score, payload=r.payload or {}) for r in results]

    def snapshot(self) -> str:
        info = self.client.create_snapshot(collection_name=self.collection_name)
        return info.name
