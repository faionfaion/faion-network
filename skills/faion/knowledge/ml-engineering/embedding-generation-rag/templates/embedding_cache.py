# purpose: EmbeddingCache — file-based cache keyed by SHA-256(model + text).
# consumes: cache_dir path + (text, model_name) pairs
# produces: cached embedding vectors persisted to disk
# depends-on: content/01-core-rules.xml r3 (SHA-256 keys mandatory)
# token-budget-impact: 0 LLM tokens; disk I/O only
"""EmbeddingCache — file-based fallback when Redis/Valkey unavailable."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional


class EmbeddingCache:
    def __init__(self, cache_dir: str = ".embedding_cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, text: str, model: str) -> str:
        # SHA-256 to avoid MD5 collisions at billion-document scale
        return hashlib.sha256(f"{model}:{text}".encode()).hexdigest()

    def get(self, text: str, model: str) -> Optional[list]:
        path = self.cache_dir / f"{self._key(text, model)}.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None

    def set(self, text: str, model: str, embedding: list) -> None:
        path = self.cache_dir / f"{self._key(text, model)}.json"
        with open(path, "w") as f:
            json.dump(embedding, f)

    def get_or_create(self, text: str, model: str, embed_fn) -> list:
        cached = self.get(text, model)
        if cached is not None:
            return cached
        vec = embed_fn(text)
        result = vec.tolist() if hasattr(vec, "tolist") else list(vec)
        self.set(text, model, result)
        return result
