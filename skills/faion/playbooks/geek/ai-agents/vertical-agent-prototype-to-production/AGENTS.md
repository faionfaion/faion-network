---
slug: vertical-agent-prototype-to-production
tier: geek
group: ai-agents
persona: P7
goal: build-ship
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Blank repo on Monday → vertical agent with paying customer-zero workload on production, eval harness, observability, drift detection, rollback button.
content_id: 884e3446ae97fa78
methodology_refs:
  - plan-execute-vs-react
  - reasoning-first-architectures
  - claude-code-headless-default
  - agents-react-pattern
  - agents-framework-selection
  - discriminated-union-output
  - refusal-field-strict-schema
  - strict-mode-required-fields
  - field-descriptions-as-prompts
  - semantic-field-naming
  - tool-description-as-prompt
  - verb-object-tool-naming
  - bundle-vs-split-tools
  - idempotent-write-tools
  - structured-tool-errors
  - semantic-xml-content
  - two-pass-reason-then-extract
  - embedded-scratchpad-field
  - filesystem-as-working-memory
  - compaction-preserve-refs
  - prompt-cache-prefix-order
  - handoff-id-payload
  - agents-memory-system
  - inverted-header-content-first
  - cheap-guardrail-tripwire
  - confidence-thresholded-cascade
  - weak-model-preselection
  - role-specialized-models
  - preference-trained-router
  - gateway-fallback-chain
  - max-turns-circuit-breaker
  - posttool-hook-self-correction
  - headless-cli-four-guards
  - cost-optimization
  - cost-reduction-strategies
  - llm-cost-basics
  - llm-judge-rubric-evidence-first
  - chaos-eval-fault-injection
  - record-replay-debugging
  - trajectory-eval-otel
  - model-evaluation
  - rag-evaluation
  - evaluation-benchmarks
  - evaluation-framework
  - evaluation-metrics
  - agents-production-deployment
  - llm-observability-stack
  - llm-observability-stack-2026
  - rag-eval-production-monitoring
  - inc-runbook-as-markdown-tagged-steps
  - inc-tool-tier-approval-gate
---

# Vertical agent: prototype to production (8 weeks)

**Playbook slug:** `vertical-agent-prototype-to-production`  
**Tier:** geek  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

Blank repo on Monday → vertical agent with paying customer-zero workload on production, eval harness, observability, drift detection, rollback button.

## Scope

Single-vertical agent (e.g. AI SDR, code-review bot, support triage) goes from blank repo to a paying customer-zero workload on production traffic, with eval harness, observability, drift detection and rollback in place. Covers prototype, eval bootstrap, hardening, customer-zero pilot, and GA rollout.

### Non-goals

- Horizontal multi-tenant platforms — out of scope, single vertical only
- Frontier-model research — uses available models off the shelf

### Prerequisites

- Defined vertical use case with a buyer who will pilot
- Access to one frontier model API + one open-weight fallback

## Success criteria

The playbook is done when:
- Working agent on production traffic for customer-zero
- CI-gated eval harness with golden trajectories
- OTEL trajectory traces visible per request
- Drift detector firing on cost/quality/refusal anomalies
- One-click rollback validated under chaos test
- GA-readiness checklist signed off

## Stages

### Stage 1: Prototype

**Intent:** Spike a working agent loop on the vertical task with one frontier model.

**Tasks:**
- Pick agent pattern: plan-execute vs ReAct
- Define tool surface and output schema
- Run end-to-end on 10 golden tasks

**Methodologies in chain:**
- `plan-execute-vs-react` → `geek/ai/ai-agents/plan-execute-vs-react`
- `reasoning-first-architectures` → `geek/ai/ai-agents/reasoning-first-architectures`
- `claude-code-headless-default` → `geek/ai/ai-agents/claude-code-headless-default`
- `agents-react-pattern` → `geek/ai/ml-engineer/agents-react-pattern`
- `agents-framework-selection` → `geek/ai/ml-engineer/agents-framework-selection`

**Outputs:**
- Prototype repo with one-command run
- 10 trace recordings of golden tasks

**Decision gate:**
> Advance if ≥7/10 golden tasks complete without manual recovery.

### Stage 2: Schema & Tools

**Intent:** Lock structured outputs and tool contracts before scaling traffic.

**Tasks:**
- Draft strict schema with refusal field
- Name tools verb-object; describe as prompts
- Decide bundle-vs-split per tool

**Methodologies in chain:**
- `discriminated-union-output` → `geek/ai/ai-agents/discriminated-union-output`
- `refusal-field-strict-schema` → `geek/ai/ai-agents/refusal-field-strict-schema`
- `strict-mode-required-fields` → `geek/ai/ai-agents/strict-mode-required-fields`
- `field-descriptions-as-prompts` → `geek/ai/ai-agents/field-descriptions-as-prompts`
- `semantic-field-naming` → `geek/ai/ai-agents/semantic-field-naming`
- `tool-description-as-prompt` → `geek/ai/ai-agents/tool-description-as-prompt`
- `verb-object-tool-naming` → `geek/ai/ai-agents/verb-object-tool-naming`
- `bundle-vs-split-tools` → `geek/ai/ai-agents/bundle-vs-split-tools`
- `idempotent-write-tools` → `geek/ai/ai-agents/idempotent-write-tools`
- `structured-tool-errors` → `geek/ai/ai-agents/structured-tool-errors`
- `semantic-xml-content` → `geek/ai/llm-integration/semantic-xml-content`
- `two-pass-reason-then-extract` → `geek/ai/ai-agents/two-pass-reason-then-extract`

**Outputs:**
- Versioned schema doc
- Tool registry with descriptions

**Decision gate:**
> Advance when schema validates 100% on golden trace replay.

### Stage 3: Memory & Context

**Intent:** Decide how agent carries state across turns and what gets evicted.

**Tasks:**
- Pick scratchpad vs filesystem memory
- Set compaction policy preserving refs
- Order prompt for cache prefix reuse

**Methodologies in chain:**
- `embedded-scratchpad-field` → `geek/ai/ai-agents/embedded-scratchpad-field`
- `filesystem-as-working-memory` → `geek/ai/ai-agents/filesystem-as-working-memory`
- `compaction-preserve-refs` → `geek/ai/ai-agents/compaction-preserve-refs`
- `prompt-cache-prefix-order` → `geek/ai/ai-agents/prompt-cache-prefix-order`
- `handoff-id-payload` → `geek/ai/ai-agents/handoff-id-payload`
- `agents-memory-system` → `geek/ai/ml-engineer/agents-memory-system`
- `inverted-header-content-first` → `geek/ai/ai-agents/inverted-header-content-first`

**Outputs:**
- Memory architecture doc
- Cache-hit baseline metric

**Decision gate:**
> Advance when context stays under budget on the longest trace.

### Stage 4: Guardrails & Routing

**Intent:** Insert cheap guardrails, model cascade, and circuit breakers.

**Tasks:**
- Wire cheap-guardrail tripwires on tool inputs
- Add weak-model preselection and cascade
- Cap turns with circuit breaker

**Methodologies in chain:**
- `cheap-guardrail-tripwire` → `geek/ai/ai-agents/cheap-guardrail-tripwire`
- `confidence-thresholded-cascade` → `geek/ai/ai-agents/confidence-thresholded-cascade`
- `weak-model-preselection` → `geek/ai/ai-agents/weak-model-preselection`
- `role-specialized-models` → `geek/ai/ai-agents/role-specialized-models`
- `preference-trained-router` → `geek/ai/ai-agents/preference-trained-router`
- `gateway-fallback-chain` → `geek/ai/ai-agents/gateway-fallback-chain`
- `max-turns-circuit-breaker` → `geek/ai/ai-agents/max-turns-circuit-breaker`
- `posttool-hook-self-correction` → `geek/ai/ai-agents/posttool-hook-self-correction`
- `headless-cli-four-guards` → `geek/ai/ai-agents/headless-cli-four-guards`
- `cost-optimization` → `geek/ai/ml-engineer/cost-optimization`
- `cost-reduction-strategies` → `geek/ai/ml-ops/cost-reduction-strategies`
- `llm-cost-basics` → `geek/ai/ml-ops/llm-cost-basics`

**Outputs:**
- Cascade policy doc
- Cost-per-success baseline

**Decision gate:**
> Advance if cost-per-success ≤ budget on golden set.

### Stage 5: Eval Harness

**Intent:** CI-gated eval harness with judges and chaos pack before pilot traffic.

**Tasks:**
- Author rubric-evidence judge
- Add chaos-eval fault injection
- Wire trajectory OTEL evals

**Methodologies in chain:**
- `llm-judge-rubric-evidence-first` → `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `chaos-eval-fault-injection` → `geek/ai/ai-agents/chaos-eval-fault-injection`
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`
- `model-evaluation` → `geek/ai/ml-engineer/model-evaluation`
- `rag-evaluation` → `geek/ai/ml-engineer/rag-evaluation`
- `evaluation-benchmarks` → `geek/ai/ml-ops/evaluation-benchmarks`
- `evaluation-framework` → `geek/ai/ml-ops/evaluation-framework`
- `evaluation-metrics` → `geek/ai/ml-ops/evaluation-metrics`

**Outputs:**
- CI job that blocks regression
- Adversarial pack

**Decision gate:**
> Advance when every prompt/model PR runs the suite.

### Stage 6: Pilot & GA

**Intent:** Customer-zero pilot, then GA with rollback wired.

**Tasks:**
- Run agent on real customer traffic shadow first
- Wire incident runbook + tier-approval gate
- Cut GA with rollback validated

**Methodologies in chain:**
- `agents-production-deployment` → `geek/ai/ml-engineer/agents-production-deployment`
- `llm-observability-stack` → `geek/ai/ml-engineer/llm-observability-stack`
- `llm-observability-stack-2026` → `geek/ai/ml-ops/llm-observability-stack-2026`
- `rag-eval-production-monitoring` → `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `inc-tool-tier-approval-gate` → `geek/sdlc-ai/inc-tool-tier-approval-gate`

**Outputs:**
- Pilot report with N failure modes
- GA cutover plan

**Decision gate:**
> Advance only after rollback button is exercised in chaos test.

## Common pitfalls

- Treating eval scores as ground truth without judge calibration
- Shipping prompt or model changes without a regression gate
- Skipping shadow rollout for routing or model swaps

## Quality checklist (self-review)

- Can I roll back this change in one step?
- Is the regression eval committed BEFORE the fix?
- Are tool / schema versions pinned in the manifest?

## Related playbooks

- `eval-harness-continuous-benchmark-suite`
- `agent-observability-drift-detection-rollout`
- `production-agent-eval-harness-week-1`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **agent-customer-zero-pilot-protocol** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **agent-ga-readiness-checklist** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **agent-rollback-button-design** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Treat this playbook as a six-stage gate sequence, not a linear waterfall. The Prototype stage is deliberately cheap so you can throw it away if the tool surface needs to change. The single most common failure mode is skipping the Schema & Tools stage and discovering at the Eval Harness stage that the agent emits free-form text — that means the entire trace set must be re-recorded. Lock the schema before measuring anything.

Customer-zero pilot is the riskiest step because it is the first moment the agent sees adversarial traffic. Run it in shadow first if at all possible, even if the customer is a friendly design partner. The brainstorm marks three explicit gaps for this playbook: an agent-customer-zero pilot protocol, an agent-GA-readiness checklist, and an agent-rollback-button design doc. Until those are authored, the operator must improvise them per-deploy.

Cost is the second risk. Stage 4 ends with a cost-per-success baseline; if that baseline already exceeds plan, do not advance to the Eval Harness stage. Instead return to Schema & Tools and consider a cascade-only architecture (Stage 4 covers the patterns).

Finally, the rollback button is not a separate stage on purpose: it must be exercised inside the Pilot & GA decision gate. If you cannot rollback during a chaos test, you do not have GA readiness. Roll back the deploy, not just the prompt.

## CLI usage

```
faion get-content vertical-agent-prototype-to-production --format md       # human-readable rendering
faion get-content vertical-agent-prototype-to-production --format context  # agent-optimised context bundle
faion get-content vertical-agent-prototype-to-production --format json     # raw structured form
```
