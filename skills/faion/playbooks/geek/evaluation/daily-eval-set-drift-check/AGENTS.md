---
slug: daily-eval-set-drift-check
tier: geek
group: evaluation
persona: P7
goal: operate-ritual
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Tomorrow's prompt/version bump might regress → today's run confirms last 24h still passes the golden set."
content_id: 1d724429ce423580
methodology_refs:
  - trajectory-eval-otel
  - schema-version-pinning
  - llm-observability-stack
  - llm-judge-rubric-evidence-first
  - model-evaluation
  - evaluation-framework
  - evaluation-metrics
---

# Daily eval-set drift check

**Playbook slug:** `daily-eval-set-drift-check`  
**Tier:** geek  
**Complexity:** light  
**Persona:** P7 — LLM Agent Developer

## Intent

Tomorrow's prompt/version bump might regress → today's run confirms last 24h still passes the golden set.

## Scope

Confirm last 24h production traffic still passes the golden eval set; flag any regression class before it ships in tomorrow's prompt/version bump. Designed as a daily ritual, 15-30 min.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Full eval-set authoring — done in playbook 1
- Long-term drift research

### Prerequisites

- Eval harness from `eval-harness-continuous-benchmark-suite`
- OTEL traces queryable for last 24h

## Success criteria

The playbook is done when:
- Last 24h traffic replayed against golden judges
- Any regression class identified before today's bump
- Decision logged: ship / hold / rollback

## Stages

### Stage 1: Pull 24h

**Intent:** Sample last 24h trajectories.

**Tasks:**
- Pull stratified sample of traces
- Confirm schema pin still valid

**Methodologies in chain:**
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`
- `llm-observability-stack` → `geek/ai/ml-engineer/llm-observability-stack`

**Outputs:**
- Last-24h sample

**Decision gate:**
> Advance once sample covers main intent buckets.

### Stage 2: Judge

**Intent:** Score sample with rubric judge.

**Tasks:**
- Run rubric-evidence-first judge
- Compare scores vs trailing 7-day baseline

**Methodologies in chain:**
- `llm-judge-rubric-evidence-first` → `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `model-evaluation` → `geek/ai/ml-engineer/model-evaluation`
- `evaluation-framework` → `geek/ai/ml-ops/evaluation-framework`
- `evaluation-metrics` → `geek/ai/ml-ops/evaluation-metrics`

**Outputs:**
- Daily judge scorecard

**Decision gate:**
> Advance to Decide whether scores fell outside SLO band.

### Stage 3: Decide

**Intent:** Ship / hold / rollback for today.

**Tasks:**
- Apply SLO thresholds
- Write one-line daily log entry

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Daily ship/hold decision logged

**Decision gate:**
> If above SLO, ship; else hold and trigger incident playbook.

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
- **eval-set-stratified-sampling-recipe** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **drift-slo-thresholds-cookbook** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Treat this as a 15-30 minute daily ritual, not a deep investigation. The purpose of the daily check is to catch regressions before the next prompt/version bump compounds them. If the daily run is consistently green, the harness from playbook 1 is doing its job; if it is consistently noisy, stop and recalibrate judges before you stop trusting the signal.

Stratified sampling is non-negotiable. A naive random sample of the last 24h will be dominated by the top one or two intent classes. Stratify by intent so rare paths still surface. The brainstorm flags this as a gap (`eval-set-stratified-sampling-recipe`); until authored, pin the same stratification table your eval harness already uses.

The SLO band is the second key piece. Without a documented threshold, every score fluctuation feels like a regression and every ritual ends in 'looks fine to me'. Pin numeric thresholds: scores within ±X of the trailing 7-day median pass; outside, hold the bump. Track threshold changes in changelog so audits show the band evolved with the system.

If the ritual triggers a hold, escalate to the hallucination-incident-triage or blameless-agent-incident-postmortem playbook depending on user impact. Do not patch silently — the eval drift is the signal that something shipped without a regression gate. Find what.

## CLI usage

```
faion get-content daily-eval-set-drift-check --format md       # human-readable rendering
faion get-content daily-eval-set-drift-check --format context  # agent-optimised context bundle
faion get-content daily-eval-set-drift-check --format json     # raw structured form
```
