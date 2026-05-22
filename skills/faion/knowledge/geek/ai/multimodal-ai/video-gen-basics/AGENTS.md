---
slug: video-gen-basics
tier: geek
group: ai-core
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Runway / Luma / Replicate video clip with structured prompt (subject + action + camera + style + lighting) and ffprobe-validated output.
content_id: "3d8b5c2e7f014a96"
complexity: medium
produces: code
est_tokens: 3700
tags: [video-generation, ai-video, runway, async-polling, ffmpeg]
---
# Video Generation Basics

## Summary

**One-sentence:** Generates a short (≤10s) AI video clip via Runway Gen-3, Luma Dream Machine, Pika, or Replicate, with a structured prompt builder and async polling.

**One-paragraph:** Wraps text-to-video and image-to-video generation with a VideoPromptBuilder that enforces explicit subject, action, setting, camera-movement, style, and lighting fields. Submits to provider, polls status (30-300s typical), downloads the pre-signed URL within the expiry window (30-60min), and runs ffprobe validation before returning. Caches generated clips by prompt hash with seed; defaults to image-to-video when subject consistency matters across shots.

**Ефективно для:** агента контент-конвеєра, що збирає короткі промо / b-roll / соцмережеві кліпи з єдиним брифом — закриває петлю між текстовим брифом і відеофайлом, готовим до монтажу.

## Applies If (ALL must hold)

- Generating short (≤10s) marketing, social, or b-roll video clips from text or image input.
- Pipeline tolerates 30-300s async latency per clip (not user-interactive).
- A structured brief (subject + action + setting) is available before the call.
- Output is consumed by ffmpeg for trim / concat / resize, not by a realtime player.
- At least one provider API key (Runway / Luma / Replicate / Pika) is configured.

## Skip If (ANY kills it)

- Precise temporal control needed (specific action at specific timestamp) — no current model enforces this.
- Character consistency across multiple shots is mandatory — models drift between generations.
- Videos longer than 10-15s without chaining — concat via ffmpeg or use `video-gen-tools` for extension.
- Real-time generation required — generation is async, 30-300s per clip.
- Faces or brand logos in the brief — providers silently FAIL on policy violations.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Brief | dict: `{subject, action, setting, camera, style, lighting, duration_s}` | content planner |
| Provider credentials | env: `RUNWAY_API_KEY`, `LUMA_API_KEY`, `REPLICATE_API_TOKEN` | secrets manager |
| Image source (optional) | URL or local path (for image-to-video) | content store |
| Output dir | filesystem path with rw | pipeline orchestrator |
| ffmpeg + ffprobe installed | apt / brew | host setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/video-gen-tools` | downstream production layer with VideoGenerationService + multi-provider fallback |
| `geek/ai/llm-integration/structured-output-basics` | upstream brief shaping (subject/action/camera as typed fields) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: explicit camera, image-to-video default, ffprobe validate, seed cache, 5s cap, no inline video read | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema of generate() result + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing camera, fixed temp paths, no ffprobe, expired URL, inline video read | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: build prompt → submit → poll → download → ffprobe → cache | ~700 |
| `content/05-examples.xml` | medium | Worked Runway Gen-3 5s clip with VideoPromptBuilder + polling + ffprobe | ~500 |
| `content/06-decision-tree.xml` | essential | Provider routing: photorealistic / cinematic / animated / prototype + text vs image input | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `build-prompt` | sonnet | Brief → VideoPromptBuilder call with camera/style choices. |
| `poll-status` | haiku | Mechanical loop, sleep+check. |
| `validate-output` | haiku | ffprobe + size check; deterministic. |
| `route-provider` | sonnet | Decision-tree walk on style_tag + input mode. |

## Templates

| File | Purpose |
|------|---------|
| `templates/video-prompt-builder.py` | VideoPromptBuilder with subject / action / setting / camera / style / lighting fields. |
| `templates/video-processor.py` | VideoProcessor: ffprobe validate, ffmpeg concat / resize / audio-merge. |
| `templates/concat-clips.sh` | Bash helper for ffmpeg concat from `clips.txt`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-gen-basics.py` | Validate generate() output JSON against 02-output-contract. | Post-generation, before downstream consumes path. |

## Related

- [[video-gen-tools]] — production service with multi-provider fallback + retry.
- [[img-gen-basics]] — image generator providing image-to-video source frames.
- [[multimodal-ai/vision-applications]] — verify generated frames against the brief.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes provider by style_tag (photorealistic → Luma; cinematic → Runway; animated → Replicate AnimateDiff; prototype → Replicate SVD), and decides text-to-video vs image-to-video based on whether subject consistency across shots is required. Use it at the generate() entry point before the first provider call.
