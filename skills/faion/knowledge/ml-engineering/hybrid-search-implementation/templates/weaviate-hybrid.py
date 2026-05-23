# purpose: minimal example of Weaviate native hybrid() call
# consumes: weaviate.Client connected to a collection with a `text` property + vectors
# produces: top-k documents fused server-side
# depends-on: content/01-core-rules.xml r1-weaviate-native-hybrid
# token-budget-impact: zero at runtime

import weaviate

client = weaviate.connect_to_local()
docs = client.collections.get("Docs")
results = docs.query.hybrid(
    query="JWT refresh token rotation",
    alpha=0.5,
    limit=10,
).objects
for r in results:
    print(r.uuid, r.metadata.score)
