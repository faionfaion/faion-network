---
slug: fine-tune-vs-prompt-engineer-decision-flow
tier: geek
group: role-ml-engineer
persona: ML / AI engineer shipping a production LLM / RAG / agent feature.
goal: govern-decide
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Fine-tune vs prompt-engineer decision flow. Take an AI feature where prompt engineering plateaued and produce a defensible decision: keep iterating on prompts, do retrieval-augment, do LoRA / SFT,..."
content_id: fb0c4eeda1ef0b25
methodology_refs:
  - cost-optimization
  - decision-framework
  - fine-tuning-lora
  - fine-tuning-openai-data-prep
  - fine-tuning-openai-deployment
  - fine-tuning-openai-dpo
  - fine-tuning-openai-eval
  - fine-tuning-openai-sft
  - llm-decision-framework
  - prompt-engineering-evaluation
  - fine-tuning-openai-production
  - finetuning-datasets
  - llm-cost-basics
  - lora-basics-dataset-prep
  - when-to-fine-tune-vs-prompt
---

# Fine-tune vs prompt-engineer decision flow

## Context

Take an AI feature where prompt engineering plateaued and produce a defensible decision: keep iterating on prompts, do retrieval-augment, do LoRA / SFT, do DPO, or buy a vertical model. Output = decision memo + costed plan + first-pass pilot result.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Take an AI feature where prompt engineering plateaued and produce a defensible decision: keep iterating on prompts, do retrieval-augment, do LoRA / SFT, do DPO, or buy a vertical model.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Fine-tune vs prompt-engineer decision flow.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `geek/ai/ml-engineer/cost-optimization`
- `geek/ai/ml-engineer/decision-framework`

Outputs:
- Written current-state map (1 page)
- Top-3 risk list with owners

### 2. Plan

Convert audit findings into a defensible execution plan with explicit cuts.

Tasks:
- Define done-state acceptance criteria
- Sequence the smallest set of changes that ship the outcome
- Cut everything that does not block the done state

Methodologies:
- `geek/ai/ml-engineer/fine-tuning-lora`
- `geek/ai/ml-engineer/fine-tuning-openai-data-prep`

Outputs:
- 1-page plan with sequenced steps
- Non-goals list (what we are NOT doing)

### 3. Build

Land the first vertical slice end-to-end in a real environment.

Tasks:
- Implement the slice behind a flag or in a sandbox
- Wire telemetry from day one
- Get a real human (not just CI) to use it

Methodologies:
- `geek/ai/ml-engineer/fine-tuning-openai-deployment`
- `geek/ai/ml-engineer/fine-tuning-openai-dpo`

Outputs:
- Working slice in a non-prod environment
- Telemetry dashboard for the slice

### 4. Harden

Find the failure modes before users do.

Tasks:
- Run failure-mode tests against the slice (load, edge cases, abuse)
- Close every must-fix; ticket every nice-to-fix
- Re-run telemetry to confirm no regression

Methodologies:
- `geek/ai/ml-engineer/fine-tuning-openai-eval`
- `geek/ai/ml-engineer/fine-tuning-openai-sft`

Outputs:
- Failure-mode report + closure log
- Ticketed nice-to-fix backlog

### 5. Pilot

Run with a controlled blast radius before broad rollout.

Tasks:
- Roll out to a controlled subset (canary, beta team, single client)
- Measure against acceptance criteria with real traffic / real work
- Capture rollback signal in writing

Methodologies:
- `geek/ai/ml-engineer/llm-decision-framework`
- `geek/ai/ml-engineer/prompt-engineering-evaluation`

Outputs:
- Pilot metrics vs. acceptance criteria
- Rollback decision criteria in writing

### 6. Rollout

Move from pilot to general availability with confidence.

Tasks:
- Stage the rollout in defined cohorts / regions / risk bands
- Hold each stage open until telemetry is clean
- Communicate state to stakeholders at each step

Methodologies:
- `geek/ai/ml-ops/fine-tuning-openai-production`
- `geek/ai/ml-ops/finetuning-datasets`

Outputs:
- Rollout log (cohort-by-cohort)
- Stakeholder update record

### 7. Operate

Hand off as a steady-state operation, not a hero ticket.

Tasks:
- Document the runbook for on-call
- Define the SLO + alert + escalation chain
- Schedule the next review cycle

Methodologies:
- `geek/ai/ml-ops/llm-cost-basics`
- `geek/_gaps/lora-basics-dataset-prep` (gap)
- `geek/_gaps/when-to-fine-tune-vs-prompt` (gap)

Outputs:
- Runbook + on-call notes
- SLO + alert config in source control

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.
- **Rollout** → Advance to the next cohort only after the previous is stable for the agreed window.
- **Operate** → Advance when on-call can resolve the top-3 likely incidents without the original author.

## References

- `geek/ai/ml-engineer/cost-optimization`
- `geek/ai/ml-engineer/decision-framework`
- `geek/ai/ml-engineer/fine-tuning-lora`
- `geek/ai/ml-engineer/fine-tuning-openai-data-prep`
- `geek/ai/ml-engineer/fine-tuning-openai-deployment`
- `geek/ai/ml-engineer/fine-tuning-openai-dpo`
- `geek/ai/ml-engineer/fine-tuning-openai-eval`
- `geek/ai/ml-engineer/fine-tuning-openai-sft`
- `geek/ai/ml-engineer/llm-decision-framework`
- `geek/ai/ml-engineer/prompt-engineering-evaluation`
- `geek/ai/ml-ops/fine-tuning-openai-production`
- `geek/ai/ml-ops/finetuning-datasets`
- `geek/ai/ml-ops/llm-cost-basics`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `lora-basics-dataset-prep` — referenced in source brainstorm but not yet authored
- `when-to-fine-tune-vs-prompt` — referenced in source brainstorm but not yet authored
- `training-data-sourcing-policy` — listed in gaps_for_this_playbook from source brainstorm
- `ai-option-cost-grid-template` — listed in gaps_for_this_playbook from source brainstorm
- `ai-failure-mode-taxonomy` — listed in gaps_for_this_playbook from source brainstorm
