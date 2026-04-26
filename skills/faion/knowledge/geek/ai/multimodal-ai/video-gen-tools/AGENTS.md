# Video Generation Tools

## Summary

API client implementations for Runway Gen-3, Luma Dream Machine, and Replicate video models (SVD, AnimateDiff, Zeroscope). Includes a production async VideoGenerationService with multi-provider fallback, retry logic, and a stub for image upload that must be implemented per storage backend.

## Why

Each provider has incompatible API shapes, async polling semantics, and URL expiry windows (30–60 min). A unified service layer with provider-specific adapters and immediate post-generation download prevents the most common production failures (expired URLs, missing timeouts, OOM from full-file-in-memory downloads).

## When To Use

- Integrating Runway, Luma, or Replicate into an automated content pipeline
- Building multi-provider fallback logic for resilience
- Extending an existing video by appending new AI-generated segments
- Wrapping async generation in retry/timeout logic for production reliability

## When NOT To Use

- Single one-off clip — use the web UI directly; API setup overhead is not justified
- Synchronous request/response architectures — all video APIs are async polling; this pattern will block
- When video quality is untested — validate provider outputs manually before automating at scale
- Latency-sensitive user flows (sub-2s response expected)

## Content

| File | What's inside |
|------|---------------|
| `content/01-providers.xml` | RunwayVideoGenerator, LumaVideoGenerator, ReplicateVideoGenerator implementations |
| `content/02-service.xml` | VideoGenerationService with multi-provider routing, retry, download; known bugs and fixes |

## Templates

| File | Purpose |
|------|---------|
| `templates/runway-generator.py` | RunwayVideoGenerator: text-to-video and image-to-video via SDK |
| `templates/luma-generator.py` | LumaVideoGenerator: generate, extend, image-to-video via REST |
| `templates/replicate-generator.py` | ReplicateVideoGenerator: SVD, AnimateDiff, Zeroscope |
| `templates/video-service.py` | VideoGenerationService with async multi-provider routing |
| `templates/prompt-generate.txt` | Agent prompt pattern for dispatching and polling a generation job |
