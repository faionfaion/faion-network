---
slug: video-generation-production-service
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "827f89b9d42fd8d7"
summary: Production video generation service — FastAPI submit/poll endpoints + priority queue + multi-provider abstraction with retry/fallback + ffmpeg post-processing — wrapping the async-api primitive into a full media pipeline service.
complexity: deep
produces: code
est_tokens: 4000
tags: [video-generation, production, fastapi, queue, ffmpeg]
---

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
