---
slug: ship-a-qa-program-for-an-ai-powered-product
tier: pro
group: role-qa-engineer
persona: QA engineer / test lead in an indie or small-team product context.
goal: build-ship
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Ship a QA program for an AI-powered product. From zero, build the QA discipline for a product whose core value is an LLM/RAG/agent feature — eval sets, hallucination + safety tests, regression gate...
content_id: 9b5b1a491c8b0c35
methodology_refs:
  - model-evaluation
  - rag-eval-production-monitoring
  - rag-eval-strategy
  - rag-eval-test-set-generation
  - ai-bug-repro-capture
  - ai-feature-eval-set-design
  - ai-feature-online-eval-loop
  - ai-feature-quality-rubric
  - bug-report-quality-rubric
  - llm-hallucination-test-patterns
  - prompt-injection-test-suite
---

# Ship a QA program for an AI-powered product

## Context

From zero, build the QA discipline for a product whose core value is an LLM/RAG/agent feature — eval sets, hallucination + safety tests, regression gates, production monitoring, and a bug-reporting rubric that captures prompt/seed/version

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: From zero, build the QA discipline for a product whose core value is an LLM/RAG/agent feature — eval sets, hallucination + safety tests, regression gates, production monitoring, and a bug-reporting rubric that captures prompt/seed/version.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Ship a QA program for an AI-powered product.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
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
- `geek/ai/rag-engineer/rag-eval-production-monitoring`

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
- `geek/ai/rag-engineer/rag-eval-strategy`

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
- `geek/ai/rag-engineer/rag-eval-test-set-generation`

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
- `pro/_gaps/ai-bug-repro-capture` (gap)

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
- `pro/_gaps/ai-feature-eval-set-design` (gap)

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
- `pro/_gaps/ai-feature-online-eval-loop` (gap)

Outputs:
- Runbook + on-call notes
- SLO + alert config in source control

### 8. Review

Close the loop with a written retro and clear next-cycle bets.

Tasks:
- Compile evidence trail + metrics from rollout
- Write retro: what worked, what didn't, what we are changing
- Decide explicit continue / iterate / kill for the next cycle

Methodologies:
- `pro/_gaps/ai-feature-quality-rubric` (gap)
- `pro/_gaps/bug-report-quality-rubric` (gap)
- `pro/_gaps/llm-hallucination-test-patterns` (gap)
- `pro/_gaps/prompt-injection-test-suite` (gap)

Outputs:
- Retro doc with evidence
- Continue / iterate / kill decision for next cycle

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.
- **Rollout** → Advance to the next cohort only after the previous is stable for the agreed window.
- **Operate** → Advance when on-call can resolve the top-3 likely incidents without the original author.
- **Review** → A written decision is mandatory; no 'see how it goes'.

## References

- `geek/ai/ml-engineer/model-evaluation`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `geek/ai/rag-engineer/rag-eval-strategy`
- `geek/ai/rag-engineer/rag-eval-test-set-generation`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `ai-bug-repro-capture` — bare-slug reference from source; methodology not yet authored
- `ai-feature-eval-set-design` — bare-slug reference from source; methodology not yet authored
- `ai-feature-online-eval-loop` — bare-slug reference from source; methodology not yet authored
- `ai-feature-quality-rubric` — bare-slug reference from source; methodology not yet authored
- `bug-report-quality-rubric` — bare-slug reference from source; methodology not yet authored
- `llm-hallucination-test-patterns` — bare-slug reference from source; methodology not yet authored
- `prompt-injection-test-suite` — bare-slug reference from source; methodology not yet authored
