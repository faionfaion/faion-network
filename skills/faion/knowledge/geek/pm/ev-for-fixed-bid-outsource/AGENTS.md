---
slug: ev-for-fixed-bid-outsource
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Earned Value variant for fixed-bid outsourcing where revenue is locked but vendor margin tracks against PV/EV/AC at the work-package level — the EVM flavour PMBoK does not document.
content_id: 131234452e0c70b6
---

# EV for Fixed-Bid Outsource

## Summary

Generic EVM assumes cost and budget belong to the same organisation. Fixed-bid outsourcing breaks that: revenue is locked to the client at signature, so client-facing CV and CPI become meaningless, but the vendor's internal margin depends on labour AC tracking against a hidden PV. P4 outsource PMs need an EVM variant that runs two parallel ledgers — client-facing scope-completion (EV vs scoped value) and vendor-facing margin (AC vs internal PV) — with explicit conversion rules at change-request boundaries. This methodology defines the variant: ledger structure, work-package granularity, change-request handling, and the three early-warning metrics that flag a margin-burn before it hits the close-out review.

## Applies If

- Engagement is fixed-bid or fixed-bid+T&M-overlay (not pure T&M).
- The vendor PM owns internal labour cost tracking with at least week-grain resolution.
- Work breakdown into work packages (≥5) is feasible and stable.
- A change-request mechanism exists in the contract.

## Skip If

- Pure T&M engagements — generic EVM suffices because revenue tracks effort.
- Engagements <6 weeks or <$50k — EVM overhead exceeds signal value.

## Content
See `content/01-core-rules.xml`.

## Related
- [[fixed-price-vs-tnm-decision-framework]]
- [[change-request-pricing-rubric]]
- [[portfolio-evm-rollup-method]]
- [[tm-to-fp-conversion-playbook]]
