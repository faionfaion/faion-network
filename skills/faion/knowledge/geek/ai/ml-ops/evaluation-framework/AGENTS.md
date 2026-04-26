# Evaluation Framework

## Summary

A Python evaluation harness for LLM outputs combining offline batch testing (`ModelEvaluator`) with LLM-as-judge scoring (`LLMJudge`) and production sampling (`ProductionEvaluator`). Establishes a structured pipeline: define test cases, apply metric functions, aggregate results, and gate deployments on threshold pass/fail.

## Why

Automated metrics alone cannot capture output quality for open-ended tasks. LLM-as-judge fills that gap by scoring criteria like accuracy, clarity, and completeness, while the batch evaluator provides statistical baselines. Combining both ensures every model change is measured before reaching production and regressions are caught in CI.

## When To Use

- Building a CI quality gate that blocks deployment if metric thresholds are not met
- Evaluating LLM outputs on complex tasks where no single ground-truth metric exists
- Running pairwise A/B comparisons between two prompt or model versions
- Setting up production sampling that monitors output quality continuously
- Comparing fine-tuned models against base models with a held-out test set

## When NOT To Use

- Fewer than 30 test cases — results are statistically unreliable; build the dataset first
- Primary signal is human preference — LLM-as-judge has position bias (~5-10% swing) and verbosity bias; use user studies instead
- Evaluation latency is critical — `LLMJudge` makes one API call per case; 1000 cases adds significant wall-clock time
- Output is non-text (images, audio, structured data) — this framework handles text outputs only
- Autonomously blocking production deployments on judge scores alone — requires human review of threshold calibration

## Content

| File | What's inside |
|------|---------------|
| `content/01-evaluator.xml` | `ModelEvaluator` class: test-case structure, metric pipeline, aggregate stats, CI quality gate pattern |
| `content/02-llm-judge.xml` | `LLMJudge` class: single scoring, pairwise comparison, batch eval, prompt templates, known biases |
| `content/03-production.xml` | `ProductionEvaluator`: sampling, automated checks, alerting, persistent logging pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-quality-gate.py` | Minimal CI gate using `ModelEvaluator` with exact_match metric (~40 lines) |
| `templates/llm-judge-prompts.txt` | Prompt templates for single scoring and pairwise comparison |

## Scripts

none
