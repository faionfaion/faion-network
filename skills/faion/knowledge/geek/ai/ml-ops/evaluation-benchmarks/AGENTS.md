---
slug: evaluation-benchmarks
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Multi-model comparison and continuous production monitoring methodology.
content_id: "884894067d8a791d"
tags: [benchmarking, model-comparison, production-monitoring, evaluation, quality-assurance]
---
# Evaluation Benchmarks

## Summary

**One-sentence:** Multi-model comparison and continuous production monitoring methodology.

**One-paragraph:** Multi-model comparison and continuous production monitoring methodology. ModelComparison runs the same test set across multiple LLMs and ranks them per metric. BenchmarkSuite standardizes evaluation across classification, QA, summarization, and code task types. ProductionEvaluator samples live traffic and runs automated quality checks with alerting.

## Applies If (ALL must hold)

- Selecting a model or provider for a new project: run ModelComparison across candidate models on a domain-representative test set
- Establishing a repeatable performance baseline before any major prompt or model change
- Setting up continuous production monitoring that detects quality regressions before users report them
- Comparing a fine-tuned model to the base model with consistent methodology
- Building a CI quality gate that blocks deployment if benchmark scores drop below threshold

## Skip If (ANY kills it)

- The test set has fewer than 100 cases — ModelComparison results will have confidence intervals too wide to be actionable
- The benchmark dataset is derived from the same source as the training data — this produces artificially inflated scores; use a held-out dataset from a different collection
- The goal is evaluating safety or alignment — ProductionEvaluator string checks are insufficient; use red-teaming and dedicated safety benchmarks (e.g., ToxiGen, BBQ)
- A single benchmark run is expected to fully characterize model quality — benchmarks capture what they measure, not everything that matters in production

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-ops/`
