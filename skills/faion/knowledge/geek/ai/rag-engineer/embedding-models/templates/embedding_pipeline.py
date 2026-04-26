"""
EmbeddingPipeline — full pipeline: chunk → cache-check → batch embed.

Usage:
    config = EmbeddingConfig(model="text-embedding-3-large", chunk_size=500)
    pipeline = EmbeddingPipeline(config)
    embeddings = pipeline.process_document(long_text)  # list[list[float]]
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import hashlib
import json
from pathlib import Path
from openai import OpenAI


@dataclass
class EmbeddingConfig:
    model: str = "text-embedding-3-large"
    dimensions: Optional[int] = None
    chunk_size: int = 500
    chunk_overlap: int = 50
    batch_size: int = 100
    cache_enabled: bool = True
    cache_dir: str = ".embedding_cache"


class EmbeddingPipeline:
    def __init__(self, config: EmbeddingConfig) -> None:
        self.config = config
        self.client = OpenAI()
        self.cache_dir = Path(config.cache_dir) if config.cache_enabled else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def process_document(self, text: str) -> list[list[float]]:
        """Chunk text → check cache → batch embed remaining → return all embeddings."""
        chunks = self._chunk(text)
        cached: dict[int, list[float]] = {}
        uncached: list[tuple[int, str]] = []

        for i, chunk in enumerate(chunks):
            hit = self._cache_get(chunk) if self.cache_dir else None
            if hit is not None:
                cached[i] = hit
            else:
                uncached.append((i, chunk))

        if uncached:
            indices, texts = zip(*uncached)
            new_embs = self._embed_batch(list(texts))
            for idx, emb in zip(indices, new_embs):
                cached[idx] = emb
                if self.cache_dir:
                    self._cache_set(chunks[idx], emb)

        return [cached[i] for i in range(len(chunks))]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _chunk(self, text: str) -> list[str]:
        chunks, start = [], 0
        while start < len(text):
            end = start + self.config.chunk_size
            chunks.append(text[start:end].strip())
            start = end - self.config.chunk_overlap
        return [c for c in chunks if c]

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        all_embs: list[list[float]] = []
        cfg = self.config
        for i in range(0, len(texts), cfg.batch_size):
            batch = texts[i : i + cfg.batch_size]
            kw: dict = {"input": batch, "model": cfg.model}
            if cfg.dimensions:
                kw["dimensions"] = cfg.dimensions
            r = self.client.embeddings.create(**kw)
            sorted_data = sorted(r.data, key=lambda x: x.index)
            all_embs.extend([e.embedding for e in sorted_data])
        return all_embs

    def _key(self, text: str) -> str:
        return hashlib.sha256(f"{self.config.model}:{text}".encode()).hexdigest()

    def _cache_get(self, text: str) -> Optional[list[float]]:
        path = self.cache_dir / f"{self._key(text)}.json"  # type: ignore[operator]
        if path.exists():
            return json.loads(path.read_text())
        return None

    def _cache_set(self, text: str, emb: list[float]) -> None:
        path = self.cache_dir / f"{self._key(text)}.json"  # type: ignore[operator]
        path.write_text(json.dumps(emb))
