# Gemini Multimodal Integration

## Summary

**One-sentence:** Gemini native multimodal — image/audio/video/PDF + code execution + 2M context + 75%-cheaper context caching, with polling + file-expiry handling.

**One-paragraph:** Gemini is the only frontier model with native video/audio understanding (no frame extraction or Whisper hop) and a 2M-token context window. For multi-document pipelines, context caching cuts input cost ~75% vs. full-price per call. Production wires need a polling state machine with a max-iteration guard, explicit FAILED handling, a 48h file-expiry handler, and either Files API or GCS URIs (Vertex AI). Code execution adds a Python sandbox (no internet, ~30s cap). Enterprise deployments must use Vertex AI (ADC, CMEK, VPC-SC) instead of the Developer API.

**Ефективно для:** інженера, який будує мультимодальний агент/пайплайн (video Q&A, OCR, audio transcribe, PDF extraction) на Gemini і потребує детермінованого state-machine + кеш-економії + Vertex AI compliance.

## Applies If (ALL must hold)

- Processing video natively without frame extraction.
- Audio transcription/analysis without a separate Whisper hop.
- Long-document pipelines exploiting the 2M-token context window.
- Combined-modality tasks (video+PDF, image+audio) in one call.
- Enterprise deployment requires CMEK / VPC-SC / IAM (Vertex AI).

## Skip If (ANY kills it)

- Text-only tasks already on OpenAI/Anthropic — adds SDK surface without gain.
- Need maximum reasoning depth — Claude Opus / o1 outperform on multi-step reasoning.
- Privacy-sensitive content that cannot leave on-prem — uploads to Google.
- Low-latency realtime voice — OpenAI Realtime API simpler than Gemini Live.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Gemini SDK + API key (or ADC for Vertex) | secret | secrets manager |
| Media file or GCS URI | bytes/uri | storage |
| Polling budget (max iterations + timeout) | int | config |
| Cache TTL policy (1h interactive / 24h batch) | duration | config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/llm-integration/gemini-api-integration` | Baseline SDK setup, safety, Files API. |
| `geek/ai/llm-integration/gemini-basics` | Model selection (1.5-pro vs 2.0-flash) and pricing tiers. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 rules: poll until ACTIVE/FAILED, max-iteration guard, 48h expiry handler, ≥32K for cache, ADC for Vertex, separate part-types for code exec, GCS URIs for large files. | ~900 |
| `content/02-output-contract.xml` | essential | JSON contract for a gemini-multimodal config — uploads, polling, cache, modality flags. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: infinite PROCESSING loop, silent re-upload, cache on <32K content, mixed Vertex/Developer auth, blind .parts[0] indexing. | ~700 |
| `content/04-procedure.xml` | medium | Steps: classify modality → choose Files API vs GCS URI → upload+poll → optionally cache → generate → extract per-part output. | ~800 |
| `content/06-decision-tree.xml` | essential | Is this multimodal AND vendor=Gemini? → modality routing → cache vs no-cache → Vertex vs Developer. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `wire-upload-poll-state-machine` | sonnet | Mechanical state machine, type-safe transitions. |
| `decide-cache-vs-direct` | opus | Cost reasoning across query patterns. |
| `audit-file-expiry` | haiku | Pattern-match for 48h expiry handling. |

## Templates

| File | Purpose |
|---|---|
| `templates/video-poll.py` | Async video upload + polling loop with max-iteration guard + FAILED handling. |
| `templates/context-cache.py` | Cache create + reuse + TTL extend + delete lifecycle. |
| `templates/vertex-setup.py` | Vertex AI init with ADC + GCS URI part construction. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gemini-multimodal.py` | Validate gemini-multimodal-config JSON: modality, polling cap, expiry handling, cache token-floor, auth match. | Pre-commit + CI. |

## Related

- [[gemini-function-calling]]
- [[gemini-api-integration]]
- [[speech-to-text-basics]]
- [[img-gen-basics]]

## Decision tree

The tree at `content/06-decision-tree.xml` walks: is the task multimodal? → is vendor Gemini? → which modality (image/audio/video/PDF/code-exec)? → does context fit a cache (≥32K, ≥2 reuses)? → Developer API vs Vertex AI based on compliance needs. Walk it before invoking the SDK so polling, caching, and auth are picked deterministically.
