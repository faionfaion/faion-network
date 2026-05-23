# purpose: VectorStoreBase abstraction to keep callers vendor-agnostic
# consumes: vector + metadata records on upsert; query embedding on search
# produces: list of {id, score, payload}
# depends-on: content/01-core-rules.xml r3, r5
# token-budget-impact: zero at runtime; abstraction only

from abc import ABC, abstractmethod
from typing import List, Dict


class VectorStoreBase(ABC):
    @abstractmethod
    def upsert(self, records: List[Dict]) -> None: ...

    @abstractmethod
    def search(self, query_embedding: List[float], k: int, filter_: Dict = None) -> List[Dict]: ...

    @abstractmethod
    def delete(self, ids: List[str]) -> None: ...


class QdrantStore(VectorStoreBase):
    def __init__(self, client, collection: str):
        self.client = client
        self.collection = collection

    def upsert(self, records):
        self.client.upsert(self.collection, points=records)

    def search(self, query_embedding, k, filter_=None):
        return self.client.query_points(self.collection, query=query_embedding, limit=k, query_filter=filter_).points

    def delete(self, ids):
        self.client.delete(self.collection, points_selector=ids)
