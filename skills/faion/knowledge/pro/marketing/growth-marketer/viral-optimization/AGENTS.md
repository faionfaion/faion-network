---
slug: viral-optimization
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Viral loop optimization iterates on an existing measured K-factor by decomposing it into its two drivers — i (invites sent per user) and c (invitee conversion rate) — identifying the bottleneck, and running A/B tests on the weakest leg.
content_id: "9144248f45c2f11b"
tags: [viral, k-factor, growth, referral, experimentation]
---
# Viral Loop Optimization

## Summary

**One-sentence:** Viral loop optimization iterates on an existing measured K-factor by decomposing it into its two drivers — i (invites sent per user) and c (invitee conversion rate) — identifying the bottleneck, and running A/B tests on the weakest leg.

**One-paragraph:** Viral loop optimization iterates on an existing measured K-factor by decomposing it into its two drivers — i (invites sent per user) and c (invitee conversion rate) — identifying the bottleneck, and running A/B tests on the weakest leg. Optimize c first (invite landing page) before optimizing i (share moments); every improvement to c multiplies all future loop turns.

## Applies If (ALL must hold)

- Product has a working invite/share path and a measured baseline K (even K = 0.05 is enough to start).
- Full event chain is tracked: invite_shown → invite_sent → invite_clicked → invitee_signup → invitee_active.
- A live A/B test framework is available (no code deploy needed to split variants).
- At least 5,000 weekly users entering the loop (otherwise sample size kills experiments).

## Skip If (ANY kills it)

- Pre-PMF: optimizing K of a product nobody loves yields K = 0.0X times any multiplier — still nothing.
- B2B enterprise where sharing is gated by procurement or security — viral mechanics do not translate.
- Markets with strict anti-spam rules (regulated finance, medical, EU consumer) where contact-import is non-compliant.
- Products where the inviter's value requires the invitee to join but the invitee has no standalone reason — forced virality churns invitees fast.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/marketing/growth-marketer/`
