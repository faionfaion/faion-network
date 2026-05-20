---
slug: pm-tools-overview
tier: pro
group: pm
domain: pm-agile
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured framework for selecting the right project management tool based on team size, workflow complexity, compliance requirements, and ecosystem fit.
content_id: "724920c932ffedf7"
tags: [pm-tools, tool-selection, moscow, requirements, adr]
---
# PM Tools Overview

## Summary

**One-sentence:** A structured framework for selecting the right project management tool based on team size, workflow complexity, compliance requirements, and ecosystem fit.

**One-paragraph:** A structured framework for selecting the right project management tool based on team size, workflow complexity, compliance requirements, and ecosystem fit. The core rule: anchor every tool selection to a MoSCoW requirements table grounded in stakeholder evidence, then apply hard constraints (price ceiling, data residency, compliance, IDP) to produce a shortlist of 3-5 candidates before evaluating features.

## Applies If (ALL must hold)

- Starting a new team or project without existing tooling.
- Outgrowing a current PM solution (capacity, compliance, or integrations).
- Consolidating multiple tools across an organization after merger or acquisition.
- Evaluating tools during vendor renewal when pricing model changes.
- Post-acquisition tool standardization requiring a defensible ADR.

## Skip If (ANY kills it)

- Single-team / solo decision with low switching cost — pick by gut, time-box a 2-week trial, ship.
- Switching tools to escape a process or personnel problem — fix the root cause instead.
- A tool already works with no measurable pain — overhead exceeds value.
- Pre-product-market-fit startups — tool-selection theatre distracts from product.
- Decisions already locked by executive preference or vendor relationship — analysis will not change the outcome.

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

- parent skill: `pro/pm/pm-agile/`
