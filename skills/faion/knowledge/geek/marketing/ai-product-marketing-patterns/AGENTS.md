---
slug: ai-product-marketing-patterns
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Marketing patterns specific to AI products: demo variance, prompt-driven value, workflow-not-feature, dangerous comparison pages, amplified trust signals.
content_id: "d35864ec209df08b"
tags: [ai-product-marketing-patterns, marketing, geek]
---

# AI Product Marketing Patterns

## Summary

**One-sentence:** Marketing patterns specific to AI products: demo variance, prompt-driven value, workflow-not-feature, dangerous comparison pages, amplified trust signals.

**One-paragraph:** Marketing an AI product is structurally different: demos vary, output depends on prompt, value is in workflow not feature, comparison pages expose LLM lottery, trust signals matter 10×. faion has zero coverage. Half of faion's ICP builds AI products. Output: pattern audit with one decision per pattern.

## Applies If (ALL must hold)

- product wraps or extends LLMs (≥1 model API call in core loop)
- buyer-facing demo is part of funnel
- comparison or 'vs.' content is considered or live
- trust signals are weak or non-existent

## Skip If (ANY kills it)

- AI purely internal tooling — defer to standard marketing
- deterministic AI (classifiers with fixed thresholds)
- marketplace AI tools (model APIs themselves) — different category

## Prerequisites

- live demo or sandbox URL
- list of current comparison/vs-competitor pages
- list of trust signals currently displayed

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/gtm-strategist` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/ai-product-positioning` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/gtm-strategist`
- peer methodology: `geek/ai/ai-product-positioning`
- external: https://review.firstround.com/marketing-ai-products
