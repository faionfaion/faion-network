---
slug: product-explainability
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Product explainability is how clearly a product communicates its purpose, value, behavior, and limits to both humans and AI systems.
content_id: "821658e3a1f4baf5"
tags: [ai-discovery, schema-markup, knowledge-base, product-representation, agent-ops]
---
# Product Explainability

## Summary

**One-sentence:** Product explainability is how clearly a product communicates its purpose, value, behavior, and limits to both humans and AI systems.

**One-paragraph:** Product explainability is how clearly a product communicates its purpose, value, behavior, and limits to both humans and AI systems. As search, recommendations, and buying guidance become AI-mediated, products need structured representation (llms.txt, schema.org JSON-LD, capability KB) that AI crawlers can retrieve accurately. The canonical artifact is product-kb.json — a structured source of truth for purpose, capabilities, limits, use cases, and audience — from which all public surfaces are generated.

## Applies If (ALL must hold)

- Pre-launch: producing or auditing the product KB that will represent the product to AI systems
- Migrating from human-only marketing copy to AI-mediated discovery
- After a major model update or SEO/AEO shift when AI traffic displaces classical organic search
- When customers report wrong AI answers ("ChatGPT said your tool can do X but it can't")
- Integrating product into agent toolchains (MCP servers, OpenAI custom GPT actions, Claude skills)
- Compliance contexts (EU AI Act Art. 13, FTC AI guidance) where documented scope is required

## Skip If (ANY kills it)

- Pre-PMF products with <100 users — fix the product, not its representation
- Internal-only tools that no AI will ever index or recommend
- One-page landing pages with a single CTA — standard Open Graph is sufficient
- Products whose purpose changes monthly — KB will be stale faster than it ships
- Hyper-niche enterprise sales reached only through human channels (RFP, channel partner)

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

- parent skill: `pro/product/product-operations/`
