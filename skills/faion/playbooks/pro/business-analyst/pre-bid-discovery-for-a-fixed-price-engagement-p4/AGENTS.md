---
slug: pre-bid-discovery-for-a-fixed-price-engagement-p4
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
summary: BA leads a structured discovery before contract signature so the SoW reflects real complexity rather than wishful pitch numbers. End state — agency / outsource shop submits a bid backed by traced a...
content_id: c98dc44992f438ce
methodology_refs:
  - ba-governance
  - ba-planning
  - ba-strategic-partnership
  - elicitation-techniques
  - requirements-documentation
  - requirements-prioritization
  - interface-analysis
  - user-story-mapping
  - methodologies-detail
  - strategy-analysis-business-need
  - strategy-analysis-current-state
  - strategy-analysis-future-state
  - procurement-management
  - risk-management
  - risk-register
  - business-model-research
  - competitive-intelligence
  - cost-estimation
  - lessons-learned
---

# Pre-bid discovery for a fixed-price engagement (P4)

**Persona:** role-ba - **Tier:** pro - **Complexity:** deep - **Angle:** global

## Context

BA leads a structured discovery before contract signature so the SoW reflects real complexity rather than wishful pitch numbers. End state — agency / outsource shop submits a bid backed by traced assumptions, evidenced estimates, explicit out-of-scope list, and a risk register the sponsor has seen.

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
- `pro/pm/pm-traditional/procurement-management`

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
- `pro/ba/business-analyst/methodologies-detail`
- `pro/pm/pm-traditional/risk-management`

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
- `pro/ba/ba-core/ba-strategic-partnership`
- `pro/ba/business-analyst/strategy-analysis-business-need`
- `pro/pm/pm-traditional/risk-register`

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
- `pro/ba/business-analyst/strategy-analysis-current-state`
- `pro/research/researcher/business-model-research`

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
- `pro/ba/business-analyst/strategy-analysis-future-state`
- `pro/research/researcher/competitive-intelligence`

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
- `pro/ba/ba-core/requirements-prioritization`
- `pro/pm/pm-traditional/cost-estimation`

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
- `pro/ba/ba-modeling/interface-analysis`
- `pro/pm/pm-traditional/lessons-learned`

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
- `pro/ba/ba-core/ba-strategic-partnership`
- `pro/ba/ba-core/elicitation-techniques`
- `pro/ba/ba-core/requirements-documentation`
- `pro/ba/ba-core/requirements-prioritization`
- `pro/ba/ba-modeling/interface-analysis`
- `pro/ba/ba-modeling/user-story-mapping`
- `pro/ba/business-analyst/methodologies-detail`
- `pro/ba/business-analyst/strategy-analysis-business-need`
- `pro/ba/business-analyst/strategy-analysis-current-state`
- `pro/ba/business-analyst/strategy-analysis-future-state`
- `pro/pm/pm-traditional/cost-estimation`
- `pro/pm/pm-traditional/lessons-learned`
- `pro/pm/pm-traditional/procurement-management`
- `pro/pm/pm-traditional/risk-management`
- `pro/pm/pm-traditional/risk-register`
- `pro/research/researcher/business-model-research`
- `pro/research/researcher/competitive-intelligence`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `bid-no-bid-scoring-rubric`
- `discovery-to-delivery-handover-protocol`
- `fixed-price-risk-loading-model`
- `sow-template-with-traced-assumptions`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content pre-bid-discovery-for-a-fixed-price-engagement-p4 --format context` to pull the full chain into an agent-readable payload.
