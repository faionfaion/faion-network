"""
purpose: Reusable embed() + cosine() + top_k() for ingest and query paths.
consumes: list of texts (ingest) or single query (query); pinned (model, dimensions).
produces: list of float vectors (ingest) or ranked (score, text) pairs (query).
depends-on: openai>=1.0, numpy>=1.24.
token-budget-impact: cost = sum(len(text) tokens) × embedding price; pin model from config.
"""
import numpy as np
from typing import List, Tuple
from openai import OpenAI

client = OpenAI()


def embed(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dims: int = 1536,
) -> List[List[float]]:
    """Embed a list of texts. Use same model+dims as ingestion for queries."""
    resp = client.embeddings.create(model=model, input=texts, dimensions=dims)
    return [d.embedding for d in resp.data]


def cosine(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two embedding vectors."""
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb)))


def top_k(
    query_emb: List[float],
    corpus_embs: List[List[float]],
    corpus_texts: List[str],
    k: int = 5,
) -> List[Tuple[float, str]]:
    """Return top-k (score, text) pairs sorted by descending similarity."""
    scores = [
        (cosine(query_emb, e), t)
        for e, t in zip(corpus_embs, corpus_texts)
    ]
    return sorted(scores, key=lambda x: x[0], reverse=True)[:k]
