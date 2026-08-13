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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/video-poll.py`

```python
"""
from __future__ import annotations

import time

try:
    from google import genai
except ImportError:
    genai = None


def upload_and_wait(client, path: str, poll_timeout_s: int = 300, interval_s: int = 5):
    if genai is None:
        raise SystemExit("google-genai required")
    file = client.files.upload(file=path)
    deadline = time.time() + poll_timeout_s
    while time.time() < deadline:
        f = client.files.get(name=file.name)
        if f.state.name == "ACTIVE":
            return f
        if f.state.name == "FAILED":
            raise RuntimeError(f"Files API upload failed: {f.name}")
        time.sleep(interval_s)
    raise TimeoutError(f"file did not become ACTIVE within {poll_timeout_s}s")
```

### `templates/context-cache.py`

```python
Context caching for Gemini — create, use, and manage caches for large documents.

Requires >=32K tokens in cached content. Cached tokens cost ~75% less than full-price input.

Usage:
    cache = create_document_cache("large_document.pdf", ttl="3600s")
    answer = query_cache(cache, "What are the payment terms?")
    cache.delete()
"""
import google.generativeai as genai
from google.generativeai import caching


def create_document_cache(
    file_path: str,
    display_name: str = "document-cache",
    system_instruction: str = "You are an expert document analyzer.",
    model: str = "gemini-1.5-pro",
    ttl: str = "3600s",
):
    """Upload file and create a context cache. Raises if token count < 32K."""
    document = genai.upload_file(file_path)
    cache = caching.CachedContent.create(
        model=model,
        display_name=display_name,
        system_instruction=system_instruction,
        contents=[document],
        ttl=ttl,
    )
    print(f"Cache: {cache.name}, tokens: {cache.usage_metadata.total_token_count}")
    return cache


def query_cache(cache, question: str) -> str:
    """Query a cached document. All calls reuse cached tokens (75% cheaper)."""
    model = genai.GenerativeModel.from_cached_content(cache)
    return model.generate_content(question).text


def extend_cache(cache, ttl: str = "7200s"):
    """Extend cache TTL before expiry."""
    cache.update(ttl=ttl)
```

### `templates/vertex-setup.py`

```python
"""
from __future__ import annotations

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def vertex_client(project: str, location: str = "us-central1"):
    if genai is None:
        raise SystemExit("google-genai required")
    return genai.Client(vertexai=True, project=project, location=location)


def gcs_part(uri: str, mime_type: str) -> "types.Part":
    if types is None:
        raise SystemExit("google-genai required")
    return types.Part.from_uri(file_uri=uri, mime_type=mime_type)
```
