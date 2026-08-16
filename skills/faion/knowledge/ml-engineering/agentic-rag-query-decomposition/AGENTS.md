# Agentic RAG — Query Decomposition

## Summary

**One-sentence:** Decomposes complex queries into 2–4 atomic sub-queries, retrieves in parallel, tracks coverage; falls back to single-pass when decomposition collapses to 1 sub-query.

**One-paragraph:** Complex queries with multiple intents waste retrieval budget when run as a single embedding. This methodology produces a `QueryDecomposer` class: a planning LLM emits 2–4 atomic sub-queries; each is retrieved in parallel via asyncio.gather; results merged with coverage tracking. If decomposition returns &lt;2 sub-queries, the original is treated atomic. If &gt;4, only the top-4 by confidence kept. Coverage gaps surfaced for review.

**Ефективно для:**

- Complex compound queries з ≥2 distinct intents.
- Latency budget allows parallel sub-query fanout.
- Track coverage gaps (sub-query without high-confidence chunk).
- Sub-query cache within one agentic run.
- Bridge from `[[agentic-rag-iterative-retrieval]]` for compound questions.

## Applies If (ALL must hold)

- Question class includes multi-intent compound queries.
- Parallel retrieval supported by infra.
- Planning LLM available distinct from generator.
- Coverage-gap surfacing acceptable (vs silent drops).

## Skip If (ANY kills it)

- Single-intent atomic queries — decomposition adds no value.
- Sequential-only retriever (no parallel infra).
- Cost budget cannot absorb planning + N retrieval rounds.
- No coverage-gap consumer (gaps would be ignored).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Planning model client | provider client | platform |
| Retriever runner | python | service repo |
| Parallel executor (asyncio / pool) | runtime | platform |
| Confidence threshold | float | retrieval policy |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agentic-rag-iterative-retrieval]]` | Iterative loop methodology. |
| `[[embedding-generation]]` | Shared embedder. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for decomposer-config | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with detector + repair | ~700 |
| `content/04-procedure.xml` | essential | 5-step: plan → cap → parallel retrieve → coverage → merge | ~700 |
| `content/06-decision-tree.xml` | essential | Routes question class to decomposition vs atomic | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-sub-queries` | sonnet | Planning judgment. |
| `score-sub-query-confidence` | haiku | Numeric scoring. |
| `merge-context` | sonnet | Multi-result synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/query_decomposer.py` | QueryDecomposer class with parallel fanout + coverage. |
| `templates/decomposer-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-query-decomposition.py` | Validate decomposer-config | Pre-commit + CI |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[agentic-rag-iterative-retrieval]]
- [[agentic-rag-self-correction]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to decomposition when question class is compound + parallel retrieval available. Atomic queries fall back to single-pass.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/query_decomposer.py`

```python
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
```

### `templates/decomposer-config.json`

```json
{
  "min_sub_queries": 2,
  "max_sub_queries": 4,
  "planner_model": "sonnet",
  "parallel": true,
  "confidence_threshold": 0.6,
  "coverage_required": true
}
```
