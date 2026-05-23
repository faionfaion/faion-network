---
slug: img-gen-tools
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a multi-provider image-generation service — DALL-E + Replicate (Flux/SDXL) + Stability adapter, S3 cache, prompt-template library, idempotent fallback.
content_id: "9f7b82dfb8a26503"
complexity: medium
produces: code
est_tokens: 3200
tags: [image-generation, multi-provider, replicate, stability, s3-cache, ai-content-production]
---
# Image Generation Tools

## Summary

**One-sentence:** Produces a multi-provider image-generation service — DALL-E + Replicate (Flux/SDXL) + Stability adapter, S3 cache, prompt-template library, idempotent fallback.

**One-paragraph:** Above the single-provider basics, production pipelines need a stable abstraction across providers (so cost or capacity migrations are config-only), an S3 cache keyed by `sha1(prompt+provider+params)` (so retries don't double-bill), a prompt-template library mapping use cases (article-header, social-card, product-mockup) to structured prompts, and an idempotent fallback chain (`dalle3 → flux-schnell → sdxl`) triggered on provider failure or budget exhaustion. Output: a typed ImageService class + provider adapters + per-call audit log.

**Ефективно для:** content engineer / media pipeline, що генерує images у production з multi-tenant budget + provider rotation + cache-on-prompt + audit trail.

## Applies If (ALL must hold)

- Multiple use cases share the generation pipeline (article-header + social-card + product-mockup).
- A multi-provider strategy is desired (cost/capacity/quality routing).
- An S3-compatible cache is available.
- Pipeline tolerates the fallback provider's quality when primary fails.

## Skip If (ANY kills it)

- Single use case + single provider — `[[img-gen-basics]]` is sufficient.
- Pixel-perfect brand on one provider — fallback chain undermines consistency.
- No cache available — re-generating the same prompt is wasteful.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Provider API keys (OpenAI + Replicate + Stability) | secret | secrets manager |
| Prompt-template library keyed by use case | YAML | content repo |
| S3-compatible cache bucket | URI | infra |
| Per-tenant cost band | YAML | finops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/multimodal-ai/img-gen-basics` | Single-provider baseline. |
| `geek/ai/llm-integration/ai-cost-attribution-schema` | Per-tenant attribution discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: provider abstraction, sha1-key cache, prompt template library, idempotent fallback, per-tenant attribution, audit log. | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for ImageService config + per-call audit log entry. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: cache key without params, no fallback, hardcoded provider, missing attribution, log without input hash. | ~700 |
| `content/04-procedure.xml` | medium | Steps: define template library → wire providers → cache layer → fallback chain → attribution → audit. | ~700 |
| `content/06-decision-tree.xml` | essential | Routes use case + cost band to a provider sequence. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft-template-library` | sonnet | YAML authoring. |
| `pick-fallback-chain` | opus | Cost vs quality reasoning. |
| `lint-cache-keys` | haiku | Pattern check on hash inputs. |

## Templates

| File | Purpose |
|---|---|
| `templates/image-service.py` | ImageService class with provider registry + cache + fallback. |
| `templates/multi-provider.py` | Provider adapters (DALL-E, Replicate, Stability). |
| `templates/cache-to-s3.py` | S3 cache layer keyed on sha1(prompt+provider+params). |
| `templates/prompt-templates.py` | Use-case → structured prompt template library. |
| `templates/prompt-generate.txt` | LLM-assisted prompt construction template. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-img-gen-tools.py` | Validate ImageService config: provider list, fallback chain, cache_uri, attribution enabled. | Pre-commit + CI. |

## Related

- [[img-gen-basics]]
- [[ai-cost-attribution-schema]]
- [[multi-provider-fallback-patterns]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes the use case (header/card/mockup) and the per-tenant cost band to a provider sequence (primary + fallbacks). Walk it before extending the use-case library so new use cases stay consistent with the cost discipline.
