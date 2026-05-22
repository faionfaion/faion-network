---
slug: multi-model-gateway-migration-lock-in-to-portability-2-months
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
summary: Move a single-vendor agent (e.g. Anthropic-only) to a portable runtime where Anthropic / OpenAI / local LLM can be swapped per-step or per-tenant, with fallback chain, cost-aware routing, and uncha...
content_id: 8c6707127be4210e
methodology_refs:
  - gateway-fallback-chain
  - mcp-gateway-composition
  - preference-trained-router
  - previous-response-id-reasoning-reuse
  - record-replay-debugging
  - structured-output-mode-picker
  - weak-model-preselection
  - claude-api-integration
  - function-calling-patterns
  - gemini-api-integration
  - local-llm-ollama
  - openai-api-integration
  - structured-output-patterns
  - ollama-python-client
  - tool-use-basics
  - ollama-setup-models
  - llm-observability-stack
  - ollama-tool-calling
  - model-evaluation
  - rag-eval-ab-testing
  - ollama-agent-integration
  - semantic-xml-content
  - ollama-deployment
  - structured-output-basics
  - ollama-prompt-engineering
---

# Multi-model gateway migration: lock-in to portability (2 months)

**Persona:** P7 - **Tier:** geek - **Complexity:** deep - **Angle:** global

## Context

Move a single-vendor agent (e.g. Anthropic-only) to a portable runtime where Anthropic / OpenAI / local LLM can be swapped per-step or per-tenant, with fallback chain, cost-aware routing, and unchanged eval bar.

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
- `geek/ai/ai-agents/gateway-fallback-chain`
- `geek/ai/llm-integration/claude-api-integration`
- `geek/ai/llm-integration/structured-output-patterns`
- `geek/ai/ml-engineer/ollama-python-client`

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
- `geek/ai/ai-agents/mcp-gateway-composition`
- `geek/ai/llm-integration/function-calling-patterns`
- `geek/ai/llm-integration/tool-use-basics`
- `geek/ai/ml-engineer/ollama-setup-models`

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
- `geek/ai/ai-agents/preference-trained-router`
- `geek/ai/llm-integration/gemini-api-integration`
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/ollama-tool-calling`

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
- `geek/ai/ai-agents/previous-response-id-reasoning-reuse`
- `geek/ai/llm-integration/local-llm-ollama`
- `geek/ai/ml-engineer/model-evaluation`
- `geek/ai/rag-engineer/rag-eval-ab-testing`

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
- `geek/ai/ai-agents/record-replay-debugging`
- `geek/ai/llm-integration/openai-api-integration`
- `geek/ai/ml-engineer/ollama-agent-integration`

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
- `geek/ai/ai-agents/structured-output-mode-picker`
- `geek/ai/llm-integration/semantic-xml-content`
- `geek/ai/ml-engineer/ollama-deployment`

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
- `geek/ai/ai-agents/weak-model-preselection`
- `geek/ai/llm-integration/structured-output-basics`
- `geek/ai/ml-engineer/ollama-prompt-engineering`

Outputs:
- Written artifact for stage 7 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 7 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `geek/ai/ai-agents/gateway-fallback-chain`
- `geek/ai/ai-agents/mcp-gateway-composition`
- `geek/ai/ai-agents/preference-trained-router`
- `geek/ai/ai-agents/previous-response-id-reasoning-reuse`
- `geek/ai/ai-agents/record-replay-debugging`
- `geek/ai/ai-agents/structured-output-mode-picker`
- `geek/ai/ai-agents/weak-model-preselection`
- `geek/ai/llm-integration/claude-api-integration`
- `geek/ai/llm-integration/function-calling-patterns`
- `geek/ai/llm-integration/gemini-api-integration`
- `geek/ai/llm-integration/local-llm-ollama`
- `geek/ai/llm-integration/openai-api-integration`
- `geek/ai/llm-integration/semantic-xml-content`
- `geek/ai/llm-integration/structured-output-basics`
- `geek/ai/llm-integration/structured-output-patterns`
- `geek/ai/llm-integration/tool-use-basics`
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/model-evaluation`
- `geek/ai/ml-engineer/ollama-agent-integration`
- `geek/ai/ml-engineer/ollama-deployment`
- `geek/ai/ml-engineer/ollama-prompt-engineering`
- `geek/ai/ml-engineer/ollama-python-client`
- `geek/ai/ml-engineer/ollama-setup-models`
- `geek/ai/ml-engineer/ollama-tool-calling`
- `geek/ai/rag-engineer/rag-eval-ab-testing`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `eu-sovereign-llm-deployment-bundle`
- `router-shadow-deploy-protocol`
- `vendor-feature-portability-matrix`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content multi-model-gateway-migration-lock-in-to-portability-2-months --format context` to pull the full chain into an agent-readable payload.
