---
slug: agent-state-debug-session-cursor-replay
tier: geek
group: llm-agent
persona: P7
goal: fix-incident
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: An agent ran 40 turns and lost the plot. Reconstruct the trajectory, find the bad state transition, ship a guardrail.
content_id: 80d754b5fc6a9ec5
methodology_refs:
  - auto-evict-tool-results
  - chaos-eval-fault-injection
  - compaction-preserve-refs
  - embedded-scratchpad-field
  - filesystem-as-working-memory
  - generator-critic-bounded-loop
  - max-turns-circuit-breaker
  - plan-execute-vs-react
  - posttool-hook-self-correction
  - record-replay-debugging
  - subagent-as-context-firewall
  - trajectory-eval-otel
  - agent-memory-architecture
  - react-loop-production
---

# Agent-state debug session (cursor + replay)

**Persona:** P7 - **Tier:** geek - **Complexity:** deep - **Angle:** atomic

## Context

An agent ran 40 turns and lost the plot. Reconstruct the trajectory, find the bad state transition, ship a guardrail.

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
- `geek/ai/ai-agents/auto-evict-tool-results`
- `geek/ai/ai-agents/generator-critic-bounded-loop`
- `geek/ai/ai-agents/subagent-as-context-firewall`

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
- `geek/ai/ai-agents/chaos-eval-fault-injection`
- `geek/ai/ai-agents/max-turns-circuit-breaker`
- `geek/ai/ai-agents/trajectory-eval-otel`

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
- `geek/ai/ai-agents/compaction-preserve-refs`
- `geek/ai/ai-agents/plan-execute-vs-react`
- `playbooks/geek/ai-agents/agent-memory-architecture`

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
- `geek/ai/ai-agents/embedded-scratchpad-field`
- `geek/ai/ai-agents/posttool-hook-self-correction`
- `playbooks/geek/ai-agents/react-loop-production`

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
- `geek/ai/ai-agents/filesystem-as-working-memory`
- `geek/ai/ai-agents/record-replay-debugging`

Outputs:
- Written artifact for stage 5 (Decide) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 5 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `geek/ai/ai-agents/auto-evict-tool-results`
- `geek/ai/ai-agents/chaos-eval-fault-injection`
- `geek/ai/ai-agents/compaction-preserve-refs`
- `geek/ai/ai-agents/embedded-scratchpad-field`
- `geek/ai/ai-agents/filesystem-as-working-memory`
- `geek/ai/ai-agents/generator-critic-bounded-loop`
- `geek/ai/ai-agents/max-turns-circuit-breaker`
- `geek/ai/ai-agents/plan-execute-vs-react`
- `geek/ai/ai-agents/posttool-hook-self-correction`
- `geek/ai/ai-agents/record-replay-debugging`
- `geek/ai/ai-agents/subagent-as-context-firewall`
- `geek/ai/ai-agents/trajectory-eval-otel`
- `playbooks/geek/ai-agents/agent-memory-architecture` *(gap)*
- `playbooks/geek/ai-agents/react-loop-production` *(gap)*

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `agent-memory-architecture`
- `agent-replay-harness-cookbook`
- `context-bleed-detection-recipe`
- `react-loop-production`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content agent-state-debug-session-cursor-replay --format context` to pull the full chain into an agent-readable payload.
