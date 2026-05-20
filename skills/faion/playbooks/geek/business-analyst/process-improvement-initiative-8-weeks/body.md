# Process improvement initiative (8 weeks)

**Persona:** role-ba - **Tier:** geek - **Complexity:** deep - **Angle:** global

## Context

BA-led continuous improvement programme on an existing internal or client process: measure baseline, design future state, pilot, roll out, lock in benefits. End state — measurable KPI shift with sustained governance after BA leaves.

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
- `pro/ba/ba-modeling/data-analysis`
- `pro/ba/business-analyst/strategy-analysis-future-state`

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
- `pro/ba/ba-core/data-driven-requirements`
- `pro/ba/ba-modeling/decision-analysis`
- `pro/ba/business-analyst/strategy-analysis-gap-analysis`

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
- `pro/ba/ba-core/process-mining-automation`
- `pro/ba/ba-modeling/interface-analysis`
- `pro/pm/pm-agile/value-stream-management`

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
- `pro/ba/business-analyst/process-mining-automation`
- `pro/pm/pm-traditional/benefits-realization`

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
- `pro/ba/ba-core/solution-assessment`
- `pro/ba/business-analyst/strategy-analysis-business-need`
- `pro/pm/pm-traditional/lessons-learned`

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
- `pro/ba/ba-modeling/acceptance-criteria`
- `pro/ba/business-analyst/strategy-analysis-change-strategy`

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
- `pro/ba/business-analyst/strategy-analysis-current-state`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/ba/ba-core/ba-governance`
- `pro/ba/ba-core/data-driven-requirements`
- `pro/ba/ba-core/process-mining-automation`
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/ba-core/solution-assessment`
- `pro/ba/ba-modeling/acceptance-criteria`
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/ba/ba-modeling/data-analysis`
- `pro/ba/ba-modeling/decision-analysis`
- `pro/ba/ba-modeling/interface-analysis`
- `pro/ba/business-analyst/process-mining-automation`
- `pro/ba/business-analyst/strategy-analysis-business-need`
- `pro/ba/business-analyst/strategy-analysis-change-strategy`
- `pro/ba/business-analyst/strategy-analysis-current-state`
- `pro/ba/business-analyst/strategy-analysis-future-state`
- `pro/ba/business-analyst/strategy-analysis-gap-analysis`
- `pro/pm/pm-agile/value-stream-management`
- `pro/pm/pm-traditional/benefits-realization`
- `pro/pm/pm-traditional/lessons-learned`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `benefit-sustainment-checklist`
- `frontline-validation-protocol`
- `kpi-drift-alarm-template`
- `process-mining-tool-shortlist`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content process-improvement-initiative-8-weeks --format context` to pull the full chain into an agent-readable payload.
