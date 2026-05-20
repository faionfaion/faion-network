---
slug: solo-change-order-mini-contract
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "8cb92a3d22ee4b24"
summary: One-page change-order template a freelancer emails when the client says "just one more thing" — signed within an hour, billable from that hour, no MSA renegotiation.
---
# Solo Change Order Mini Contract

## Summary

**One-sentence:** A one-page change-order email template that converts "just one more thing" into a signed, dated, priced amendment to the existing engagement — sent and signed within 60 minutes.

**One-paragraph:** Scope management methodologies define the conversation; ops-legal-basics covers the master agreement. Neither bridges the gap of "we are on day 14 of a fixed-bid project and the client just asked for a feature." The freelancer needs a one-page change-order pack: subject line, three-paragraph body, embedded summary table (scope delta, price delta, schedule delta, payment terms), and a "reply YES to authorize" close that is legally sufficient under e-signature norms (E-SIGN, eIDAS) for sub-$10k modifications to an existing signed agreement. Anchored to "Scope-change conversation when client says 'just one more thing'" for the technical freelancer.

## Applies If (ALL must hold)

- An existing signed master agreement / SOW already covers the engagement.
- The new ask is sub-$10k (or sub-MSA threshold) — material enough to bill, small enough to skip full SOW.
- The freelancer operates in a jurisdiction where e-signature ("reply YES") is enforceable for modifications (US E-SIGN, EU eIDAS, UK ECA).
- The client is reachable by email or chat.

## Skip If (ANY kills it)

- No master agreement in place — write a fresh SOW, not a change order.
- New ask is large enough to renegotiate retainer or rate — go full SOW.
- Client is an enterprise procurement org that requires PO + paper signature — follow their process.
- Jurisdiction lacks reliable e-signature enforceability for modifications — escalate to a real signature.

## Prerequisites

- Active master SOW with a change-order clause (or change-order silence, which most jurisdictions interpret permissively).
- Standard rate card or hourly figure to plug into the template.
- Email or chat thread with the client.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context |
| `pro/pm/scope-creep-prevention-on-hourly` if present | Sibling — the conversation context this template ends |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every change-order email enforces | ~900 |

## Related

- parent skill: `pro/pm/`
- triggering activity: `p3-technical-freelancer/Scope-change conversation when client says 'just one more thing'`
- adjacent: `pro/pm/change-request-pricing-rubric`, `pro/marketing/scope-creep-prevention-on-hourly`
