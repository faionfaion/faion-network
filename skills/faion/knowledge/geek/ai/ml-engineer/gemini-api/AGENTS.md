---
slug: gemini-api
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a production Google Gemini API client wiring up streaming, function calling, multimodal input (image/audio/video), context caching, and Live API for real-time voice/video sessions.
content_id: "d71eec35f131f01a"
complexity: medium
produces: code
est_tokens: 3600
tags: [gemini, llm-api, multimodal, real-time, long-context]
---
# Gemini API Integration

## Summary

**One-sentence:** Produces a production Google Gemini API client wiring up streaming, function calling, multimodal input (image/audio/video), context caching, and Live API for real-time voice/video sessions.

**One-paragraph:** Produces a production-ready Google Gemini API client. Models: Gemini 3 Pro/Flash (1M+ context, dynamic thinking), Gemini 2.0 Flash (fast, agentic), Gemini 1.5 Pro (2M context). Key differentiators: native video/audio input, Live API for real-time voice/video, code execution sandbox, Google Search grounding, context caching (75% cost reduction on repeated context). Standardises retry/backoff, structured-output JSON mode, safety settings, and cache-key pattern.

**Ефективно для:** Бекенд-розробник для multimodal feature — за один прохід отримує client.py з streaming + caching + safety.

## Applies If (ALL must hold)

- Building an LLM integration where Gemini is the chosen provider (or one of several).
- Need at least one of: long context (>200k tokens), multimodal input (image/audio/video), Google Search grounding, code execution.
- Production deployment — needs retry, backoff, structured output, safety controls.
- Caching repeated context (system prompts >1024 tokens) is worthwhile economically.
- Real-time voice/video session use case (Live API) is in scope.

## Skip If (ANY kills it)

- Pure text LLM use case with no Gemini-specific differentiators — pick whichever provider is cheaper.
- Latency-critical interactive UI with sub-200ms target — Gemini Flash but not Pro.
- Strict data-residency outside Google's regions — verify region map.
- No Google Cloud / API key access — out of scope.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| API key | env var GOOGLE_API_KEY | ops |
| Model choice | string (gemini-3-pro / gemini-3-flash / ...) | ML lead |
| Use-case profile | yaml | product |
| Safety settings policy | yaml | trust+safety |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Selects Gemini as the provider. |
| `geek/ai/ml-engineer/llm-observability-stack` | Traces every Gemini call for cost / latency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: wire-client → enable-streaming → add-tools → wire-cache → wire-safety. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by model variant + caching + Live API. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-client` | haiku | Fill gemini-client.py from inputs. |
| `integrate-feature` | sonnet | Wire one Gemini-specific feature (cache, search grounding, code exec). |
| `debug-live-api` | opus | Real-time voice/video session debugging — cross-cutting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gemini-client.py` | Production client: retry, streaming, function calling, structured output. |
| `templates/gemini-multimodal.py` | Image / audio / video input variants. |
| `templates/gemini-cache.py` | Context cache create + reuse pattern. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gemini-api.py` | Validate the client config (model, safety, cache_ttl, structured_output_schema). | Pre-merge of every Gemini-client PR. |

## Related

- [[llm-decision-framework]] — provider choice.
- [[llm-observability-stack]] — tracing surface.
- [[claude-api]] — sibling provider methodology.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks Gemini variant (3 Pro / 3 Flash / 2.0 Flash / 1.5 Pro) + caching strategy + Live-API toggle.
