# purpose: top-N → reranker → top-K skeleton with provider abstraction + fallback
# consumes: query, first-stage candidates from vector / hybrid retrieval
# produces: code (drop-in module for second-stage rerank in RAG pipeline)
# depends-on: cohere OR sentence-transformers OR flashrank; optional BGE local for fallback
# token-budget-impact: ~200 tokens if loaded into LLM context for editing
"""Two-stage rerank: retrieve top-N first-stage candidates, rerank to top-K."""
from __future__ import annotations

import os
from typing import Callable

import cohere


class RerankProviderError(RuntimeError):
    pass


def cohere_rerank(query: str, candidates: list[dict], top_k: int, model: str) -> list[dict]:
    client = cohere.Client(api_key=os.environ["COHERE_API_KEY"])
    docs = [c["content"] for c in candidates]
    response = client.rerank(
        model=model,
        query=query,
        documents=docs,
        top_n=top_k,
    )
    return [
        {**candidates[r.index], "rerank_score": r.relevance_score}
        for r in response.results
    ]


def bge_local_rerank(query: str, candidates: list[dict], top_k: int, model: str) -> list[dict]:
    from sentence_transformers import CrossEncoder
    ce = CrossEncoder(model)
    pairs = [(query, c["content"]) for c in candidates]
    scores = ce.predict(pairs)
    ranked = sorted(
        ({"score": s, **c} for s, c in zip(scores, candidates)),
        key=lambda x: -x["score"],
    )[:top_k]
    return ranked


def rerank_with_fallback(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    primary: Callable = cohere_rerank,
    primary_kwargs: dict | None = None,
    fallback: Callable = bge_local_rerank,
    fallback_kwargs: dict | None = None,
) -> tuple[list[dict], bool]:
    """Return (top-k reranked, degraded_flag)."""
    primary_kwargs = primary_kwargs or {"model": "rerank-multilingual-v3.0"}
    fallback_kwargs = fallback_kwargs or {"model": "BAAI/bge-reranker-base"}
    try:
        return primary(query, candidates, top_k, **primary_kwargs), False
    except Exception:  # noqa: BLE001
        return fallback(query, candidates, top_k, **fallback_kwargs), True
