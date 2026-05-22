---
slug: run-a-blameless-agent-incident-postmortem-when-the-agent-is-the-defendant
tier: geek
group: llm-agent
persona: P7
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: When the agent ships a hallucinated answer, mis-calls a tool, or jailbreaks itself, the team produces a structured postmortem that attributes cause to model/prompt/tool/context layer, lands a regre...
content_id: 4d7741549d3bbbae
methodology_refs:
  - chaos-eval-fault-injection
  - generator-critic-bounded-loop
  - record-replay-debugging
  - trajectory-eval-otel
  - inc-postmortem-auto-draft-no-publish
---

# Run a blameless agent-incident postmortem when the agent is the defendant

**Persona:** P7 - **Tier:** geek - **Complexity:** medium - **Angle:** synthesis

## Context

When the agent ships a hallucinated answer, mis-calls a tool, or jailbreaks itself, the team produces a structured postmortem that attributes cause to model/prompt/tool/context layer, lands a regression eval, and prevents recurrence.

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
- `geek/ai/ai-agents/chaos-eval-fault-injection`

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
- `geek/ai/ai-agents/generator-critic-bounded-loop`

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
- `geek/ai/ai-agents/record-replay-debugging`

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
- `geek/ai/ai-agents/trajectory-eval-otel`

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
- `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`

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

Outputs:
- Written artifact for stage 6 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 6 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `geek/ai/ai-agents/chaos-eval-fault-injection`
- `geek/ai/ai-agents/generator-critic-bounded-loop`
- `geek/ai/ai-agents/record-replay-debugging`
- `geek/ai/ai-agents/trajectory-eval-otel`
- `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `agent-failure-taxonomy`
- `agent-incident-postmortem-template`
- `regression-eval-before-fix-rule`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content run-a-blameless-agent-incident-postmortem-when-the-agent-is-the-defendant --format context` to pull the full chain into an agent-readable payload.
