---
slug: fine-tune-vs-prompt-engineer-decision-flow-4-weeks-worst-case
tier: geek
group: llm-agent
persona: P7
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Structured decision and execution path: from baseline scorecard to a clear go/no-go on fine-tuning, including LoRA SFT/DPO data prep, training, eval, and deployment — or staying with prompt+retriev..."
content_id: 0bcbb758873dd0dc
methodology_refs:
  - confidence-thresholded-cascade
  - record-replay-debugging
  - role-specialized-models
  - schema-version-pinning
  - cost-optimization
  - decision-framework
  - fine-tuning-lora
  - fine-tuning-openai-data-prep
  - fine-tuning-openai-deployment
  - fine-tuning-openai-dpo
  - fine-tuning-openai-eval
  - fine-tuning-openai-sft
  - prompt-engineering-evaluation
  - cost-reduction-strategies
  - fine-tuning-openai-basics
  - fine-tuning-openai-production
  - finetuning-basics
  - finetuning
  - finetuning-datasets
  - llm-decision-framework
  - lora-qlora
---

# Fine-tune vs prompt-engineer decision flow (4 weeks worst case)

**Persona:** P7 - **Tier:** geek - **Complexity:** deep - **Angle:** global

## Context

Structured decision and execution path: from baseline scorecard to a clear go/no-go on fine-tuning, including LoRA SFT/DPO data prep, training, eval, and deployment — or staying with prompt+retrieval if economics don't beat the floor.

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
- `geek/ai/ai-agents/confidence-thresholded-cascade`
- `geek/ai/ml-engineer/fine-tuning-openai-data-prep`
- `geek/ai/ml-engineer/prompt-engineering-evaluation`

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
- `geek/ai/ai-agents/record-replay-debugging`
- `geek/ai/ml-engineer/fine-tuning-openai-deployment`
- `geek/ai/ml-ops/cost-reduction-strategies`

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
- `geek/ai/ai-agents/role-specialized-models`
- `geek/ai/ml-engineer/fine-tuning-openai-dpo`
- `geek/ai/ml-ops/fine-tuning-openai-basics`

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
- `geek/ai/ai-agents/schema-version-pinning`
- `geek/ai/ml-engineer/fine-tuning-openai-eval`
- `geek/ai/ml-ops/fine-tuning-openai-production`

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
- `geek/ai/ml-engineer/cost-optimization`
- `geek/ai/ml-engineer/fine-tuning-openai-sft`
- `geek/ai/ml-ops/finetuning-basics`

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
- `geek/ai/ml-engineer/decision-framework`
- `geek/ai/ml-engineer/finetuning`
- `geek/ai/ml-ops/finetuning-datasets`

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
- `geek/ai/ml-engineer/fine-tuning-lora`
- `geek/ai/ml-engineer/llm-decision-framework`
- `geek/ai/ml-ops/lora-qlora`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `geek/ai/ai-agents/confidence-thresholded-cascade`
- `geek/ai/ai-agents/record-replay-debugging`
- `geek/ai/ai-agents/role-specialized-models`
- `geek/ai/ai-agents/schema-version-pinning`
- `geek/ai/ml-engineer/cost-optimization`
- `geek/ai/ml-engineer/decision-framework`
- `geek/ai/ml-engineer/fine-tuning-lora`
- `geek/ai/ml-engineer/fine-tuning-openai-data-prep`
- `geek/ai/ml-engineer/fine-tuning-openai-deployment`
- `geek/ai/ml-engineer/fine-tuning-openai-dpo`
- `geek/ai/ml-engineer/fine-tuning-openai-eval`
- `geek/ai/ml-engineer/fine-tuning-openai-sft`
- `geek/ai/ml-engineer/finetuning`
- `geek/ai/ml-engineer/llm-decision-framework`
- `geek/ai/ml-engineer/prompt-engineering-evaluation`
- `geek/ai/ml-ops/cost-reduction-strategies`
- `geek/ai/ml-ops/fine-tuning-openai-basics`
- `geek/ai/ml-ops/fine-tuning-openai-production`
- `geek/ai/ml-ops/finetuning-basics`
- `geek/ai/ml-ops/finetuning-datasets`
- `geek/ai/ml-ops/lora-qlora`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `fine-tune-vs-prompt-economic-model`
- `production-trace-mining-for-training-data`
- `tuned-model-shadow-deploy-protocol`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content fine-tune-vs-prompt-engineer-decision-flow-4-weeks-worst-case --format context` to pull the full chain into an agent-readable payload.
