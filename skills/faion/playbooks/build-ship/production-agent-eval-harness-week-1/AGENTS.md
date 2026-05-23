# Stand up a production agent eval harness in week 1

**Playbook slug:** `production-agent-eval-harness-week-1`  
**Tier:** geek  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

New agent builder → CI-runnable eval harness with golden trajectories, behavioral evals, judge rubrics, drift signal in week 1.

## Scope

New agent builder has a CI-runnable eval harness with golden trajectories, behavioral evals, judge rubrics, and a drift signal that fires before users see regressions. Bootstrap shape, not deep.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Long-term eval-set authoring — covered by playbook 1
- Productizing the harness

### Prerequisites

- A working agent loop
- CI runner available

## Success criteria

The playbook is done when:
- ≥10 golden trajectories committed
- ≥1 behavioral adversarial set wired
- Judges committed with rubrics
- Drift signal firing on a known regression
- CI gates the PR

## Stages

### Stage 1: Golden Set

**Intent:** Seed ≥10 trajectories.

**Tasks:**
- Sample first traces
- Replay-record them
- Tag expected behaviour

**Methodologies in chain:**
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`

**Outputs:**
- golden.jsonl

**Decision gate:**
> Advance only when ≥10 reliable trajectories exist.

### Stage 2: Behaviorals

**Intent:** Add chaos pack and judge.

**Tasks:**
- Chaos-eval fault injection
- Author rubric judge

**Methodologies in chain:**
- `chaos-eval-fault-injection` → `geek/ai/ai-agents/chaos-eval-fault-injection`
- `llm-judge-rubric-evidence-first` → `geek/ai/ai-agents/llm-judge-rubric-evidence-first`

**Outputs:**
- Behavioural set + judges

**Decision gate:**
> Advance only when judges score on the golden set.

### Stage 3: CI Gate

**Intent:** Wire CI to fail on regression.

**Tasks:**
- Hook CI on PR
- Wire observability stack

**Methodologies in chain:**
- `llm-observability-stack` → `geek/ai/ml-engineer/llm-observability-stack`
- `llm-observability-stack-2026` → `geek/ai/ml-ops/llm-observability-stack-2026`

**Outputs:**
- CI workflow YAML

**Decision gate:**
> Ship only when a known-bad PR is blocked.

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
- **agent-eval-harness-bootstrap-recipe** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **agent-drift-detection-statistical** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **agent-eval-cost-budget-policy** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Bootstrap shape, not deep harness. The point is to have a harness that fails the PR by Friday, not the perfect eval suite by Q3. If a stage takes more than two days, the scope is wrong — narrow until it fits.

Ten golden trajectories is the minimum. Fewer than ten and the suite gives false confidence; more than fifty in week one and you are over-investing before you have CI green. Pick ten that cover your top three intent classes plus two edge cases. Replay-record them with deterministic seeds.

The judge is the second risk. A rubric judge in week one should have three to five criteria, evidence-first, and be sanity-checked against your own human reading on at least three trajectories. If you and the judge disagree, the rubric is wrong, not the judge model.

Chaos-eval fault injection in week one adds one or two failure cases — tool-rate-limit and tool-error are the two highest-value to wire. Resist adding indirect-prompt-injection cases until at least week two; they deserve the dedicated hardening playbook.

CI gate is the deliverable. A harness that does not fail PRs is theatre. Test the gate by intentionally submitting a known-bad PR (e.g. a prompt regression you already understand) and verifying the gate fires before calling the playbook done. Brainstorm marks three gaps: bootstrap recipe, drift-detection statistical, eval cost-budget policy.

## CLI usage

```
faion get-content production-agent-eval-harness-week-1 --format md       # human-readable rendering
faion get-content production-agent-eval-harness-week-1 --format context  # agent-optimised context bundle
faion get-content production-agent-eval-harness-week-1 --format json     # raw structured form
```
