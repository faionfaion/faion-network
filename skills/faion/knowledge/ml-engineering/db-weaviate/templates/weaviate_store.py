# purpose: minimal Weaviate v4 wrapper for schema + hybrid query + cross-refs
# consumes: cluster URL + API key + class definition + alpha + filters
# produces: hybrid search response dict per templates/weaviate-schema.json
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: small
"""WeaviateStore — minimal v4-client wrapper for hybrid + cross-ref queries."""
from __future__ import annotations

import weaviate
from weaviate.classes.config import Configure, Property, ReferenceProperty, DataType
from weaviate.classes.query import MetadataQuery


class WeaviateStore:
    def __init__(self, http_url: str, grpc_url: str, api_key: str | None = None) -> None:
        self.client = weaviate.connect_to_custom(
            http_host=http_url, http_port=8080, http_secure=False,
            grpc_host=grpc_url, grpc_port=50051, grpc_secure=False,
            auth_credentials=weaviate.auth.AuthApiKey(api_key) if api_key else None,
        )

    def ensure_class(self, name: str, replication_factor: int = 2) -> None:
        if not self.client.collections.exists(name):
            self.client.collections.create(
                name=name,
                properties=[
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="content", data_type=DataType.TEXT),
                ],
                references=[
                    ReferenceProperty(name="author", target_collection="Author"),
                ],
                replication_config=Configure.replication(factor=replication_factor),
            )

    def hybrid_search(self, class_name: str, query: str, alpha: float = 0.5, top_k: int = 5) -> dict:
        coll = self.client.collections.get(class_name)
        res = coll.query.hybrid(
            query=query, alpha=alpha, limit=top_k,
            return_metadata=MetadataQuery(score=True, explain_score=True),
        )
        hits = []
        for obj in res.objects:
            hits.append({
                "uuid": str(obj.uuid),
                "score": float(obj.metadata.score or 0.0),
                "vector_score": None,
                "bm25_score": None,
                "properties": dict(obj.properties),
            })
        return {
            "class_name": class_name, "query_type": "hybrid",
            "alpha": alpha, "top_k": top_k, "hits": hits,
        }

    def close(self) -> None:
        self.client.close()
