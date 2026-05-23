# Solo-Scale Affiliate Program

## Summary

**One-sentence:** Generates an affiliate program spec sized for solopreneurs — platform choice, payout rules, fraud guardrails, refund policy, attribution window — using Lemon Squeezy / Gumroad / Stripe / Rewardful built-ins.

**One-paragraph:** Solo-Scale Affiliate Program produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder with ≥$5K MRR who needs an affiliate channel set up via built-in platform tools (not custom code) with payout + fraud + refund rules pinned before the first dispute.

## Applies If (ALL must hold)

- Product has ≥$5K MRR or ≥100 paid customers (signal to monetise referrals)
- Billing on a platform with built-in affiliate (Lemon Squeezy / Gumroad / Stripe + Rewardful)
- Founder has bandwidth to onboard + monitor ≤20 affiliates initially

## Skip If (ANY kills it)

- <$5K MRR — referrals will not move the needle yet
- Custom billing without affiliate hooks — different methodology (build vs buy)
- B2B enterprise sale handled via partners — different programme

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pricing + margin model | spec | billing |
| Refund policy (days, conditions) | doc | ToS |
| Affiliate platform choice | service | lemonsqueezy|gumroad|rewardful |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `ops-pricing-strategy` | Margin floor determines affordable commission. |
| `ops-customer-support` | Refunds drive clawbacks; align policies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-platform-builtin-only, r2-commission-leq-margin, r3-cookie-window-30-90-days, r4-fraud-rules-up-front, r5-named-owner-and-cap, r6-refund-clawback-policy | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-affiliate-program-solo` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-affiliate-program-solo` | haiku | Schema check + threshold checks; deterministic. |
| `review-affiliate-program-solo` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/affiliate-program-solo.json` | JSON skeleton conforming to the output contract schema. |
| `templates/affiliate-program-solo.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-affiliate-program-solo.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[ops-pricing-strategy]]
- [[ops-customer-support]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
