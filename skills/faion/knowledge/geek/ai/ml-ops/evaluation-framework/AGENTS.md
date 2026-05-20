---
slug: evaluation-framework
tier: geek
group: ai
domain: ml-ops
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Python evaluation harness for LLM outputs combining offline batch testing (ModelEvaluator) with LLM-as-judge scoring (LLMJudge) and production sampling (ProductionEvaluator).
content_id: "945838d7dc15c444"
tags: [evaluation, llm-as-judge, quality-gate, testing, ci-cd]
---
# Evaluation Framework

## Summary

**One-sentence:** Python evaluation harness for LLM outputs combining offline batch testing (ModelEvaluator) with LLM-as-judge scoring (LLMJudge) and production sampling (ProductionEvaluator).

**One-paragraph:** Python evaluation harness for LLM outputs combining offline batch testing (ModelEvaluator) with LLM-as-judge scoring (LLMJudge) and production sampling (ProductionEvaluator). Establishes a structured pipeline: define test cases, apply metric functions, aggregate results, and gate deployments on threshold pass/fail.

## Applies If (ALL must hold)

- Building a reusable offline evaluation harness for LLM features that runs in CI before deployment
- Implementing LLM-as-judge to assess complex outputs where no ground-truth metric exists (helpfulness, coherence, instruction-following)
- Running pairwise A/B comparisons between two prompt versions or model versions
- Setting up a quality gate that blocks deployment if metric thresholds are not met
- Creating a production sampling evaluator that continuously monitors output quality

## Skip If (ANY kills it)

- The system has fewer than 30 test cases — ModelEvaluator results are statistically unreliable at this scale; build the dataset first
- The task requires human preference evaluation as the primary signal — LLM-as-judge has known biases (position bias, verbosity bias) and cannot substitute for user studies on subjective tasks
- Evaluation latency matters — LLMJudge makes one API call per evaluated case; at 1000 cases this adds significant wall-clock time and cost
- The output format is non-text (images, audio, structured data) — this framework handles text outputs only

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
