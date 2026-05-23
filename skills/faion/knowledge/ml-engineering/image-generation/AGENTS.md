# AI Image Generation — Model Selection & Pipeline

## Summary

**One-sentence:** Picks model by task class (text-in-image / photorealism / brand-consistent / bulk), enforces the 6-element prompt formula, and emits a batch pipeline config with cost + safety policy.

**One-paragraph:** No single model wins everywhere — DALL-E 3 / GPT-4o for in-image text, Flux Pro for photorealism, Flux schnell (Apache 2.0) for high-volume bulk, SD+LoRA for brand-consistent assets. This methodology codifies which model fits which task class, the mandatory 6-element prompt structure (Subject + Style + Lighting + Composition + Details + Technical), the batch concurrency and retry policy, and the safety filter for likeness / legal risk. Output: `image-gen-config.json`.

**Ефективно для:**

- AI news pipeline — кожна стаття отримує унікальний header image; cost per image критичний.
- A/B test creatives — згенеруй 8 варіантів на тестування при тому ж бюджеті.
- UI/UX prototyping — швидкий моок інтерфейсу до фігми.
- Brand-consistent ілюстрації — LoRA / Flux Kontext fixed character identity через серію.

## Applies If (ALL must hold)

- Need to generate ≥10 images programmatically (one-offs use the chat UI).
- Output policy lets a generative model produce the asset (no real-person likeness, no legal/medical illustrations).
- Per-image cost or latency matters enough to justify model selection (not flat-rate everything via DALL-E 3).

## Skip If (ANY kills it)

- Logos / vector assets — generative models output raster only.
- Real named people photorealism — content policy + likeness rights kill it.
- Single one-off image — chat UI is cheaper than building a pipeline.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use-case spec | Markdown | product brief |
| Budget per image | float USD | finance |
| Brand style guide (if brand-consistent) | reference images | brand team |
| API keys (OpenAI / Flux / SD host) | env | secrets manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `llm-decision-framework` | Provider choice mirrors LLM provider posture. |
| `cost-optimization` | Per-image cost drives model selection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: model-by-task, six-element-prompt, schnell-for-bulk, lora-for-brand, no-likeness | 1000 |
| `content/02-output-contract.xml` | essential | Schema for image-gen-config.json | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: wrong-model-for-text, vague-prompt, missing-rate-limit, no-content-filter | 800 |
| `content/04-procedure.xml` | essential | 5 steps: classify-task → pick-model → build-prompt-template → pipeline-batch → safety-filter | 600 |
| `content/06-decision-tree.xml` | essential | Task → model selector | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick_image_model` | haiku | Decision-tree lookup. |
| `craft_prompt_template` | sonnet | Creative + structural. |

## Templates

| File | Purpose |
|------|---------|
| `templates/image-gen-config.json` | Skeleton config |
| `templates/prompt_formula.txt` | 6-element prompt template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-image-generation.py` | Validate image-gen-config.json | Pre-deploy gate |

## Related

- [[llm-decision-framework]] — same provider posture as text models
- [[cost-optimization]] — per-image cost drives Flux schnell vs DALL-E choice
- [[multimodal-ai]] — broader vision/audio context

## Decision tree

See `content/06-decision-tree.xml`. Branches on text-in-image y/n, brand-consistency requirement, and volume.
