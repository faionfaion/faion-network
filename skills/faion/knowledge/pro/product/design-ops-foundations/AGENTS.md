---
slug: design-ops-foundations
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Rituals, tooling stack, design-team capacity model for the missing 'design-ops' sibling of marketing-ops and dev-ops.
content_id: "6ffc908737f4d610"
tags: [design-ops-foundations, product, pro]
---

# Design Ops Foundations

## Summary

**One-sentence:** Rituals, tooling stack, design-team capacity model for the missing 'design-ops' sibling of marketing-ops and dev-ops.

**One-paragraph:** Design Ops is a real industry sub-discipline (NN/g, DesignOps Assembly). Corpus has marketing-ops and dev-ops siblings but no design-ops methodology covering rituals, tooling stack, design-team capacity model. Output: ritual calendar + tool inventory + capacity model + critique cadence.

## Applies If (ALL must hold)

- design team ≥3 people OR 1 design lead + 2+ engineers consuming design
- design assets serve ≥2 surfaces (web + mobile, or product + marketing)
- design lead has authority to set rituals + standardize tooling

## Skip If (ANY kills it)

- solo designer — use solo/ux/ui-designer instead
- design fully outsourced — different governance
- ad-hoc team with no continuity — establish design hiring first

## Prerequisites

- list of current tools (Figma, FigJam, Linear, Notion, etc.) with seat counts
- weekly design throughput (designs shipped or PRs reviewed)
- named design lead

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/ux/ux-ui-designer` | peer methodology — produces inputs or consumes outputs |
| `pro/pm/pm-agile` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/product/product-manager/`
- peer methodology: `pro/ux/ux-ui-designer`
- peer methodology: `pro/pm/pm-agile`
- external: https://www.nngroup.com/articles/design-ops-101/ (NN/g DesignOps 101); https://designopsassembly.com/
