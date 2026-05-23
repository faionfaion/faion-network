# Subscription Models

## Summary

**One-sentence:** Generates a subscription-business spec: model type (SaaS / membership / replenishment / curation), tier design with strategic feature gating, MRR / churn / LTV instrumentation, dunning automation, and full lifecycle policy (trial → win-back).

**One-paragraph:** Subscription Models produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder building or repricing a subscription business who needs a spec covering model type, tier feature gating, MRR/churn/LTV instrumentation, dunning, and lifecycle policy — before churn silently eats growth.

## Applies If (ALL must hold)

- Recurring revenue is the intended monetisation
- Billing platform supports automatic renewals + dunning (Stripe, LemonSqueezy, Paddle)
- Founder commits to monthly MRR/churn/LTV review

## Skip If (ANY kills it)

- One-time purchase product — different model entirely
- Donation-funded or grant-funded — different governance
- Marketplace with seller-set subscriptions — out of scope

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Model intent (SaaS / membership / replenishment / curation) | doc | founder brief |
| Feature inventory + cost-to-deliver per feature | table | product + infra |
| Billing platform credentials | creds | Stripe / LS / Paddle |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `ops-pricing-strategy` | Pricing baseline drives tier shape. |
| `ops-financial-planning` | MRR + churn feed runway projection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-model-declared-upfront, r2-tier-feature-strategic, r3-mrr-churn-ltv-instrumented, r4-dunning-automation-on, r5-lifecycle-policy-trial-to-winback, r6-grandfather-on-tier-change | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ops-subscription-models` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-ops-subscription-models` | haiku | Schema check + threshold checks; deterministic. |
| `review-ops-subscription-models` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-subscription-models.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ops-subscription-models.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-subscription-models.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[ops-pricing-strategy]]
- [[ops-financial-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
