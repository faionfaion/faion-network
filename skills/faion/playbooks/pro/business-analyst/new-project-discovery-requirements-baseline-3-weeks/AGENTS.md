---
slug: new-project-discovery-requirements-baseline-3-weeks
tier: pro
group: business-analyst
persona: role-ba
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "From kickoff to a signed-off requirements baseline: stakeholders mapped, business need articulated, scope boundary drawn, prioritised backlog with acceptance criteria, traceability matrix v1, gloss..."
content_id: 9bde0434f31335d6
methodology_refs:
  - ba-governance
  - ba-planning
  - data-driven-requirements
  - elicitation-techniques
  - requirements-documentation
  - requirements-lifecycle
  - requirements-prioritization
  - requirements-traceability
  - requirements-validation
  - stakeholder-analysis
  - strategy-basics
  - acceptance-criteria
  - decision-analysis
  - strategy-analysis-change-strategy
  - interface-analysis
  - strategy-analysis-current-state
  - use-case-modeling
  - strategy-analysis-future-state
  - user-story-mapping
  - strategy-analysis-gap-analysis
  - stakeholder-register
  - business-process-analysis
  - knowledge-areas-overview
  - continuous-discovery
  - data-analysis
  - strategy-analysis-business-need
---

# New project discovery + requirements baseline (3 weeks)

**Persona:** role-ba - **Tier:** pro - **Complexity:** deep - **Angle:** global

## Context

From kickoff to a signed-off requirements baseline: stakeholders mapped, business need articulated, scope boundary drawn, prioritised backlog with acceptance criteria, traceability matrix v1, glossary v1. End state — dev team can pull tickets without re-asking the BA what 'done' means.

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
- `pro/ba/ba-core/requirements-traceability`
- `pro/ba/ba-modeling/decision-analysis`
- `pro/ba/business-analyst/strategy-analysis-change-strategy`

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
- `pro/ba/ba-core/ba-planning`
- `pro/ba/ba-core/requirements-validation`
- `pro/ba/ba-modeling/interface-analysis`
- `pro/ba/business-analyst/strategy-analysis-current-state`

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
- `pro/ba/ba-core/data-driven-requirements`
- `pro/ba/ba-core/stakeholder-analysis`
- `pro/ba/ba-modeling/use-case-modeling`
- `pro/ba/business-analyst/strategy-analysis-future-state`

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
- `pro/ba/ba-core/elicitation-techniques`
- `pro/ba/ba-core/strategy-basics`
- `pro/ba/ba-modeling/user-story-mapping`
- `pro/ba/business-analyst/strategy-analysis-gap-analysis`

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
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/ba-modeling/acceptance-criteria`
- `pro/ba/business-analyst/elicitation-techniques`
- `pro/pm/pm-traditional/stakeholder-register`

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
- `pro/ba/ba-core/requirements-lifecycle`
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/ba/business-analyst/knowledge-areas-overview`
- `pro/research/researcher/continuous-discovery`

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
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/ba-modeling/data-analysis`
- `pro/ba/business-analyst/strategy-analysis-business-need`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/ba/ba-core/ba-governance`
- `pro/ba/ba-core/ba-planning`
- `pro/ba/ba-core/data-driven-requirements`
- `pro/ba/ba-core/elicitation-techniques`
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/ba-core/requirements-lifecycle`
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/ba-core/requirements-traceability`
- `pro/ba/ba-core/requirements-validation`
- `pro/ba/ba-core/stakeholder-analysis`
- `pro/ba/ba-core/strategy-basics`
- `pro/ba/ba-modeling/acceptance-criteria`
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/ba/ba-modeling/data-analysis`
- `pro/ba/ba-modeling/decision-analysis`
- `pro/ba/ba-modeling/interface-analysis`
- `pro/ba/ba-modeling/use-case-modeling`
- `pro/ba/ba-modeling/user-story-mapping`
- `pro/ba/business-analyst/elicitation-techniques`
- `pro/ba/business-analyst/knowledge-areas-overview`
- `pro/ba/business-analyst/strategy-analysis-business-need`
- `pro/ba/business-analyst/strategy-analysis-change-strategy`
- `pro/ba/business-analyst/strategy-analysis-current-state`
- `pro/ba/business-analyst/strategy-analysis-future-state`
- `pro/ba/business-analyst/strategy-analysis-gap-analysis`
- `pro/pm/pm-traditional/stakeholder-register`
- `pro/research/researcher/continuous-discovery`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `ai-assisted-requirements-elicitation`
- `ba-onboarding-week-one-template`
- `compliance-checklist-by-domain`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content new-project-discovery-requirements-baseline-3-weeks --format context` to pull the full chain into an agent-readable payload.
