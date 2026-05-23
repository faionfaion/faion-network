# Migrate LLM provider / model generation

## Context

Move a production AI feature from model N to model N+1 (e.g. Claude 4 -> 5, GPT-4o -> next, or cross-provider) without regression: eval-gated rollout, prompts re-tuned for the new model's quirks, cost + latency budget re-baselined, fallback chain updated, customers unaware anything changed.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Move a production AI feature from model N to model N+1 (e.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Migrate LLM provider / model generation.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `geek/ai/ml-engineer/decision-framework`
- `geek/ai/ml-engineer/llm-decision-framework`

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
- `geek/ai/ml-engineer/llm-observability`
- `geek/ai/ml-engineer/llm-observability-stack`

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
- `geek/ai/ml-engineer/model-evaluation`
- `geek/ai/ml-engineer/prompt-engineering-evaluation`

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
- `geek/ai/ml-engineer/prompt-engineering-production`
- `geek/ai/ml-engineer/structured-output`

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
- `geek/ai/ml-engineer/tool-use-function-calling`
- `geek/ai/ml-ops/evaluation-framework`

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
- `geek/ai/ml-ops/evaluation-metrics`
- `geek/_gaps/model-routing-cheap-vs-strong` (gap)

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
- `geek/_gaps/prompt-caching-strategy` (gap)
- `geek/_gaps/behavioral-evals-adversarial` (gap)
- `geek/_gaps/function-calling-tool-use` (gap)
- `geek/_gaps/llm-fallback-chains` (gap)

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

- `geek/ai/ml-engineer/decision-framework`
- `geek/ai/ml-engineer/llm-decision-framework`
- `geek/ai/ml-engineer/llm-observability`
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/model-evaluation`
- `geek/ai/ml-engineer/prompt-engineering-evaluation`
- `geek/ai/ml-engineer/prompt-engineering-production`
- `geek/ai/ml-engineer/structured-output`
- `geek/ai/ml-engineer/tool-use-function-calling`
- `geek/ai/ml-ops/evaluation-framework`
- `geek/ai/ml-ops/evaluation-metrics`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `model-routing-cheap-vs-strong` — referenced in source brainstorm but not yet authored
- `prompt-caching-strategy` — referenced in source brainstorm but not yet authored
- `behavioral-evals-adversarial` — referenced in source brainstorm but not yet authored
- `function-calling-tool-use` — referenced in source brainstorm but not yet authored
- `llm-fallback-chains` — referenced in source brainstorm but not yet authored
- `prompt-portability-audit` — listed in gaps_for_this_playbook from source brainstorm
- `auto-rollback-policy-design` — listed in gaps_for_this_playbook from source brainstorm
- `model-migration-checklist` — listed in gaps_for_this_playbook from source brainstorm
