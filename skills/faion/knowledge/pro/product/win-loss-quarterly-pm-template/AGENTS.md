---
slug: win-loss-quarterly-pm-template
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Quarterly synthesis stitching CRM data + interviews + competitive notes — the integrated artefact P6 PMs own.
content_id: "e40b5ac0f34ba324"
tags: [win-loss-quarterly-pm-template, product, pro]
---

# Win-Loss Quarterly PM Template

## Summary

**One-sentence:** Quarterly synthesis stitching CRM data + interviews + competitive notes — the integrated artefact P6 PMs own.

**One-paragraph:** Pro PMs in P6 product teams own quarterly win-loss; no current methodology stitches CRM + interviews + competitive into one. Output: quarterly template + stitching protocol + roadmap-feeding decisions.

## Applies If (ALL must hold)

- PM owns win-loss in a B2B SaaS product
- CRM data available + interview pipeline running
- team has competitive-intel function (formal or informal)

## Skip If (ANY kills it)

- PLG self-serve with no sales motion (different process)
- interview program not yet established (use win-loss-interview-program first)
- single-rep startup where PM is rep (conflict of interest; use external interviewer)

## Prerequisites

- CRM with stage / loss-reason fields populated
- ≥10 win-loss interviews per quarter
- competitive intelligence source

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/research/win-loss-interview-program` | peer methodology — produces inputs or consumes outputs |
| `pro/product/product-manager` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `pro/research/win-loss-interview-program`
- peer methodology: `pro/product/product-manager`
- peer methodology: `pro/marketing/conversion-optimizer`
- external: https://primaryintelligence.com/; https://www.lennyrachitsky.com/p/win-loss-analysis
