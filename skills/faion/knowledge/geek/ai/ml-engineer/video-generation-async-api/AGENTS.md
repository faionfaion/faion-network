---
slug: video-generation-async-api
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "ec4082babe7c1e86"
summary: Async-API pattern for video generation providers (Runway, Luma, Veo, Sora) — submit, poll with exponential backoff, fetch artefact, retry on transient failures, with provider-fallback and idempotency-key.
complexity: medium
produces: code
est_tokens: 3400
tags: [video-generation, async, polling, runway, api-integration]
---

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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-generation-async-api.py` | Lint VideoJob OR provider-config | Pre-commit |

## Related

- [[video-generation-production-service]] · [[video-generation-prompt-engineering]]
- external: [Runway API](https://docs.dev.runwayml.com/) · [Luma API](https://docs.lumalabs.ai/) · [Google Veo](https://cloud.google.com/vertex-ai/generative-ai/docs/video-generation/overview)

## Decision tree

See `content/06-decision-tree.xml`. Routes job lifecycle status → action: in-progress / succeeded / failed-transient / failed-permanent / timeout → fallback.
