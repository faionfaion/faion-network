---
slug: scope-creep-prevention-on-hourly
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Hourly-specific countermeasure: explicit weekly-budget gate, billable-vs-non-billable taxonomy, async approval-before-work rule.
content_id: "01bcacf917923580"
tags: [scope-creep-prevention-on-hourly, marketing, pro]
---

# Scope Creep Prevention on Hourly Engagements

## Summary

**One-sentence:** Hourly-specific countermeasure: explicit weekly-budget gate, billable-vs-non-billable taxonomy, async approval-before-work rule.

**One-paragraph:** Existing pro/client-engagement/scope-creep-management is fixed-price-shaped (change-request → SOW addendum). On hourly engagements, scope creep manifests as 'just one more thing' that bleeds time. Output: weekly budget gate + billable taxonomy + approval rules.

## Applies If (ALL must hold)

- freelancer on hourly retainer or hourly billable
- weekly billable hours target (e.g., 20-40h)
- scope creep observed (actual hours > target OR fluctuating)

## Skip If (ANY kills it)

- fixed-fee engagements (different scope-creep dynamics)
- no weekly cadence (e.g., monthly only)
- single-client + healthy margin — over-engineered

## Prerequisites

- current contract with hourly rate + cap
- time-tracking discipline
- client comms cadence (Slack, email)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/late-invoice-dunning-sequence` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/rate-raise-conversation-script` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/late-invoice-dunning-sequence`
- peer methodology: `pro/marketing/rate-raise-conversation-script`
- peer methodology: `pro/client-engagement/scope-creep-management`
- external: https://www.freelancersunion.org/resources/contract-templates/; https://philipmorganconsulting.com/scope-creep/
