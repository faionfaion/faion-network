---
slug: feature-flag-rollout-decision-v2
tier: pro
group: product-team
persona: p6-product-dev-team
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Tech lead + PM review every open feature flag weekly. For each: keep dark / ramp / GA / kill. Decision criteria are explicit (SLO impact, error rate, adoption metric). Flags that drift out of lifec..."
content_id: 0bb4b899a180709e
methodology_refs:
  - release-planning
  - feature-flags-core-implementation
  - feature-flags-rollout-targeting
  - feature-flags-services-testing
  - feature-flags-types-lifecycle
  - trunk-based-feature-flags
  - quality-gates-confidence
---

# Feature flag rollout decision (weekly)

## Context

Tech lead + PM review every open feature flag weekly. For each: keep dark / ramp / GA / kill. Decision criteria are explicit (SLO impact, error rate, adoption metric). Flags that drift out of lifecycle get auto-flagged for deletion.

## Outcome

By the end of this playbook, the operator has run the 3 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 3 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Score Active Flags

Get the flag inventory current.

Tasks:
- List every flag, owner, age, and current rollout %
- Tag each flag: ramping, in-test, stuck, decommission-ready
- Flag any flag older than the kill-threshold

Outputs:
- flag inventory table
- tags per flag
- kill-threshold list

Decision gate: Advance only when every active flag has a tag and an owner.

### 2. Decide per Flag

Ramp, hold, kill — pick one.

Tasks:
- For each flag: ramp +X% / hold / roll back / decommission
- Verify the decision against business and ops dashboards
- Communicate the per-flag decision to owners

Outputs:
- per-flag decision
- dashboard checks
- owner comms

Decision gate: Advance only when every flag has a written decision this week.

### 3. Execute

Touch the flags, not just the doc.

Tasks:
- Apply each flag decision in the platform
- Watch dashboards for 1 hour after any ramp ≥10%
- Pause or revert on threshold breach

Outputs:
- flag-config diff
- dashboard watch log
- pause/revert log

Decision gate: Required output: a logged execution per decision.

## Decision points

- Stage 1 (Score Active Flags): Advance only when every active flag has a tag and an owner.
- Stage 2 (Decide per Flag): Advance only when every flag has a written decision this week.
- Stage 3 (Execute): Required output: a logged execution per decision.

## References

- `release-planning`
- `feature-flags-core-implementation`
- `feature-flags-rollout-targeting`
- `feature-flags-services-testing`
- `feature-flags-types-lifecycle`
- `trunk-based-feature-flags`
- `quality-gates-confidence`

Gaps (status: draft until empty):
- `feature-flag-weekly-review-template` (see `gaps[]` in `playbook.yaml`)
- `flag-killswitch-decision-criteria` (see `gaps[]` in `playbook.yaml`)
