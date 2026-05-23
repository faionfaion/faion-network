# Video Generation Tools

## Summary

**One-sentence:** Wraps Runway Gen-3, Luma Dream Machine, and Replicate adapters behind a unified async VideoGenerationService with multi-provider fallback and immediate download.

**One-paragraph:** RunwayVideoGenerator (official SDK, timeout-protected polling), LumaVideoGenerator (REST + custom timeout fix), ReplicateVideoGenerator (pinned model hashes for SVD / AnimateDiff / Zeroscope), and a VideoGenerationService that selects provider by style_tag, retries on transient failure, fallbacks across providers, and streams the pre-signed URL to disk before the 30-60 min expiry. The `_upload_image` method is intentionally a stub — must be implemented per storage backend (S3 / GCS / Cloudinary) before image-to-video works.

**Ефективно для:** інженера AI-конвеєра, що будує надійну відеогенерацію з фолбеком провайдерів і архівацією — закриває петлю між сирим брифом і файлом у постійному сховищі.

## Applies If (ALL must hold)

- Integrating Runway / Luma / Replicate into an automated content pipeline.
- Multi-provider fallback is required (one provider's failure cannot break the pipeline).
- Generation calls happen in an async runtime (asyncio, FastAPI, LiveKit).
- Output must be in permanent storage within the pre-signed URL expiry window (30-60 min).
- Provider rate limits are known and enforced (Runway 10 concurrent tasks, Luma plan-dependent).

## Skip If (ANY kills it)

- Single one-off clip — use `video-gen-basics` direct call; service setup overhead unjustified.
- Synchronous request/response architecture — all video APIs are async polling, will block sync handler.
- Output quality not yet validated — manually verify provider output before automating at scale.
- Latency-sensitive user flow (sub-2s response) — generation is 30-300s; pre-generate or cache.
- No permanent storage backend wired up — pre-signed URLs WILL expire and clips WILL be lost.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| VideoGenerationConfig | dataclass: provider, default_duration, max_retries, timeout, output_dir | pipeline config |
| Provider credentials | env: `RUNWAY_API_KEY`, `LUMA_API_KEY`, `REPLICATE_API_TOKEN` | secrets manager |
| Image upload backend | callable `_upload_image(local_path) -> public_url` | per-host implementation |
| Permanent storage | S3 / GCS bucket with rw + sync IAM | infra team |
| ffmpeg + ffprobe | apt / brew | host setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/video-gen-basics` | core VideoPromptBuilder + ffprobe validation reused by every adapter. |
| `geek/ai/multimodal-ai/img-gen-basics` | upstream source for anchor frames passed to image-to-video. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: immediate download, streaming download, pin model hashes, provider-id isolation, log prompt+task, validate ffprobe | ~1000 |
| `content/02-output-contract.xml` | essential | Schema of service.generate() result with retries, fallback chain, archived_path | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: expired URL, OOM download, cross-provider id mix, retry on policy violation, stub upload | ~900 |
| `content/04-procedure.xml` | deep | 8-step procedure: dispatch → poll → stream-download → ffprobe → archive → fallback → retry → log | ~900 |
| `content/05-examples.xml` | medium | Worked Runway → Luma fallback for a cinematic 5s clip; S3 archival path | ~600 |
| `content/06-decision-tree.xml` | essential | Provider routing + fallback ordering by style_tag and recent provider failure state | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `dispatch-provider` | haiku | Adapter dispatch is mechanical. |
| `route-by-style` | sonnet | Decision-tree walk on style_tag + provider health state. |
| `archive-to-s3` | haiku | Sweep + upload + metadata write; mechanical. |
| `analyze-policy-failure` | sonnet | When FAILED with terse error, judge if it's a policy violation vs transient. |

## Templates

| File | Purpose |
|------|---------|
| `templates/runway-generator.py` | RunwayVideoGenerator — text-to-video, image-to-video, timeout-protected polling. |
| `templates/luma-generator.py` | LumaVideoGenerator — REST + timeout fix; generation_id tracking for extend. |
| `templates/replicate-generator.py` | ReplicateVideoGenerator — SVD / AnimateDiff / Zeroscope with pinned hashes. |
| `templates/video-service.py` | VideoGenerationService with multi-provider fallback + retry + streaming download. |
| `templates/prompt-generate.txt` | Agent prompt for dispatching + polling + returning structured result. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-gen-tools.py` | Validate service.generate() output against 02-output-contract. | Post-generation; before sweeper archives to S3. |

## Related

- [[video-gen-basics]] — single-call layer this service builds on.
- [[img-gen-tools]] — generates anchor frames for image-to-video.
- [[multimodal-ai/vision-applications]] — post-hoc verification of generated frames against brief.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` selects primary provider by style_tag (photorealistic → Luma; cinematic → Runway; animated → Replicate AnimateDiff), then defines the fallback chain when the primary returns FAILED or TIMEOUT or a policy violation is suspected. Use it at the dispatch step in VideoGenerationService.generate() before any provider call.
