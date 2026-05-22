---
slug: user-story-decomposition-session
tier: pro
group: business-analyst
persona: role-ba
goal: plan-design
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: One oversized epic or feature ends the session decomposed into INVEST-sized stories with prioritisation rationale, mapped to a story-map slice.
content_id: 3cc5e6d59d9ff8e2
methodology_refs:
  - requirements-prioritization
  - requirements-validation
  - user-story-mapping
  - agile-ba-frameworks
---

# User-story decomposition session

**Persona:** role-ba - **Tier:** pro - **Complexity:** medium - **Angle:** atomic

## Context

One oversized epic or feature ends the session decomposed into INVEST-sized stories with prioritisation rationale, mapped to a story-map slice.

Most operators improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step.

## Outcome

By the final stage, the operator holds a written artifact for every step, every decision-gate passed in writing, and a documented go / no-go (or kill) trail another person can audit without asking a question.

## Steps

### 1. Prep

*Intent:* Get inputs, environment, and prior context lined up before the session starts.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-prioritization`

Outputs:
- Written artifact for stage 1 (Prep) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 1 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 2. Frame

*Intent:* Name the single outcome and the boundaries; lock the inputs in writing.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-core/requirements-validation`

Outputs:
- Written artifact for stage 2 (Frame) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 2 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 3. Execute

*Intent:* Run the core activity end-to-end without context switches.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/ba-modeling/user-story-mapping`

Outputs:
- Written artifact for stage 3 (Execute) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 3 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 4. Capture

*Intent:* Write the outputs down in a form a teammate can read later.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/business-analyst/agile-ba-frameworks`

Outputs:
- Written artifact for stage 4 (Capture) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 4 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 5. Decide

*Intent:* Apply the decision gate; produce a go/no-go or next-action note.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `pro/ba/business-analyst/user-story-mapping`

Outputs:
- Written artifact for stage 5 (Decide) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 5 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/ba-core/requirements-validation`
- `pro/ba/ba-modeling/user-story-mapping`
- `pro/ba/business-analyst/agile-ba-frameworks`
- `pro/ba/business-analyst/user-story-mapping`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `invest-split-recipes`
- `wsjf-quick-scoring`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content user-story-decomposition-session --format context` to pull the full chain into an agent-readable payload.
