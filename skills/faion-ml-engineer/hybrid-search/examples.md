# Hybrid Search Code Examples

Production-ready code examples for implementing hybrid search with various vector databases and fusion methods.

## Table of Contents

1. [Weaviate Hybrid Search](#weaviate-hybrid-search)
2. [Qdrant Hybrid Search](#qdrant-hybrid-search)
3. [Pinecone Hybrid Search](#pinecone-hybrid-search)
4. [Elasticsearch Hybrid Search](#elasticsearch-hybrid-search)
5. [pgvector + BM25 Hybrid](#pgvector--bm25-hybrid)
6. [MongoDB Atlas Hybrid Search](#mongodb-atlas-hybrid-search)
7. [Fusion Method Examples](#fusion-method-examples)
8. [LangChain Integration](#langchain-integration)
9. [LlamaIndex Integration](#llamaindex-integration)
10. [Performance Optimization Examples](#performance-optimization-examples)

---

## Weaviate Hybrid Search

Weaviate provides native hybrid search with built-in BM25 and vector fusion.

### Basic Hybrid Search

```python
import weaviate
from weaviate.classes.query import HybridFusion, MetadataQuery
from weaviate.classes.init import Auth
import os

# Connect to Weaviate
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ["WEAVIATE_URL"],
    auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
    headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]}
)

def weaviate_hybrid_search(
    collection_name: str,
    query: str,
    alpha: float = 0.5,
    limit: int = 10,
    filters: dict | None = None
) -> list[dict]:
    """
    Weaviate native hybrid search.

    Args:
        collection_name: Name of the collection to search
        query: Search query string
        alpha: Balance between vector (1.0) and keyword (0.0) search
        limit: Maximum number of results
        filters: Optional metadata filters

    Returns:
        List of search results with content and scores
    """
    collection = client.collections.get(collection_name)

    # Build filter if provided
    weaviate_filter = None
    if filters:
        from weaviate.classes.query import Filter
        conditions = [
            Filter.by_property(key).equal(value)
            for key, value in filters.items()
        ]
        weaviate_filter = conditions[0] if len(conditions) == 1 else Filter.all_of(conditions)

    response = collection.query.hybrid(
        query=query,
        alpha=alpha,
        limit=limit,
        fusion_type=HybridFusion.RELATIVE_SCORE,  # or RANKED for RRF
        return_metadata=MetadataQuery(score=True, explain_score=True),
        filters=weaviate_filter
    )

    return [
        {
            "content": obj.properties.get("content"),
            "metadata": {k: v for k, v in obj.properties.items() if k != "content"},
            "score": obj.metadata.score,
            "explain": obj.metadata.explain_score
        }
        for obj in response.objects
    ]


# Example with different fusion types
def weaviate_rrf_search(collection_name: str, query: str, limit: int = 10) -> list[dict]:
    """Use Reciprocal Rank Fusion instead of relative score fusion."""
    collection = client.collections.get(collection_name)

    response = collection.query.hybrid(
        query=query,
        limit=limit,
        fusion_type=HybridFusion.RANKED,  # RRF fusion
        return_metadata=MetadataQuery(score=True)
    )

    return [
        {"content": obj.properties.get("content"), "score": obj.metadata.score}
        for obj in response.objects
    ]
```

### Weaviate Collection Setup

```python
from weaviate.classes.config import Configure, Property, DataType

def create_hybrid_collection(client, collection_name: str, embedding_model: str = "text-embedding-3-small"):
    """Create a Weaviate collection with hybrid search capabilities."""

    client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model=embedding_model,
            vectorize_collection_name=False
        ),
        properties=[
            Property(name="content", data_type=DataType.TEXT),
            Property(name="title", data_type=DataType.TEXT),
            Property(name="source", data_type=DataType.TEXT),
            Property(name="chunk_id", data_type=DataType.INT),
            Property(name="created_at", data_type=DataType.DATE),
        ],
        # BM25 configuration
        inverted_index_config=Configure.inverted_index(
            bm25_b=0.75,
            bm25_k1=1.5
        )
    )
```

---

## Qdrant Hybrid Search

Qdrant supports hybrid search through sparse-dense vector combinations.

### Setup with SPLADE Sparse Vectors

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models
from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch
import numpy as np

# Initialize clients
qdrant = QdrantClient(url="http://localhost:6333")

# SPLADE sparse encoder
splade_tokenizer = AutoTokenizer.from_pretrained("naver/splade-cocondenser-ensembledistil")
splade_model = AutoModelForMaskedLM.from_pretrained("naver/splade-cocondenser-ensembledistil")

def encode_sparse(text: str) -> tuple[list[int], list[float]]:
    """Generate SPLADE sparse vector."""
    tokens = splade_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        output = splade_model(**tokens)

    # Get sparse representation
    vec = torch.max(
        torch.log(1 + torch.relu(output.logits)) * tokens.attention_mask.unsqueeze(-1),
        dim=1
    )[0].squeeze()

    # Get non-zero indices and values
    indices = vec.nonzero().squeeze().cpu().tolist()
    values = vec[indices].cpu().tolist()

    if isinstance(indices, int):
        indices = [indices]
        values = [values]

    return indices, values


def create_qdrant_hybrid_collection(collection_name: str, dense_dim: int = 1536):
    """Create Qdrant collection with sparse-dense vectors."""

    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": models.VectorParams(
                size=dense_dim,
                distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={
            "sparse": models.SparseVectorParams(
                index=models.SparseIndexParams(on_disk=False)
            )
        }
    )


def qdrant_hybrid_search(
    collection_name: str,
    query: str,
    query_dense_vector: list[float],
    limit: int = 10,
    filters: dict | None = None
) -> list[dict]:
    """
    Qdrant hybrid search with prefetch and RRF fusion.
    """
    # Generate sparse vector for query
    sparse_indices, sparse_values = encode_sparse(query)

    # Build filter if provided
    qdrant_filter = None
    if filters:
        conditions = [
            models.FieldCondition(key=k, match=models.MatchValue(value=v))
            for k, v in filters.items()
        ]
        qdrant_filter = models.Filter(must=conditions)

    # Hybrid search with prefetch
    results = qdrant.query_points(
        collection_name=collection_name,
        prefetch=[
            # Dense vector search
            models.Prefetch(
                query=query_dense_vector,
                using="dense",
                limit=limit * 2,
                filter=qdrant_filter
            ),
            # Sparse vector search
            models.Prefetch(
                query=models.SparseVector(indices=sparse_indices, values=sparse_values),
                using="sparse",
                limit=limit * 2,
                filter=qdrant_filter
            )
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),  # RRF fusion
        limit=limit
    )

    return [
        {
            "id": point.id,
            "content": point.payload.get("content"),
            "metadata": {k: v for k, v in point.payload.items() if k != "content"},
            "score": point.score
        }
        for point in results.points
    ]


def qdrant_upsert_hybrid(
    collection_name: str,
    doc_id: str,
    content: str,
    dense_vector: list[float],
    metadata: dict | None = None
):
    """Upsert document with both dense and sparse vectors."""
    sparse_indices, sparse_values = encode_sparse(content)

    payload = {"content": content}
    if metadata:
        payload.update(metadata)

    qdrant.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=doc_id,
                vector={
                    "dense": dense_vector,
                    "sparse": models.SparseVector(indices=sparse_indices, values=sparse_values)
                },
                payload=payload
            )
        ]
    )
```

---

## Pinecone Hybrid Search

Pinecone supports hybrid search with sparse-dense vectors.

```python
from pinecone import Pinecone, ServerlessSpec
from pinecone_text.sparse import BM25Encoder
import os

# Initialize
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Create index with sparse-dense support
def create_pinecone_hybrid_index(index_name: str, dimension: int = 1536):
    """Create Pinecone index for hybrid search."""

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="dotproduct",  # Required for hybrid
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return pc.Index(index_name)


# Initialize BM25 encoder
class PineconeHybridSearch:
    def __init__(self, index_name: str, documents: list[str] | None = None):
        self.index = pc.Index(index_name)
        self.bm25 = BM25Encoder()

        if documents:
            self.bm25.fit(documents)

    def fit_bm25(self, documents: list[str]):
        """Fit BM25 on corpus."""
        self.bm25.fit(documents)

    def save_bm25(self, path: str):
        """Save BM25 params for later use."""
        self.bm25.dump(path)

    def load_bm25(self, path: str):
        """Load BM25 params."""
        self.bm25 = BM25Encoder().load(path)

    def upsert_hybrid(
        self,
        doc_id: str,
        content: str,
        dense_vector: list[float],
        metadata: dict | None = None
    ):
        """Upsert document with sparse and dense vectors."""
        sparse_vector = self.bm25.encode_documents(content)

        self.index.upsert(
            vectors=[{
                "id": doc_id,
                "values": dense_vector,
                "sparse_values": sparse_vector,
                "metadata": {"content": content, **(metadata or {})}
            }]
        )

    def search(
        self,
        query: str,
        dense_vector: list[float],
        alpha: float = 0.5,
        top_k: int = 10,
        filters: dict | None = None
    ) -> list[dict]:
        """
        Hybrid search with configurable alpha.

        alpha: 0 = pure sparse, 1 = pure dense
        """
        sparse_vector = self.bm25.encode_queries(query)

        # Scale vectors based on alpha
        scaled_dense = [v * alpha for v in dense_vector]
        scaled_sparse = {
            "indices": sparse_vector["indices"],
            "values": [v * (1 - alpha) for v in sparse_vector["values"]]
        }

        results = self.index.query(
            vector=scaled_dense,
            sparse_vector=scaled_sparse,
            top_k=top_k,
            include_metadata=True,
            filter=filters
        )

        return [
            {
                "id": match.id,
                "content": match.metadata.get("content"),
                "metadata": {k: v for k, v in match.metadata.items() if k != "content"},
                "score": match.score
            }
            for match in results.matches
        ]


# Usage example
def pinecone_example():
    # Initialize with documents
    documents = [
        "Python async programming with asyncio",
        "Database connection pooling in PostgreSQL",
        "FastAPI async endpoint best practices"
    ]

    searcher = PineconeHybridSearch("my-hybrid-index", documents)

    # Search
    query = "async database connection"
    dense_vec = get_embedding(query)  # Your embedding function

    results = searcher.search(
        query=query,
        dense_vector=dense_vec,
        alpha=0.5,
        top_k=10
    )

    return results
```

---

## Elasticsearch Hybrid Search

Elasticsearch 8.x+ supports native hybrid search with kNN and BM25.

```python
from elasticsearch import Elasticsearch
from typing import Any

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "password")
)

def create_hybrid_index(index_name: str, dense_dim: int = 1536):
    """Create Elasticsearch index for hybrid search."""

    mapping = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stop", "snowball"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "title": {
                    "type": "text",
                    "analyzer": "custom_analyzer",
                    "boost": 2.0
                },
                "embedding": {
                    "type": "dense_vector",
                    "dims": dense_dim,
                    "index": True,
                    "similarity": "cosine"
                },
                "source": {"type": "keyword"},
                "created_at": {"type": "date"}
            }
        }
    }

    es.indices.create(index=index_name, body=mapping, ignore=400)


def es_hybrid_search_rrf(
    index_name: str,
    query_text: str,
    query_vector: list[float],
    k: int = 10,
    rrf_rank_constant: int = 60,
    filters: dict | None = None
) -> list[dict]:
    """
    Elasticsearch hybrid search using RRF fusion (ES 8.8+).
    """
    # Build filter clause
    filter_clause = []
    if filters:
        for key, value in filters.items():
            filter_clause.append({"term": {key: value}})

    query = {
        "retriever": {
            "rrf": {
                "retrievers": [
                    # BM25 retriever
                    {
                        "standard": {
                            "query": {
                                "bool": {
                                    "should": [
                                        {"match": {"content": {"query": query_text}}},
                                        {"match": {"title": {"query": query_text, "boost": 2}}}
                                    ],
                                    "filter": filter_clause
                                }
                            }
                        }
                    },
                    # kNN retriever
                    {
                        "knn": {
                            "field": "embedding",
                            "query_vector": query_vector,
                            "k": k * 2,
                            "num_candidates": 100,
                            "filter": filter_clause
                        }
                    }
                ],
                "rank_constant": rrf_rank_constant,
                "rank_window_size": k * 3
            }
        },
        "size": k
    }

    response = es.search(index=index_name, body=query)

    return [
        {
            "id": hit["_id"],
            "content": hit["_source"].get("content"),
            "title": hit["_source"].get("title"),
            "score": hit["_score"],
            "source": hit["_source"].get("source")
        }
        for hit in response["hits"]["hits"]
    ]


def es_hybrid_search_linear(
    index_name: str,
    query_text: str,
    query_vector: list[float],
    alpha: float = 0.5,
    k: int = 10,
    filters: dict | None = None
) -> list[dict]:
    """
    Elasticsearch hybrid search with linear score combination.
    Uses script_score for custom fusion.
    """
    filter_clause = []
    if filters:
        for key, value in filters.items():
            filter_clause.append({"term": {key: value}})

    query = {
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"content": {"query": query_text}}},
                            {"match": {"title": {"query": query_text, "boost": 2}}}
                        ],
                        "filter": filter_clause,
                        "minimum_should_match": 0
                    }
                },
                "script": {
                    "source": """
                        double bm25Score = _score;
                        double vectorScore = cosineSimilarity(params.query_vector, 'embedding') + 1.0;
                        return params.alpha * vectorScore + (1 - params.alpha) * bm25Score;
                    """,
                    "params": {
                        "query_vector": query_vector,
                        "alpha": alpha
                    }
                }
            }
        },
        "size": k
    }

    response = es.search(index=index_name, body=query)

    return [
        {
            "id": hit["_id"],
            "content": hit["_source"].get("content"),
            "score": hit["_score"]
        }
        for hit in response["hits"]["hits"]
    ]
```

---

## pgvector + BM25 Hybrid

Combining PostgreSQL pgvector with full-text search for hybrid search.

```python
import psycopg2
from psycopg2.extras import execute_values
import numpy as np

def setup_hybrid_table(conn):
    """Create table with vector and full-text search support."""

    with conn.cursor() as cur:
        # Enable extensions
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

        # Create table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                title TEXT,
                embedding vector(1536),
                content_tsv tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
                    setweight(to_tsvector('english', coalesce(content, '')), 'B')
                ) STORED,
                metadata JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        # Create indexes
        cur.execute("""
            CREATE INDEX IF NOT EXISTS documents_embedding_idx
            ON documents USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS documents_tsv_idx
            ON documents USING GIN (content_tsv);
        """)

        conn.commit()


def pgvector_hybrid_search(
    conn,
    query_text: str,
    query_vector: list[float],
    alpha: float = 0.5,
    limit: int = 10
) -> list[dict]:
    """
    PostgreSQL hybrid search combining vector similarity and full-text search.
    Uses RRF-style fusion.
    """

    query = """
    WITH vector_results AS (
        SELECT
            id,
            content,
            title,
            metadata,
            1 - (embedding <=> %s::vector) as vector_score,
            ROW_NUMBER() OVER (ORDER BY embedding <=> %s::vector) as vector_rank
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    ),
    text_results AS (
        SELECT
            id,
            content,
            title,
            metadata,
            ts_rank_cd(content_tsv, plainto_tsquery('english', %s)) as text_score,
            ROW_NUMBER() OVER (
                ORDER BY ts_rank_cd(content_tsv, plainto_tsquery('english', %s)) DESC
            ) as text_rank
        FROM documents
        WHERE content_tsv @@ plainto_tsquery('english', %s)
        ORDER BY text_score DESC
        LIMIT %s
    ),
    combined AS (
        SELECT
            COALESCE(v.id, t.id) as id,
            COALESCE(v.content, t.content) as content,
            COALESCE(v.title, t.title) as title,
            COALESCE(v.metadata, t.metadata) as metadata,
            COALESCE(v.vector_score, 0) as vector_score,
            COALESCE(t.text_score, 0) as text_score,
            COALESCE(v.vector_rank, 1000) as vector_rank,
            COALESCE(t.text_rank, 1000) as text_rank,
            -- RRF fusion
            (1.0 / (60 + COALESCE(v.vector_rank, 1000))) +
            (1.0 / (60 + COALESCE(t.text_rank, 1000))) as rrf_score
        FROM vector_results v
        FULL OUTER JOIN text_results t ON v.id = t.id
    )
    SELECT
        id, content, title, metadata,
        vector_score, text_score, rrf_score
    FROM combined
    ORDER BY rrf_score DESC
    LIMIT %s;
    """

    with conn.cursor() as cur:
        # Vector needs to be passed 3 times for the query
        cur.execute(query, (
            query_vector, query_vector, query_vector, limit * 2,  # vector search
            query_text, query_text, query_text, limit * 2,  # text search
            limit  # final limit
        ))

        results = cur.fetchall()

    return [
        {
            "id": row[0],
            "content": row[1],
            "title": row[2],
            "metadata": row[3],
            "vector_score": row[4],
            "text_score": row[5],
            "rrf_score": row[6]
        }
        for row in results
    ]


def pgvector_hybrid_linear(
    conn,
    query_text: str,
    query_vector: list[float],
    alpha: float = 0.5,
    limit: int = 10
) -> list[dict]:
    """
    PostgreSQL hybrid search with linear combination.
    Requires score normalization.
    """

    query = """
    WITH vector_results AS (
        SELECT
            id, content, title, metadata,
            1 - (embedding <=> %s::vector) as raw_vector_score
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    ),
    vector_normalized AS (
        SELECT
            *,
            (raw_vector_score - MIN(raw_vector_score) OVER ()) /
            NULLIF(MAX(raw_vector_score) OVER () - MIN(raw_vector_score) OVER (), 0) as vector_score
        FROM vector_results
    ),
    text_results AS (
        SELECT
            id,
            ts_rank_cd(content_tsv, plainto_tsquery('english', %s)) as raw_text_score
        FROM documents
        WHERE content_tsv @@ plainto_tsquery('english', %s)
        ORDER BY raw_text_score DESC
        LIMIT %s
    ),
    text_normalized AS (
        SELECT
            id,
            (raw_text_score - MIN(raw_text_score) OVER ()) /
            NULLIF(MAX(raw_text_score) OVER () - MIN(raw_text_score) OVER (), 0) as text_score
        FROM text_results
    ),
    combined AS (
        SELECT
            v.id, v.content, v.title, v.metadata,
            COALESCE(v.vector_score, 0) as vector_score,
            COALESCE(t.text_score, 0) as text_score,
            %s * COALESCE(v.vector_score, 0) + (1 - %s) * COALESCE(t.text_score, 0) as hybrid_score
        FROM vector_normalized v
        LEFT JOIN text_normalized t ON v.id = t.id
    )
    SELECT * FROM combined
    ORDER BY hybrid_score DESC
    LIMIT %s;
    """

    with conn.cursor() as cur:
        cur.execute(query, (
            query_vector, query_vector, limit * 2,
            query_text, query_text, limit * 2,
            alpha, alpha,
            limit
        ))

        return [
            {
                "id": row[0],
                "content": row[1],
                "title": row[2],
                "metadata": row[3],
                "vector_score": row[4],
                "text_score": row[5],
                "hybrid_score": row[6]
            }
            for row in cur.fetchall()
        ]
```

---

## MongoDB Atlas Hybrid Search

MongoDB Atlas 8.0+ supports vector search combined with text search.

```python
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

client = MongoClient("mongodb+srv://...")
db = client["rag_database"]
collection = db["documents"]

def create_mongodb_hybrid_indexes():
    """Create vector and text search indexes."""

    # Vector search index
    vector_index = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1536,
                    "similarity": "cosine"
                },
                {
                    "type": "filter",
                    "path": "source"
                }
            ]
        },
        name="vector_index",
        type="vectorSearch"
    )

    # Text search index
    text_index = SearchIndexModel(
        definition={
            "mappings": {
                "dynamic": False,
                "fields": {
                    "content": {
                        "type": "string",
                        "analyzer": "lucene.standard"
                    },
                    "title": {
                        "type": "string",
                        "analyzer": "lucene.standard",
                        "multi": {
                            "keyword": {
                                "type": "string",
                                "analyzer": "lucene.keyword"
                            }
                        }
                    }
                }
            }
        },
        name="text_index",
        type="search"
    )

    collection.create_search_indexes([vector_index, text_index])


def mongodb_hybrid_search(
    query_text: str,
    query_vector: list[float],
    limit: int = 10,
    filters: dict | None = None
) -> list[dict]:
    """
    MongoDB Atlas hybrid search with RRF fusion.
    """

    # Build filter stage
    filter_stage = {}
    if filters:
        filter_stage = {"$match": filters}

    pipeline = [
        # Vector search
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": limit * 10,
                "limit": limit * 2
            }
        },
        {
            "$group": {
                "_id": None,
                "vector_docs": {
                    "$push": {
                        "doc": "$$ROOT",
                        "vector_score": {"$meta": "vectorSearchScore"}
                    }
                }
            }
        },
        # Add text search results
        {
            "$lookup": {
                "from": "documents",
                "pipeline": [
                    {
                        "$search": {
                            "index": "text_index",
                            "text": {
                                "query": query_text,
                                "path": ["content", "title"]
                            }
                        }
                    },
                    {"$limit": limit * 2},
                    {
                        "$project": {
                            "doc": "$$ROOT",
                            "text_score": {"$meta": "searchScore"}
                        }
                    }
                ],
                "as": "text_docs"
            }
        },
        # RRF fusion
        {
            "$project": {
                "all_docs": {
                    "$concatArrays": [
                        {
                            "$map": {
                                "input": {"$range": [0, {"$size": "$vector_docs"}]},
                                "as": "idx",
                                "in": {
                                    "doc": {"$arrayElemAt": ["$vector_docs.doc", "$$idx"]},
                                    "rrf_score": {"$divide": [1, {"$add": [60, {"$add": ["$$idx", 1]}]}]}
                                }
                            }
                        },
                        {
                            "$map": {
                                "input": {"$range": [0, {"$size": "$text_docs"}]},
                                "as": "idx",
                                "in": {
                                    "doc": {"$arrayElemAt": ["$text_docs.doc", "$$idx"]},
                                    "rrf_score": {"$divide": [1, {"$add": [60, {"$add": ["$$idx", 1]}]}]}
                                }
                            }
                        }
                    ]
                }
            }
        },
        {"$unwind": "$all_docs"},
        {
            "$group": {
                "_id": "$all_docs.doc._id",
                "doc": {"$first": "$all_docs.doc"},
                "total_rrf": {"$sum": "$all_docs.rrf_score"}
            }
        },
        {"$sort": {"total_rrf": -1}},
        {"$limit": limit}
    ]

    results = list(collection.aggregate(pipeline))

    return [
        {
            "id": str(r["_id"]),
            "content": r["doc"].get("content"),
            "title": r["doc"].get("title"),
            "score": r["total_rrf"]
        }
        for r in results
    ]
```

---

## Fusion Method Examples

### Reciprocal Rank Fusion (RRF)

```python
from collections import defaultdict
from typing import TypedDict

class SearchResult(TypedDict):
    id: str
    content: str
    score: float

def reciprocal_rank_fusion(
    *rankings: list[SearchResult],
    k: int = 60
) -> list[SearchResult]:
    """
    Combine multiple rankings using RRF.

    Args:
        *rankings: Variable number of ranked result lists
        k: Smoothing constant (default 60)

    Returns:
        Fused ranking sorted by RRF score
    """
    rrf_scores: dict[str, float] = defaultdict(float)
    doc_map: dict[str, SearchResult] = {}

    for ranking in rankings:
        for rank, result in enumerate(ranking):
            doc_id = result["id"]
            rrf_scores[doc_id] += 1.0 / (k + rank + 1)
            doc_map[doc_id] = result

    # Sort by RRF score
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

    return [
        {**doc_map[doc_id], "score": rrf_scores[doc_id]}
        for doc_id in sorted_ids
    ]


# Example usage
vector_results = [{"id": "1", "content": "...", "score": 0.95}, ...]
bm25_results = [{"id": "2", "content": "...", "score": 12.3}, ...]

fused = reciprocal_rank_fusion(vector_results, bm25_results, k=60)
```

### Weighted Linear Combination

```python
import numpy as np

def normalize_scores(scores: list[float], method: str = "minmax") -> list[float]:
    """Normalize scores to [0, 1] range."""
    if not scores:
        return scores

    scores_array = np.array(scores)

    if method == "minmax":
        min_s, max_s = scores_array.min(), scores_array.max()
        if max_s - min_s == 0:
            return [0.5] * len(scores)
        return ((scores_array - min_s) / (max_s - min_s)).tolist()

    elif method == "zscore":
        mean_s, std_s = scores_array.mean(), scores_array.std()
        if std_s == 0:
            return [0.5] * len(scores)
        # Convert z-scores to [0, 1] using sigmoid
        z_scores = (scores_array - mean_s) / std_s
        return (1 / (1 + np.exp(-z_scores))).tolist()

    else:
        raise ValueError(f"Unknown normalization method: {method}")


def linear_fusion(
    vector_results: list[SearchResult],
    keyword_results: list[SearchResult],
    alpha: float = 0.5,
    normalize: str = "minmax"
) -> list[SearchResult]:
    """
    Combine rankings using weighted linear combination.

    Args:
        vector_results: Results from vector search
        keyword_results: Results from keyword search
        alpha: Weight for vector scores (1-alpha for keyword)
        normalize: Normalization method ("minmax" or "zscore")

    Returns:
        Combined ranking sorted by hybrid score
    """
    # Build score dictionaries
    vector_scores = {r["id"]: r["score"] for r in vector_results}
    keyword_scores = {r["id"]: r["score"] for r in keyword_results}

    all_ids = set(vector_scores.keys()) | set(keyword_scores.keys())

    # Normalize scores
    if vector_scores:
        v_norm = normalize_scores(list(vector_scores.values()), normalize)
        vector_norm = dict(zip(vector_scores.keys(), v_norm))
    else:
        vector_norm = {}

    if keyword_scores:
        k_norm = normalize_scores(list(keyword_scores.values()), normalize)
        keyword_norm = dict(zip(keyword_scores.keys(), k_norm))
    else:
        keyword_norm = {}

    # Combine scores
    combined_scores = {}
    for doc_id in all_ids:
        v_score = vector_norm.get(doc_id, 0)
        k_score = keyword_norm.get(doc_id, 0)
        combined_scores[doc_id] = alpha * v_score + (1 - alpha) * k_score

    # Build result list
    doc_map = {r["id"]: r for r in vector_results + keyword_results}
    sorted_ids = sorted(combined_scores.keys(), key=lambda x: combined_scores[x], reverse=True)

    return [
        {**doc_map[doc_id], "score": combined_scores[doc_id]}
        for doc_id in sorted_ids
    ]
```

### Convex Combination (Distribution-Based)

```python
def convex_combination_fusion(
    vector_results: list[SearchResult],
    keyword_results: list[SearchResult],
    alpha: float = 0.5
) -> list[SearchResult]:
    """
    Convex combination treating scores as probability distributions.
    Assumes scores are already normalized to [0, 1].
    """
    # Softmax normalization for each ranking
    def softmax(scores):
        exp_scores = np.exp(np.array(scores) - np.max(scores))
        return exp_scores / exp_scores.sum()

    # Get all document IDs
    all_ids = list(set(r["id"] for r in vector_results + keyword_results))

    # Build score arrays
    vector_score_map = {r["id"]: r["score"] for r in vector_results}
    keyword_score_map = {r["id"]: r["score"] for r in keyword_results}

    vector_scores = [vector_score_map.get(doc_id, 0) for doc_id in all_ids]
    keyword_scores = [keyword_score_map.get(doc_id, 0) for doc_id in all_ids]

    # Apply softmax
    vector_probs = softmax(vector_scores)
    keyword_probs = softmax(keyword_scores)

    # Convex combination
    combined_probs = alpha * vector_probs + (1 - alpha) * keyword_probs

    # Build results
    doc_map = {r["id"]: r for r in vector_results + keyword_results}
    sorted_indices = np.argsort(combined_probs)[::-1]

    return [
        {**doc_map.get(all_ids[i], {"id": all_ids[i], "content": ""}), "score": float(combined_probs[i])}
        for i in sorted_indices
    ]
```

---

## LangChain Integration

### EnsembleRetriever

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def create_langchain_hybrid_retriever(
    documents: list,
    k: int = 10,
    weights: list[float] | None = None
):
    """
    Create LangChain EnsembleRetriever for hybrid search.
    """
    # Initialize BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = k

    # Initialize vector retriever
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(documents, embeddings)
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    # Combine with ensemble
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=weights or [0.5, 0.5]  # Equal weight by default
    )

    return ensemble_retriever


# Usage in RAG chain
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def create_hybrid_rag_chain(documents: list):
    retriever = create_langchain_hybrid_retriever(documents)
    llm = ChatOpenAI(model="gpt-4o-mini")

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return chain
```

### Custom Hybrid Retriever with Reranking

```python
from langchain.schema import BaseRetriever, Document
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from typing import List
import cohere

class HybridRetrieverWithReranking(BaseRetriever):
    """Custom hybrid retriever with Cohere reranking."""

    bm25_retriever: BM25Retriever
    vector_retriever: any  # VectorStoreRetriever
    cohere_client: cohere.Client
    k: int = 10
    rerank_top_n: int = 100

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # Get results from both retrievers
        bm25_docs = self.bm25_retriever.get_relevant_documents(query)
        vector_docs = self.vector_retriever.get_relevant_documents(query)

        # Deduplicate and combine
        seen_contents = set()
        combined_docs = []

        for doc in bm25_docs + vector_docs:
            content_hash = hash(doc.page_content)
            if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                combined_docs.append(doc)

        # Limit to rerank_top_n
        combined_docs = combined_docs[:self.rerank_top_n]

        if not combined_docs:
            return []

        # Rerank with Cohere
        rerank_response = self.cohere_client.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=[doc.page_content for doc in combined_docs],
            top_n=self.k
        )

        # Return reranked documents
        return [combined_docs[r.index] for r in rerank_response.results]
```

---

## LlamaIndex Integration

### Hybrid Search with QueryFusion

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.node_parser import SentenceSplitter

def create_llamaindex_hybrid_retriever(
    documents_path: str,
    similarity_top_k: int = 10,
    mode: str = "reciprocal_rerank"  # or "simple", "relative_score"
):
    """
    Create LlamaIndex hybrid retriever with query fusion.
    """
    # Load and parse documents
    documents = SimpleDirectoryReader(documents_path).load_data()
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(documents)

    # Create vector index
    vector_index = VectorStoreIndex(nodes)
    vector_retriever = vector_index.as_retriever(similarity_top_k=similarity_top_k)

    # Create BM25 retriever
    bm25_retriever = BM25Retriever.from_defaults(
        nodes=nodes,
        similarity_top_k=similarity_top_k
    )

    # Create fusion retriever
    hybrid_retriever = QueryFusionRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        similarity_top_k=similarity_top_k,
        num_queries=1,  # 1 = no query generation, just fusion
        mode=mode,
        use_async=True
    )

    return hybrid_retriever


# Usage
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI

def create_llamaindex_hybrid_rag(documents_path: str):
    retriever = create_llamaindex_hybrid_retriever(documents_path)
    llm = OpenAI(model="gpt-4o-mini")

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm
    )

    return query_engine
```

---

## Performance Optimization Examples

### Async Parallel Search

```python
import asyncio
from typing import Callable, Awaitable

async def parallel_hybrid_search(
    query: str,
    query_vector: list[float],
    bm25_search: Callable[[str], Awaitable[list]],
    vector_search: Callable[[list], Awaitable[list]],
    fusion_fn: Callable[[list, list], list]
) -> list:
    """
    Execute BM25 and vector search in parallel.
    """
    # Run searches concurrently
    bm25_task = asyncio.create_task(bm25_search(query))
    vector_task = asyncio.create_task(vector_search(query_vector))

    bm25_results, vector_results = await asyncio.gather(bm25_task, vector_task)

    # Fuse results (synchronous, fast)
    return fusion_fn(bm25_results, vector_results)


# Example async implementations
async def async_bm25_search(es_client, index: str, query: str, k: int = 50):
    """Async Elasticsearch BM25 search."""
    response = await es_client.search(
        index=index,
        body={"query": {"match": {"content": query}}, "size": k}
    )
    return [
        {"id": hit["_id"], "content": hit["_source"]["content"], "score": hit["_score"]}
        for hit in response["hits"]["hits"]
    ]


async def async_vector_search(qdrant_client, collection: str, vector: list, k: int = 50):
    """Async Qdrant vector search."""
    results = await qdrant_client.search(
        collection_name=collection,
        query_vector=vector,
        limit=k
    )
    return [
        {"id": str(r.id), "content": r.payload["content"], "score": r.score}
        for r in results
    ]
```

### Caching Layer

```python
from functools import lru_cache
import hashlib
import json
import redis
from typing import Optional

class HybridSearchCache:
    """Redis-based caching for hybrid search results."""

    def __init__(self, redis_client: redis.Redis, ttl: int = 900):  # 15 min TTL
        self.redis = redis_client
        self.ttl = ttl

    def _cache_key(self, query: str, alpha: float, k: int, filters: Optional[dict]) -> str:
        """Generate cache key from search parameters."""
        key_data = {
            "query": query,
            "alpha": alpha,
            "k": k,
            "filters": filters or {}
        }
        key_hash = hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
        return f"hybrid_search:{key_hash}"

    def get(self, query: str, alpha: float, k: int, filters: Optional[dict] = None) -> Optional[list]:
        """Get cached results."""
        key = self._cache_key(query, alpha, k, filters)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def set(self, query: str, alpha: float, k: int, results: list, filters: Optional[dict] = None):
        """Cache search results."""
        key = self._cache_key(query, alpha, k, filters)
        self.redis.setex(key, self.ttl, json.dumps(results))

    def invalidate_pattern(self, pattern: str = "hybrid_search:*"):
        """Invalidate cached searches matching pattern."""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)


# Usage with search function
class CachedHybridSearch:
    def __init__(self, search_fn, cache: HybridSearchCache):
        self.search_fn = search_fn
        self.cache = cache

    def search(self, query: str, alpha: float = 0.5, k: int = 10, filters: dict | None = None):
        # Check cache
        cached = self.cache.get(query, alpha, k, filters)
        if cached:
            return cached

        # Execute search
        results = self.search_fn(query, alpha, k, filters)

        # Cache results
        self.cache.set(query, alpha, k, results, filters)

        return results
```

### Batch Embedding with Rate Limiting

```python
import asyncio
from typing import List
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

class BatchEmbedder:
    """Efficient batch embedding with rate limiting."""

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        batch_size: int = 100,
        requests_per_minute: int = 3000
    ):
        self.client = openai.AsyncOpenAI()
        self.model = model
        self.batch_size = batch_size
        self.semaphore = asyncio.Semaphore(requests_per_minute // 60)  # Per second

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a single batch with retry."""
        async with self.semaphore:
            response = await self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [e.embedding for e in response.data]

    async def embed_all(self, texts: List[str]) -> List[List[float]]:
        """Embed all texts in batches."""
        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            embeddings = await self._embed_batch(batch)
            all_embeddings.extend(embeddings)

        return all_embeddings


# Usage
async def index_documents(documents: list[dict], embedder: BatchEmbedder):
    texts = [doc["content"] for doc in documents]
    embeddings = await embedder.embed_all(texts)

    # Now index documents with embeddings
    for doc, embedding in zip(documents, embeddings):
        doc["embedding"] = embedding

    return documents
```

### Quantization for Memory Efficiency

```python
import numpy as np

def quantize_vectors(vectors: np.ndarray, bits: int = 8) -> tuple[np.ndarray, dict]:
    """
    Scalar quantization of vectors to reduce memory.

    Args:
        vectors: Original float32 vectors (N x D)
        bits: Number of bits for quantization (8 or 16)

    Returns:
        Quantized vectors and calibration parameters
    """
    # Compute per-dimension min/max
    v_min = vectors.min(axis=0)
    v_max = vectors.max(axis=0)

    # Avoid division by zero
    v_range = v_max - v_min
    v_range[v_range == 0] = 1

    # Normalize to [0, 1]
    normalized = (vectors - v_min) / v_range

    # Quantize
    if bits == 8:
        quantized = (normalized * 255).astype(np.uint8)
    elif bits == 16:
        quantized = (normalized * 65535).astype(np.uint16)
    else:
        raise ValueError(f"Unsupported bits: {bits}")

    calibration = {
        "v_min": v_min.tolist(),
        "v_range": v_range.tolist(),
        "bits": bits
    }

    return quantized, calibration


def dequantize_vectors(quantized: np.ndarray, calibration: dict) -> np.ndarray:
    """Restore quantized vectors to float32."""
    v_min = np.array(calibration["v_min"])
    v_range = np.array(calibration["v_range"])
    bits = calibration["bits"]

    if bits == 8:
        normalized = quantized.astype(np.float32) / 255
    elif bits == 16:
        normalized = quantized.astype(np.float32) / 65535

    return normalized * v_range + v_min


# Memory comparison
def memory_comparison():
    n_vectors = 1_000_000
    dims = 1536

    # Original: float32
    original_bytes = n_vectors * dims * 4  # 6.14 GB

    # Quantized: uint8
    quantized_bytes = n_vectors * dims * 1  # 1.54 GB

    print(f"Original: {original_bytes / 1e9:.2f} GB")
    print(f"Quantized (8-bit): {quantized_bytes / 1e9:.2f} GB")
    print(f"Reduction: {(1 - quantized_bytes / original_bytes) * 100:.1f}%")
```

---

## References

- [Weaviate Hybrid Search Docs](https://weaviate.io/developers/weaviate/search/hybrid)
- [Qdrant Hybrid Search](https://qdrant.tech/articles/hybrid-search/)
- [Pinecone Sparse-Dense Vectors](https://docs.pinecone.io/docs/hybrid-search)
- [Elasticsearch RRF](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html)
- [LangChain EnsembleRetriever](https://python.langchain.com/docs/modules/data_connection/retrievers/ensemble)
- [LlamaIndex QueryFusion](https://docs.llamaindex.ai/en/stable/examples/retrievers/query_fusion_retriever/)
