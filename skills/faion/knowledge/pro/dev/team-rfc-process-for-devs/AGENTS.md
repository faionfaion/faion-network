---
slug: team-rfc-process-for-devs
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Dev-scope RFC template + lifecycle (draft → review → accepted/rejected → archived) for P6 product-team devs.
content_id: "189de7c1e70bccab"
tags: [team-rfc-process-for-devs, dev, pro]
---

# Team RFC Process for Devs

## Summary

**One-sentence:** Dev-scope RFC template + lifecycle (draft → review → accepted/rejected → archived) for P6 product-team devs.

**One-paragraph:** P6 product-team devs are expected to propose changes via RFC/ADR but only architecture-decision-records exists (architect-tier). Need a dev-scope RFC template + lifecycle. Output: template + lifecycle + review SLA.

## Applies If (ALL must hold)

- dev team ≥4 with shared codebase
- team uses PR-based review
- decisions exist that need pre-PR consensus

## Skip If (ANY kills it)

- team uses ADRs only (architect-tier) and that's sufficient
- single-tech-lead team (decisions flow from lead)
- team has formal RFC process already (e.g., Rust-style)

## Prerequisites

- shared doc store (repo /rfcs/, Outline, Notion)
- review SLA (e.g., 5 business days)
- named editor or rotation

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems` | parent skill — provides operating context for this methodology |
| `solo/dev/architecture-decision-records` | peer methodology — produces inputs or consumes outputs |
| `pro/sdd/internal-rfc-template` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/dev/backend-systems/`
- peer methodology: `solo/dev/architecture-decision-records`
- peer methodology: `pro/sdd/internal-rfc-template`
- peer methodology: `pro/dev/software-developer`
- external: https://github.com/rust-lang/rfcs/blob/master/text/0002-rfc-process.md (Rust); https://oxide.computer/blog/rfd-1-requests-for-discussion (Oxide RFD)
