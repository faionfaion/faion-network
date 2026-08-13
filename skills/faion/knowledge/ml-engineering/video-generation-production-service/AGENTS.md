# AI Video Generation Production Service

## Summary

**One-sentence:** Wraps the async-api primitive into a deployable FastAPI service with priority queue, multi-provider abstraction, ffmpeg post-processing (concat / overlay / encode), cost guardrail, and per-tenant rate limit.

**One-paragraph:** A production service requires more than a client. Callers submit jobs over HTTP/gRPC; queue persists across restarts (Redis/SQS); workers pick by priority and provider weight; each worker speaks to the async-api client per `video-generation-async-api`; ffmpeg post-processes outputs (concat clips, add overlays, transcode); cost-cap rejects submit when over monthly budget; per-tenant quotas prevent noisy-neighbour. Output: a deployable service + `service-config.yaml` + Docker image.

**Ефективно для:**

- Media-pipeline продуктів (TikTok / YT / Reels) — submit endpoint + priority queue відокремлює producer (UI / scheduler) від consumer (workers).
- Multi-tenant SaaS — per-tenant квоти і cost-cap ловлять зловживання.
- Hybrid clip pipelines — ffmpeg концатенація / overlay після генерації окремих 5s shotів у один 30s ролик.
- Cost-bounded workloads — explicit cost cap rejects submits, не пост-факт.

## Applies If (ALL must hold)

- Need durable submit/poll endpoints (not just a one-off script)
- Multi-provider strategy desired
- Post-processing (concat, encode, overlay) needed
- Per-tenant quotas / cost cap required

## Skip If (ANY kills it)

- One-off batch script — async-api client alone suffices
- Single provider, no quotas — over-engineered
- No ffmpeg available — adapt the post-processing pipeline first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `service-config.yaml` | YAML | provider keys + storage + queue |
| `tenant-quotas.yaml` | YAML | per-tenant monthly cap |
| `ffmpeg available on workers` | env | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `video-generation-async-api` | Underlying primitive |
| `video-generation-prompt-engineering` | Prompts the service accepts |
| `tool-use-function-calling` | If exposed as a tool to upstream agent |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: persistent queue, per-tenant quota, ffmpeg post-process declared, cost cap pre-submit, idempotent-by-design | 1100 |
| `content/02-output-contract.xml` | essential | `service-config.yaml` schema | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: in-memory queue, no quota, ffmpeg-on-call, missing cost-cap, no idempotency | 900 |
| `content/04-procedure.xml` | essential | 6 steps: queue → workers → ffmpeg → quota → cost cap → ship | 900 |
| `content/05-examples.xml` | essential | Worked example: 30s reel pipeline = 6×5s Runway clips + ffmpeg concat | 600 |
| `content/06-decision-tree.xml` | essential | Routes by priority + provider weight to worker | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `service_config_drafting` | sonnet | Schema synthesis |
| `runbook_drafting` | sonnet | Trade-offs |
| `service_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/fastapi-service.py` | Submit + poll endpoints |
| `templates/worker.py` | Queue consumer with provider abstraction |
| `templates/ffmpeg-concat.sh` | Post-process concat script |
| `templates/service-config.schema.yaml` | Schema |
| `templates/_smoke-test.yaml` | Minimum-viable service-config |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-generation-production-service.py` | Lint service-config.yaml | Pre-commit |

## Related

- [[video-generation-async-api]] — underlying primitive
- [[video-generation-prompt-engineering]] — prompts the service accepts
- external: [FastAPI](https://fastapi.tiangolo.com/) · [Runway API](https://docs.dev.runwayml.com/) · [ffmpeg](https://ffmpeg.org/)

## Decision tree

See `content/06-decision-tree.xml`. Routes submit by tenant quota + cost cap + priority + provider weight to a worker.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/fastapi-service.py`

```python
"""FastAPI video-gen service: submit + poll with idempotency + quotas + cost cap."""
from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="video-gen-service")


class SubmitRequest(BaseModel):
    prompt: str
    duration_seconds: int = 5
    provider_preference: str | None = None
    post_processing: list[str] = []


class SubmitResponse(BaseModel):
    job_id: str
    deduped: bool = False


def projected_breach(tenant_id: str, this_job_cost_usd: float) -> bool:
    # placeholder: compare service.this_month + this_job vs cap × 0.95
    return False


def quota_breach(tenant_id: str, this_job_cost_usd: float) -> bool:
    return False


@app.post("/v1/jobs", response_model=SubmitResponse)
def submit(req: SubmitRequest, idempotency_key: str | None = Header(default=None),
           x_tenant_id: str = Header(default="anonymous")):
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header required (r5)")
    # 1. dedup
    existing = redis_lookup(idempotency_key)
    if existing:
        return SubmitResponse(job_id=existing, deduped=True)
    # 2. cost cap
    cost_estimate = estimate_cost(req)
    if projected_breach(x_tenant_id, cost_estimate):
        raise HTTPException(status_code=402, detail="global cost cap exceeded (r4)")
    if quota_breach(x_tenant_id, cost_estimate):
        raise HTTPException(status_code=429, detail="tenant quota exceeded (r2)")
    # 3. enqueue
    job_id = enqueue(req, x_tenant_id, idempotency_key)
    redis_set(idempotency_key, job_id, ex=86400)  # 24h
    return SubmitResponse(job_id=job_id, deduped=False)


@app.get("/v1/jobs/{job_id}")
def poll(job_id: str):
    return job_lookup(job_id)


# placeholders for clarity
def redis_lookup(k): return None
def redis_set(k, v, ex=None): pass
def estimate_cost(req) -> float: return 0.50
def enqueue(req, t, k) -> str: return "job_abc"
def job_lookup(jid): return {"job_id": jid, "status": "running"}
```

### `templates/worker.py`

```python
"""Worker consumer for video gen jobs."""
from __future__ import annotations

import subprocess
import sys


def process_one(job: dict) -> dict:
    # 1. submit via async-api client
    video_job = submit_async(job["prompt"], job["params"], provider=job["provider"],
                             idempotency_key=job["idempotency_key"])
    # 2. poll
    while True:
        status = poll(video_job.job_id)
        if status in ("succeeded", "failed-permanent", "timeout"):
            break
    # 3. on success, post-process
    if status == "succeeded":
        local = download(video_job.artefact_url)
        for op in job["post_processing"]:
            local = apply_ffmpeg_op(op, local)
        s3_url = upload(local)
        return {"status": "succeeded", "artefact_url": s3_url}
    return {"status": status}


def apply_ffmpeg_op(op: str, in_path: str) -> str:
    out_path = in_path.replace(".mp4", f"_{op}.mp4")
    if op == "concat":
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-i", "list.txt", "-c", "copy", out_path], check=True)
    elif op == "overlay-watermark":
        subprocess.run(["ffmpeg", "-y", "-i", in_path, "-i", "watermark.png", "-filter_complex", "overlay=10:10", out_path], check=True)
    elif op == "transcode-h264-720p":
        subprocess.run(["ffmpeg", "-y", "-i", in_path, "-vf", "scale=-1:720", "-c:v", "libx264", out_path], check=True)
    return out_path


def submit_async(prompt, params, provider, idempotency_key): ...
def poll(jid): ...
def download(url): ...
def upload(path): ...


if __name__ == "__main__":
    sys.exit(0)
```

### `templates/ffmpeg-concat.sh`

```bash
set -euo pipefail

OUT="${1:-out.mp4}"
CLIPS_DIR="${2:-clips}"

# build concat list
> list.txt
for f in "$CLIPS_DIR"/*.mp4; do
  echo "file '$PWD/$f'" >> list.txt
done

# concat
ffmpeg -y -f concat -safe 0 -i list.txt -c copy "$OUT"

# optional watermark
if [ -f watermark.png ]; then
  ffmpeg -y -i "$OUT" -i watermark.png -filter_complex "overlay=W-w-10:H-h-10" -codec:a copy "${OUT%.mp4}_wm.mp4"
fi
```

### `templates/service-config.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [queue, workers, providers, ffmpeg, tenant_quotas, cost_cap, idempotency]
properties:
  queue:
    type: object
    required: [kind, connection]
    properties:
      kind: {type: string, enum: [redis-streams, sqs, rabbitmq]}
  workers:
    type: object
    required: [count, concurrency]
  providers:
    type: array
    minItems: 2
    items:
      type: object
      required: [name, weight]
  ffmpeg:
    type: object
    required: [enabled, operations]
  tenant_quotas:
    type: object
    required: [default_monthly_jobs, default_monthly_usd]
    properties:
      default_monthly_jobs: {type: integer, minimum: 1}
      default_monthly_usd: {type: number, minimum: 0.01}
  cost_cap:
    type: object
    required: [global_monthly_usd, reject_at_pct]
    properties:
      global_monthly_usd: {type: number, minimum: 0}
      reject_at_pct: {type: integer, minimum: 50, maximum: 100}
  idempotency:
    type: object
    required: [window_hours]
    properties:
      window_hours: {type: integer, minimum: 1}
```

### `templates/_smoke-test.yaml`

```yaml
queue: {kind: redis-streams, connection: redis://x:6379}
workers: {count: 8, concurrency: 5}
providers:
  - {name: runway, weight: 0.6}
  - {name: luma, weight: 0.4}
ffmpeg: {enabled: true, operations: [concat, transcode-h264-720p]}
tenant_quotas: {default_monthly_jobs: 100, default_monthly_usd: 50}
cost_cap: {global_monthly_usd: 2500, reject_at_pct: 95}
idempotency: {window_hours: 24}
```
