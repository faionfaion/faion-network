---
slug: figma-ai-ecosystem
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Figma AI tools (Config 2025+) compress the prototype-to-stakeholder-review cycle from days to hours.
content_id: "6ba71d5e338c9818"
tags: [figma, figma-make, figma-ai, ai-image-tools, prototyping]
---
# Figma AI Ecosystem

## Summary

**One-sentence:** Figma AI tools (Config 2025+) compress the prototype-to-stakeholder-review cycle from days to hours.

**One-paragraph:** Figma AI tools (Config 2025+) compress the prototype-to-stakeholder-review cycle from days to hours. However, each tool has hard limits: Make prototypes are static, Sites output is not a CMS, AI image expansion fails on complex textures, and all AI features are gated behind paid plans. Knowing which tasks belong to Figma AI vs a Claude agent prevents building workflows that don't exist.

## Applies If (ALL must hold)

- Generating web app prototypes rapidly from a text brief using Figma Make
- Removing objects or expanding image backgrounds on the Figma canvas without export/re-import
- Publishing a static site from Figma via Figma Sites for early stakeholder review
- Producing vector sketch assets using Figma Draw for illustration-heavy UI components
- Auditing a team's Figma AI feature adoption and identifying workflow gaps

## Skip If (ANY kills it)

- Production web development — Figma Sites output is for demos and landing pages, not complex apps
- Complex multi-state interactive prototyping requiring custom conditional logic
- Brand-critical image editing where exact pixel control matters — AI image tools are probabilistic
- Figma Draw for precise icon creation — generative output lacks manual vector precision

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

- parent skill: `geek/ux/ux-ui-designer/`
