---
slug: solo-freelancer-contract-clauses
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "72775de410d042f8"
summary: Lean contract clause pack for solo freelancers — IP-on-payment, late-fee with auto-stop-work, kill fee, mutual NDA, freelancer-jurisdiction default — no MSA pre-requirement.
---
# Solo Freelancer Contract Clauses

## Summary

**One-sentence:** Clause pack designed for a single technical freelancer signing direct contracts with mid-sized clients, replacing the standard $40k web-build SOW boilerplate with five lean, defensible provisions.

**One-paragraph:** `statement-of-work` covers a heavy SOW between two LLCs. SaaS-side ops-legal-basics covers ToS / Privacy. Solo freelancers landing $5–30k projects need neither — they need a small, opinionated clause pack: (1) IP assignment-on-PAID, not on-signed (the single most important inversion); (2) late-fee with automatic stop-work after N days unpaid; (3) kill fee for client-initiated termination (typically 30% of remaining); (4) mutual NDA scoped to the engagement; (5) jurisdiction defaulted to the freelancer's country with arbitration carve-out. The pack is meant to slot into an otherwise-simple email-signed agreement, with no MSA prereq. Anchored to "Inbound-to-signed-retainer in one client cycle" for the technical freelancer.

## Applies If (ALL must hold)

- Solo technical freelancer (one human, no employees, may have subcontractors).
- Client engagement is B2B services, sub-$30k initial project value.
- Freelancer wants to ship a signed agreement without a $2k lawyer review per deal.
- Local jurisdiction recognizes electronic signatures for service agreements.

## Skip If (ANY kills it)

- Engagement is with a regulated industry that mandates specific clauses (gov, healthcare, defense) — escalate to counsel.
- Client is an enterprise procurement org that pushes their MSA — negotiate within their MSA, not against it.
- Cross-border with hostile jurisdiction risk (sanctions-list, no treaty) — escalate to counsel.

## Prerequisites

- Freelancer's company / sole-trader registration in place.
- A baseline service-agreement document (one page) into which the clauses slot.
- A payment processor that supports invoicing with explicit due-dates (Stripe, Wise, etc.).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | Parent group context |
| `pro/marketing/freelance-tax-cashflow-basics` if present | Sibling — the operational side of the contract |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every clause-pack instance enforces | ~950 |

## Related

- parent skill: `pro/marketing/`
- triggering activity: `p3-technical-freelancer/Inbound-to-signed-retainer in one client cycle`
- adjacent: `pro/pm/solo-change-order-mini-contract`, `pro/marketing/late-invoice-dunning-sequence`
