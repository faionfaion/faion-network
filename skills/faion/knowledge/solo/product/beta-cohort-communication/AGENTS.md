---
slug: beta-cohort-communication
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Templated weekly/biweekly broadcast + targeted-feedback flow to keep beta cohorts engaged from recruit through graduation.
content_id: "8568a51f42df0751"
tags: [beta-cohort-communication, product, solo]
---

# Beta Cohort Communication Cadence

## Summary

**One-sentence:** Templated weekly/biweekly broadcast + targeted-feedback flow to keep beta cohorts engaged from recruit through graduation.

**One-paragraph:** Beta cohorts churn without a comms cadence; PMs need a structured weekly/biweekly broadcast + targeted feedback flow with graduation criteria + alumni program. faion has product-launch and feedback-management but not the beta-specific muscle. Output: cadence calendar + broadcast template + graduation criteria + alumni plan.

## Applies If (ALL must hold)

- beta program with ≥10 enrolled users
- ≥4 weeks of beta runtime ahead
- PM has authority to set cadence + reach users directly

## Skip If (ANY kills it)

- alpha (≤10 internal) — too small for cadence
- open public beta with no enrollment — no cohort to communicate with
- users on NDA-only access — comms must follow NDA constraints (use enterprise patterns)

## Prerequisites

- list of enrolled beta users with consent to receive comms
- feedback channel (form, Loom thread, Slack)
- PM availability ≥2h/week for cohort comms

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning` | parent skill — provides operating context for this methodology |
| `solo/product/product-launch` | peer methodology — produces inputs or consumes outputs |
| `solo/research/feedback-management` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/product/product-planning/`
- peer methodology: `solo/product/product-launch`
- peer methodology: `solo/research/feedback-management`
- external: https://www.lennyrachitsky.com/p/beta-program-best-practices (Lenny Rachitsky)
