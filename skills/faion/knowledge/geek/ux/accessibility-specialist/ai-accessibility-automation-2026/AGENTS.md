---
slug: ai-accessibility-automation-2026
tier: geek
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Full continuous accessibility automation pipeline for products with frequent deployments: axe-playwright scans every deploy, AI ranks and de-duplicates violations, code fixes are suggested per issue, VPAT 2.
content_id: "5612b610ab8b56d7"
tags: [accessibility, wcag, ada-compliance, automation, vpat]
---
# AI Accessibility Automation 2026

## Summary

**One-sentence:** Full continuous accessibility automation pipeline for products with frequent deployments: axe-playwright scans every deploy, AI ranks and de-duplicates violations, code fixes are suggested per issue, VPAT 2.

**One-paragraph:** Full continuous accessibility automation pipeline for products with frequent deployments: axe-playwright scans every deploy, AI ranks and de-duplicates violations, code fixes are suggested per issue, VPAT 2.5 drafts are generated from scan summaries, and caption/alt-text pipelines run on every media upload. All AI outputs are gated by a human accessibility lead before entering the developer backlog.

## Applies If (ALL must hold)

- Establishing continuous accessibility monitoring in a CI/CD pipeline for a product with frequent deployments
- Generating ADA Title II compliance documentation (effective 2026) for public-sector or higher-education digital products
- Scaling accessibility remediation across a large codebase where manual triaging is cost-prohibitive
- Producing AI-assisted VPAT drafts for enterprise procurement processes
- Automating captioning and audio description pipelines for video-heavy content operations
- Setting up regression prevention so new code does not reintroduce fixed violations

## Skip If (ANY kills it)

- The team has no existing accessibility baseline — start with a manual audit first to understand the real state
- Product is in pre-MVP prototyping — defer automation until the UI stabilizes
- AI automation is being proposed as a replacement for user testing with people who use assistive technology
- The team plans to deploy AI overlay widgets as the compliance strategy (overlays do not satisfy ADA Title II)
- Budget is the only driver — automation tools cost $100–$2,000/month; weigh against compliance risk

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

- parent skill: `geek/ux/accessibility-specialist/`
