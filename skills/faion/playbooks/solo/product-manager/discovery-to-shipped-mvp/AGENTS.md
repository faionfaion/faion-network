---
slug: discovery-to-shipped-mvp
tier: solo
group: product-manager
persona: role-pm
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: From an opportunity hypothesis through evidence-backed problem framing, MVP scoping, build, launch, and first iteration. Ends when MVP is in production with success metrics tracked.
content_id: 9cb1fcda27daa405
methodology_refs:
  - competitive-positioning
  - audience-segmentation
  - opportunity-solution-trees
  - persona-building
  - continuous-discovery
  - product-discovery
  - spec-writing
  - user-story-mapping
  - backlog-management
  - feedback-management
  - product-analytics
  - technical-debt-management
  - product-launch
  - jobs-to-be-done
  - pain-point-research
  - problem-validation-2026
  - success-metrics-definition
  - micro-mvps
  - user-interviews
  - mvp-scoping
  - value-proposition-design
---

# Discovery to shipped MVP

**Persona:** role-pm - **Tier:** solo - **Complexity:** deep - **Angle:** global

## Context

From an opportunity hypothesis through evidence-backed problem framing, MVP scoping, build, launch, and first iteration. Ends when MVP is in production with success metrics tracked.

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
- `pro/product/product-manager/competitive-positioning`
- `solo/product/product-manager/user-story-mapping`
- `solo/product/product-planning/product-launch`

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
- `pro/research/researcher/audience-segmentation`
- `solo/product/product-operations/backlog-management`
- `solo/research/researcher/jobs-to-be-done`

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
- `pro/research/researcher/opportunity-solution-trees`
- `solo/product/product-operations/feedback-management`
- `solo/research/researcher/pain-point-research`

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
- `pro/research/researcher/persona-building`
- `solo/product/product-operations/product-analytics`
- `solo/research/researcher/problem-validation-2026`

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
- `solo/product/product-manager/continuous-discovery`
- `solo/product/product-operations/technical-debt-management`
- `solo/research/researcher/success-metrics-definition`

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
- `solo/product/product-manager/product-discovery`
- `solo/product/product-planning/micro-mvps`
- `solo/research/researcher/user-interviews`

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
- `solo/product/product-manager/spec-writing`
- `solo/product/product-planning/mvp-scoping`
- `solo/research/researcher/value-proposition-design`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/product/product-manager/competitive-positioning`
- `pro/research/researcher/audience-segmentation`
- `pro/research/researcher/opportunity-solution-trees`
- `pro/research/researcher/persona-building`
- `solo/product/product-manager/continuous-discovery`
- `solo/product/product-manager/product-discovery`
- `solo/product/product-manager/spec-writing`
- `solo/product/product-manager/user-story-mapping`
- `solo/product/product-operations/backlog-management`
- `solo/product/product-operations/feedback-management`
- `solo/product/product-operations/product-analytics`
- `solo/product/product-operations/technical-debt-management`
- `solo/product/product-planning/micro-mvps`
- `solo/product/product-planning/mvp-scoping`
- `solo/product/product-planning/product-launch`
- `solo/research/researcher/jobs-to-be-done`
- `solo/research/researcher/pain-point-research`
- `solo/research/researcher/problem-validation-2026`
- `solo/research/researcher/success-metrics-definition`
- `solo/research/researcher/user-interviews`
- `solo/research/researcher/value-proposition-design`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `beta-cohort-recruitment`
- `kill-criteria-template`
- `mvp-instrumentation-checklist`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content discovery-to-shipped-mvp --format context` to pull the full chain into an agent-readable payload.
