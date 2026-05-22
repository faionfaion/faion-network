# purpose: minimal example of Qdrant native hybrid via prefetch + FusionQuery
# consumes: pre-computed sparse vectors (indices, values) per query
# produces: fused top-k from dense + sparse legs
# depends-on: content/01-core-rules.xml r2-qdrant-precompute-sparse
# token-budget-impact: zero at runtime

from qdrant_client import QdrantClient, models

client = QdrantClient("localhost", port=6333)

dense_query = [0.1] * 1536  # from embedding model
sparse_query = models.SparseVector(indices=[5, 42, 99], values=[0.7, 0.4, 0.3])

response = client.query_points(
    collection_name="docs",
    prefetch=[
        models.Prefetch(query=dense_query, using="dense", limit=30),
        models.Prefetch(query=sparse_query, using="sparse", limit=30),
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    limit=10,
)
for p in response.points:
    print(p.id, p.score)
