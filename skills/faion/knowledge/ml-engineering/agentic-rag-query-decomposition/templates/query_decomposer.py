# purpose: QueryDecomposer — planning + parallel sub-query retrieval + coverage tracking.
# consumes: decomposer-config.json + planner_client + retriever_async + embedder
# produces: merged context + zero-coverage audit log
# depends-on: content/01-core-rules.xml r1, r2, r3
# token-budget-impact: 1 planner call + N parallel retrieval calls; N capped at 4
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable


@dataclass
class DecomposerConfig:
    min_sub_queries: int = 2
    max_sub_queries: int = 4
    planner_model: str = "sonnet"
    parallel: bool = True
    confidence_threshold: float = 0.6
    coverage_required: bool = True


@dataclass
class QueryDecomposer:
    config: DecomposerConfig
    plan: Callable[[str], list[tuple[str, float]]]
    retrieve: Callable[[str], Awaitable[list[dict]]]

    def __post_init__(self) -> None:
        if self.config.max_sub_queries > 4:
            raise ValueError("max_sub_queries cap is 4 (rule r1)")
        if not self.config.parallel:
            raise ValueError("parallel must be true (rule r2)")

    def _cap(self, raw: list[tuple[str, float]]) -> list[str] | None:
        # rule r1: <2 → atomic fallback (None); >4 → keep top-4 by confidence
        if len(raw) < self.config.min_sub_queries:
            return None
        ranked = sorted(raw, key=lambda x: x[1], reverse=True)[: self.config.max_sub_queries]
        return [sq for sq, _ in ranked]

    async def run(self, query: str) -> dict[str, Any]:
        raw = self.plan(query)
        sub_queries = self._cap(raw)
        if sub_queries is None:
            # atomic fallback
            chunks = await self.retrieve(query)
            return {"mode": "atomic", "chunks": chunks, "coverage_gaps": []}
        # rule r2: parallel
        results = await asyncio.gather(*[self.retrieve(sq) for sq in sub_queries])
        # rule r3: coverage tracking
        gaps: list[str] = []
        merged: list[dict] = []
        seen_ids: set[str] = set()
        thr = self.config.confidence_threshold
        for sq, chunks in zip(sub_queries, results, strict=True):
            high = [c for c in chunks if (c.get("score") or 0.0) > thr]
            if not high:
                gaps.append(sq)
            for c in chunks:
                cid = c.get("chunk_id")
                if cid and cid in seen_ids:
                    continue
                if cid:
                    seen_ids.add(cid)
                merged.append(c)
        return {"mode": "decomposed", "sub_queries": sub_queries, "chunks": merged, "coverage_gaps": gaps}
