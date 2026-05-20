# Agent-state debug session (cursor + replay)

**Playbook slug:** `agent-state-debug-cursor-replay-session`  
**Tier:** geek  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

Agent ran 40 turns and lost the plot → reconstruct trajectory, find bad transition, ship a guardrail.

## Scope

An agent ran 40 turns and lost the plot. Reconstruct the trajectory, find the bad state transition, ship a guardrail. Intended for one focused debug session per incident.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Full incident postmortem — see blameless playbook
- Cost optimization — see daily watch

### Prerequisites

- Full trace of the failing run
- Local replay environment

## Success criteria

The playbook is done when:
- Bad state transition isolated
- Cause categorized: context bleed / tool error / planner divergence
- Guardrail shipped
- Regression eval row added

## Stages

### Stage 1: Replay

**Intent:** Reconstruct trajectory locally.

**Tasks:**
- Pull trace + OTEL spans
- Record-replay the full run

**Methodologies in chain:**
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`

**Outputs:**
- Local replay log

**Decision gate:**
> Advance only when local run reproduces the failure.

### Stage 2: Inspect

**Intent:** Find the bad transition.

**Tasks:**
- Inspect scratchpad field
- Inspect filesystem memory state
- Check auto-eviction history
- Audit compaction preserve-refs

**Methodologies in chain:**
- `embedded-scratchpad-field` → `geek/ai/ai-agents/embedded-scratchpad-field`
- `filesystem-as-working-memory` → `geek/ai/ai-agents/filesystem-as-working-memory`
- `auto-evict-tool-results` → `geek/ai/ai-agents/auto-evict-tool-results`
- `compaction-preserve-refs` → `geek/ai/ai-agents/compaction-preserve-refs`
- `subagent-as-context-firewall` → `geek/ai/ai-agents/subagent-as-context-firewall`

**Outputs:**
- Annotated trajectory

**Decision gate:**
> Advance only when a single bad transition is named.

### Stage 3: Categorize

**Intent:** Layer attribution: planner / executor / memory / tool.

**Tasks:**
- Check plan-execute vs ReAct mismatch
- Inspect generator-critic loop bound
- Check posttool hook firing
- Verify max-turns circuit breaker

**Methodologies in chain:**
- `plan-execute-vs-react` → `geek/ai/ai-agents/plan-execute-vs-react`
- `generator-critic-bounded-loop` → `geek/ai/ai-agents/generator-critic-bounded-loop`
- `posttool-hook-self-correction` → `geek/ai/ai-agents/posttool-hook-self-correction`
- `max-turns-circuit-breaker` → `geek/ai/ai-agents/max-turns-circuit-breaker`
- `chaos-eval-fault-injection` → `geek/ai/ai-agents/chaos-eval-fault-injection`

**Outputs:**
- Failure category note

**Decision gate:**
> Advance only when category is decided.

### Stage 4: Guardrail

**Intent:** Ship guardrail + add regression eval.

**Tasks:**
- Ship guardrail PR
- Add row to permanent eval

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Guardrail PR
- Eval row

**Decision gate:**
> Close session only after PR is merged.

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
- **agent-replay-harness-cookbook** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **context-bleed-detection-recipe** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## CLI usage

```
faion get-content agent-state-debug-cursor-replay-session --format md       # human-readable rendering
faion get-content agent-state-debug-cursor-replay-session --format context  # agent-optimised context bundle
faion get-content agent-state-debug-cursor-replay-session --format json     # raw structured form
```
