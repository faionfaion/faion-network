# purpose: async parallel embedding batcher with content-hash dedup + cache + order preservation
# consumes: list[str] inputs, batch+cache config dict
# produces: list[list[float]] vectors in input order
# depends-on: openai>=1.30 (stub here), redis>=5 OR sqlitedict>=2 (optional)
# token-budget-impact: pays once per UNIQUE (text, model, dim) tuple; cache + dedup cut bills 60-95%
from __future__ import annotations

import asyncio
import hashlib
import random
from typing import Any, Sequence


def _cache_key(text: str, model_id: str, dim: int) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{h}:{model_id}:{dim}"


async def _call_provider(batch: Sequence[str], cfg: dict) -> list[list[float]]:
    # Replace with provider SDK; stub returns zero-vectors of the right dim.
    return [[0.0] * cfg["dimension"] for _ in batch]


async def _retry(fn, max_attempts: int):
    for attempt in range(max_attempts):
        try:
            return await fn()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            await asyncio.sleep(min(2 ** attempt + random.uniform(0, 1), 60))


async def embed(inputs: list[str], cfg: dict, cache: Any = None) -> list[list[float]]:
    n = len(inputs)
    out: list[list[float] | None] = [None] * n
    # 1. Dedup by cache key, remember positions
    uniq_keys: dict[str, int] = {}
    uniq_texts: list[str] = []
    positions: dict[str, list[int]] = {}
    for i, t in enumerate(inputs):
        k = _cache_key(t, cfg["model_id"], cfg["dimension"])
        positions.setdefault(k, []).append(i)
        if k not in uniq_keys:
            uniq_keys[k] = len(uniq_texts)
            uniq_texts.append(t)
    # 2. Cache lookup
    need_call: list[tuple[int, str]] = []  # (uniq_idx, text)
    cached: dict[int, list[float]] = {}
    if cache is not None:
        for u_idx, t in enumerate(uniq_texts):
            k = _cache_key(t, cfg["model_id"], cfg["dimension"])
            v = cache.get(k)
            if v is not None:
                cached[u_idx] = v
            else:
                need_call.append((u_idx, t))
    else:
        need_call = [(i, t) for i, t in enumerate(uniq_texts)]
    # 3. Batch parallel call on missing
    batch_size = cfg["batch"]["size"]
    sem = asyncio.Semaphore(cfg["batch"]["concurrency"])
    batches = [need_call[i:i + batch_size] for i in range(0, len(need_call), batch_size)]
    new_vecs: dict[int, list[float]] = {}

    async def run(batch: list[tuple[int, str]]) -> None:
        async with sem:
            vecs = await _retry(lambda: _call_provider([t for _, t in batch], cfg), cfg["retry"]["max_attempts"])
        for (u_idx, t), v in zip(batch, vecs):
            new_vecs[u_idx] = v
            if cache is not None:
                cache.set(_cache_key(t, cfg["model_id"], cfg["dimension"]), v)

    await asyncio.gather(*(run(b) for b in batches))
    # 4. Reassemble in input order
    for k, idxs in positions.items():
        u_idx = uniq_keys[k]
        v = cached.get(u_idx) or new_vecs[u_idx]
        for i in idxs:
            out[i] = v
    assert all(v is not None for v in out)
    return out  # type: ignore[return-value]
