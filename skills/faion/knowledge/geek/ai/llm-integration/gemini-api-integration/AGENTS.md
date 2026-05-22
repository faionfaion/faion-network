---
slug: gemini-api-integration
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a working Gemini API integration — model selection (Pro vs Flash), 1M-context handling, Files API upload pattern, generation config + safety settings.
content_id: "fd2ba6000ce8c8c8"
complexity: medium
produces: code
est_tokens: 3300
tags: [gemini, google-ai, vertex, multimodal, integration]
---
# Gemini API Integration

## Summary

**One-sentence:** Produces a working Gemini API integration — model selection (Pro vs Flash), 1M-context handling, Files API upload pattern, generation config + safety settings.

**One-paragraph:** Google's Gemini API is the canonical entry point to gemini-2.x-pro and gemini-2.x-flash. Distinct shape vs Anthropic/OpenAI: large 1M-token context, Files API for video/audio uploads (vs inline base64), `generation_config` block (temperature, top_p, top_k, max_output_tokens, response_mime_type), and explicit `safety_settings` per category. This methodology produces a baseline integration: pick Flash for cost-sensitive paths and Pro for quality-sensitive; upload large media via Files API with TTL tracking; set generation_config defaults; configure safety thresholds to avoid silent BLOCK_REASON returns.

**Ефективно для:** ingesting long documents and full codebases, video analysis pipelines, cost-sensitive bulk classification, Vertex-anchored stacks.

## Applies If (ALL must hold)

- Gemini is the chosen vendor for this call site (cost, context, multimodal, or compliance reason).
- Either google-genai SDK or Vertex AI client is acceptable.
- Network access to Google AI endpoint.
- A response-handling layer can detect BLOCK_REASON and surface it.

## Skip If (ANY kills it)

- Pure text Q&A at &lt;8k context — Anthropic/OpenAI are equally fine and often faster at p50.
- Hard regulatory exclusion of Google AI in scope.
- Fine-tuning required as a first-class need — Gemini's fine-tuning is region-restricted.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Google AI / Vertex credentials | secret | secrets manager |
| Use case + expected context size | doc | spec |
| Latency budget per call site | ms | SLO |
| Safety policy (per category) | doc | safety review |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[gemini-basics]]` | Sibling baseline on SDK usage. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: pick model by cost+context, Files API for &gt;10MB, generation_config default, safety_settings explicit, retry on 429, block_reason surfaced | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for gemini-config.json + response-handler shape | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: inline base64 for big media, missing safety_settings, BLOCK_REASON swallowed, no retry on 429, model-mix on same call site | ~600 |
| `content/04-procedure.xml` | medium | 6-step: pick model → set generation_config → handle Files API → wire safety → handle block reasons → retry + monitor | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "Gemini is the chosen vendor for this call site?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Pick Pro vs Flash | sonnet | Cost/quality tradeoff. |
| Upload via Files API | runtime | Mechanical. |
| Surface BLOCK_REASON | sonnet | Pattern code. |
| Tune safety thresholds | opus | Policy reasoning. |

## Templates

| File | Purpose |
|---|---|
| `templates/gemini-config.schema.json` | JSON Schema for gemini-config.json. |
| `templates/gemini-client.py` | Reference Python integration with Files API + safety. |
| `templates/safety-defaults.yaml` | Default safety thresholds per category. |
| `templates/_smoke-test.json` | Minimum valid gemini-config. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gemini-api-integration.py` | Validates gemini-config.json against schema and asserts safety_settings cover all 4 standard categories. | Pre-commit on config; CI before deploy. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[gemini-basics]]`
- `[[gemini-multimodal]]`
- `[[gemini-function-calling]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` selects this methodology when Gemini is the chosen vendor. Branches by model choice (Pro vs Flash) given cost/quality budget; routes media-heavy calls to use Files API; skips when vendor is not Gemini.
