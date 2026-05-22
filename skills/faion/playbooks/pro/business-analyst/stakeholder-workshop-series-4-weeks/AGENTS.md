---
slug: stakeholder-workshop-series-4-weeks
tier: pro
group: business-analyst
persona: role-ba
goal: discover-validate
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Plan, run, and harvest a structured series of 4–6 workshops that converges contradictory stakeholders on a shared mental model, decisions log, and committed scope. End state — sponsor has a single...
content_id: fbb84f72d7c7a1f0
methodology_refs:
  - ba-governance
  - elicitation-techniques
  - requirements-documentation
  - requirements-prioritization
  - requirements-validation
  - stakeholder-analysis
  - business-process-analysis
  - user-story-mapping
  - methodologies-detail
  - strategy-analysis-future-state
  - stakeholder-engagement
  - stakeholder-engagement-advanced
---

# Stakeholder workshop series (4 weeks)

**Persona:** role-ba - **Tier:** pro - **Complexity:** deep - **Angle:** global

## Context

Plan, run, and harvest a structured series of 4–6 workshops that converges contradictory stakeholders on a shared mental model, decisions log, and committed scope. End state — sponsor has a single source of truth document of decisions made and parking-lotted topics.

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
- `pro/ba/ba-modeling/user-story-mapping`

Outputs:
- Written artifact for stage 1 (Frame) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 1 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 2. Discover

*Intent:* Pull the evidence and prior art needed to make informed choices.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/elicitation-techniques`
- `pro/ba/business-analyst/elicitation-techniques`

Outputs:
- Written artifact for stage 2 (Discover) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 2 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 3. Design

*Intent:* Sketch the target system / process / artifact before touching anything live.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/business-analyst/methodologies-detail`

Outputs:
- Written artifact for stage 3 (Design) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 3 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 4. Build

*Intent:* Implement the smallest version that exercises the validated chain end-to-end.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/business-analyst/stakeholder-analysis`

Outputs:
- Written artifact for stage 4 (Build) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 4 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 5. Validate

*Intent:* Stress-test against the rubric, real users / data, or eval harness.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-validation`
- `pro/ba/business-analyst/strategy-analysis-future-state`

Outputs:
- Written artifact for stage 5 (Validate) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 5 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 6. Ship

*Intent:* Roll out to the target audience with rollback path and observability.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/stakeholder-analysis`
- `pro/pm/pm-traditional/stakeholder-engagement`

Outputs:
- Written artifact for stage 6 (Ship) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 6 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 7. Close

*Intent:* Decide go/no-go, write the postmortem, and archive artifacts for re-use.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/pm/pm-traditional/stakeholder-engagement-advanced`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/ba/ba-core/ba-governance`
- `pro/ba/ba-core/elicitation-techniques`
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/ba-core/requirements-validation`
- `pro/ba/ba-core/stakeholder-analysis`
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/ba/ba-modeling/user-story-mapping`
- `pro/ba/business-analyst/elicitation-techniques`
- `pro/ba/business-analyst/methodologies-detail`
- `pro/ba/business-analyst/stakeholder-analysis`
- `pro/ba/business-analyst/strategy-analysis-future-state`
- `pro/pm/pm-traditional/stakeholder-engagement`
- `pro/pm/pm-traditional/stakeholder-engagement-advanced`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `decision-options-memo-template`
- `facilitation-anti-patterns`
- `remote-workshop-toolkit`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content stakeholder-workshop-series-4-weeks --format context` to pull the full chain into an agent-readable payload.
