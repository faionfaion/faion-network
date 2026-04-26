"""Production RAG pipeline with Qdrant: ingest, hybrid search, metadata filter."""
import hashlib
import os
from typing import Optional

from anthropic import Anthropic
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
    PointStruct,
    VectorParams,
)

COLLECTION = "knowledge_base"
EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072
CHAT_MODEL = "claude-opus-4-5"

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
anthropic = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
qdrant = QdrantClient(url=os.environ.get("QDRANT_URL", "http://localhost:6333"))


def ensure_collection() -> None:
    if not qdrant.collection_exists(COLLECTION):
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


def embed(text: str) -> list[float]:
    response = openai.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding


def ingest(documents: list[dict], tenant_id: str) -> None:
    """Ingest documents with tenant isolation via payload filter."""
    ensure_collection()
    points = []
    for doc in documents:
        content = doc["content"]
        doc_id = hashlib.sha256(content.encode()).hexdigest()
        vector = embed(content)
        points.append(PointStruct(
            id=doc_id,
            vector=vector,
            payload={
                "content": content,
                "source": doc.get("source", ""),
                "tenant_id": tenant_id,
            },
        ))
    qdrant.upsert(collection_name=COLLECTION, points=points)


def search(query: str, tenant_id: str, top_k: int = 5) -> list[dict]:
    """Hybrid search with mandatory tenant filter."""
    vector = embed(query)
    results = qdrant.search(
        collection_name=COLLECTION,
        query_vector=vector,
        limit=top_k,
        query_filter=Filter(
            must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
        ),
        with_payload=True,
        score_threshold=0.6,
    )
    return [{"content": r.payload["content"], "source": r.payload["source"], "score": r.score}
            for r in results]


def answer(query: str, tenant_id: str) -> str:
    """Retrieve context and synthesize answer with source citations."""
    nodes = search(query, tenant_id)
    if not nodes:
        return "I don't have enough information to answer that question."

    context = "\n\n".join(
        f"[{i+1}] {n['content']} (source: {n['source']})"
        for i, n in enumerate(nodes)
    )
    response = anthropic.messages.create(
        model=CHAT_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}],
        system="Answer based only on the context provided. Cite sources as [N]. If the answer is not in the context, say so.",
    )
    return response.content[0].text
