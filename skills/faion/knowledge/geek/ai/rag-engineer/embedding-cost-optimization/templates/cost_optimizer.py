# purpose: CostOptimizer — apply 5 cost levers in order with bench gate per lever.
# consumes: cost-opt-config.json + corpus + bench client + embed client + cache
# produces: optimized pipeline config + cost-savings audit row
# depends-on: content/01-core-rules.xml r1, r2, r3, r4, r5
# token-budget-impact: 0 LLM tokens; provider API calls + cache ops only
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
