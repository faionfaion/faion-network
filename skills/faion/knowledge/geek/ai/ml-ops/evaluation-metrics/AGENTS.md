---
slug: evaluation-metrics
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Selects per-task metrics across accuracy, quality, latency, cost, safety, and reliability; produces a metric card that the eval harness consumes.
content_id: "0c0f4f798a9e43af"
complexity: medium
produces: spec
est_tokens: 3800
tags: [evaluation, metrics, llm, ml-ops, benchmarking]
---
# Evaluation Metrics for LLMs

## Summary

**One-sentence:** Selects per-task metrics across accuracy, quality, latency, cost, safety, and reliability; produces a metric card that the eval harness consumes.

**One-paragraph:** Generic 'is it good' metrics fail. This methodology picks per-task metrics across six dimensions: accuracy (exact-match / F1), quality (LLM-as-judge rubric), latency (p50/p95 ms), cost ($/call), safety (refusal rate / toxicity), reliability (parse-success / retry rate). The output is a metric card — one YAML per task — that the evaluation harness reads to know what to compute.

**Ефективно для:**

- Onboarding new task to the eval harness.
- Refactoring a vague 'looks good' eval into a measurable contract.
- Cross-team alignment on what 'better' means.
- Compliance: demonstrating measurable safety + reliability.

## Applies If (ALL must hold)

- A task has at least one quantifiable dimension.
- Multiple stakeholders disagree on what 'better' means.
- An eval harness exists or will exist.

## Skip If (ANY kills it)

- Task is wholly subjective (creative writing) — pick a quality-only proxy and move on.
- <10 examples — metrics are noisy below that.
- Stakes are zero — picking metrics is overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task brief | markdown | Product + BA |
| Sample inputs/outputs | JSONL | Pilot run |
| Stakeholder list | list | Product + Eng + Legal |

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
| `dimension_pick` | sonnet | Choose subset of 6 dimensions. |
| `metric_select` | sonnet | Per dimension, pick a measurable metric. |
| `card_write` | haiku | Emit YAML card. |

## Templates

| File | Purpose |
|------|---------|
| `templates/metric-card.yaml` | Per-task metric card skeleton |
| `templates/rubric.md` | LLM-as-judge rubric template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-evaluation-metrics.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[evaluation-framework]]
- [[evaluation-benchmarks]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is the task's quality dimension quantifiable by exact-match or F1? Branches route to a rule id from `content/01-core-rules.xml` (metric-per-dim-or-na, anchored-rubric, safety-and-reliability-floor, ...) so every leaf is traceable to a testable statement.
