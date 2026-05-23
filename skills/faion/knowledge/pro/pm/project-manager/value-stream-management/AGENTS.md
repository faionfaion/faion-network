---
slug: value-stream-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Maps end-to-end flow request→value, measures Flow Metrics + DORA, locates the constraint via Theory of Constraints, runs targeted experiments; emits a `ValueStreamReport` with constraint, throughput by work-type, and ranked experiments.
content_id: "0ecee09a700718ba"
complexity: deep
produces: report
est_tokens: 4600
tags: [flow-metrics, dora, value-stream, theory-of-constraints, kersten]
---
# Value Stream Management

## Summary

**One-sentence:** Maps the end-to-end value stream (customer request → customer value), measures Flow Metrics (Lead/Cycle/Throughput/WIP/%C&A) + DORA (DF/CLT/CFR/MTTR), identifies the constraint via Theory of Constraints, runs targeted experiments, and emits a `ValueStreamReport` with ranked interventions.

**One-paragraph:** AI productivity gains and DevOps automation frequently fail to improve customer-visible delivery time because the bottleneck lives outside the software team (product spec, design review, compliance gate, support queue). Flow Metrics expose end-to-end flow; DORA measures only DevOps efficiency. Used together they locate where value actually stalls. This methodology codifies a 5-step procedure (instrument → map → measure DORA → identify constraint → experiment), with three sub-agents (flow-instrumenter, dora-collector, bottleneck-analyzer) and a hard minimum sample size (≥ 50 items per work type) before declaring a constraint. Output is a typed `ValueStreamReport` carrying constraint stage, distribution by Kersten's four work types (feature/defect/risk/debt), DORA four-tuple, and 1–3 ranked experiments with expected throughput lift / cost.

**Ефективно для:**

- DevOps automation shipped but customer lead time has not improved.
- Cross-functional bottleneck suspected across product → design → eng → release → support.
- Org adopting SAFe / FAST Agile / Project-to-Product and shifting from output to flow metrics.
- DORA elite labels reaching diminishing returns — need upstream Flow Metrics for honest signal.

## Applies If (ALL must hold)

- Telemetry exists for at least 3 of: Jira/Linear, GitHub/GitLab, deploy log, PagerDuty, Zendesk.
- Stable system: each work type has ≥ 50 historical items (Little's Law assumptions hold).
- Stakeholders own at least 2 stages of the stream (single-team without upstream/downstream ≠ value-stream).
- 90+ days of timestamp data available.

## Skip If (ANY kills it)

- Single-team pre-PMF startup — premature optimisation.
- No telemetry baseline (no commit timestamps, no deploy log) — instrument first.
- Pure cost-cutting / layoff context — VSM is not a layoff lever.
- Teams without shared ownership across the stream — VSM names the bottleneck but cannot move it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool ID-link map | YAML | platform team |
| Git + deploy log access | API tokens | platform team |
| Work-type taxonomy | YAML (feature/defect/risk/debt) | Kersten Flow Framework |
| 90+ days timestamp data | per source | git/jira/deploy/incident |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[work-breakdown-structure]] | Provides the deliverable taxonomy each flow item maps to. |
| [[team-development]] | Throughput shape is an input to Tuckman staging. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: customer-anchored boundary, work-type split, pair DORA metrics, ≥50-item sample before constraint, no elite-label without trend, AI-PR human/bot split | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `ValueStreamReport` + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: hallucinated ID links, timezone bugs, elite-DORA-no-trend, webhook drops, AI-PR flood | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: instrument → map → DORA → constraint → experiment | ~800 |
| `content/05-examples.xml` | medium | One worked report: 90-day window, design-review constraint surfaced, 3 ranked experiments | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: telemetry coverage + sample size + work-type split → suppress/measure/declare-constraint | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `flow-instrumenter` | sonnet | ID-link reasoning + timestamp normalisation. |
| `dora-collector` | haiku | Mechanical reduction of git + incident logs. |
| `bottleneck-analyzer` | sonnet | Theory-of-Constraints application + experiment ranking. |
| `experiment-tracker` | sonnet | Before/after distribution comparison with judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flow-item.yaml` | Schema for a single traced work item across VSM stages |
| `templates/dora-quick.sh` | Bash script: compute last-30-day DORA from git + deploy log |
| `templates/_smoke-test.json` | Minimum-viable filled `ValueStreamReport` for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-value-stream-management.py` | Validate a `ValueStreamReport` against the JSON Schema | Pre-commit on every report change |

## Related

- [[work-breakdown-structure]]
- [[team-development]]
- [[wbs-creation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (telemetry coverage, sample-size per work type, customer-boundary anchor) to a concrete action — instrument-first, measure-only, declare-constraint, or run-experiment — each leaf references a rule in `01-core-rules.xml` so claims are grounded in checkable invariants.
