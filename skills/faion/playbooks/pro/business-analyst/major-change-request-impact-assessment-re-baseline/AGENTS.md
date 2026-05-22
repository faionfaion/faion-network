---
slug: major-change-request-impact-assessment-re-baseline
tier: pro
group: business-analyst
persona: role-ba
goal: govern-decide
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "End-to-end handling of a non-trivial CR mid-project (>15% scope or schedule impact, or breaking a signed baseline). End state — sponsor has costed, traced, validated options to decide; team has a r..."
content_id: 60947d7cc89ba228
methodology_refs:
  - ba-governance
  - requirements-documentation
  - requirements-lifecycle
  - requirements-prioritization
  - requirements-traceability
  - solution-assessment
  - strategy-methods
  - business-process-analysis
  - decision-analysis
  - stakeholder-analysis
  - change-control
  - cost-estimation
  - lessons-learned
  - risk-register
  - schedule-development
  - scope-management
---

# Major change-request impact assessment + re-baseline

**Persona:** role-ba - **Tier:** pro - **Complexity:** medium - **Angle:** global

## Context

End-to-end handling of a non-trivial CR mid-project (>15% scope or schedule impact, or breaking a signed baseline). End state — sponsor has costed, traced, validated options to decide; team has a re-baselined plan or formal rejection memo.

Most operators improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step.

## Outcome

By the final stage, the operator holds a written artifact for every step, every decision-gate passed in writing, and a documented go / no-go (or kill) trail another person can audit without asking a question.

## Steps

### 1. Frame

*Intent:* State the outcome, constraints, and exit-condition in one paragraph.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/ba-governance`
- `pro/ba/ba-core/strategy-methods`
- `pro/pm/pm-traditional/lessons-learned`

Outputs:
- Written artifact for stage 1 (Frame) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 1 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 2. Discover

*Intent:* Pull evidence and prior art before any design decision.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/pm/pm-traditional/risk-register`

Outputs:
- Written artifact for stage 2 (Discover) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 2 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 3. Design

*Intent:* Sketch target structure with explicit cuts and trade-offs.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-lifecycle`
- `pro/ba/ba-modeling/decision-analysis`
- `pro/pm/pm-traditional/schedule-development`

Outputs:
- Written artifact for stage 3 (Design) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 3 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 4. Build

*Intent:* Implement the smallest version that proves the chain works.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/business-analyst/stakeholder-analysis`
- `pro/pm/pm-traditional/scope-management`

Outputs:
- Written artifact for stage 4 (Build) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 4 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 5. Validate

*Intent:* Test against the rubric or real data before broad rollout.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-traceability`
- `pro/pm/pm-traditional/change-control`

Outputs:
- Written artifact for stage 5 (Validate) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 5 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 6. Close

*Intent:* Apply decision gate, document outcome, archive for re-use.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/solution-assessment`
- `pro/pm/pm-traditional/cost-estimation`

Outputs:
- Written artifact for stage 6 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 6 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/ba/ba-core/ba-governance`
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/ba-core/requirements-lifecycle`
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/ba-core/requirements-traceability`
- `pro/ba/ba-core/solution-assessment`
- `pro/ba/ba-core/strategy-methods`
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/ba/ba-modeling/decision-analysis`
- `pro/ba/business-analyst/stakeholder-analysis`
- `pro/pm/pm-traditional/change-control`
- `pro/pm/pm-traditional/cost-estimation`
- `pro/pm/pm-traditional/lessons-learned`
- `pro/pm/pm-traditional/risk-register`
- `pro/pm/pm-traditional/schedule-development`
- `pro/pm/pm-traditional/scope-management`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `ai-cr-impact-suggestion`
- `cr-options-matrix-template`
- `fixed-price-vs-tm-cr-pricing-playbook`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content major-change-request-impact-assessment-re-baseline --format context` to pull the full chain into an agent-readable payload.
