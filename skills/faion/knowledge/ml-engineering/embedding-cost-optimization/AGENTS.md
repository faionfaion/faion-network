# Embedding Cost Optimization

## Summary

**One-sentence:** Five-lever cost optimization for embedding pipelines — Matryoshka dim reduction, batch API, aggressive cache, two-stage retrieval, dedup-on-ingest.

**One-paragraph:** Embedding cost compounds with corpus size. This methodology produces a `CostOptimizer` config + pipeline that pulls 5 levers in order: (1) dedup-on-ingest (drop exact + near-dup); (2) batch API (batch_size 256–1024); (3) embedding cache; (4) Matryoshka dim reduction (text-embedding-3-large at dim=512 vs 3072); (5) two-stage retrieval (cheap candidate + expensive rerank). Output is a versioned cost-opt-config artefact + cost-savings audit metric.

**Ефективно для:**

- Embedding budget &gt;$1k/month — every lever pulls 20–40%.
- Re-ingestion pipelines — dedup + cache compound.
- Multi-tenant systems with overlapping content.
- Storage cost optimization through Matryoshka.
- RAG retrieval с two-stage rerank.

## Applies If (ALL must hold)

- Monthly embedding cost ≥$500 OR projected to scale.
- Eval bench available to confirm no quality regression per lever.
- Cache backend available.
- Named owner.

## Skip If (ANY kills it)

- Cost &lt;$100/month (overhead exceeds savings).
- No bench set → cannot validate quality preservation.
- Single-shot ingestion already complete.
- All levers already pulled.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current cost report (per-provider) | YAML | finance/finops |
| Eval bench set | JSONL | eval repo |
| Cache backend client | client | platform |
| Provider rate-limit policy | YAML | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-caching]]` | Cache lever. |
| `[[embedding-applications]]` | Pipeline that consumes the config. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for cost-opt-config | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | essential | 5-step: audit cost → dedup → cache → dim-reduce → two-stage | ~700 |
| `content/06-decision-tree.xml` | essential | Routes cost level to lever priority | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-current-cost` | haiku | Numeric. |
| `pick-levers` | sonnet | Multi-axis judgment. |
| `validate-no-regression` | opus | Cross-metric synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost_optimizer.py` | CostOptimizer config + lever applicator. |
| `templates/cost-opt-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-cost-optimization.py` | Validate cost-opt-config | Pre-commit + CI |

## Related

- [[embedding-caching]]
- [[embedding-applications]]
- [[embedding-generation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes cost level to lever priority — high-cost pipelines pull all 5 levers; small pipelines start with just dedup + cache.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cost_optimizer.py`

```python
from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass
class CostOptConfig:
    dedup_on_ingest: bool = True
    batch_size: int = 512
    cache_enabled: bool = True
    matryoshka_dim: int = 512
    two_stage_retrieval: bool = True
    recall_tolerance_pp: float = 1.0


@dataclass
class CostOptimizer:
    config: CostOptConfig

    def __post_init__(self) -> None:
        if not self.config.dedup_on_ingest:
            raise ValueError("dedup_on_ingest must be true (rule r1)")
        if self.config.batch_size < 32 or self.config.batch_size > 2048:
            raise ValueError("batch_size out of [32,2048] (rule r2)")
        if self.config.matryoshka_dim < 256:
            raise ValueError("matryoshka_dim must be ≥256 (rule r4)")
        if self.config.recall_tolerance_pp > 5.0:
            raise ValueError("recall_tolerance_pp must be ≤5 (rule r4)")

    def dedup(self, docs: list[dict]) -> list[dict]:
        seen: set[str] = set()
        out: list[dict] = []
        for d in docs:
            h = hashlib.sha256(d["text"].encode("utf-8")).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            out.append({**d, "content_hash": h})
        return out

    def estimate_savings_pct(self, baseline_calls: int, new_calls: int) -> float:
        return 100.0 * (baseline_calls - new_calls) / max(1, baseline_calls)
```

### `templates/cost-opt-config.json`

```json
{
  "dedup_on_ingest": true,
  "batch_size": 512,
  "cache_enabled": true,
  "matryoshka_dim": 512,
  "two_stage_retrieval": true,
  "recall_tolerance_pp": 1.0
}
```
