# purpose: async batched embedding producer with content-hash cache + retry
# consumes: list[str] chunks, producer-config JSON
# produces: list[list[float]] vectors (L2-normalized when config.normalize=true)
# depends-on: openai>=1.30 (or voyageai>=0.2), redis>=5 OR sqlitedict>=2
# token-budget-impact: per-input ~chunk_tokens; cache hit avoids the call entirely
from __future__ import annotations

import asyncio
import hashlib
import math
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Config:
    model_id: str
    dimension: int
    normalize: bool
    batch_size: int = 1024
    concurrency: int = 4
    max_attempts: int = 5


def _cache_key(text: str, cfg: Config) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{h}:{cfg.model_id}:{cfg.dimension}"


def _l2_normalize(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


async def _call_provider(batch: Sequence[str], cfg: Config) -> list[list[float]]:
    # Replace with provider SDK call. Stub returns zero-vectors for shape only.
    return [[0.0] * cfg.dimension for _ in batch]


async def _retry(coro_fn, cfg: Config):
    import random
    for attempt in range(cfg.max_attempts):
        try:
            return await coro_fn()
        except Exception:
            if attempt == cfg.max_attempts - 1:
                raise
            wait = min(2 ** attempt + random.uniform(0, 1), 60)
            await asyncio.sleep(wait)


async def embed(chunks: Iterable[str], cfg: Config, cache=None) -> list[list[float]]:
    chunks_list = list(chunks)
    out: list[list[float] | None] = [None] * len(chunks_list)
    missing_idx: list[int] = []
    if cache is not None:
        for i, c in enumerate(chunks_list):
            v = cache.get(_cache_key(c, cfg))
            if v is not None:
                out[i] = v
            else:
                missing_idx.append(i)
    else:
        missing_idx = list(range(len(chunks_list)))

    sem = asyncio.Semaphore(cfg.concurrency)
    batches = [missing_idx[i:i + cfg.batch_size] for i in range(0, len(missing_idx), cfg.batch_size)]

    async def run_batch(idxs: list[int]) -> None:
        texts = [chunks_list[i] for i in idxs]
        async with sem:
            vecs = await _retry(lambda: _call_provider(texts, cfg), cfg)
        for i, v in zip(idxs, vecs):
            if cfg.normalize:
                v = _l2_normalize(v)
            assert len(v) == cfg.dimension, "dimension mismatch"
            out[i] = v
            if cache is not None:
                cache.set(_cache_key(chunks_list[i], cfg), v)

    await asyncio.gather(*(run_batch(b) for b in batches))
    assert all(v is not None for v in out), "missing vectors"
    return out  # type: ignore[return-value]
