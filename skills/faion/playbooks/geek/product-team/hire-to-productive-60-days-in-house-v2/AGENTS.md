---
slug: hire-to-productive-60-days-in-house-v2
tier: geek
group: product-team
persona: p6-product-dev-team
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Posting -> sourcing -> structured interview -> offer -> 30/60-day onboarding tuned for in-house product context (not agency client engagement). Output: new hire shipping their first owned feature b..."
content_id: 213e477d15fe09f1
methodology_refs:
  - onboarding-30-day
  - onboarding-60-90-day
  - structured-interview-design
---

# Hire-to-productive in 60 days for in-house product roles

## Context

Posting -> sourcing -> structured interview -> offer -> 30/60-day onboarding tuned for in-house product context (not agency client engagement). Output: new hire shipping their first owned feature by day 45

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Hire Right

60 days starts at offer, not start date.

Tasks:
- Run the hiring loop to a calibrated yes/no
- Sign offer with start date and first-30 plan attached
- Pre-stage access and dev env before day 1

Outputs:
- scored loop
- signed offer + 30-day plan
- day-1 access ready

Decision gate: Advance only when day-1 access and plan are pre-staged.

### 2. Days 1-15 — Land

Belonging, orientation, first shipped work.

Tasks:
- Day 1-3: intros, comms norms, mission, dev env
- Day 4-10: pair on one real piece of work, ship first PR
- Day 11-15: own first small ticket end-to-end

Outputs:
- onboarding checklist done
- first PR merged
- first small ticket shipped

Decision gate: Advance only when first ticket has shipped to prod.

### 3. Days 16-45 — Expand

Own scope; meet most of the surface area.

Tasks:
- Take on 3-4 tickets of growing complexity
- Lead 1 small initiative end-to-end
- Embed in standups, retros, and reviews

Outputs:
- tickets shipped
- owned initiative
- ceremony participation

Decision gate: Advance only when initiative ships and feedback signal is positive.

### 4. Days 46-60 — Productive

On the bar; review and commit.

Tasks:
- Run the 60-day check with manager + peer feedback
- Score against the role rubric on day 60
- Decide: keep on bar / extend ramp / part ways

Outputs:
- 60-day check notes
- scored rubric
- keep/extend/part decision

Decision gate: Required output: a written 60-day decision in HR records.

## Decision points

- Stage 1 (Hire Right): Advance only when day-1 access and plan are pre-staged.
- Stage 2 (Days 1-15 — Land): Advance only when first ticket has shipped to prod.
- Stage 3 (Days 16-45 — Expand): Advance only when initiative ships and feedback signal is positive.
- Stage 4 (Days 46-60 — Productive): Required output: a written 60-day decision in HR records.

## References

- `onboarding-30-day`
- `onboarding-60-90-day`
- `structured-interview-design`

Gaps (status: draft until empty):
- `role-specific-interview-rubrics` (see `gaps[]` in `playbook.yaml`)
- `in-house-take-home-design` (see `gaps[]` in `playbook.yaml`)
- `in-house-onboarding-playbook` (see `gaps[]` in `playbook.yaml`)
- `codebase-orientation-tour-template` (see `gaps[]` in `playbook.yaml`)
