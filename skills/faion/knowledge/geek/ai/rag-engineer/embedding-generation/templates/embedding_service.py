"""
EmbeddingService — production-ready provider-dispatching embedding service.

Usage:
    config = EmbeddingConfig(provider="openai", model="text-embedding-3-small")
    svc = EmbeddingService(config)
    vec = svc.embed("hello world")
    vecs = svc.embed_batch(["hello", "world"])
    score = svc.similarity("cat", "feline")
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import logging
import numpy as np


@dataclass
class EmbeddingConfig:
    provider: str = "openai"          # openai | local | ollama | cohere
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None  # only for text-embedding-3 models
    batch_size: int = 100
    cache_enabled: bool = True


class EmbeddingService:
    def __init__(self, config: Optional[EmbeddingConfig] = None) -> None:
        self.config = config or EmbeddingConfig()
        self.logger = logging.getLogger(__name__)
        self.cache = None
        if self.config.cache_enabled:
            from .embedding_cache import EmbeddingCache  # type: ignore[import]
            self.cache = EmbeddingCache()
        self._init_model()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def embed(self, text: str) -> np.ndarray:
        """Return a 1-D numpy array for one text."""
        if self.cache:
            cached = self.cache.get(text, self.config.model)
            if cached is not None:
                return np.array(cached)
        vec = self._generate(text)
        if self.cache:
            self.cache.set(text, self.config.model, vec.tolist())
        return vec

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Return a 2-D numpy array (N, D) for multiple texts."""
        if self.config.provider == "openai":
            return self._embed_batch_openai(texts)
        if self.config.provider == "local":
            return self._model.encode(texts, batch_size=self.config.batch_size)  # type: ignore[union-attr]
        return np.array([self.embed(t) for t in texts])

    def similarity(self, text1: str, text2: str) -> float:
        e1, e2 = self.embed(text1), self.embed(text2)
        return float(np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2)))

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _init_model(self) -> None:
        if self.config.provider == "openai":
            from openai import OpenAI
            self._client = OpenAI()
        elif self.config.provider == "local":
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.config.model)
        elif self.config.provider == "ollama":
            import ollama as _ollama
            self._ollama = _ollama
        elif self.config.provider == "cohere":
            import cohere
            self._cohere = cohere.Client()

    def _generate(self, text: str) -> np.ndarray:
        if self.config.provider == "openai":
            kw: dict = {"input": text, "model": self.config.model}
            if self.config.dimensions:
                kw["dimensions"] = self.config.dimensions
            r = self._client.embeddings.create(**kw)
            return np.array(r.data[0].embedding)
        if self.config.provider == "local":
            return self._model.encode(text)  # type: ignore[union-attr]
        if self.config.provider == "ollama":
            r = self._ollama.embeddings(model=self.config.model, prompt=text)
            return np.array(r["embedding"])
        raise ValueError(f"Unknown provider: {self.config.provider}")

    def _embed_batch_openai(self, texts: list[str]) -> np.ndarray:
        all_embs: list = []
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i : i + self.config.batch_size]
            kw: dict = {"input": batch, "model": self.config.model}
            if self.config.dimensions:
                kw["dimensions"] = self.config.dimensions
            r = self._client.embeddings.create(**kw)
            sorted_data = sorted(r.data, key=lambda x: x.index)
            all_embs.extend([e.embedding for e in sorted_data])
        return np.array(all_embs)
