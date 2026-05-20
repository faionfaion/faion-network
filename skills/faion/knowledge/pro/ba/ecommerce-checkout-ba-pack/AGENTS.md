---
slug: ecommerce-checkout-ba-pack
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Payment-method requirements (PCI-DSS scope), VAT rules per jurisdiction, fraud decision tables, cart-abandonment rules, returns flow — the vertical BA pack the corpus is missing.
content_id: "93f70d58f1e94170"
tags: [ecommerce-checkout-ba-pack, ba, pro]
---

# E-commerce Checkout BA Pack

## Summary

**One-sentence:** Payment-method requirements (PCI-DSS scope), VAT rules per jurisdiction, fraud decision tables, cart-abandonment rules, returns flow — the vertical BA pack the corpus is missing.

**One-paragraph:** Most common BA work in outsource is e-commerce. A checkout pack would cover payment requirements, tax / VAT, fraud, cart abandonment, returns. Today the corpus has nothing vertical at all. Output: checkout requirement template + decision tables + regulatory checklist.

## Applies If (ALL must hold)

- BA assigned to an e-commerce project
- scope includes checkout, payments, or fulfillment
- client expects requirements covering ≥1 of: PCI-DSS, VAT, fraud, returns

## Skip If (ANY kills it)

- marketplace project (multi-vendor) — requires marketplace BA pack instead
- B2B procurement portal — different flow; use B2B-procurement BA pack
- purely informational e-commerce (catalog without transactions)

## Prerequisites

- client's payment processor + countries of operation
- list of payment methods supported (cards, wallets, BNPL, bank transfer)
- fraud baseline data (current chargeback rate or estimate)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent skill — provides operating context for this methodology |
| `pro/ba/business-analyst` | peer methodology — produces inputs or consumes outputs |
| `pro/ba/ba-modeling` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/ba/business-analyst/`
- peer methodology: `pro/ba/business-analyst`
- peer methodology: `pro/ba/ba-modeling`
- peer methodology: `pro/sec/data-classification`
- external: https://www.pcisecuritystandards.org/ (PCI-DSS); https://stripe.com/docs/tax (Stripe Tax docs); https://docs.adyen.com/risk-management
