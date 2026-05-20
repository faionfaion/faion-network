---
slug: late-invoice-dunning-sequence
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: B2B 30/60/90-day invoice dunning: reminder cadence, escalation script, late-fee trigger, work-stoppage trigger, collections/small-claims gate.
content_id: "c5a6ddedb15680a4"
tags: [late-invoice-dunning-sequence, marketing, pro]
---

# Late-Invoice Dunning Sequence

## Summary

**One-sentence:** B2B 30/60/90-day invoice dunning: reminder cadence, escalation script, late-fee trigger, work-stoppage trigger, collections/small-claims gate.

**One-paragraph:** Payment delays are the #2 pain (freelancer context). solo/launch-operations/payment-flow covers Stripe checkout. Nothing covers B2B invoice dunning. Output: dunning sequence + script templates + escalation triggers.

## Applies If (ALL must hold)

- freelancer or agency on Net-30/Net-60 invoice terms
- ≥1 invoice ≥30 days late OR clear policy needed
- founder/operator has authority to invoke late fees + work stoppage

## Skip If (ANY kills it)

- fully prepaid / retainer-only — different payment model
- single-client situation where dunning risks the relationship — escalate manually
- regulated industry with contractual non-late-fee terms

## Prerequisites

- active contracts with payment terms documented
- invoice aging report
- late-fee clause in contract OR willingness to enforce

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/rate-raise-conversation-script` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/client-firing-protocol` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `pro/marketing/rate-raise-conversation-script`
- peer methodology: `pro/marketing/client-firing-protocol`
- peer methodology: `pro/marketing/freelance-tax-cashflow-basics`
- external: https://www.uscourts.gov/services-forms/forms (US small-claims forms); https://www.gov.uk/make-court-claim-for-money (UK MCOL)
