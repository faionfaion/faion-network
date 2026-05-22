---
slug: openai-chat-completions
tier: geek
group: ai
domain: llm-integration
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates a production-grade OpenAI Chat Completions caller with deterministic params, finish-reason guard, exponential backoff, rate-limit header inspection, and per-call token+cost logging.
content_id: "d6a311d947a72fda"
complexity: medium
produces: code
est_tokens: 4200
tags: [openai, chat-completions, api, streaming, vision]
---
# OpenAI Chat Completions

## Summary

**One-sentence:** Disciplined wrapper around `client.chat.completions.create` that pins model, temperature, response_format, finish-reason check, retry policy, and usage logging — so pipelines do not silently truncate, double-spend, or hit rate-limits blind.

**One-paragraph:** Complete guide to the OpenAI Chat Completions endpoint (`/v1/chat/completions`): request structure, model selection (gpt-4o vs gpt-4o-mini vs o-series), parameters (temperature, max_tokens, response_format, seed), streaming, vision (URL and base64), error handling with exponential backoff via tenacity, rate-limit headers, and cost tracking via tiktoken. The core rule: always read `finish_reason` — `"length"` means silent truncation; never parse JSON from a truncated response.

**Ефективно для:** AI/ML інженера, що збирає продакшн-агентний pipeline на OpenAI — закриває петлю між запитом, обробкою помилок та обліком вартості.

## Applies If (ALL must hold)

- Building agent pipelines calling OpenAI models (gpt-4o, gpt-4o-mini, o1, o3-mini).
- Streaming partial outputs to users or downstream pipeline steps in real time.
- Generating structured JSON via `response_format={"type": "json_object"}` (not strict-schema parse).
- Multi-image or screenshot analysis inside an automated workflow.
- Cost-sensitive pipelines where gpt-4o-mini quality is acceptable.

## Skip If (ANY kills it)

- Persistent conversation state across sessions — use Assistants API.
- Guaranteed schema compliance — use Structured Outputs (`beta.parse`), not JSON Mode.
- More than 128K context required — switch to Claude 200K or Gemini.
- Anthropic Claude is available and the task is quality-sensitive — Claude wins on long-form reasoning.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `OPENAI_API_KEY` | env var | OpenAI dashboard, vault, or 1Password |
| `model` choice | string | matched to task complexity per model table |
| `messages` array | list[dict] | pipeline upstream (system+user+optional assistant turns) |
| Token budget cap | int | pipeline cost policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/prompt-basics` | Message-role discipline upstream of the call. |
| `geek/ai/llm-integration/structured-output-basics` | Decision between `json_object` vs strict-schema `beta.parse`. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: finish_reason guard, temperature discipline, mini-first routing, async-throttle, usage logging, header pre-check | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one logged call (model, usage, finish_reason, content); valid + invalid examples; forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix: truncated-JSON, blind-retry, model-not-found, vision-cost-blowup, sequential-batch-saturation | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: pick model → build messages → set params → call with retry → check finish_reason → log usage | ~700 |
| `content/06-decision-tree.xml` | essential | Picks `json_object` vs `beta.parse`, mini vs flagship, sync vs async; references rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inner-loop-extraction` | haiku | Cheap structured fill where mini quality matches. |
| `prompt-authoring` | sonnet | Per-prompt judgment, balance cost vs reliability. |
| `error-mode-synthesis` | opus | Multi-call failure analysis when usage / costs spike. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retry-client.py` | OpenAI client wrapper with tenacity retry on RateLimitError and APIError, plus finish_reason guard. |
| `templates/encode-image.py` | Base64 image-to-data-URL helper for vision messages, with MIME detection. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openai-chat-completions.py` | Validate a logged-call JSON record matches the output contract (model, usage, finish_reason, content shape). | Post-call in pipeline; nightly audit of call logs. |

## Related

- [[openai-function-calling]] — strict-schema extraction via `beta.parse`.
- [[openai-embeddings]] — embedding sibling for the same SDK.
- [[structured-output-basics]] — picking JSON Mode vs Structured Outputs.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides three things from the call site: (a) gpt-4o-mini vs gpt-4o vs o-series by task class; (b) `json_object` vs `beta.parse` vs free-form; (c) sync vs async based on parallel-fan-out > 2. Use it at the top of every new pipeline stage that calls Chat Completions.
