---
slug: pricing-experiment-hypothesis-to-result
tier: pro
group: role-product-manager
persona: role-product-manager
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Run a controlled pricing or packaging test from hypothesis through experiment design, segment selection, rollout, measurement, and a packaging decision the business can act on.
content_id: cba18a4cca93842f
methodology_refs:
  - competitive-positioning
  - experimentation-at-scale
  - stakeholder-management
  - competitive-intelligence-methods
  - audience-segmentation
  - survey-design
  - ops-pricing-strategy
  - ops-subscription-models
  - okr-setting
  - product-analytics
  - release-planning
  - pricing-research
  - success-metrics-definition
  - user-interviews
---

# Pricing experiment, hypothesis to result

## Context

Run a controlled pricing or packaging test from hypothesis through experiment design, segment selection, rollout, measurement, and a packaging decision the business can act on.

Tier: **pro**. Complexity: **deep**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Written hypothesis with numeric prediction.
- Pre-registered experiment design + stop rule.
- Honest read of the result (confirm / refute / inconclusive).
- Packaging decision doc the business can act on.

## Steps

### 1. Hypothesis

Frame the pricing or packaging question the experiment must answer.

Tasks:
- Write a one-sentence pricing hypothesis with expected lift.
- Identify the segment whose behaviour the experiment will move.
- Define the primary metric and a tripwire metric.

Outputs:
- Hypothesis doc with primary + tripwire metrics.
- Named segment + sample-size estimate.

Decision gate: Advance when the hypothesis has a numeric prediction and a single primary metric.

### 2. Design

Convert the hypothesis into a runnable experiment.

Tasks:
- Choose experiment type (A/B, holdout, sequential, willingness-to-pay survey).
- Lock variants and exposure rules.
- Pre-register stopping criteria.

Outputs:
- Experiment design doc.
- Pre-registered stop rule.

Decision gate: Advance when design is reviewable by a non-PM stakeholder and the stop rule is unambiguous.

### 3. Segment selection

Pick the audience cohort that will receive the variant.

Tasks:
- Pull cohort definitions from analytics.
- Validate the cohort can be reached by billing tooling.
- Confirm cohort exclusions for compliance / contracts.

Outputs:
- Cohort ID + size.
- Exclusion rationale.

Decision gate: Advance when the cohort is reachable in production with the engineering team's confirmation.

### 4. Rollout

Ship the variant with reversible controls.

Tasks:
- Coordinate billing + entitlement changes with engineering.
- Wire instrumentation against the primary metric.
- Run a smoke test on a tiny exposure first.

Outputs:
- Live experiment with reversible plumbing.
- Smoke-test report.

Decision gate: Advance when smoke test confirms instrumentation fires correctly and rollback was rehearsed.

### 5. Measurement

Read the experiment honestly.

Tasks:
- Wait the pre-registered duration before peeking.
- Run the analysis exactly as pre-registered.
- Surface practical significance, not only statistical.

Outputs:
- Analysis doc with confidence interval.
- Practical-significance verdict.

Decision gate: Advance when the verdict is one of {confirm, refute, inconclusive} backed by the pre-registered analysis.

### 6. Decision

Convert the result into a packaging decision.

Tasks:
- Document the packaging change (or no-change).
- Sequence the rollout schedule for affected accounts.
- Brief sales + support before broad rollout.

Outputs:
- Packaging decision doc.
- Rollout schedule.

Decision gate: Required: a written packaging decision the business can ship.

## Decision points

- Sequential test vs classic A/B — pick sequential when traffic is tight, A/B when segment is large.
- Practical vs statistical significance — a tiny lift across millions is real; a 30% lift on 50 users is not.
- Refute vs inconclusive — distinguish 'we proved no lift' from 'we have no signal yet'.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/product/product-manager/competitive-positioning`
- `pro/product/product-operations/experimentation-at-scale`
- `pro/product/product-operations/stakeholder-management`
- `pro/research/market-researcher/competitive-intelligence-methods`
- `pro/research/researcher/audience-segmentation`
- `pro/research/researcher/survey-design`
- `solo/marketing/gtm-strategist/ops-pricing-strategy`
- `solo/marketing/gtm-strategist/ops-subscription-models`
- `solo/product/product-manager/okr-setting`
- `solo/product/product-operations/product-analytics`
- `solo/product/product-planning/release-planning`
- `solo/research/market-researcher/pricing-research`
- `solo/research/researcher/success-metrics-definition`
- `solo/research/researcher/user-interviews`
