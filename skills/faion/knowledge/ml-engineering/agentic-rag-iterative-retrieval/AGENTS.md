# Agentic RAG — Iterative Retrieval

## Summary

**One-sentence:** Produces an iterative-retrieval RAG agent class — LLM judge decides sufficiency, refines query, retries up to a hard cap; drift detection + dedup + per-step model routing.

**One-paragraph:** Single-pass RAG fails on multi-hop questions where the answer lives across disjoint chunks. This methodology produces an `IterativeRetriever` class that runs retrieve → judge sufficiency → refine query → retrieve loop up to `max_iterations` (default 3, hard cap 5). Sufficiency judge runs on cheap model (Haiku/Sonnet); final answer synthesis on Opus. Drift detection: cosine sim between original and refined query embeddings <0.7 → reset to original. Dedup by chunk_id between iterations.

**Ефективно для:**

- Multi-hop QA — answer require combining ≥2 disjoint docs.
- Research synthesis tasks: explore → evaluate → refine → conclude.
- Latency budget 3–10s per query and cost budget 3–5x baseline RAG.
- Adversarial-corpus-aware deployments — judge model must differ from generator.
- Bounded budget — hard iteration cap is non-negotiable.

## Applies If (ALL must hold)

- Multi-hop / synthesis questions where single-pass RAG fails &gt;20% of evals.
- Latency SLA ≥3s allowed.
- Cost budget supports 3–5x single-pass RAG.
- Sufficiency judge model available distinct from generator.

## Skip If (ANY kills it)

- Single-turn factual lookup — standard RAG suffices.
- &lt;2s latency SLA.
- Untrusted/adversarial corpora без sanitisation pipeline.
- Cost budget cannot absorb 3–5x.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Query embedder | model name + dim | platform |
| Retriever (BM25 / dense / hybrid) | runner | service repo |
| Judge model client | provider client | platform |
| Generator model client | provider client | platform |
| Chunk-id dedup helper | python | service repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-generation]]` | Same-model indexing/query rule applies. |
| `[[rag-bench-harness-template]]` | Bench harness consumes the agent. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for iterative-retriever-config | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with detector + repair | ~700 |
| `content/04-procedure.xml` | essential | 5-step: wire retriever → wire judge → loop + dedup → drift gate → generator | ~700 |
| `content/06-decision-tree.xml` | essential | Routes question class to iterative vs single-pass | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sufficiency-judge` | haiku | Yes/no judgement; cheap. |
| `query-refinement` | sonnet | Light judgment. |
| `final-answer-synthesis` | opus | Multi-chunk reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/iterative_retriever.py` | IterativeRetriever class with budget + dedup + drift gate. |
| `templates/iterative-retriever-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-iterative-retrieval.py` | Validate iterative-retriever-config | Pre-commit + CI |

## Related

- [[agentic-rag-query-decomposition]]
- [[agentic-rag-self-correction]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to iterative retrieval only for multi-hop / synthesis questions with latency tolerance ≥3s. Walk it before wiring; using iterative for single-hop wastes 3–5x latency.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/iterative_retriever.py`

```python
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
```

### `templates/iterative-retriever-config.json`

```json
{
  "max_iterations": 3,
  "judge_model": "haiku",
  "generator_model": "opus",
  "dedup_by_chunk_id": true,
  "drift_threshold": 0.7,
  "sanitise_chunks": true
}
```
