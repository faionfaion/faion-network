# purpose: EmbeddingCache — SHA-256 keyed cache layer in front of embedding provider.
# consumes: cache-config.json + cache backend client + embed callable + metric emitter
# produces: cached embedding vectors + per-call hit/miss metric
# depends-on: content/01-core-rules.xml r1, r2, r3, r4
# token-budget-impact: cache hits = 0 provider calls; misses = 1 provider call
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class CacheConfig:
    backend: str = "valkey"
    hash_algo: str = "sha256"
    key_components: tuple[str, ...] = ("model_name", "model_version", "text")
    ttl_days: int = 90
    emit_hit_metric: bool = True


@dataclass
class EmbeddingCache:
    config: CacheConfig
    backend_get: Callable[[str], list[float] | None]
    backend_set: Callable[[str, list[float], int], None]
    embed: Callable[[str], list[float]]
    emit_metric: Callable[[str, dict[str, Any]], None]
    model_name: str
    model_version: str

    def __post_init__(self) -> None:
        if self.config.hash_algo != "sha256":
            raise ValueError("hash_algo must be sha256 (rule r1)")
        if "model_version" not in self.config.key_components:
            raise ValueError("key_components must include model_version (rule r2)")
        if self.config.ttl_days < 1 or self.config.ttl_days > 365:
            raise ValueError("ttl_days must be in [1,365] (rule r3)")
        if not self.config.emit_hit_metric:
            raise ValueError("emit_hit_metric must be true (rule r4)")

    def _key(self, text: str) -> str:
        parts = []
        if "model_name" in self.config.key_components:
            parts.append(self.model_name)
        if "model_version" in self.config.key_components:
            parts.append(self.model_version)
        if "text" in self.config.key_components:
            parts.append(hashlib.sha256(text.encode("utf-8")).hexdigest())
        return ":".join(parts)

    def get_or_embed(self, text: str) -> list[float]:
        key = self._key(text)
        cached = self.backend_get(key)
        if cached is not None:
            self.emit_metric("embedding_cache.hit", {"model": self.model_name})
            return cached
        self.emit_metric("embedding_cache.miss", {"model": self.model_name})
        v = self.embed(text)
        ttl_seconds = self.config.ttl_days * 86400
        self.backend_set(key, v, ttl_seconds)
        return v
