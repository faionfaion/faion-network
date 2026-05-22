---
slug: weekly-prompt-version-ab-review
tier: geek
group: prompt-engineering
persona: P7
goal: operate-ritual
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Last week's prompt-version candidates → one merged, one rolled-back, one parked."
content_id: f93495ffa8eceaed
methodology_refs:
  - schema-version-pinning
  - prompt-cache-prefix-order
  - rag-eval-ab-testing
  - llm-judge-rubric-evidence-first
  - two-pass-reason-then-extract
  - prompt-engineering-evaluation
  - prompt-engineering-production
---

# Weekly prompt-version A/B review

**Playbook slug:** `weekly-prompt-version-ab-review`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

Last week's prompt-version candidates → one merged, one rolled-back, one parked.

## Scope

Decide which of last week's prompt-version candidates graduates to default. Output: one merged PR, one rolled-back PR, one parked. Weekly cadence, ~60-90 min.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Model-version A/Bs — covered by `bench-against-new-sota-model`
- End-to-end UX A/Bs

### Prerequisites

- A/B fixture from eval-harness playbook
- ≥2 prompt candidates with at least 100 traces each

## Success criteria

The playbook is done when:
- Each candidate scored on judge + cost
- Decision per candidate (merge/rollback/park)
- Pinned prompt version manifest updated

## Stages

### Stage 1: Pull A/B Results

**Intent:** Collect last week's A/B traces per candidate.

**Tasks:**
- Pull traces grouped by prompt version
- Confirm prompt-cache prefix order didn't change

**Methodologies in chain:**
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`
- `prompt-cache-prefix-order` → `geek/ai/ai-agents/prompt-cache-prefix-order`
- `rag-eval-ab-testing` → `geek/ai/rag-engineer/rag-eval-ab-testing`

**Outputs:**
- A/B trace bundle

**Decision gate:**
> Advance when each candidate has enough traces for power.

### Stage 2: Judge & Compare

**Intent:** Run judges, compare against control.

**Tasks:**
- Run rubric judge
- Two-pass reason-then-extract scoring
- Score cost + quality delta

**Methodologies in chain:**
- `llm-judge-rubric-evidence-first` → `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `two-pass-reason-then-extract` → `geek/ai/ai-agents/two-pass-reason-then-extract`
- `prompt-engineering-evaluation` → `geek/ai/ml-engineer/prompt-engineering-evaluation`
- `prompt-engineering-production` → `geek/ai/ml-engineer/prompt-engineering-production`

**Outputs:**
- Comparison table

**Decision gate:**
> Advance only when delta is statistically credible.

### Stage 3: Land Decisions

**Intent:** Three PRs: merge, rollback, park.

**Tasks:**
- Merge the winner with version pin
- Rollback the loser
- Park the inconclusive with calendar reminder

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Merged PR
- Rollback PR
- Parked tracking issue

**Decision gate:**
> Ship only after pin manifest is updated.

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
- **prompt-ab-power-calculator** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **prompt-version-pinning-runbook** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

The discipline of three outcomes — merge, rollback, park — exists to prevent the most common anti-pattern: leaving every candidate live indefinitely in the hope that 'we'll get back to it'. A merged prompt with an inconclusive A/B is technical debt; a rolled-back prompt is closed-loop learning; a parked candidate must have a calendar reminder or it dies in the backlog.

Power is the silent failure mode. If a candidate has fewer than ~100 traces, even a real lift looks like noise. The brainstorm flags `prompt-ab-power-calculator` as a gap; until authored, default to ≥200 traces per arm before scoring, and longer windows for rare intents.

Prompt-cache prefix order matters more than people expect. A small candidate that changes a leading paragraph invalidates the entire cache and shows a cost regression that has nothing to do with the candidate's quality. Always inspect cache hit rate as part of the comparison; if it dropped, the apparent cost regression may be cache invalidation, not prompt design.

Pin the merged version explicitly in the manifest. `prompt-version-pinning-runbook` is the second flagged gap; the pin is the artefact the rollback decision points at if next week's check fails. Without it, rollback is a guess.

## CLI usage

```
faion get-content weekly-prompt-version-ab-review --format md       # human-readable rendering
faion get-content weekly-prompt-version-ab-review --format context  # agent-optimised context bundle
faion get-content weekly-prompt-version-ab-review --format json     # raw structured form
```
