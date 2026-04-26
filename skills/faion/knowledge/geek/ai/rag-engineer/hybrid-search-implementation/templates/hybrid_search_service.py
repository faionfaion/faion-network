"""
HybridSearchService — backend-agnostic BM25 + dense hybrid search with RRF and linear fusion.

Usage:
    svc = HybridSearchService(documents, embedding_service)
    results = svc.search("query text", top_k=10, alpha=0.6)
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import logging
import numpy as np


class FusionMethod(Enum):
    RRF = "rrf"
    LINEAR = "linear"


@dataclass
class HybridSearchConfig:
    alpha: float = 0.5
    fusion_method: FusionMethod = FusionMethod.RRF
    bm25_k1: float = 1.5
    bm25_b: float = 0.75
    rrf_k: int = 60
    enable_auto_alpha: bool = False


class HybridSearchService:
    def __init__(
        self,
        documents: List[Dict[str, Any]],
        embedding_service,
        config: Optional[HybridSearchConfig] = None,
    ) -> None:
        self.documents = documents
        self.embedding_service = embedding_service
        self.config = config or HybridSearchConfig()
        self.logger = logging.getLogger(__name__)
        self._build_indices()

    def _build_indices(self) -> None:
        from rank_bm25 import BM25Okapi
        tokenized = [d["content"].lower().split() for d in self.documents]
        self.bm25 = BM25Okapi(tokenized, k1=self.config.bm25_k1, b=self.config.bm25_b)
        texts = [d["content"] for d in self.documents]
        self.embeddings = self.embedding_service.embed_batch(texts)

    def search(
        self,
        query: str,
        top_k: int = 10,
        alpha: Optional[float] = None,
        filters: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        if alpha is None:
            alpha = self._auto_alpha(query) if self.config.enable_auto_alpha else self.config.alpha

        vec_ranking = self._vector_search(query, top_k * 2)
        kw_ranking = self._keyword_search(query, top_k * 2)

        if self.config.fusion_method == FusionMethod.RRF:
            fused = self._rrf(vec_ranking, kw_ranking)
        else:
            fused = self._linear(vec_ranking, kw_ranking, alpha)

        if filters:
            fused = [r for r in fused if all(r["document"].get("metadata", {}).get(k) == v
                                              for k, v in filters.items())]
        return fused[:top_k]

    def _vector_search(self, query: str, top_k: int) -> List[Tuple[int, float]]:
        qemb = self.embedding_service.embed(query)
        sims = np.dot(self.embeddings, qemb)
        idx = np.argsort(sims)[::-1][:top_k]
        return [(int(i), float(sims[i])) for i in idx]

    def _keyword_search(self, query: str, top_k: int) -> List[Tuple[int, float]]:
        scores = self.bm25.get_scores(query.lower().split())
        idx = np.argsort(scores)[::-1][:top_k]
        return [(int(i), float(scores[i])) for i in idx]

    def _rrf(self, vec: List[Tuple[int, float]], kw: List[Tuple[int, float]]) -> List[Dict]:
        scores: dict = defaultdict(float)
        k = self.config.rrf_k
        for rank, (idx, _) in enumerate(vec):
            scores[idx] += 1.0 / (k + rank + 1)
        for rank, (idx, _) in enumerate(kw):
            scores[idx] += 1.0 / (k + rank + 1)
        return [{"document": self.documents[i], "score": s, "fusion": "rrf"}
                for i, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

    def _linear(self, vec: List[Tuple[int, float]], kw: List[Tuple[int, float]], alpha: float) -> List[Dict]:
        vd, kd = dict(vec), dict(kw)
        combined = {i: alpha * vd.get(i, 0) + (1 - alpha) * kd.get(i, 0)
                    for i in set(vd) | set(kd)}
        return [{"document": self.documents[i], "score": s, "fusion": "linear", "alpha": alpha}
                for i, s in sorted(combined.items(), key=lambda x: x[1], reverse=True)]

    def _auto_alpha(self, query: str) -> float:
        if '"' in query:
            return 0.3
        if any(c.isdigit() for c in query):
            return 0.4
        if len(query.split()) <= 3:
            return 0.5
        return 0.7
