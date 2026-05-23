# AI-assisted requirements discovery on a new outsource engagement

**Persona:** role-ba - **Tier:** pro - **Complexity:** deep - **Angle:** synthesis

## Context

From kickoff to signed-off baseline requirements doc, with AI accelerating every step and a BA retaining accountability. Output: stakeholder map, interview-transcript-derived requirements, ambiguity-flagged spec, AC pack, traceability matrix v1.

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
- `ai-acceptance-criteria-generator-reviewer`
- `pro/ba/ba-core/elicitation-techniques`
- `requirement-quality-scorecard`

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
- `ai-elicitation-prompt-patterns`
- `pro/ba/ba-core/requirements-documentation`
- `traceability-auto-maintenance`

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
- `ai-user-story-decomposition`
- `pro/ba/ba-core/requirements-traceability`

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
- `ambiguity-contradiction-detector`
- `pro/ba/ba-core/requirements-validation`

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
- `ba-to-developer-handoff-template`
- `pro/ba/ba-core/stakeholder-analysis`

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
- `ba-to-qa-handoff-template`
- `pro/ba/ba-modeling/acceptance-criteria`

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
- `geek/ba/ba-core/ai-enabled-business-analysis`
- `pro/ba/ba-modeling/user-story-mapping`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `ai-acceptance-criteria-generator-reviewer` *(gap)*
- `ai-elicitation-prompt-patterns` *(gap)*
- `ai-user-story-decomposition` *(gap)*
- `ambiguity-contradiction-detector` *(gap)*
- `ba-to-developer-handoff-template` *(gap)*
- `ba-to-qa-handoff-template` *(gap)*
- `geek/ba/ba-core/ai-enabled-business-analysis`
- `pro/ba/ba-core/elicitation-techniques`
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/ba-core/requirements-traceability`
- `pro/ba/ba-core/requirements-validation`
- `pro/ba/ba-core/stakeholder-analysis`
- `pro/ba/ba-modeling/acceptance-criteria`
- `pro/ba/ba-modeling/user-story-mapping`
- `requirement-quality-scorecard` *(gap)*
- `traceability-auto-maintenance` *(gap)*

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `ai-acceptance-criteria-generator-reviewer`
- `ai-elicitation-prompt-patterns`
- `ai-user-story-decomposition`
- `ambiguity-contradiction-detector`
- `ba-to-developer-handoff-template`
- `ba-to-qa-handoff-template`
- `glossary-management-as-code`
- `requirement-quality-scorecard`
- `traceability-auto-maintenance`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content ai-assisted-requirements-discovery-on-a-new-outsource-engagement --format context` to pull the full chain into an agent-readable payload.
