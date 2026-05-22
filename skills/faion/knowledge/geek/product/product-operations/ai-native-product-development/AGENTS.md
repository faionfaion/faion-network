---
slug: ai-native-product-development
tier: geek
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI integration strategy for products designed around AI from day one.
content_id: "f8c074c1537ed9b5"
tags: [ai-native, product-operations, build-vs-buy, ai-integration-strategy, compliance]
---
# AI-Native Product Development (Operations)

## Summary

**One-sentence:** AI integration strategy for products designed around AI from day one.

**One-paragraph:** AI integration strategy for products designed around AI from day one. Evaluate opportunities across layers (research, design, dev, test, analytics, support). Make build-vs-buy decisions. Operationalize EU AI Act compliance.

## Applies If (ALL must hold)

- Defining the AI integration strategy for a new product from day one (not retrofitting AI onto an existing feature)
- Evaluating which layers of the product stack (research, design, development, testing, analytics, support) should use AI tooling vs. traditional approaches
- Making build-vs-buy decisions for AI features: is this a core differentiator or a commodity capability?
- Ensuring EU AI Act compliance is designed into the product before launch rather than bolted on after
- Choosing the right MVP pattern when the product's UX loop involves AI generation (define intent → AI generates → human refines)
- Briefing a product team or stakeholder on what "AI-native" means operationally and what it changes about delivery

## Skip If (ANY kills it)

- Product is purely data-driven without a generative or reasoning component — use standard product operations instead
- Team has no ML/AI production experience; AI-native development amplifies complexity for inexperienced teams before it accelerates delivery
- Infrastructure for AI (inference budget, observability, data pipelines) does not yet exist — set this up first
- Evaluating an existing feature for incremental AI enhancement; that is AI-augmentation, not AI-native design

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

- parent skill: `geek/product/product-operations/`
