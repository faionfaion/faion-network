# purpose: IterativeRetriever — multi-hop RAG agent with judge + refine loop + drift gate + dedup.
# consumes: iterative-retriever-config.json + judge_client + generator_client + retriever + embedder
# produces: answer string + audit trail of iterations
# depends-on: content/01-core-rules.xml r1, r2, r3, r4
# token-budget-impact: judge cost x max_iterations + 1 generator pass; bound by config.max_iterations
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable

_INJECTION_RE = re.compile(r"(ignore|override|disregard)\s+(previous|all)\s+(instructions|rules)", re.I)


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def _sanitise(text: str) -> str:
    return _INJECTION_RE.sub("[REDACTED-INJECTION]", text)


@dataclass
class IterativeRetrieverConfig:
    max_iterations: int = 3
    judge_model: str = "haiku"
    generator_model: str = "opus"
    drift_threshold: float = 0.7
    dedup_by_chunk_id: bool = True
    sanitise_chunks: bool = True


@dataclass
class IterativeRetriever:
    config: IterativeRetrieverConfig
    retriever: Callable[[str], list[dict]]
    embed: Callable[[str], list[float]]
    judge: Callable[[str, str, list[dict]], bool]
    refine: Callable[[str, list[dict]], str]
    generate: Callable[[str, list[dict]], str]

    def __post_init__(self) -> None:
        # rule r1: hard cap
        if self.config.max_iterations > 5:
            raise ValueError("max_iterations cap is 5 (rule r1)")
        # rule r2: judge != generator
        if self.config.judge_model == self.config.generator_model:
            raise ValueError("judge_model must differ from generator_model (rule r2)")

    def answer(self, original_query: str) -> dict[str, Any]:
        seen: set[str] = set()
        context: list[dict] = []
        current_query = original_query
        original_emb = self.embed(original_query)
        trace: list[dict] = []
        for i in range(self.config.max_iterations):
            chunks = self.retriever(current_query)
            # rule r3: dedup
            new_chunks = []
            for c in chunks:
                cid = c.get("chunk_id")
                if self.config.dedup_by_chunk_id and cid and cid in seen:
                    continue
                if cid:
                    seen.add(cid)
                if self.config.sanitise_chunks:
                    c = {**c, "text": _sanitise(c.get("text", ""))}
                new_chunks.append(c)
            context.extend(new_chunks)
            sufficient = self.judge(original_query, current_query, context)
            trace.append({"iter": i, "query": current_query, "added": len(new_chunks), "sufficient": sufficient})
            if sufficient:
                break
            if i == self.config.max_iterations - 1:
                # rule r1: cap reached without sufficient — escalate
                return {"answer": None, "needs_human_review": True, "trace": trace}
            refined = self.refine(current_query, context)
            # rule r4: drift gate
            refined_emb = self.embed(refined)
            if _cosine(original_emb, refined_emb) < self.config.drift_threshold:
                refined = original_query
                trace[-1]["drift_reset"] = True
            current_query = refined
        answer = self.generate(original_query, context)
        return {"answer": answer, "needs_human_review": False, "trace": trace}
