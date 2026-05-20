# Bench against new SOTA model

**Playbook slug:** `bench-against-new-sota-model`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

New frontier or open-weight model dropped → decide within a day whether it enters cascade, replaces a tier, or is shelved.

## Scope

A new frontier or open-weight model dropped. Decide within a day whether it enters the cascade, replaces a tier, or is shelved. Goal: ship the decision same day with cost+quality table.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Re-architecting the agent — out of scope
- Long-term capability research

### Prerequisites

- Eval harness with golden + adversarial sets
- Gateway adapter for the new model

## Success criteria

The playbook is done when:
- Bench results on golden + adversarial
- Cost+quality pareto plotted
- Decision: enter cascade / replace tier / shelve
- Decision logged with evidence

## Stages

### Stage 1: Onboard

**Intent:** Wire the model behind adapter; pin schema.

**Tasks:**
- Wire endpoint
- Pin response schema version

**Methodologies in chain:**
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`
- `previous-response-id-reasoning-reuse` → `geek/ai/ai-agents/previous-response-id-reasoning-reuse`

**Outputs:**
- New adapter live

**Decision gate:**
> Advance only when adapter calls succeed.

### Stage 2: Bench

**Intent:** Run golden + adversarial sets.

**Tasks:**
- Run golden eval
- Run adversarial eval
- Inspect refusal field behaviour

**Methodologies in chain:**
- `evaluation-benchmarks` → `geek/ai/ml-ops/evaluation-benchmarks`
- `llm-decision-framework` → `geek/ai/ml-engineer/llm-decision-framework`
- `refusal-field-strict-schema` → `geek/ai/ai-agents/refusal-field-strict-schema`

**Outputs:**
- Bench table

**Decision gate:**
> Advance only when both sets ran end-to-end.

### Stage 3: Decide

**Intent:** Cascade / replace / shelve.

**Tasks:**
- Plot cost-quality pareto
- Pick router placement
- Decide on confidence cascade
- Pick role assignment if specialized
- Confirm reasoning-first architecture if applicable

**Methodologies in chain:**
- `preference-trained-router` → `geek/ai/ai-agents/preference-trained-router`
- `confidence-thresholded-cascade` → `geek/ai/ai-agents/confidence-thresholded-cascade`
- `role-specialized-models` → `geek/ai/ai-agents/role-specialized-models`
- `reasoning-first-architectures` → `geek/ai/ai-agents/reasoning-first-architectures`

**Outputs:**
- Decision doc

**Decision gate:**
> Ship only when decision is one of: cascade / replace / shelve.

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
- **sota-onboarding-1day-runbook** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **cost-quality-pareto-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## CLI usage

```
faion get-content bench-against-new-sota-model --format md       # human-readable rendering
faion get-content bench-against-new-sota-model --format context  # agent-optimised context bundle
faion get-content bench-against-new-sota-model --format json     # raw structured form
```
