---
slug: evaluation-framework
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Ships a Python evaluation harness that runs an offline batch (ModelEvaluator), an LLM-as-judge scorer (LLMJudge), and a sampled production evaluator (ProductionEvaluator) against a shared rubric.
content_id: "7fdaf9bea87fb6cc"
complexity: deep
produces: code
est_tokens: 4600
tags: [evaluation, llm-as-judge, quality-gate, testing, ci-cd]
---
# Evaluation Framework — Offline Harness + LLM-as-Judge + Production Sampling

## Summary

**One-sentence:** Ships a Python evaluation harness that runs an offline batch (ModelEvaluator), an LLM-as-judge scorer (LLMJudge), and a sampled production evaluator (ProductionEvaluator) against a shared rubric.

**One-paragraph:** An evaluation harness is the difference between 'we think it's better' and 'we know with 95% CI'. This methodology defines three composable Python classes: ModelEvaluator (runs N candidates on a fixed dataset), LLMJudge (rubric-anchored 1-5 scoring with explanation), ProductionEvaluator (samples K% of live traffic, scores with the same judge, publishes a drift dashboard). All three reuse one rubric module so offline / online results are comparable.

**Ефективно для:**

- CI gating: PR fails when win-rate vs baseline drops below threshold.
- Vendor swap decision evidence pack.
- Continuous quality monitoring with shared rubric.
- Onboarding: new dev runs the harness to understand the metric.

## Applies If (ALL must hold)

- Task has a measurable quality dimension (correctness, helpfulness, format).
- A dataset of ≥100 examples is curatable.
- Engineering capacity exists to wire CI / dashboards.

## Skip If (ANY kills it)

- Quality is fully subjective (creative writing for entertainment) — need different metrics.
- <10 examples available — wait until you have data.
- Cost is the only KPI — use cost-reduction-strategies instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dataset | JSONL | BA + Eng |
| Rubric | markdown | evaluation-metrics methodology |
| CI runner | GitHub Actions / GitLab CI | DevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `dataset_curate` | sonnet | Choose examples covering edge cases. |
| `rubric_author` | sonnet | Anchor 1-5 scoring. |
| `harness_impl` | sonnet | Python class wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-evaluator.py` | ModelEvaluator class skeleton |
| `templates/llm-judge.py` | LLMJudge class with rubric loader |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-evaluation-framework.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[evaluation-benchmarks]]
- [[evaluation-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is this an offline harness run or a production sample? Branches route to a rule id from `content/01-core-rules.xml` (three-class-split, rubric-module-shared, ci-gate-threshold, ...) so every leaf is traceable to a testable statement.
