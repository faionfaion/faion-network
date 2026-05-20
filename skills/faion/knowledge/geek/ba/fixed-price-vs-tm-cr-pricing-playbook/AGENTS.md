---
slug: fixed-price-vs-tm-cr-pricing-playbook
tier: geek
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "69d80b50bc7ab429"
summary: "Change-request playbook for P4 outsource BAs at the BA/procurement boundary: classify each CR by contract type (fixed-price vs T&M), apply absorb / negotiate-addendum / scope-swap decisions per category, and price the residual risk explicitly so neither side discovers cost surprises at handover."
tags: [ba, geek, p4-outsource, change-request, fixed-price, tm, pricing]
---
# Fixed-Price vs T&M Change-Request Pricing Playbook

## Summary

Change requests behave radically differently under fixed-price and T&M contracts, and Faion currently has no BA-side methodology bridging change management to commercial structure. Under fixed-price every CR is a margin event and needs an addendum-or-absorb decision rooted in residual contingency; under T&M every CR is a velocity event and needs a re-baseline impact only. This playbook gives the P4 outsource BA a single decision tree that classifies the CR by contract type, then by size, then by risk exposure, and produces one of four actions (absorb, scope-swap, addendum, defer-to-phase-2). It explicitly prices residual risk and keeps the BA / procurement / sponsor handoff legible.

## Applies If

- The engagement is an active outsource contract with a defined commercial structure (fixed-price, T&M, or hybrid).
- A change request has been submitted by client or vendor that materially alters scope, schedule, or cost.
- The BA has read access to the original SOW, the master agreement (MSA), and the running burn-down or hours ledger.
- A named sponsor on each side (client and vendor) is reachable for an addendum decision.

## Skip If

- The change is a clarification of existing scope (no scope delta, no cost delta) — record and move on, no playbook needed.
- The engagement has no fixed scope at all (pure staff augmentation) — CRs do not apply; renegotiate weekly capacity instead.
- The CR is regulator-mandated and must be implemented regardless of price — escalate immediately, not via this playbook.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules covering contract-type classification, size thresholds, residual-risk pricing, the absorb/swap/addendum decision tree, and the cross-boundary handoff to procurement |

## Related

- parent skill: `geek/ba/`
- triggering activity: `Major change-request impact assessment + re-baseline`, `Pre-bid discovery for a fixed-price engagement (P4)`
- neighbouring: `pro/ba/change-request-impact-rubric`, `pro/ba/cr-options-matrix-template`, `geek/ba/fixed-price-risk-loading-model`
