---
slug: stand-up-eval-harness-benchmark-suite
tier: geek
group: llm-agent
persona: p7-llm-agent-developer
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: From zero to a CI-integrated eval harness that gates every prompt/tool/model change with a regression score, an adversarial pack, a cost-per-success budget, and trajectory-level OTEL traces.
content_id: 5768c4742aebe438
methodology_refs:
  - chaos-eval-fault-injection
  - llm-judge-rubric-evidence-first
  - record-replay-debugging
  - schema-version-pinning
  - trajectory-eval-otel
  - llm-observability
  - model-evaluation
  - evaluation-benchmarks
  - evaluation-framework
  - evaluation-metrics
  - rag-eval-ab-testing
  - rag-eval-generation-metrics
  - rag-eval-retrieval-metrics
  - rag-eval-strategy
  - rag-eval-test-set-generation
  - mr-error-tracker-draft-pr
  - test-mutation-feedback-loop
  - test-property-based-llm-invariants
  - test-self-healing-locators-audited
---

# Stand up an eval harness + continuous benchmark suite (3 weeks)

## Context

From zero to a CI-integrated eval harness that gates every prompt/tool/model change with a regression score, an adversarial pack, a cost-per-success budget, and trajectory-level OTEL traces.

## Outcome

By the end of this playbook, the operator has run the 5 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 5 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Define What to Measure

Pick metrics tied to user value.

Tasks:
- List metrics: accuracy, faithfulness, latency, cost, safety
- Tie each metric to a buyer-visible outcome
- Set the bar per metric

Outputs:
- metrics list
- metric-to-outcome map
- bar per metric

Decision gate: Advance only when every metric has a tied outcome and a bar.

### 2. Build Golden Set

Cases you trust as ground truth.

Tasks:
- Curate 50-200 golden cases that span the workflow
- Get human raters to label edge cases
- Version-control the golden set

Outputs:
- golden cases
- rater labels
- versioned dataset

Decision gate: Advance only when golden set is reviewed and versioned.

### 3. Build the Harness

Repeatable, automatable, observable.

Tasks:
- Implement the harness to run agent vs golden cases
- Wire up metric computation per run
- Surface results in a dashboard

Outputs:
- running harness
- metrics per run
- dashboard

Decision gate: Advance only when harness runs end-to-end and emits stable metrics.

### 4. Baseline + Continuous Run

Treat eval like CI.

Tasks:
- Run the harness on every meaningful change
- Block merge on regressions beyond the bar
- Publish a weekly benchmark digest

Outputs:
- CI integration
- regression-block rule
- weekly digest

Decision gate: Advance only when a regression has actually been blocked once.

### 5. Tune & Expand

Add SOTA comparisons + new failure modes.

Tasks:
- Add new failure-mode cases as you find them
- Benchmark against new SOTA models on a cadence
- Decide: keep / extend / retire each metric

Outputs:
- new cases added
- SOTA benchmarks
- metric lifecycle decisions

Decision gate: Required output: a written metric lifecycle for every metric.

## Decision points

- Stage 1 (Define What to Measure): Advance only when every metric has a tied outcome and a bar.
- Stage 2 (Build Golden Set): Advance only when golden set is reviewed and versioned.
- Stage 3 (Build the Harness): Advance only when harness runs end-to-end and emits stable metrics.
- Stage 4 (Baseline + Continuous Run): Advance only when a regression has actually been blocked once.
- Stage 5 (Tune & Expand): Required output: a written metric lifecycle for every metric.

## References

- `chaos-eval-fault-injection`
- `llm-judge-rubric-evidence-first`
- `record-replay-debugging`
- `schema-version-pinning`
- `trajectory-eval-otel`
- `llm-observability`
- `model-evaluation`
- `evaluation-benchmarks`
- `evaluation-framework`
- `evaluation-metrics`
- `rag-eval-ab-testing`
- `rag-eval-generation-metrics`
- `rag-eval-retrieval-metrics`
- `rag-eval-strategy`
- `rag-eval-test-set-generation`
- `mr-error-tracker-draft-pr`
- `test-mutation-feedback-loop`
- `test-property-based-llm-invariants`
- `test-self-healing-locators-audited`

Gaps (status: draft until empty):
- `agent-eval-test-set-curation` (see `gaps[]` in `playbook.yaml`)
- `judge-calibration-protocol` (see `gaps[]` in `playbook.yaml`)
- `eval-as-ci-gate-thresholds` (see `gaps[]` in `playbook.yaml`)
