---
slug: gemini-multimodal
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Gemini multimodal integration — Files API upload + ACTIVE polling, image/audio/video inline limits, context caching for repeated docs, file-expiry handler.
content_id: "84e848cad8338495"
complexity: medium
produces: code
est_tokens: 3200
tags: [gemini, multimodal, video, audio, context-cache]
---
# Gemini Multimodal Integration

## Summary

**One-sentence:** Produces a Gemini multimodal integration — Files API upload + ACTIVE polling, image/audio/video inline limits, context caching for repeated docs, file-expiry handler.

**One-paragraph:** Gemini natively ingests images, audio, video, and PDFs without separate pipelines. The shape: small images (≤4 MB total) can be inlined as base64 parts; everything else goes through Files API which is async (states PROCESSING → ACTIVE → FAILED). Caller polls until ACTIVE before sending, sets a 48h TTL alarm, and re-uploads on FAILED. Context caching lets repeated documents (>32K tokens cached) cut per-call cost ~75%. Must surface BLOCK_REASON the same way as text calls.

**Ефективно для:** video summarisation, audio transcription pipelines, multi-document analysis, code/diagram understanding, multimodal chat.

## Applies If (ALL must hold)

- Vendor is Gemini AND at least one input modality is image/audio/video/PDF.
- Caller can wait for Files API upload (async, seconds to minutes).
- Storage cost / TTL acceptable for cached documents.
- Outputs flow through the safety + block-reason handling from `[[gemini-api-integration]]`.

## Skip If (ANY kills it)

- Text-only inputs — use `[[gemini-basics]]`.
- Real-time live voice — Gemini Live API is separate.
- Privacy-restricted content that cannot leave on-prem.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Media inputs | file paths or bytes | application |
| Files API quota | doc | finops |
| Context-cache budget | doc | finops |
| Gemini config (safety + generation) | JSON | `[[gemini-api-integration]]` |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[gemini-api-integration]]` | Safety + finish_reason handling. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: Files API for &gt;4 MB / video / audio, ACTIVE poll before send, TTL alarm, context cache for &gt;32K repeat, surface BLOCK_REASON, mime-type explicit | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for multimodal-config.json | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: inline-base64 video, send-during-PROCESSING, ignore TTL, no cache for repeat doc, BLOCK swallowed | ~600 |
| `content/04-procedure.xml` | medium | 6-step: classify input → upload via Files API → poll → cache if repeat → send → handle response | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "any non-text input?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Classify input | sonnet | Mechanical. |
| Upload + poll | runtime | Mechanical. |
| Cache decisions | opus | Cost reasoning. |
| Handle BLOCK_REASON | sonnet | Pattern. |

## Templates

| File | Purpose |
|---|---|
| `templates/multimodal-config.schema.json` | JSON Schema for multimodal-config.json. |
| `templates/files-api-client.py` | Files API upload + ACTIVE polling + TTL alarm. |
| `templates/context-cache.py` | Context-cache create + reuse pattern. |
| `templates/_smoke-test.json` | Minimum valid multimodal-config. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gemini-multimodal.py` | Validates multimodal-config: inline_limit_mb ≤4, files_api enabled if video/audio. | Pre-commit on config. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[gemini-api-integration]]`
- `[[gemini-basics]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` routes: text-only → skip; small images (≤4MB total) → inline; everything else → Files API path.
