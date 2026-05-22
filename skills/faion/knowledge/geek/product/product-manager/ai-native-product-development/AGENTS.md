---
slug: ai-native-product-development
tier: geek
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A product strategy methodology for products where AI is not a feature but the delivery mechanism across all layers (research, design, development, testing, analytics, support).
content_id: "f8c074c1537ed9b5"
tags: [ai-native, product-strategy, inference-cost, build-vs-buy, compliance]
---
# AI-Native Product Development

## Summary

**One-sentence:** A product strategy methodology for products where AI is not a feature but the delivery mechanism across all layers (research, design, development, testing, analytics, support).

**One-paragraph:** A product strategy methodology for products where AI is not a feature but the delivery mechanism across all layers (research, design, development, testing, analytics, support). The development loop shifts from "build → test → iterate" to "define intent → AI generates → human refines → test." Inference cost, model versioning, and explainability are first-class product concerns. Covers build-vs-buy decisions and EU AI Act compliance framing.

## Applies If (ALL must hold)

- Writing roadmap strategy for a product where AI is not a feature but the delivery mechanism (AI-first architecture)
- Deciding which AI capabilities to build vs. buy for a given product; structuring the build-vs-buy decision for a stakeholder presentation
- Onboarding a product team to the "AI-native" development pattern: define intent → AI generates → human refines → test
- Framing EU AI Act obligations for a product — which AI components require documentation, explainability, and bias testing
- Identifying which product layers (research, design, dev, test, analytics, support) are highest-priority candidates for AI integration
- Transitioning a traditional product roadmap to an AI-native one where inference cost, model versioning, and explainability are first-class concerns

## Skip If (ANY kills it)

- The product has no AI components and none are planned — standard product management methodologies apply
- Team is exploring whether to use AI at all; this methodology assumes the decision to go AI-native is already made
- Product operates in a domain where current AI models cannot achieve acceptable quality (e.g., domain-specific medical diagnosis without specialized fine-tuning)
- Sprint/quarter planning without a strategic product context — this methodology operates at the strategy layer, not at the task execution layer

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

- parent skill: `geek/product/product-manager/`
