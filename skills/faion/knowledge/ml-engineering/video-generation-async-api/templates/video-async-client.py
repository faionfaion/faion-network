# purpose: generic async client for video gen providers — submit + poll + fetch + fallback
# consumes: prompt, params, provider config
# produces: code (drop-in module returning VideoJob with durable S3 artefact_url)
# depends-on: requests/httpx + boto3 + provider SDK
# token-budget-impact: ~250 tokens if loaded into LLM context
"""Generic async video generation client with idempotency + backoff + fallback."""
from __future__ import annotations

import hashlib
import json
import random
import time
from dataclasses import dataclass


def idem_key(prompt: str, params: dict, provider: str) -> str:
    blob = json.dumps({"prompt": prompt, "params": params, "provider": provider}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


@dataclass
class VideoJob:
    job_id: str
    provider: str
    status: str
    idempotency_key: str
    artefact_url: str | None = None
    cost_usd: float = 0.0
    elapsed_s: float = 0.0


def poll_with_backoff(check_fn, total_wait_cap: int = 600) -> tuple[str, float]:
    backoff = [1, 2, 4, 8, 16, 30]
    started = time.monotonic()
    i = 0
    while True:
        elapsed = time.monotonic() - started
        if elapsed >= total_wait_cap:
            return ("timeout", elapsed)
        status = check_fn()
        if status in ("succeeded", "failed-permanent", "failed-transient"):
            return (status, elapsed)
        sleep = min(backoff[min(i, len(backoff) - 1)], 30) + random.uniform(0, 0.5)
        time.sleep(sleep)
        i += 1


def submit_with_fallback(submit_fn, primary: str, fallback: str, prompt: str, params: dict, **kw):
    key = idem_key(prompt, params, primary)
    try:
        return submit_fn(provider=primary, idempotency_key=key, prompt=prompt, params=params, **kw)
    except Exception:  # noqa: BLE001
        return submit_fn(provider=fallback, idempotency_key=key, prompt=prompt, params=params, **kw)
