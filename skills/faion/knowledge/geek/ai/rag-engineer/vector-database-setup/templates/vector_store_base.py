"""
VectorStoreBase — provider-agnostic ABC for vector stores.

Implementations: PineconeStore, ChromaStore. Factory: VectorStoreFactory.

Usage:
    store = VectorStoreFactory.create("chroma", collection_name="docs")
    store.upsert([{"id": "1", "embedding": [...], "content": "text", "metadata": {...}}])
    results = store.search(query_vector, top_k=5)
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SearchResult:
    id: str
    score: float
    content: str
    metadata: Dict[str, Any]


class VectorStoreBase(ABC):
    @abstractmethod
    def upsert(self, documents: List[Dict]) -> None: ...

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int = 5) -> List[SearchResult]: ...

    @abstractmethod
    def delete(self, ids: List[str]) -> None: ...


class PineconeStore(VectorStoreBase):
    def __init__(self, index_name: str, api_key: str) -> None:
        from pinecone import Pinecone
        self.index = Pinecone(api_key=api_key).Index(index_name)

    def upsert(self, documents: List[Dict]) -> None:
        self.index.upsert(vectors=[
            {"id": d["id"], "values": d["embedding"], "metadata": d.get("metadata", {})}
            for d in documents
        ])

    def search(self, query_vector: List[float], top_k: int = 5) -> List[SearchResult]:
        r = self.index.query(vector=query_vector, top_k=top_k, include_metadata=True)
        return [SearchResult(id=m.id, score=m.score,
                             content=m.metadata.get("content", ""), metadata=m.metadata)
                for m in r.matches]

    def delete(self, ids: List[str]) -> None:
        self.index.delete(ids=ids)


class ChromaStore(VectorStoreBase):
    def __init__(self, collection_name: str, persist_dir: str = "./chroma") -> None:
        import chromadb
        self._col = chromadb.PersistentClient(path=persist_dir).get_or_create_collection(collection_name)

    def upsert(self, documents: List[Dict]) -> None:
        self._col.upsert(
            ids=[d["id"] for d in documents],
            embeddings=[d["embedding"] for d in documents],
            documents=[d.get("content", "") for d in documents],
            metadatas=[d.get("metadata", {}) for d in documents],
        )

    def search(self, query_vector: List[float], top_k: int = 5) -> List[SearchResult]:
        r = self._col.query(query_embeddings=[query_vector], n_results=top_k,
                            include=["documents", "metadatas", "distances"])
        return [
            SearchResult(id=r["ids"][0][i], score=1 - r["distances"][0][i],
                         content=r["documents"][0][i], metadata=r["metadatas"][0][i])
            for i in range(len(r["ids"][0]))
        ]

    def delete(self, ids: List[str]) -> None:
        self._col.delete(ids=ids)


class VectorStoreFactory:
    @staticmethod
    def create(provider: str, **kwargs) -> VectorStoreBase:
        if provider == "pinecone":
            return PineconeStore(index_name=kwargs["index_name"], api_key=kwargs["api_key"])
        if provider == "chroma":
            return ChromaStore(collection_name=kwargs["collection_name"],
                               persist_dir=kwargs.get("persist_dir", "./chroma"))
        raise ValueError(f"Unknown provider: {provider}")
