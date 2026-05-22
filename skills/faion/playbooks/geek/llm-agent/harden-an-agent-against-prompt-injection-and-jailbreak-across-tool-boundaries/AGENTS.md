---
slug: harden-an-agent-against-prompt-injection-and-jailbreak-across-tool-boundaries
tier: geek
group: llm-agent
persona: P7
goal: build-ship
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Agent with file-read / web-fetch / MCP tools survives an indirect-prompt-injection red-team suite without exfiltrating data, escalating permissions, or violating refusal policy.
content_id: 6a5c06d179ae6690
methodology_refs:
  - bundle-vs-split-tools
  - chaos-eval-fault-injection
  - cheap-guardrail-tripwire
  - discriminated-union-output
  - idempotent-write-tools
  - refusal-field-strict-schema
  - behavioral-evals-adversarial
  - pii-redaction-pipeline
---

# Harden an agent against prompt injection and jailbreak across tool boundaries

**Persona:** P7 - **Tier:** geek - **Complexity:** deep - **Angle:** synthesis

## Context

Agent with file-read / web-fetch / MCP tools survives an indirect-prompt-injection red-team suite without exfiltrating data, escalating permissions, or violating refusal policy.

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
- `geek/ai/ai-agents/bundle-vs-split-tools`
- `playbooks/geek/evaluation/behavioral-evals-adversarial`

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
- `geek/ai/ai-agents/chaos-eval-fault-injection`

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
- `geek/ai/ai-agents/cheap-guardrail-tripwire`

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
- `geek/ai/ai-agents/discriminated-union-output`

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
- `geek/ai/ai-agents/idempotent-write-tools`

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
- `geek/ai/ai-agents/refusal-field-strict-schema`

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
- `playbooks/geek/ai-safety/pii-redaction-pipeline`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `geek/ai/ai-agents/bundle-vs-split-tools`
- `geek/ai/ai-agents/chaos-eval-fault-injection`
- `geek/ai/ai-agents/cheap-guardrail-tripwire`
- `geek/ai/ai-agents/discriminated-union-output`
- `geek/ai/ai-agents/idempotent-write-tools`
- `geek/ai/ai-agents/refusal-field-strict-schema`
- `playbooks/geek/ai-safety/pii-redaction-pipeline` *(gap)*
- `playbooks/geek/evaluation/behavioral-evals-adversarial` *(gap)*

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `behavioral-evals-adversarial`
- `data-exfiltration-canary-tokens`
- `indirect-prompt-injection-defense`
- `jailbreak-eval-suite-bootstrap`
- `pii-redaction-pipeline`
- `tool-trust-boundary-model`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content harden-an-agent-against-prompt-injection-and-jailbreak-across-tool-boundaries --format context` to pull the full chain into an agent-readable payload.
