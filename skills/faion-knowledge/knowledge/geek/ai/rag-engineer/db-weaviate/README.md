# Weaviate Vector Database

Vector database with knowledge graph capabilities and hybrid search.

## Overview

Weaviate excels at knowledge graphs and hybrid search (semantic + keyword). GraphQL native.

**Best For:** Knowledge graphs | **Scale:** 10M+ vectors | **Hosting:** Self/Cloud

---

## Installation

```bash
# Docker
docker run -p 8080:8080 -p 50051:50051 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -v weaviate_data:/var/lib/weaviate \
  semitechnologies/weaviate:latest

# Python client
pip install weaviate-client
```

---

## Schema Design

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

# Connect
client = weaviate.connect_to_local()
# or cloud: weaviate.connect_to_wcs(cluster_url, auth_credentials)

# Create collection with schema
documents = client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.none(),  # Bring your own vectors
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="page", data_type=DataType.INT),
        Property(name="category", data_type=DataType.TEXT,
                 skip_vectorization=True),
    ],
    vector_index_config=Configure.VectorIndex.hnsw(
        ef=100,
        max_connections=16,
        distance_metric=Configure.VectorDistances.COSINE,
    ),
)

# With cross-references (knowledge graph)
client.collections.create(
    name="Author",
    properties=[
        Property(name="name", data_type=DataType.TEXT),
        Property(name="email", data_type=DataType.TEXT),
    ],
)

documents = client.collections.get("Document")
documents.config.add_reference(
    weaviate.classes.config.ReferenceProperty(
        name="hasAuthor",
        target_collection="Author"
    )
)
```

---

## Inserting Data

```python
documents = client.collections.get("Document")

# Single insert
uuid = documents.data.insert(
    properties={
        "text": "Document content...",
        "source": "file.pdf",
        "page": 1,
        "category": "technical"
    },
    vector=embedding_vector,
)

# Batch insert
with documents.batch.dynamic() as batch:
    for doc in documents_list:
        batch.add_object(
            properties={
                "text": doc["text"],
                "source": doc["source"],
            },
            vector=doc["embedding"],
        )
```

---

## Searching

```python
documents = client.collections.get("Document")

# Vector search
response = documents.query.near_vector(
    near_vector=query_embedding,
    limit=10,
    return_metadata=weaviate.classes.query.MetadataQuery(certainty=True)
)

for obj in response.objects:
    print(f"ID: {obj.uuid}")
    print(f"Certainty: {obj.metadata.certainty}")
    print(f"Text: {obj.properties['text'][:100]}")

# Hybrid search (vector + BM25)
response = documents.query.hybrid(
    query="search keywords",
    vector=query_embedding,
    alpha=0.5,  # 0=pure BM25, 1=pure vector
    limit=10,
)

# Filtered search
from weaviate.classes.query import Filter

response = documents.query.near_vector(
    near_vector=query_embedding,
    filters=Filter.by_property("category").equal("technical"),
    limit=10,
)
```

---

## GraphQL Queries (Advanced)

```python
# Raw GraphQL
result = client.graphql_raw_query("""
{
  Get {
    Document(
      nearVector: {vector: [...], certainty: 0.7}
      where: {path: ["category"], operator: Equal, valueText: "technical"}
      limit: 10
    ) {
      text
      source
      _additional {certainty}
    }
  }
}
""")

# Aggregate queries
result = client.graphql_raw_query("""
{
  Aggregate {
    Document {
      meta {count}
      category {
        count
        topOccurrences {value occurs}
      }
    }
  }
}
""")
```

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## Sources

- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Weaviate Python Client](https://weaviate.io/developers/weaviate/client-libraries/python)
- [Weaviate Cloud](https://weaviate.io/developers/wcs)
- [Knowledge Graphs with Weaviate](https://weaviate.io/blog/knowledge-graphs)
