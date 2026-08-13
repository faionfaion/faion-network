# AI Video Generation Async API Patterns

## Summary

**One-sentence:** Standardised submit + poll + fetch pattern for video generation APIs (60-300s latency) with exponential backoff, idempotency keys, provider-fallback, and bounded retry on transient failures.

**One-paragraph:** Every AI video provider is async: submit returns a job_id; client polls until ready (60-300s); fetch returns URL with TTL (24h-7d). Naive polling burns API quota; tight retry on transient 5xx makes things worse. The pattern: submit with idempotency-key (so retries don't double-bill); poll with exponential backoff (1s, 2s, 4s, 8s, 16s, capped at 30s); cap total wait at 10min; on timeout flip to fallback provider; download artefact to durable storage immediately (URLs expire). Output: a typed `VideoJob` client + provider-config block.

**Ефективно для:**

- Media pipelines (TikTok / YT / podcast) — стабільний async pattern замість ad-hoc polling що ламається кожен релізом.
- Multi-provider strategy — той самий клас VideoJob працює з Runway / Luma / Veo / Sora через адаптери.
- Cost-sensitive workloads — idempotency ключ уникає double-billing при retry.
- Long-running batches — backoff polling не зливає quota poll-spam-ом.

## Applies If (ALL must hold)

- Provider has async generation API (Runway Gen-3, Luma Dream Machine, Google Veo, OpenAI Sora)
- Pipeline can wait minutes (not interactive UI)
- Need to fetch artefact and store before URL expires
- Acceptable to retry / fall back across providers

## Skip If (ANY kills it)

- Provider has synchronous API (no need for polling)
- Interactive UI requires &lt;5s — async won't fit
- Single provider with no alternative — fallback irrelevant

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `provider-keys.yaml` | YAML (secret-manager refs) | infra |
| `storage-bucket.yaml` | YAML | S3/GCS bucket for artefacts |
| `cost-budget.yaml` | YAML | monthly cap |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `video-generation-production-service` | Service wrapper |
| `video-generation-prompt-engineering` | Prompts that drive submit() |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: idempotency-key, exp backoff polling, total-wait cap, download-before-expiry, provider fallback | 1100 |
| `content/02-output-contract.xml` | essential | `VideoJob` shape + provider-config schema | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: poll-tight, no idempotency, no fallback, miss artefact TTL, no cost cap | 900 |
| `content/04-procedure.xml` | essential | 5 steps: submit → poll backoff → fetch artefact → download to bucket → audit | 700 |
| `content/05-examples.xml` | essential | Worked example: Runway Gen-3 submit + poll + S3 download | 500 |
| `content/06-decision-tree.xml` | essential | Routes a job lifecycle event by status | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `submit_request_drafting` | sonnet | Prompt composition |
| `poll_loop` | n/a | Pure logic |
| `video_job_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/video-async-client.py` | Generic async-client with submit + poll + fetch |
| `templates/video-job.schema.yaml` | Schema |
| `templates/_smoke-test.yaml` | Minimum-viable VideoJob fixture |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-generation-async-api.py` | Lint VideoJob OR provider-config | Pre-commit |

## Related

- [[video-generation-production-service]] · [[video-generation-prompt-engineering]]
- external: [Runway API](https://docs.dev.runwayml.com/) · [Luma API](https://docs.lumalabs.ai/) · [Google Veo](https://cloud.google.com/vertex-ai/generative-ai/docs/video-generation/overview)

## Decision tree

See `content/06-decision-tree.xml`. Routes job lifecycle status → action: in-progress / succeeded / failed-transient / failed-permanent / timeout → fallback.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/video-async-client.py`

```python
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
```

### `templates/video-job.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [provider, idempotency_key, poll_backoff_seconds, total_wait_cap_seconds, artefact_storage, fallback]
properties:
  provider: {type: string, enum: [runway, luma, veo, sora, kling]}
  idempotency_key: {type: string, minLength: 16}
  poll_backoff_seconds:
    type: array
    minItems: 3
    items: {type: number, minimum: 1}
  total_wait_cap_seconds: {type: integer, minimum: 60, maximum: 900}
  artefact_storage:
    type: object
    required: [bucket, key_prefix]
  fallback:
    type: object
    required: [provider, trigger]
    properties:
      provider: {type: string}
      trigger: {type: string}
```

### `templates/_smoke-test.yaml`

```yaml
provider: runway
idempotency_key: "8f2a000000000000"
poll_backoff_seconds: [1, 2, 4, 8, 16, 30]
total_wait_cap_seconds: 600
artefact_storage: {bucket: prod-media, key_prefix: video/2026/}
fallback: {provider: luma, trigger: timeout-or-permanent-fail}
```
