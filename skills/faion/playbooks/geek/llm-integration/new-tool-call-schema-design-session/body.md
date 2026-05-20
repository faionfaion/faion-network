# New tool-call schema design session

**Playbook slug:** `new-tool-call-schema-design-session`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

Add or change a tool the agent can invoke → ship versioned schema + structured error contract + eval entries, no breaking change in prod.

## Scope

Add or change one tool the agent can invoke; ship a versioned schema + structured error contract + eval entries; no breaking change in prod. Single-session focused work, ~half-day.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Multi-tool refactors — split into separate sessions
- Tool-deprecation lifecycle — see future playbook

### Prerequisites

- Tool spec written
- Eval harness reachable

## Success criteria

The playbook is done when:
- Versioned schema landed
- Structured error contract documented
- Eval rows covering happy + failure paths
- Backward-compat confirmed in shadow

## Stages

### Stage 1: Design

**Intent:** Name, scope, and describe the tool as a prompt.

**Tasks:**
- Verb-object name
- Description-as-prompt
- Decide bundle vs split

**Methodologies in chain:**
- `verb-object-tool-naming` → `geek/ai/ai-agents/verb-object-tool-naming`
- `tool-description-as-prompt` → `geek/ai/ai-agents/tool-description-as-prompt`
- `bundle-vs-split-tools` → `geek/ai/ai-agents/bundle-vs-split-tools`
- `field-descriptions-as-prompts` → `geek/ai/ai-agents/field-descriptions-as-prompts`

**Outputs:**
- Tool card draft

**Decision gate:**
> Advance once description passes 'an LLM should know when to call this' read.

### Stage 2: Schema

**Intent:** Strict required fields + structured errors.

**Tasks:**
- Strict-mode required fields
- Structured error contract
- Idempotent write semantics
- Cheap guardrail tripwires on inputs

**Methodologies in chain:**
- `strict-mode-required-fields` → `geek/ai/ai-agents/strict-mode-required-fields`
- `structured-tool-errors` → `geek/ai/ai-agents/structured-tool-errors`
- `idempotent-write-tools` → `geek/ai/ai-agents/idempotent-write-tools`
- `cheap-guardrail-tripwire` → `geek/ai/ai-agents/cheap-guardrail-tripwire`
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`
- `tool-use-function-calling` → `geek/ai/ml-engineer/tool-use-function-calling`
- `guardrails-custom-pipeline` → `geek/ai/ml-engineer/guardrails-custom-pipeline`

**Outputs:**
- Schema v.x.y.z
- Error code table

**Decision gate:**
> Advance only when schema passes contract tests.

### Stage 3: Eval & Ship

**Intent:** Eval rows + shadow rollout.

**Tasks:**
- Add happy + failure rows to golden set
- Shadow-call in production
- Promote on green

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Eval rows added
- Tool live behind flag

**Decision gate:**
> Promote only when shadow is green and no regressions.

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
- **tool-deprecation-lifecycle** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **tool-card-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## CLI usage

```
faion get-content new-tool-call-schema-design-session --format md       # human-readable rendering
faion get-content new-tool-call-schema-design-session --format context  # agent-optimised context bundle
faion get-content new-tool-call-schema-design-session --format json     # raw structured form
```
