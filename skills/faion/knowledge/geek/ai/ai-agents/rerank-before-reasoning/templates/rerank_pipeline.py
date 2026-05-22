# purpose: retrieve-then-rerank pipeline emitted by rerank-before-reasoning methodology
# consumes: query string + vector store handle + reranker client
# produces: top-k_final candidates after cross-encoder rerank
# depends-on: r1-rerank-required, r3-reranker-model-shipped, r5-fallback-on-rerank-timeout
# token-budget-impact: ~250 tokens
"""Two-stage retrieve-then-rerank pipeline.

Input  → query string, vector store, reranker client.
Output → top-N (chunk, score) tuples ready to feed the reasoner.

Defaults:
    - Recall window     K=75
    - Final cut         N=8
    - Score threshold   0.30 (tune on your eval set)

The candidate window K and threshold are knobs — sweep both on a labelled
suite before shipping. See content/01-two-stage-pipeline.xml.
"""

from dataclasses import dataclass


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict


@dataclass
class Scored:
    chunk: Chunk
    score: float


class RerankPipeline:
    def __init__(
        self,
        vector_store,
        reranker,
        recall_k: int = 75,
        final_n: int = 8,
        threshold: float = 0.30,
    ) -> None:
        self.store = vector_store
        self.reranker = reranker
        self.recall_k = recall_k
        self.final_n = final_n
        self.threshold = threshold

    def retrieve(self, query: str) -> list[Scored]:
        candidates: list[Chunk] = self.store.search(query, top_k=self.recall_k)
        if not candidates:
            return []
        scores = self.reranker.rank(query, [c.text for c in candidates])
        scored = [Scored(c, s) for c, s in zip(candidates, scores)]
        scored.sort(key=lambda x: x.score, reverse=True)
        return [s for s in scored if s.score >= self.threshold][: self.final_n]
