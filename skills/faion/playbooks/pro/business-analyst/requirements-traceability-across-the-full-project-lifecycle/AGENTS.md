---
slug: requirements-traceability-across-the-full-project-lifecycle
tier: pro
group: business-analyst
persona: role-ba
goal: operate-ritual
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Continuous flow that runs from project start to closure. Establish, populate, audit, and retire a traceability matrix linking business need → requirement → design → AC → test → release → benefit. E...
content_id: af387002c9c466e4
methodology_refs:
  - ba-governance
  - ba-requirements-mgmt
  - requirements-lifecycle
  - requirements-traceability
  - requirements-validation
  - solution-assessment
  - acceptance-criteria
  - azure-devops-boards
  - jira-workflow-management
  - benefits-realization
  - change-control
  - lessons-learned
  - requirements-management
  - project-closure
---

# Requirements traceability across the full project lifecycle

**Persona:** role-ba - **Tier:** pro - **Complexity:** deep - **Angle:** global

## Context

Continuous flow that runs from project start to closure. Establish, populate, audit, and retire a traceability matrix linking business need → requirement → design → AC → test → release → benefit. End state — at every release, sponsor sees evidence that what was funded is what shipped.

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
- `pro/ba/ba-modeling/acceptance-criteria`

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
- `pro/ba/ba-core/ba-requirements-mgmt`
- `pro/pm/pm-agile/azure-devops-boards`

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
- `pro/ba/ba-core/requirements-lifecycle`
- `pro/pm/pm-agile/jira-workflow-management`

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
- `pro/ba/ba-core/requirements-management`
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
- `pro/ba/ba-core/requirements-traceability`
- `pro/pm/pm-traditional/change-control`

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
- `pro/ba/ba-core/requirements-validation`
- `pro/pm/pm-traditional/lessons-learned`

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
- `pro/ba/ba-core/solution-assessment`
- `pro/pm/pm-traditional/project-closure`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/ba/ba-core/ba-governance`
- `pro/ba/ba-core/ba-requirements-mgmt`
- `pro/ba/ba-core/requirements-lifecycle`
- `pro/ba/ba-core/requirements-management` *(gap)*
- `pro/ba/ba-core/requirements-traceability`
- `pro/ba/ba-core/requirements-validation`
- `pro/ba/ba-core/solution-assessment`
- `pro/ba/ba-modeling/acceptance-criteria`
- `pro/pm/pm-agile/azure-devops-boards`
- `pro/pm/pm-agile/jira-workflow-management`
- `pro/pm/pm-traditional/benefits-realization`
- `pro/pm/pm-traditional/change-control`
- `pro/pm/pm-traditional/lessons-learned`
- `pro/pm/pm-traditional/project-closure`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `ai-orphan-link-detection`
- `requirements-management`
- `scope-drift-early-warning-metrics`
- `traceability-tooling-comparison-jira-ado-polarion`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content requirements-traceability-across-the-full-project-lifecycle --format context` to pull the full chain into an agent-readable payload.
