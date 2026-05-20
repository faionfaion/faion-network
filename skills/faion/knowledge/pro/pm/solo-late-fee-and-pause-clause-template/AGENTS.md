---
slug: solo-late-fee-and-pause-clause-template
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Boilerplate contract clauses — late-fee schedule, work-pause right, re-engagement terms — that a freelancer can drop into a SOW or master agreement.
content_id: "ae34fe13d0863d3a"
tags: [solo-late-fee-and-pause-clause-template, pm, pro]
---
# Solo Late-Fee & Pause-Clause Template

## Summary

**One-sentence:** Drop-in contract language for late-fee escalation, work-pause rights, and paid re-engagement so a freelancer is not improvising terms during a dispute.

**One-paragraph:** Existing legal-compliance methodologies stop at "send an invoice and chase it". When the client goes 14, 30, 60 days past due, the freelancer has no contractual lever and ends up negotiating from zero. This methodology supplies the actual clause text — 1.5% per month late fee, automatic right to pause work after 14 days unpaid, paid re-engagement fee on resumption — in a form that pastes into a SOW. Tier `pro` because solo SaaS founders rarely need it; freelancers and consultancies need it on every engagement.

## Applies If (ALL must hold)

- the operator sells services on T&M or fixed-price contract (not subscription)
- engagements run 4+ weeks (long enough for an invoice to age)
- there is an existing SOW or MSA the clause can attach to
- jurisdiction allows late fees (most do, with rate caps)

## Skip If (ANY kills it)

- product is SaaS / subscription — billing is automated, no late-fee mechanic needed
- engagement is < 2 weeks and pre-paid — overhead exceeds risk
- jurisdiction prohibits late fees outright (some EU consumer contexts) — defer to legal
- a corporate procurement contract is in place — their paper, their terms

## Prerequisites

- a base SOW or MSA template the clause attaches to
- one-pass review by a local lawyer for the operator's jurisdiction (template is starting point, not legal advice)
- knowledge of the client's payment-terms baseline (Net 14 vs Net 30 vs Net 60)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent skill — engagement contract context |
| `pro/marketing/late-invoice-dunning-sequence` | sibling — what to send before invoking pause clause |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: clause-in-sow-not-email, late-fee-tiered, pause-after-14-days, re-engagement-fee, jurisdiction-review | ~1000 |

## Related

- parent skill: `pro/pm/project-manager`
- upstream playbook: `p3-technical-freelancer/Invoice send + chase-up`
- sibling: `pro/marketing/late-invoice-dunning-sequence`
