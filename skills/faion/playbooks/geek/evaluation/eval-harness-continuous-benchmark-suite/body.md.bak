# Stand up an eval harness + continuous benchmark suite (3 weeks)

**Playbook slug:** `eval-harness-continuous-benchmark-suite`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

No eval harness → CI-integrated eval harness gating every prompt/tool/model change with regression score, adversarial pack, cost-per-success budget.

## Scope

From zero to a CI-integrated eval harness that gates every prompt/tool/model change with a regression score, an adversarial pack, a cost-per-success budget, and trajectory-level OTEL traces. Output: a green-or-red gate on every PR touching agent behavior.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Online RLHF/preference training — separate playbook
- Human-in-the-loop UX — covered elsewhere

### Prerequisites

- At least one production agent path with logged traces
- CI runner with secrets access

## Success criteria

The playbook is done when:
- Golden eval set ≥50 trajectories with judge labels
- Adversarial pack ≥20 entries covering injection, refusal, drift
- Cost-per-success metric tracked per PR
- CI fails the PR on regression
- OTEL traces queryable by trajectory id

## Stages

### Stage 1: Curate Test Set

**Intent:** Source golden trajectories from production and synthetic seeds.

**Tasks:**
- Sample N production trajectories stratified by intent
- Add synthetic edge cases from rag-eval test-set generator
- Tag each trajectory with expected behavior

**Methodologies in chain:**
- `rag-eval-test-set-generation` → `geek/ai/rag-engineer/rag-eval-test-set-generation`
- `rag-eval-strategy` → `geek/ai/rag-engineer/rag-eval-strategy`
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`

**Outputs:**
- golden-trajectories.jsonl
- Stratification table

**Decision gate:**
> Advance when the set covers each intent class ≥5 cases.

### Stage 2: Build Judges

**Intent:** Calibrate LLM-judge rubrics and property-based invariants.

**Tasks:**
- Write rubric-evidence-first judge prompts
- Add property-based invariants on outputs
- Sample-check judge against humans

**Methodologies in chain:**
- `llm-judge-rubric-evidence-first` → `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `test-property-based-llm-invariants` → `geek/sdlc-ai/test-property-based-llm-invariants`
- `model-evaluation` → `geek/ai/ml-engineer/model-evaluation`
- `rag-eval-generation-metrics` → `geek/ai/rag-engineer/rag-eval-generation-metrics`
- `rag-eval-retrieval-metrics` → `geek/ai/rag-engineer/rag-eval-retrieval-metrics`

**Outputs:**
- Judge prompt set
- Judge calibration report

**Decision gate:**
> Advance when judge κ ≥0.6 against human sample.

### Stage 3: Adversarial Pack

**Intent:** Stress the agent with fault injection and mutation cases.

**Tasks:**
- Inject tool failures and rate limits
- Mutation-test inputs
- Add A/B harness for prompt versions

**Methodologies in chain:**
- `chaos-eval-fault-injection` → `geek/ai/ai-agents/chaos-eval-fault-injection`
- `test-mutation-feedback-loop` → `geek/sdlc-ai/test-mutation-feedback-loop`
- `rag-eval-ab-testing` → `geek/ai/rag-engineer/rag-eval-ab-testing`

**Outputs:**
- adversarial-pack.jsonl
- A/B fixture

**Decision gate:**
> Advance when pack covers ≥20 named failure modes.

### Stage 4: CI Wiring

**Intent:** Make the suite block every PR touching prompts, tools, or models.

**Tasks:**
- Add CI job running suite on every PR
- Tracker draft-PR on judge regression
- Wire OTEL trace upload per run

**Methodologies in chain:**
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`
- `llm-observability` → `geek/ai/ml-engineer/llm-observability`
- `mr-error-tracker-draft-pr` → `geek/sdlc-ai/mr-error-tracker-draft-pr`
- `test-self-healing-locators-audited` → `geek/sdlc-ai/test-self-healing-locators-audited`
- `evaluation-benchmarks` → `geek/ai/ml-ops/evaluation-benchmarks`
- `evaluation-framework` → `geek/ai/ml-ops/evaluation-framework`
- `evaluation-metrics` → `geek/ai/ml-ops/evaluation-metrics`

**Outputs:**
- CI workflow YAML
- Trace dashboard

**Decision gate:**
> Advance only when a known regression PR is correctly blocked.

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
- **agent-eval-test-set-curation** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **judge-calibration-protocol** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **eval-as-ci-gate-thresholds** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

The single hardest part of standing up a harness is the test set itself. Synthetic generation alone produces an eval that the agent passes by definition; production sampling alone produces an eval that drifts with the agent. Stage 1 mandates both: stratified production traces plus synthetic seeds for edge cases the production traffic has not yet covered. Keep the stratification table reviewed weekly.

Judges are the second hard part. A rubric that lists too many criteria becomes noisy — three to five criteria with explicit evidence requirements outperforms a checklist of fifteen. Calibrate judges against humans on the first 20 entries before trusting them in CI.

The adversarial pack is the third hard part. It must include indirect prompt injection cases if the agent reads any external content (web, files, MCP), tool failure injection, and rate-limit cases. Mutation testing on the inputs catches schema brittleness without manual case authoring.

CI wiring is the easy part if the rest is in place. The gate must run on every PR that touches prompts, tools, models, or the gateway. Skipping the gate on 'pure refactor' PRs is the most common foot-gun — refactors that change context ordering or compaction also change agent behaviour.

Brainstorm flagged three gaps (test-set curation, judge calibration protocol, eval-as-CI-gate thresholds). The playbook is publishable only after those land.

## CLI usage

```
faion get-content eval-harness-continuous-benchmark-suite --format md       # human-readable rendering
faion get-content eval-harness-continuous-benchmark-suite --format context  # agent-optimised context bundle
faion get-content eval-harness-continuous-benchmark-suite --format json     # raw structured form
```
