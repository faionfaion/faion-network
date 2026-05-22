---
slug: observability-drift-detection-rollout-3-weeks
tier: geek
group: llm-agent
persona: P7
goal: build-ship
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Production agent goes from blind-running to fully observed: per-step OTEL traces, eval-in-prod sampling, drift detection on inputs/outputs/costs, alerting, and an on-call runbook."
content_id: 9e83c112aa7f4b1e
methodology_refs:
  - llm-judge-rubric-evidence-first
  - schema-version-pinning
  - stream-json-orchestration
  - trajectory-eval-otel
  - ai-governance-compliance
  - eu-ai-act-compliance
  - guardrails-concepts
  - llm-observability
  - llm-observability-stack
  - prompt-engineering-security
  - evaluation-framework
  - rag-eval-production-monitoring
  - vector-database-setup
  - inc-postmortem-auto-draft-no-publish
  - inc-read-only-investigation-default
  - inc-runbook-as-markdown-tagged-steps
  - inc-tool-tier-approval-gate
---

# Observability + drift detection rollout (3 weeks)

**Persona:** P7 - **Tier:** geek - **Complexity:** medium - **Angle:** global

## Context

Production agent goes from blind-running to fully observed: per-step OTEL traces, eval-in-prod sampling, drift detection on inputs/outputs/costs, alerting, and an on-call runbook.

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
- `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `geek/ai/ml-engineer/guardrails-concepts`
- `geek/ai/rag-engineer/vector-database-setup`

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
- `geek/ai/ai-agents/schema-version-pinning`
- `geek/ai/ml-engineer/llm-observability`
- `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`

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
- `geek/ai/ai-agents/stream-json-orchestration`
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/sdlc-ai/inc-read-only-investigation-default`

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
- `geek/ai/ml-engineer/prompt-engineering-security`
- `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`

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
- `geek/ai/ml-engineer/ai-governance-compliance`
- `geek/ai/ml-ops/evaluation-framework`
- `geek/sdlc-ai/inc-tool-tier-approval-gate`

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
- `geek/ai/ml-engineer/eu-ai-act-compliance`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`

Outputs:
- Written artifact for stage 6 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 6 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `geek/ai/ai-agents/schema-version-pinning`
- `geek/ai/ai-agents/stream-json-orchestration`
- `geek/ai/ai-agents/trajectory-eval-otel`
- `geek/ai/ml-engineer/ai-governance-compliance`
- `geek/ai/ml-engineer/eu-ai-act-compliance`
- `geek/ai/ml-engineer/guardrails-concepts`
- `geek/ai/ml-engineer/llm-observability`
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/prompt-engineering-security`
- `geek/ai/ml-ops/evaluation-framework`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `geek/ai/rag-engineer/vector-database-setup`
- `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`
- `geek/sdlc-ai/inc-read-only-investigation-default`
- `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `geek/sdlc-ai/inc-tool-tier-approval-gate`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `agent-on-call-runbook-template`
- `drift-detection-input-distribution`
- `eval-in-prod-sampling-policy`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content observability-drift-detection-rollout-3-weeks --format context` to pull the full chain into an agent-readable payload.
