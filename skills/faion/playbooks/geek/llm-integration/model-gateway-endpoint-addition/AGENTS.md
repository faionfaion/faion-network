---
slug: model-gateway-endpoint-addition
tier: geek
group: llm-integration
persona: P7
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: New provider/model dropped → onboard as routable target without changing call sites.
content_id: 07508af4d07cf12d
methodology_refs:
  - llm-decision-framework
  - gateway-fallback-chain
  - preference-trained-router
  - role-specialized-models
  - model-evaluation
  - evaluation-benchmarks
---

# Model-gateway endpoint addition

**Playbook slug:** `model-gateway-endpoint-addition`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

New provider/model dropped → onboard as routable target without changing call sites.

## Scope

Onboard a new provider/model (e.g. new Sonnet, Gemini point release, local Ollama) as a routable target without changing call sites. ~half-day per model.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Building the gateway itself — see `multi-model-gateway-migration-portability`
- Bench against the new model — separate playbook

### Prerequisites

- Existing gateway adapter
- Eval suite green on current backends

## Success criteria

The playbook is done when:
- Adapter for new model wired
- Routing rule + fallback updated
- Eval run on the new backend
- Routing pinned with rollback

## Stages

### Stage 1: Wrap

**Intent:** Wire adapter behind unchanged call sites.

**Tasks:**
- Add adapter for new endpoint
- Confirm decision-framework signal

**Methodologies in chain:**
- `llm-decision-framework` → `geek/ai/ml-engineer/llm-decision-framework`

**Outputs:**
- Adapter PR

**Decision gate:**
> Advance only when call sites are unchanged.

### Stage 2: Route

**Intent:** Routing + fallback policy update.

**Tasks:**
- Update gateway fallback chain
- Update preference-trained router
- Pick role assignment

**Methodologies in chain:**
- `gateway-fallback-chain` → `geek/ai/ai-agents/gateway-fallback-chain`
- `preference-trained-router` → `geek/ai/ai-agents/preference-trained-router`
- `role-specialized-models` → `geek/ai/ai-agents/role-specialized-models`

**Outputs:**
- Updated routing manifest

**Decision gate:**
> Advance only when policy change is reviewable.

### Stage 3: Bench & Pin

**Intent:** Run eval; pin and ship.

**Tasks:**
- Bench on golden set
- Pin model id in manifest

**Methodologies in chain:**
- `model-evaluation` → `geek/ai/ml-engineer/model-evaluation`
- `evaluation-benchmarks` → `geek/ai/ml-ops/evaluation-benchmarks`

**Outputs:**
- Bench results
- Pin manifest update

**Decision gate:**
> Ship only when bench passes and rollback is one-line.

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
- **model-onboarding-checklist** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **gateway-adapter-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Half-day per model. This is a focused onboarding playbook, not the decision-to-bench playbook (see `bench-against-new-sota-model`). The decision to onboard should already be made before opening this playbook.

Adapter wrapping is the cheap stage but it is also the most fragile: a new endpoint with a slightly different request schema can silently change tool-calling semantics. Run the eval suite on the new adapter before wiring it into routing; a passing adapter is one whose outputs match the current backend on at least the happy-path golden set.

Routing policy changes are the second risk. Updating the gateway fallback chain or the preference-trained router without a shadow window is the most common cause of next-morning regressions. Default behaviour: the new endpoint enters the chain in fallback position only, not as a primary or preferred. Promote position only after observability shows it stable.

Role assignment depends on observed strengths. A new SOTA model often wins on planner roles before it wins on worker roles; assign by role, not by reputation. Pin the model id in the manifest with a content hash if the provider supports it; a silent model upgrade by the provider is indistinguishable from your own routing regression otherwise.

Brainstorm flags a model-onboarding-checklist and gateway adapter template as gaps. Until authored, copy the closest existing adapter.

## CLI usage

```
faion get-content model-gateway-endpoint-addition --format md       # human-readable rendering
faion get-content model-gateway-endpoint-addition --format context  # agent-optimised context bundle
faion get-content model-gateway-endpoint-addition --format json     # raw structured form
```
