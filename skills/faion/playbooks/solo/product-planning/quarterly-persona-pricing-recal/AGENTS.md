---
slug: quarterly-persona-pricing-recal
tier: solo
group: product-planning
persona: P1
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Drifted ICP and stale pricing → adjusted ICP one-liner + 1 queued price experiment.
content_id: 0da3bd2b4091a08f
methodology_refs:
  - product-analytics
  - market-researcher
  - growth-landing-page-design
  - ops-pricing-strategy
  - ops-subscription-models
  - architecture-decision-records
---

# Quarterly persona and pricing recalibration

**Playbook slug:** `quarterly-persona-pricing-recal`  
**Tier:** solo  
**Complexity:** medium  
**Persona:** P1 — Solo SaaS Builder

## Intent

Drifted ICP and stale pricing → adjusted ICP one-liner + 1 queued price experiment.

## Scope

Solo founder runs a 2-hour quarterly review: paid-cohort signal reviewed, ICP one-liner adjusted, one price experiment queued or rejected, free-to-paid funnel decision recorded. Exit artifact is updated positioning doc + ADR for pricing decision.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Full ICP rewrite — adjustments only at this cadence
- Pricing UI redesign — copy-only edits here

### Prerequisites

- ≥1 quarter of paid-cohort data (Stripe + analytics)
- Existing ICP one-liner

## Success criteria

The playbook is done when:
- Paid-cohort traits reviewed and documented
- ICP one-liner adjusted (or confirmed unchanged with evidence)
- 1 price experiment queued OR rejected with rationale
- Free-to-paid funnel decision recorded in ADR

## Stages

### Stage 1: Review

**Intent:** Look at who actually paid, not who we thought would.

**Tasks:**
- Pull paid-cohort traits from Stripe + analytics
- Compare to current ICP one-liner
- Note delta

**Methodologies in chain:**
- `product-analytics` → `solo/product/product-operations/product-analytics`
- `market-researcher` → `solo/research/market-researcher`

**Outputs:**
- Paid-cohort trait doc

**Decision gate:**
> Advance when traits are documented. Refuse to skip — drift accumulates silently.

### Stage 2: Adjust ICP

**Intent:** Sharper ICP one-liner OR confirm with evidence.

**Tasks:**
- Rewrite ICP one-liner with current traits
- Diff against landing copy
- Ship copy edit if delta is wide

**Methodologies in chain:**
- `growth-landing-page-design` → `solo/marketing/conversion-optimizer/growth-landing-page-design`

**Outputs:**
- Updated ICP one-liner

**Decision gate:**
> Advance when one-liner is honest about current customers. Stay if vague.

### Stage 3: Price

**Intent:** 1 price experiment queued or rejected.

**Tasks:**
- Score candidate experiments (raise / restructure / add tier)
- Pick one OR document reject
- Set success metric + date

**Methodologies in chain:**
- `ops-pricing-strategy` → `solo/marketing/gtm-strategist/ops-pricing-strategy`
- `ops-subscription-models` → `solo/marketing/gtm-strategist/ops-subscription-models`
- `architecture-decision-records` → `solo/sdd/sdd/architecture-decision-records`

**Outputs:**
- Pricing ADR

**Decision gate:**
> Required output: ADR with decision + reasoning. No 'maybe next quarter'.

## Common pitfalls

- Raising prices reflexively because someone on Twitter said 'charge more' — needs cohort evidence
- Holding ICP fixed because rewriting feels like 'admitting we were wrong'

## Quality checklist (self-review)

- Does the ICP one-liner describe my actual top 10 paying customers?
- Is the pricing ADR honest about risk, or does it only list upside?

## Related playbooks

- `pmf-hunt-post-mvp`
- `friday-metrics-mrr-pulse`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **icp-fit-scorecard-solo** (tier `solo`, blocks stage 1) — Review stage needs scorecard to compare actual buyers vs ICP
- **pricing-experiment-runbook** (tier `solo`, blocks stage 3) — Price stage needs runbook for safely experimenting on small revenue base

## CLI usage

```
faion get-content quarterly-persona-pricing-recal --format md       # human-readable rendering
faion get-content quarterly-persona-pricing-recal --format context  # agent-optimised context bundle
faion get-content quarterly-persona-pricing-recal --format json     # raw structured form
```
