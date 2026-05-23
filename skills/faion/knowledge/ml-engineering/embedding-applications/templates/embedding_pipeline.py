# purpose: EmbeddingPipeline — multi-agent shortlist → bench → batched insert → quality gate.
# consumes: embedding-pipeline-config.json + provider clients + domain bench JSONL
# produces: deployed embedding pipeline OR blocked deploy with reasons
# depends-on: content/01-core-rules.xml r1, r2, r3, r4, r5, r6, r7
# token-budget-impact: 0 LLM tokens; provider embedding API calls only
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class EmbeddingPipelineConfig:
    model_name: str
    model_version: str
    provider: str
    batch_size: int = 256
    normalize: bool = True
    metric: str = "cosine"
    domain_bench_path: str = ""
    recall10_threshold: float = 0.7
    vector_metadata_fields: tuple[str, ...] = ("model_name", "model_version", "created_at")


def _normalize(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v))
    if n < 1e-9:
        raise ValueError("zero-length vector (rule r3)")
    return [x / n for x in v]


@dataclass
class EmbeddingPipeline:
    config: EmbeddingPipelineConfig
    embed_batch: Callable[[list[str]], list[list[float]]]
    db_upsert: Callable[[list[dict]], None]
    db_get_config: Callable[[], dict]
    bench_recall10: Callable[[str, EmbeddingPipelineConfig], float]

    def __post_init__(self) -> None:
        if self.config.batch_size < 32 or self.config.batch_size > 2048:
            raise ValueError("batch_size out of [32,2048] (rule r5)")
        if self.config.metric == "cosine" and not self.config.normalize:
            raise ValueError("cosine metric requires normalize=true (rule r3)")
        for fld in ("model_name", "model_version"):
            if fld not in self.config.vector_metadata_fields:
                raise ValueError(f"vector_metadata_fields missing {fld} (rule r7)")

    def ingest(self, docs: list[dict]) -> dict[str, Any]:
        # rule r6: schema check before upsert
        cfg = self.db_get_config()
        if cfg.get("metric") != self.config.metric:
            raise ValueError(f"DB metric {cfg.get('metric')} != config {self.config.metric} (rule r6)")
        inserted = 0
        for start in range(0, len(docs), self.config.batch_size):
            batch = docs[start : start + self.config.batch_size]
            vectors = self.embed_batch([d["text"] for d in batch])
            if self.config.normalize:
                vectors = [_normalize(v) for v in vectors]
            rows = [
                {
                    "id": d["id"],
                    "vector": v,
                    "metadata": {
                        "model_name": self.config.model_name,
                        "model_version": self.config.model_version,
                        "created_at": d.get("created_at"),
                    },
                }
                for d, v in zip(batch, vectors, strict=True)
            ]
            self.db_upsert(rows)
            inserted += len(rows)
        return {"inserted": inserted}

    def quality_gate(self) -> dict[str, Any]:
        # rule r4: gate on Recall@10
        recall = self.bench_recall10(self.config.domain_bench_path, self.config)
        ok = recall >= self.config.recall10_threshold
        return {"recall10": recall, "promoted": ok}
