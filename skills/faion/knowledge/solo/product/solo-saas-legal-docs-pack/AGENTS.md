---
slug: solo-saas-legal-docs-pack
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Minimum viable legal-doc pack — ToS, Privacy, refund policy, cookie banner, DPA — a solo SaaS needs in place before charging the first customer.
content_id: "c3de9d8937b69245"
tags: [solo-saas-legal-docs-pack, product, solo]
---
# Solo SaaS Legal Docs Pack

## Summary

**One-sentence:** The five legal documents every solo SaaS needs before processing the first paid charge — ToS, Privacy Policy, Refund Policy, Cookie Banner, basic DPA — with explicit "do not ship without" gates.

**One-paragraph:** Most solo founders improvise legal copy from a Notion template found on Twitter, then run into a Stripe risk-review email or a GDPR complaint within the first 6 months. This methodology fixes the minimum five documents, the canonical sources to base them on (Stripe / Iubenda / Termly / Vanta starter kit), and the gates that block billing activation until they are live. It does not replace a lawyer — it defines what "good enough to bill" looks like for the bootstrap phase.

## Applies If (ALL must hold)

- product is about to start charging real money
- product collects any PII (email at minimum)
- the founder is selling internationally (≥1 EU / UK / California customer expected)
- billing platform (Stripe / Paddle / Lemon Squeezy) requires a public ToS + privacy URL

## Skip If (ANY kills it)

- product is free with no PII and no signups — overhead exceeds risk
- a corporate legal team owns the docs already
- product is sold exclusively B2B with a master agreement per customer
- jurisdiction requires bespoke legal review beyond this pack (medical, financial-services, child-safety)

## Prerequisites

- a public website at a stable URL (legal docs need a permalink)
- a chosen billing platform (the ToS will reference it)
- the founder's legal entity name + jurisdiction of incorporation
- a `legal@` or `support@` contact email that is monitored

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning` | parent skill |
| `solo/product/gdpr-for-solo-saas` | sibling — Privacy Policy must align with the GDPR posture set there |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: five-docs-minimum, no-template-without-edit, billing-gate, jurisdiction-named, monitored-contact | ~1000 |

## Related

- parent skill: `solo/product/product-planning`
- upstream playbook: `p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production`
- sibling: `solo/product/gdpr-for-solo-saas`
