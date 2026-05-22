---
slug: prompt-techniques
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced prompting patterns, testing, and management strategies.
content_id: "5cb213522bb7d680"
tags: [prompt-optimization, meta-prompting, prompt-chaining, prompt-testing, a-b-testing]
---
# Advanced Prompt Techniques

## Summary

**One-sentence:** Advanced prompting patterns, testing, and management strategies.

**One-paragraph:** Advanced prompting patterns, testing, and management strategies.

## Applies If (ALL must hold)

- A prompt is underperforming (wrong format, missing edge cases, hallucinating) and needs systematic improvement via meta-prompting or A/B testing
- A pipeline has multiple discrete LLM steps that should be decoupled into a PromptChain for maintainability
- The project needs a versioned PromptLibrary so prompts can be updated without code deployments
- You need to validate prompt accuracy against a known test set before releasing a new version
- Prompt injection or delimiter confusion is causing failures in production

## Skip If (ANY kills it)

- The prompt is simple (<50 words) and passes manual inspection — over-engineering with libraries adds maintenance cost
- The task changes frequently; a rigid PromptLibrary with versioning becomes a burden if prompts are iterated daily
- You need model-specific optimizations (e.g., Anthropic XML tags vs. OpenAI system messages) — a cross-provider library hides these differences and can regress quality
- Budget is tight and meta-prompting (using GPT-4o to generate prompts) doubles token cost on every iteration

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/llm-integration/`
