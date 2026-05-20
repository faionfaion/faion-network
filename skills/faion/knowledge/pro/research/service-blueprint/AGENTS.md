---
slug: service-blueprint
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Service-blueprint methodology extending solo journey-mapping with back-stage operations, support systems, and line-of-visibility for B2B and ops-dependent UX work."
content_id: "72022f7f190f51c4"
tags: [service-blueprint, research, pro]
---
# Service Blueprint

## Summary

**One-sentence:** Extends a customer journey map with back-stage actors, support systems, and the line-of-visibility, producing a single artefact that ties UX friction to operational root causes.

**One-paragraph:** Journey-mapping is in the solo tier; the back-stage / service-blueprint extension is what enterprise UX, B2B, and P6 product-team work needs to ship. A journey map tells you "the user gets frustrated here"; a service blueprint tells you "the user gets frustrated here BECAUSE the support agent has no view into the billing system." This methodology defines the canonical 5-swimlane blueprint (customer actions, frontstage interactions, line of visibility, backstage actions, support processes/systems), the failure-point notation, and the moment-of-truth scoring. Output is a single-page blueprint that engineering, ops, and design can all act on.

## Applies If (ALL must hold)

- you already have a customer journey map (or are creating one as input)
- the product involves backstage actors (ops, support, fulfillment, finance) the user doesn't see
- the goal is to reduce friction by changing back-stage processes, not just UI
- tier == pro or higher

## Skip If (ANY kills it)

- the product is pure self-serve software with no back-stage human involvement
- a service blueprint already exists < 6 months old for the same journey
- regulatory constraint mandates a different blueprint template (defer to that template)

## Prerequisites

- a journey map covering the target experience
- access to back-stage actors for interviews (support, ops, finance, success)
- a list of internal systems touched by the back-stage actors

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent role/operating context |
| `pro/research/jtbd-switch-interview` | input frame for the customer-side narrative |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable blueprint rules + 1 worked friction example | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_backstage_actors` | sonnet | interview synthesis |
| `map_systems_per_step` | sonnet | enumerate systems per journey step |
| `score_moments_of_truth` | sonnet | bounded scoring against frustration / drop-off |

## Related

- parent skill: `pro/research/`
- `pro/research/researcher`
- upstream playbook: `role-ux-ui-designer/Journey-map-driven attack: from friction map to ranked design-backlog`
