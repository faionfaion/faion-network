# Embed RAG into an existing product

## Context

Ship a tier-1 RAG feature (retrieval-grounded answers over the product's own corpus) from kickoff to GA: ingestion pipeline live, chunking + embeddings tuned, hybrid retrieval + reranking deployed, eval harness in CI, p95 latency + cost SLOs met, on-call runbook handed to ops.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Ship a tier-1 RAG feature (retrieval-grounded answers over the product's own corpus) from kickoff to GA: ingestion pipeline live, chunking + embeddings tuned, hybrid retrieval + reranking deployed, eval harness in CI, p95 latency + cost SLOs met, on-call runbook handed to ops.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Embed RAG into an existing product.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `geek/ai/ml-engineer/cost-optimization`
- `geek/ai/ml-engineer/embeddings-evaluation`
- `geek/ai/ml-engineer/guardrails-concepts`
- `geek/ai/ml-engineer/guardrails-custom-pipeline`

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
- `geek/ai/ml-engineer/llm-decision-framework`
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/structured-output`
- `geek/ai/ml-engineer/vector-db-index-tuning`

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
- `geek/ai/ml-engineer/vector-db-setup-prod`
- `geek/ai/rag-engineer/chunking-document-structure`
- `geek/ai/rag-engineer/chunking-production-service`
- `geek/ai/rag-engineer/chunking-semantic`

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
- `geek/ai/rag-engineer/db-comparison`
- `geek/ai/rag-engineer/embedding-caching`
- `geek/ai/rag-engineer/embedding-model-selection`
- `geek/ai/rag-engineer/hybrid-search-basics`

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
- `geek/ai/rag-engineer/hybrid-search-implementation`
- `geek/ai/rag-engineer/rag-architecture`
- `geek/ai/rag-engineer/rag-eval-ab-testing`
- `geek/ai/rag-engineer/rag-eval-generation-metrics`

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
- `geek/ai/rag-engineer/rag-eval-pipeline`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `geek/ai/rag-engineer/rag-eval-retrieval-metrics`
- `geek/ai/rag-engineer/rag-eval-strategy`

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
- `geek/ai/rag-engineer/rag-eval-test-set-generation`
- `geek/ai/rag-engineer/reranking-pipeline-integration`
- `geek/ai/rag-engineer/reranking-two-stage`
- `geek/ai/rag-engineer/vector-database-setup`

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
- `geek/_gaps/model-routing-cheap-vs-strong` (gap)
- `geek/_gaps/prompt-caching-strategy` (gap)
- `geek/_gaps/llm-as-judge-harness` (gap)
- `geek/_gaps/rag-hybrid-search-bm25-vector` (gap)
- `geek/_gaps/rag-reranking` (gap)
- `geek/_gaps/retrieval-evaluation-ragas` (gap)

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

- `geek/ai/ml-engineer/cost-optimization`
- `geek/ai/ml-engineer/embeddings-evaluation`
- `geek/ai/ml-engineer/guardrails-concepts`
- `geek/ai/ml-engineer/guardrails-custom-pipeline`
- `geek/ai/ml-engineer/llm-decision-framework`
- `geek/ai/ml-engineer/llm-observability-stack`
- `geek/ai/ml-engineer/structured-output`
- `geek/ai/ml-engineer/vector-db-index-tuning`
- `geek/ai/ml-engineer/vector-db-setup-prod`
- `geek/ai/rag-engineer/chunking-document-structure`
- `geek/ai/rag-engineer/chunking-production-service`
- `geek/ai/rag-engineer/chunking-semantic`
- `geek/ai/rag-engineer/db-comparison`
- `geek/ai/rag-engineer/embedding-caching`
- `geek/ai/rag-engineer/embedding-model-selection`
- `geek/ai/rag-engineer/hybrid-search-basics`
- `geek/ai/rag-engineer/hybrid-search-implementation`
- `geek/ai/rag-engineer/rag-architecture`
- `geek/ai/rag-engineer/rag-eval-ab-testing`
- `geek/ai/rag-engineer/rag-eval-generation-metrics`
- `geek/ai/rag-engineer/rag-eval-pipeline`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `geek/ai/rag-engineer/rag-eval-retrieval-metrics`
- `geek/ai/rag-engineer/rag-eval-strategy`
- `geek/ai/rag-engineer/rag-eval-test-set-generation`
- `geek/ai/rag-engineer/reranking-pipeline-integration`
- `geek/ai/rag-engineer/reranking-two-stage`
- `geek/ai/rag-engineer/vector-database-setup`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `model-routing-cheap-vs-strong` — referenced in source brainstorm but not yet authored
- `prompt-caching-strategy` — referenced in source brainstorm but not yet authored
- `llm-as-judge-harness` — referenced in source brainstorm but not yet authored
- `rag-hybrid-search-bm25-vector` — referenced in source brainstorm but not yet authored
- `rag-reranking` — referenced in source brainstorm but not yet authored
- `retrieval-evaluation-ragas` — referenced in source brainstorm but not yet authored
- `rag-corpus-discovery-interview` — listed in gaps_for_this_playbook from source brainstorm
- `rag-feature-acceptance-contract` — listed in gaps_for_this_playbook from source brainstorm
- `rag-canary-rollout-plan` — listed in gaps_for_this_playbook from source brainstorm
