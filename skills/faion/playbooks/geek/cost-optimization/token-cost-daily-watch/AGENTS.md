---
slug: token-cost-daily-watch
tier: geek
group: cost-optimization
persona: P7
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Catch cost spikes within 24h → decide if model-routing, caching, or context-engineering change is needed before billing close.
content_id: 49d1263590815ca2
methodology_refs:
  - llm-observability
  - cost-optimization
  - llm-cost-basics
  - prompt-cache-prefix-order
  - confidence-thresholded-cascade
  - weak-model-preselection
  - max-turns-circuit-breaker
  - batch-cache-stack
---

# Token-cost daily watch

**Playbook slug:** `token-cost-daily-watch`  
**Tier:** geek  
**Complexity:** light  
**Persona:** P7 — LLM Agent Developer

## Intent

Catch cost spikes within 24h → decide if model-routing, caching, or context-engineering change is needed before billing close.

## Scope

Catch cost spikes within 24h. Decide if model-routing, caching, or context-engineering change is needed before billing close. ~15 min daily.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Long-term cost reforecasting — separate playbook
- Vendor contract negotiation

### Prerequisites

- Per-trajectory cost tagged in OTEL
- Cost dashboard reachable

## Success criteria

The playbook is done when:
- Today's $/success measured
- Spike threshold breached → action picked
- Daily log line written

## Stages

### Stage 1: Read

**Intent:** Pull last 24h cost-per-success.

**Tasks:**
- Pull token usage and success counts
- Compare against trailing 7-day median

**Methodologies in chain:**
- `llm-observability` → `geek/ai/ml-engineer/llm-observability`
- `cost-optimization` → `geek/ai/ml-engineer/cost-optimization`
- `llm-cost-basics` → `geek/ai/ml-ops/llm-cost-basics`

**Outputs:**
- Daily cost line

**Decision gate:**
> Advance to Decide only when above SLO band.

### Stage 2: Decide Lever

**Intent:** Pick lever: routing / caching / context.

**Tasks:**
- Audit prompt-cache hit rate
- Inspect cascade for over-spend on weak path
- Cap max turns
- Batch cache where applicable

**Methodologies in chain:**
- `prompt-cache-prefix-order` → `geek/ai/ai-agents/prompt-cache-prefix-order`
- `confidence-thresholded-cascade` → `geek/ai/ai-agents/confidence-thresholded-cascade`
- `weak-model-preselection` → `geek/ai/ai-agents/weak-model-preselection`
- `max-turns-circuit-breaker` → `geek/ai/ai-agents/max-turns-circuit-breaker`
- `batch-cache-stack` → `geek/ai/ai-agents/batch-cache-stack`

**Outputs:**
- Lever decision note

**Decision gate:**
> Advance only when a single lever is picked.

### Stage 3: Ship Or Log

**Intent:** Ship the cheapest lever or schedule for tomorrow.

**Tasks:**
- Land lever PR or schedule
- Write one-line daily log

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Daily cost log entry

**Decision gate:**
> Close ritual only after log entry is written.

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
- **cost-slo-per-task-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **cache-hit-audit-script** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Daily ritual, ~15 minutes. The point is to catch cost spikes within the billing window, not to optimize forever. If today's number is in band, write the one-line log and move on; do not over-engineer.

$/success is the metric, not raw token count. A 10% token-cost rise that comes with a 15% success-rate rise is a feature, not a regression. Conversely, flat tokens with falling success means you are paying the same and getting less — that is the spike the ritual must catch.

When the band breaks, pick exactly one lever. The four candidates in Stage 2 are routing (force more requests through the weak/cascade path), caching (audit prompt-cache prefix order and hit rate), context (compact or evict tool results), and circuit-breaking (max-turns cap).

The most common lever is caching. A prompt change earlier in the week often invalidates the cache silently; the ritual catches it the next day. Restore prefix order and the cost drops without any model change.

Cascade tuning is the second most common. If the cheap model preselects too aggressively, success rate drops and weak-to-strong escalations spike. Re-tune the confidence threshold instead of swapping models. Brainstorm lists cost-slo-per-task-template and cache-hit-audit-script as gaps; interim, use spreadsheet thresholds.

## CLI usage

```
faion get-content token-cost-daily-watch --format md       # human-readable rendering
faion get-content token-cost-daily-watch --format context  # agent-optimised context bundle
faion get-content token-cost-daily-watch --format json     # raw structured form
```
