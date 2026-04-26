"""
RerankerService — production reranking with cross-encoder/Cohere dispatch, fallback, and FastAPI endpoint.

Usage:
    svc = RerankerService(RerankerConfig(reranker_type=RerankerType.CROSS_ENCODER))
    results = svc.rerank(query="...", documents=[...], top_k=5)
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np


class RerankerType(Enum):
    CROSS_ENCODER = "cross_encoder"
    COHERE = "cohere"
    LLM = "llm"


@dataclass
class RerankerConfig:
    reranker_type: RerankerType = RerankerType.CROSS_ENCODER
    model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    batch_size: int = 32
    timeout: float = 30.0
    fallback_to_original: bool = True


class RerankerService:
    def __init__(self, config: Optional[RerankerConfig] = None) -> None:
        self.config = config or RerankerConfig()
        self.logger = logging.getLogger(__name__)
        self._init()

    def _init(self) -> None:
        if self.config.reranker_type == RerankerType.CROSS_ENCODER:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.config.model)
        elif self.config.reranker_type == RerankerType.COHERE:
            import cohere
            self._cohere = cohere.Client()

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        metadata: Optional[List[Dict]] = None,
    ) -> List[Dict[str, Any]]:
        start = time.time()
        try:
            if self.config.reranker_type == RerankerType.CROSS_ENCODER:
                results = self._cross_encoder(query, documents, top_k)
            elif self.config.reranker_type == RerankerType.COHERE:
                results = self._cohere_rerank(query, documents, top_k)
            else:
                results = self._llm_rerank(query, documents, top_k)
            if metadata:
                for r in results:
                    idx = r["index"]
                    if idx < len(metadata):
                        r["metadata"] = metadata[idx]
            self.logger.info(f"Reranking done in {time.time() - start:.3f}s")
            return results
        except Exception as e:
            self.logger.error(f"Reranking failed: {e}")
            if self.config.fallback_to_original:
                return [{"document": d, "score": 1.0 - i / len(documents), "index": i}
                        for i, d in enumerate(documents[:top_k])]
            raise

    def _cross_encoder(self, query: str, docs: List[str], top_k: int) -> List[Dict]:
        scores = self._model.predict([[query, d] for d in docs], batch_size=self.config.batch_size)
        idx = np.argsort(scores)[::-1][:top_k]
        return [{"document": docs[i], "score": float(scores[i]), "index": int(i)} for i in idx]

    def _cohere_rerank(self, query: str, docs: List[str], top_k: int) -> List[Dict]:
        r = self._cohere.rerank(query=query, documents=docs, top_n=top_k, model="rerank-english-v3.0")
        return [{"document": docs[res.index], "score": res.relevance_score, "index": res.index}
                for res in r.results]

    def _llm_rerank(self, query: str, docs: List[str], top_k: int) -> List[Dict]:
        import json
        from openai import OpenAI
        client = OpenAI()
        doc_list = "\n".join([f"[{i}] {d[:500]}" for i, d in enumerate(docs)])
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f'Score relevance 0-10.\nQuery: {query}\nDocs:\n{doc_list}\nJSON: {{"scores":[{{"index":0,"score":8}}]}}'}],
            response_format={"type": "json_object"}, temperature=0,
        )
        scores = sorted(json.loads(r.choices[0].message.content)["scores"], key=lambda x: x["score"], reverse=True)
        return [{"document": docs[s["index"]], "score": s["score"] / 10.0, "index": s["index"]}
                for s in scores[:top_k] if s["index"] < len(docs)]


# ------------------------------------------------------------------
# FastAPI endpoint (optional)
# ------------------------------------------------------------------

def create_fastapi_app(reranker: RerankerService):
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    app = FastAPI()

    class RerankRequest(BaseModel):
        query: str
        documents: List[str]
        top_k: int = 5

    @app.post("/rerank")
    async def rerank(req: RerankRequest):
        start = time.time()
        try:
            return {"results": reranker.rerank(req.query, req.documents, req.top_k),
                    "latency": time.time() - start}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app
