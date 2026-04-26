"""
ChromaStore — minimal Chroma wrapper implementing upsert, search, delete.

Converts Chroma distances to similarity scores (1 - distance) for cosine space.

Usage:
    store = ChromaStore("documents", persist_dir="./chroma_db")
    store.upsert([{"id": "1", "embedding": [...], "content": "...", "metadata": {...}}])
    results = store.search(query_embedding, top_k=5)
    store.delete(["1", "2"])
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import chromadb


@dataclass
class SearchResult:
    id: str
    score: float      # similarity (1 - distance for cosine)
    content: str
    metadata: Dict[str, Any]


class ChromaStore:
    def __init__(
        self,
        collection_name: str,
        persist_dir: Optional[str] = "./chroma_db",
        distance: str = "cosine",  # cosine | l2 | ip
    ) -> None:
        if persist_dir:
            self._client = chromadb.PersistentClient(path=persist_dir)
        else:
            self._client = chromadb.Client()
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": distance},
        )
        self._distance = distance

    def upsert(self, documents: List[Dict[str, Any]]) -> None:
        """documents: list of {id, embedding, content, metadata}."""
        self._collection.upsert(
            ids=[str(d["id"]) for d in documents],
            embeddings=[d["embedding"] for d in documents],
            documents=[d.get("content", "") for d in documents],
            metadatas=[d.get("metadata", {}) for d in documents],
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None,
    ) -> List[SearchResult]:
        kwargs: Dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where
        r = self._collection.query(**kwargs)
        results = []
        for i in range(len(r["ids"][0])):
            dist = r["distances"][0][i]
            score = 1.0 - dist if self._distance == "cosine" else -dist
            results.append(SearchResult(
                id=r["ids"][0][i],
                score=score,
                content=r["documents"][0][i],
                metadata=r["metadatas"][0][i],
            ))
        return results

    def delete(self, ids: List[str]) -> None:
        self._collection.delete(ids=[str(i) for i in ids])
