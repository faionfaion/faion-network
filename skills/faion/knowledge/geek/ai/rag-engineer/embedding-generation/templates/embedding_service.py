# purpose: EmbeddingService — batched, cached, normalized, guarded embed pipeline.
# consumes: embedder-config.json + provider client + tokenizer + cache backend (optional)
# produces: list[list[float]] unit-normalized vectors + per-text audit (skipped/cached/embedded)
# depends-on: content/01-core-rules.xml r1, r2, r3, r4, r5, r6
# token-budget-impact: provider embedding API only; 0 LLM tokens for the wiring
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Any, Callable

PROVIDER_CAPS = {"openai": 2048, "cohere": 96, "voyage": 128, "google": 250, "azure": 2048, "local": 1024}


@dataclass
class EmbedderConfig:
    model_name: str
    model_version: str
    provider: str
    batch_size: int = 256
    normalize: bool = True
    cache_hash_algo: str = "sha256"
    max_input_tokens: int = 8191
    input_type_index: str = "n/a"
    input_type_query: str = "n/a"


def _normalize(v: list[float]) -> list[float] | None:
    n = math.sqrt(sum(x * x for x in v))
    if n < 1e-9:
        return None
    return [x / n for x in v]


@dataclass
class EmbeddingService:
    config: EmbedderConfig
    embed_provider: Callable[[list[str], dict[str, Any]], list[list[float]]]
    tokenize: Callable[[str], list[str]]
    cache_get: Callable[[str], list[float] | None] | None = None
    cache_set: Callable[[str, list[float]], None] | None = None

    def __post_init__(self) -> None:
        if self.config.batch_size > PROVIDER_CAPS.get(self.config.provider, 2048):
            raise ValueError("batch_size > provider cap (rule r2)")
        if self.config.cache_hash_algo != "sha256":
            raise ValueError("cache_hash_algo must be sha256 (rule r3)")
        if self.config.provider == "cohere":
            if not self.config.input_type_index or not self.config.input_type_query:
                raise ValueError("Cohere requires input_type_index + input_type_query (rule r6)")

    def _key(self, text: str) -> str:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return f"{self.config.model_name}:{self.config.model_version}:{h}"

    def _safe(self, text: str) -> bool:
        if not text or not text.strip():
            return False
        if len(self.tokenize(text)) > self.config.max_input_tokens:
            return False
        return True

    def embed_batch(self, texts: list[str], *, is_query: bool = False) -> dict[str, Any]:
        valid: list[tuple[int, str]] = [(i, t) for i, t in enumerate(texts) if self._safe(t)]
        cached: dict[int, list[float]] = {}
        misses: list[tuple[int, str]] = []
        for i, t in valid:
            if self.cache_get is not None:
                v = self.cache_get(self._key(t))
                if v is not None:
                    cached[i] = v
                    continue
            misses.append((i, t))
        cap = PROVIDER_CAPS.get(self.config.provider, 2048)
        new_vectors: dict[int, list[float]] = {}
        for start in range(0, len(misses), min(self.config.batch_size, cap)):
            chunk = misses[start : start + min(self.config.batch_size, cap)]
            kwargs: dict[str, Any] = {}
            if self.config.provider == "cohere":
                kwargs["input_type"] = self.config.input_type_query if is_query else self.config.input_type_index
            vectors = self.embed_provider([t for _, t in chunk], kwargs)
            for (i, t), v in zip(chunk, vectors, strict=True):
                if self.config.normalize:
                    nv = _normalize(v)
                    if nv is None:
                        continue
                    v = nv
                new_vectors[i] = v
                if self.cache_set is not None:
                    self.cache_set(self._key(t), v)
        result: list[list[float] | None] = [None] * len(texts)
        for i, v in cached.items():
            result[i] = v
        for i, v in new_vectors.items():
            result[i] = v
        return {"vectors": result, "cache_hits": len(cached), "embedded": len(new_vectors), "skipped": len(texts) - len(valid)}
