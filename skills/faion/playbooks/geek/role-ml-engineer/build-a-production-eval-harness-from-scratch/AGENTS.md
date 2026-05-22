---
slug: build-a-production-eval-harness-from-scratch
tier: geek
group: role-ml-engineer
persona: ML / AI engineer shipping a production LLM / RAG / agent feature.
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Build a production eval harness from scratch. Stand up the team's first real eval harness so model + prompt changes stop being vibes-based: golden test set, automated metrics, LLM-as-judge with rub..."
content_id: f2620d4cb090ccd4
methodology_refs:
  - llm-observability-stack
  - model-evaluation
  - prompt-engineering-evaluation
  - prompt-engineering-production
  - evaluation-benchmarks
  - evaluation-framework
  - evaluation-metrics
  - finetuning-datasets
  - rag-eval-pipeline
  - rag-eval-production-monitoring
  - rag-eval-test-set-generation
  - behavioral-evals-adversarial
  - llm-as-judge-harness
  - model-monitoring-drift
---

# Build a production eval harness from scratch

## Context

Stand up the team's first real eval harness so model + prompt changes stop being vibes-based: golden test set, automated metrics, LLM-as-judge with rubric, CI gating, drift monitor in prod, dashboards for PM. Used by every AI feature thereafter.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Stand up the team's first real eval harness so model + prompt changes stop being vibes-based: golden test set, automated metrics, LLM-as-judge with rubric, CI gating, drift monitor in prod, dashboards for PM.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Build a production eval harness from scratch.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/model-evaluation`

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
- `geek/ai/ml-engineer/prompt-engineering-evaluation`
- `geek/ai/ml-engineer/prompt-engineering-production`

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
- `geek/ai/ml-ops/evaluation-benchmarks`
- `geek/ai/ml-ops/evaluation-framework`

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
- `geek/ai/ml-ops/evaluation-metrics`
- `geek/ai/ml-ops/finetuning-datasets`

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
- `geek/ai/rag-engineer/rag-eval-pipeline`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`

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
- `geek/ai/rag-engineer/rag-eval-test-set-generation`
- `geek/_gaps/behavioral-evals-adversarial` (gap)

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
- `geek/_gaps/llm-as-judge-harness` (gap)
- `geek/_gaps/model-monitoring-drift` (gap)

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

- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/model-evaluation`
- `geek/ai/ml-engineer/prompt-engineering-evaluation`
- `geek/ai/ml-engineer/prompt-engineering-production`
- `geek/ai/ml-ops/evaluation-benchmarks`
- `geek/ai/ml-ops/evaluation-framework`
- `geek/ai/ml-ops/evaluation-metrics`
- `geek/ai/ml-ops/finetuning-datasets`
- `geek/ai/rag-engineer/rag-eval-pipeline`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `geek/ai/rag-engineer/rag-eval-test-set-generation`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `behavioral-evals-adversarial` — referenced in source brainstorm but not yet authored
- `llm-as-judge-harness` — referenced in source brainstorm but not yet authored
- `model-monitoring-drift` — referenced in source brainstorm but not yet authored
- `pii-scrubbing-recipe-for-eval-sets` — listed in gaps_for_this_playbook from source brainstorm
- `ci-eval-gate-config` — listed in gaps_for_this_playbook from source brainstorm
- `eval-contract-template` — listed in gaps_for_this_playbook from source brainstorm
