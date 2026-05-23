# Vertical agent: prototype to production (8 weeks)

## Context

Single-vertical agent (e.g. AI SDR, code-review bot, support triage) goes from blank repo to a paying customer-zero workload on production traffic, with eval harness, observability, drift detection and rollback in place.

## Outcome

By the end of this playbook, the operator has run the 7 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 7 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Define the Job

Pick one narrow vertical to win.

Tasks:
- Write the vertical's job-to-be-done and the surrounding workflow
- Pick the boundary: what the agent does vs what it hands to humans
- Define success criteria the buyer cares about

Outputs:
- JTBD + workflow map
- agent-vs-human boundary
- success criteria

Decision gate: Advance only when JTBD and boundary are written.

### 2. Prototype

Cheapest working agent that runs end-to-end.

Tasks:
- Design the agent flow (tools, prompts, memory)
- Implement with the strongest available model first
- Run on 10 real cases; log outcomes

Outputs:
- agent design
- running prototype
- 10-case log

Decision gate: Advance only when the prototype completes ≥7/10 cases acceptably.

### 3. Stand Up Evals

You can't ship what you can't measure.

Tasks:
- Define evals for accuracy, safety, latency, cost
- Build the eval harness with golden cases
- Run the eval against the current prototype

Outputs:
- eval definitions
- harness running
- baseline eval results

Decision gate: Advance only when baseline meets the buyer's accuracy bar.

### 4. Harden

Closed-set behaviour; observability on.

Tasks:
- Add guardrails (prompt-injection, rate-limit, output-validation)
- Add structured logging and traces per step
- Run failure-mode tests; fix top-3

Outputs:
- guardrails impl
- structured logs + traces
- top-3 failure fixes

Decision gate: Advance only when guardrails pass the failure-mode tests.

### 5. Pilot With 3 Customers

Real users; not your friends.

Tasks:
- Sign 3 pilot customers with a written agreement
- Onboard each with a tailored deployment
- Run weekly review with each pilot

Outputs:
- pilot agreements
- deployment runbook
- weekly pilot reviews

Decision gate: Advance only when at least 2 pilots reach the success criteria.

### 6. Ship to Production

GA with the eval bar protecting the floor.

Tasks:
- Roll out via flag with eval-gated promotion
- Stand up the on-call + drift monitoring
- Open the order form for new customers

Outputs:
- flag rollout
- on-call + drift monitoring
- open order form

Decision gate: Advance when post-GA evals stay above bar for 7 days.

### 7. Iterate

Each customer is a learning loop.

Tasks:
- Run weekly eval review with the harness
- Iterate prompts, tools, and guardrails on real signal
- Decide quarterly: deepen / pivot / kill

Outputs:
- weekly eval review
- iteration log
- deepen/pivot/kill memo

Decision gate: Required output: a written quarterly go-forward decision.

## Decision points

- Stage 1 (Define the Job): Advance only when JTBD and boundary are written.
- Stage 2 (Prototype): Advance only when the prototype completes ≥7/10 cases acceptably.
- Stage 3 (Stand Up Evals): Advance only when baseline meets the buyer's accuracy bar.
- Stage 4 (Harden): Advance only when guardrails pass the failure-mode tests.
- Stage 5 (Pilot With 3 Customers): Advance only when at least 2 pilots reach the success criteria.
- Stage 6 (Ship to Production): Advance when post-GA evals stay above bar for 7 days.
- Stage 7 (Iterate): Required output: a written quarterly go-forward decision.

## References

- `bundle-vs-split-tools`
- `chaos-eval-fault-injection`
- `cheap-guardrail-tripwire`
- `claude-code-headless-default`
- `compaction-preserve-refs`
- `confidence-thresholded-cascade`
- `discriminated-union-output`
- `embedded-scratchpad-field`
- `field-descriptions-as-prompts`
- `filesystem-as-working-memory`
- `gateway-fallback-chain`
- `handoff-id-payload`
- `headless-cli-four-guards`
- `idempotent-write-tools`
- `inverted-header-content-first`
- `llm-judge-rubric-evidence-first`
- `max-turns-circuit-breaker`
- `plan-execute-vs-react`
- `posttool-hook-self-correction`
- `preference-trained-router`
- `prompt-cache-prefix-order`
- `reasoning-first-architectures`
- `record-replay-debugging`
- `refusal-field-strict-schema`
- `role-specialized-models`
- `semantic-field-naming`
- `strict-mode-required-fields`
- `structured-tool-errors`
- `tool-description-as-prompt`
- `trajectory-eval-otel`
- `two-pass-reason-then-extract`
- `verb-object-tool-naming`
- `weak-model-preselection`
- `semantic-xml-content`
- `agents-framework-selection`
- `agents-memory-system`
- `agents-production-deployment`
- `agents-react-pattern`
- `cost-optimization`
- `llm-observability-stack`
- `model-evaluation`
- `rag-evaluation`
- `cost-reduction-strategies`
- `evaluation-benchmarks`
- `evaluation-framework`
- `evaluation-metrics`
- `llm-cost-basics`
- `llm-observability-stack-2026`
- `rag-eval-production-monitoring`
- `inc-runbook-as-markdown-tagged-steps`
- `inc-tool-tier-approval-gate`

Gaps (status: draft until empty):
- `agent-customer-zero-pilot-protocol` (see `gaps[]` in `playbook.yaml`)
- `agent-ga-readiness-checklist` (see `gaps[]` in `playbook.yaml`)
- `agent-rollback-button-design` (see `gaps[]` in `playbook.yaml`)
