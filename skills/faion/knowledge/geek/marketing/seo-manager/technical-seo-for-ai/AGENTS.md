---
slug: technical-seo-for-ai
tier: geek
group: marketing
domain: seo-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Technical optimizations that make content accessible and trustworthy to AI crawlers (GPTBot, Claude-Web, PerplexityBot): creating `llms.
content_id: "78c5847137fd8339"
tags: [seo, ai-crawlers, technical-seo, schema-markup, core-web-vitals]
---
# Technical SEO for AI

## Summary

**One-sentence:** Technical optimizations that make content accessible and trustworthy to AI crawlers (GPTBot, Claude-Web, PerplexityBot): creating `llms.

**One-paragraph:** Technical optimizations that make content accessible and trustworthy to AI crawlers (GPTBot, Claude-Web, PerplexityBot): creating `llms.txt` for AI crawler guidance, implementing Article schema with author credentials, clean URL structure, proper heading hierarchy, entity consistency, and explicit author authority signals. Different from traditional SEO — AI crawlers evaluate factual accuracy and authority, not just keyword density.

## Applies If (ALL must hold)

- Setting up a new content site or blog that needs AI crawler visibility from launch.
- Auditing an existing site for AI crawlability issues (missing schema, no `llms.txt`, ambiguous entity naming).
- Implementing author credential markup to improve E-E-A-T signals for AI systems.
- Optimizing Core Web Vitals for AI crawler accessibility (LCP < 2.5s, CLS < 0.1).

## Skip If (ANY kills it)

- Paywalled or premium content sites where AI crawling of content is undesirable — configure `llms.txt` to block rather than optimize.
- Sites with no original content (pure aggregators) — technical optimization cannot compensate for lack of authority.
- Short-lived campaign landing pages with no long-term SEO value.

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

- parent skill: `geek/marketing/seo-manager/`
