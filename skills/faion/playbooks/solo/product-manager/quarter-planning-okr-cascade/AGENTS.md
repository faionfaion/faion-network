---
slug: quarter-planning-okr-cascade
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
summary: "Quarter starts with a published roadmap, OKRs cascaded from company → product → squad level, prioritised bets locked, capacity reserved, and a written 'what we are NOT doing' anti-roadmap."
content_id: f8735df4ba69a14e
methodology_refs:
  - competitive-positioning
  - portfolio-strategy
  - stakeholder-management
  - opportunity-solution-trees
  - continuous-discovery
  - okr-setting
  - outcome-based-roadmaps
  - outcome-based-roadmaps-advanced
  - roadmap-design
  - backlog-management
  - feature-prioritization-moscow
  - feature-prioritization-rice
  - product-analytics
---

# Quarter planning + OKR cascade

**Persona:** role-pm - **Tier:** solo - **Complexity:** deep - **Angle:** global

## Context

Quarter starts with a published roadmap, OKRs cascaded from company → product → squad level, prioritised bets locked, capacity reserved, and a written 'what we are NOT doing' anti-roadmap.

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
- `solo/product/product-manager/outcome-based-roadmaps-advanced`

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
- `pro/product/product-manager/portfolio-strategy`
- `solo/product/product-manager/roadmap-design`

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
- `pro/product/product-operations/stakeholder-management`
- `solo/product/product-operations/backlog-management`

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
- `pro/research/researcher/opportunity-solution-trees`
- `solo/product/product-operations/feature-prioritization-moscow`

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
- `solo/product/product-operations/feature-prioritization-rice`

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
- `solo/product/product-manager/okr-setting`
- `solo/product/product-operations/product-analytics`

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
- `solo/product/product-manager/outcome-based-roadmaps`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `pro/product/product-manager/competitive-positioning`
- `pro/product/product-manager/portfolio-strategy`
- `pro/product/product-operations/stakeholder-management`
- `pro/research/researcher/opportunity-solution-trees`
- `solo/product/product-manager/continuous-discovery`
- `solo/product/product-manager/okr-setting`
- `solo/product/product-manager/outcome-based-roadmaps`
- `solo/product/product-manager/outcome-based-roadmaps-advanced`
- `solo/product/product-manager/roadmap-design`
- `solo/product/product-operations/backlog-management`
- `solo/product/product-operations/feature-prioritization-moscow`
- `solo/product/product-operations/feature-prioritization-rice`
- `solo/product/product-operations/product-analytics`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `anti-roadmap-template`
- `capacity-vs-ask-balancer`
- `okr-cascade-multi-squad`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content quarter-planning-okr-cascade --format context` to pull the full chain into an agent-readable payload.
