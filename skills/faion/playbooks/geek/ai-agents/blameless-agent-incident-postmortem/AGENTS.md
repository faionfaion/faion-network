---
slug: blameless-agent-incident-postmortem
tier: geek
group: ai-agents
persona: P7
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Agent shipped hallucinated answer / mis-called tool / jailbroke itself → blameless postmortem attributes cause to layer, lands regression eval, prevents recurrence.
content_id: d809ed7f42157e57
methodology_refs:
  - record-replay-debugging
  - trajectory-eval-otel
  - chaos-eval-fault-injection
  - generator-critic-bounded-loop
  - inc-postmortem-auto-draft-no-publish
---

# Run a blameless agent-incident postmortem when the agent is the defendant

**Playbook slug:** `blameless-agent-incident-postmortem`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

Agent shipped hallucinated answer / mis-called tool / jailbroke itself → blameless postmortem attributes cause to layer, lands regression eval, prevents recurrence.

## Scope

When the agent ships a hallucinated answer, mis-calls a tool, or jailbreaks itself, the team produces a structured postmortem that attributes cause to model/prompt/tool/context layer, lands a regression eval, and prevents recurrence.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Customer comms response — out of scope
- Long-term architecture rewrite

### Prerequisites

- Trace of the incident
- Eval harness reachable

## Success criteria

The playbook is done when:
- Postmortem doc written
- Layer attribution: model / prompt / tool / context
- Regression eval row landed before fix
- Action items tracked

## Stages

### Stage 1: Reconstruct

**Intent:** Replay the bad trajectory.

**Tasks:**
- Pull trace
- Record-replay

**Methodologies in chain:**
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`

**Outputs:**
- Reproduced incident

**Decision gate:**
> Advance only when failure reproduces.

### Stage 2: Attribute

**Intent:** Layer-by-layer attribution with chaos cross-check.

**Tasks:**
- Chaos-eval cross-check
- Generator-critic bound check

**Methodologies in chain:**
- `chaos-eval-fault-injection` → `geek/ai/ai-agents/chaos-eval-fault-injection`
- `generator-critic-bounded-loop` → `geek/ai/ai-agents/generator-critic-bounded-loop`

**Outputs:**
- Attribution note

**Decision gate:**
> Advance only when one layer is clearly implicated.

### Stage 3: Prevent

**Intent:** Land regression eval + auto-draft postmortem.

**Tasks:**
- Add regression eval BEFORE the fix
- Auto-draft postmortem; gate publish
- Track action items

**Methodologies in chain:**
- `inc-postmortem-auto-draft-no-publish` → `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`

**Outputs:**
- Postmortem doc
- Eval row added

**Decision gate:**
> Close only when postmortem is signed and eval row landed.

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
- **agent-incident-postmortem-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **agent-failure-taxonomy** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **regression-eval-before-fix-rule** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Blameless means the agent is the defendant, not a human. The point is to produce a structural fix and a regression eval, not to assign moral responsibility to the prompt author. If the postmortem reads like a performance review, redraft.

Reconstruct first, attribute second. Record-replay is the precondition. Without a reproducible failure, attribution becomes opinion. If the incident does not reproduce, the postmortem itself must document the non-determinism and what change would make the next one reproducible.

Layer attribution discipline: model / prompt / tool / context. Cheap answers like 'the model hallucinated' are almost always wrong; the real cause is usually context (compaction, retrieval) or tool (silent error, wrong schema). Cross-check with chaos-eval fault injection: if injecting the suspected failure reproduces the incident, you have the layer.

The regression eval must land BEFORE the fix. This is the only mechanism that prevents recurrence: a fix without a regression row is a fix that the next refactor silently undoes. Auto-draft the postmortem during reconstruction so the team is not writing from scratch; gate publication behind a sign-off review.

Brainstorm flags agent-incident-postmortem-template, agent-failure-taxonomy, and regression-eval-before-fix-rule as open gaps. Use the auto-draft template from `inc-postmortem-auto-draft-no-publish` as the interim shape.

## CLI usage

```
faion get-content blameless-agent-incident-postmortem --format md       # human-readable rendering
faion get-content blameless-agent-incident-postmortem --format context  # agent-optimised context bundle
faion get-content blameless-agent-incident-postmortem --format json     # raw structured form
```
