# Image Generation Basics: DALL-E, Flux, and SDXL

## Summary

**One-sentence:** Produces an image-generation integration — DALL-E 3 / Flux / SDXL via Replicate, ImagePromptBuilder + revised_prompt audit + immediate download + rate-limit handling.

**One-paragraph:** DALL-E 3 is the gold standard for photorealistic generation but rewrites prompts silently (`revised_prompt` in response), has a 5 imgs/min rate limit per org, and returns URLs expiring in ~1 hour. Production wires: log `revised_prompt` for audit, structure prompts via ImagePromptBuilder (subject + style + lighting + composition + technical), download images immediately to durable storage, respect rate limits with exponential backoff, manually verify the first 3 outputs before launching a 100-image batch. For cost-sensitive batches use Flux-schnell or SDXL via Replicate (~100x cheaper).

**Ефективно для:** content engineer, що генерує article headers / social cards / product mockups і потребує детермінованої pipeline з audit trail, rate-limit safety, і cost-aware provider routing.

## Applies If (ALL must hold)

- Generating article headers, social media visuals, or product mockups from text descriptions.
- Pipeline can tolerate prompt rewriting (DALL-E 3) or wants Flux/SDXL cost profile.
- Outputs will pass human review before publish for regulated content (medical / legal / financial).
- A durable artefact storage (S3 / GCS) is available for immediate download.

## Skip If (ANY kills it)

- Pixel-perfect brand consistency required — DALL-E 3 revised prompts silently alter inputs.
- Images used without human review in regulated contexts.
- Subject requires real-person likeness — OpenAI policy blocks this.
- Exact text rendering in image required — all current models struggle.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Provider API key (OpenAI or Replicate) | secret | secrets manager |
| ImagePromptBuilder template + style guide | doc | brand repo |
| Durable artefact storage | S3/GCS URI | infra |
| Rate-limit budget (5/min tier 1) | doc | finops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/multimodal-ai/img-gen-tools` | Sibling: production patterns + multi-provider fallback. |
| `geek/ai/llm-integration/openai-api-integration` | OpenAI SDK baseline for DALL-E. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: structured prompts, log revised_prompt, download immediately, respect rate limit, manual smoke before batch, route by cost. | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for img-gen-config: provider, prompt_builder fields, storage, rate_limit. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: lost revised_prompt, cached URL 404, RL shared key, real-person likeness, on-image text expectation. | ~700 |
| `content/04-procedure.xml` | medium | Steps: pick provider → build prompt → smoke 3 → batch with RL → download to storage → log audit. | ~700 |
| `content/06-decision-tree.xml` | essential | Routes by cost-tolerance + brand-precision needs to DALL-E vs Flux vs SDXL. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `build-prompt` | sonnet | Template fill from style guide. |
| `pick-provider` | opus | Cost vs quality reasoning. |
| `audit-revised-prompt` | haiku | Diff and log. |

## Templates

| File | Purpose |
|---|---|
| `templates/dalle3.py` | DALL-E 3 client with revised_prompt logging + immediate download. |
| `templates/prompt-builder.py` | ImagePromptBuilder (subject + style + lighting + composition + technical). |
| `templates/batch-generator.py` | Batch driver with rate-limit aware backoff. |
| `templates/prompt-generate.txt` | Prompt-template for LLM-assisted prompt construction. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-img-gen-basics.py` | Validate img-gen-config: provider, storage URI, RL budget, prompt_builder fields. | Pre-commit + CI. |

## Related

- [[img-gen-tools]]
- [[openai-api-integration]]
- [[ai-cost-attribution-schema]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes by cost-tolerance + brand-precision: tight brand + cost OK → DALL-E 3; high-volume social → Flux-schnell via Replicate; cost-only with editable seed → SDXL. Walk it before wiring a generator so provider and storage are picked deterministically.
